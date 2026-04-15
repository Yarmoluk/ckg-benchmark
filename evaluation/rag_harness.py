"""
RAG Harness — Retrieval-Augmented Generation baseline.

For each benchmark query, this harness:
1. Loads domain chapter .md files from corpus/
2. Chunks into 512-token windows with 50-token overlap
3. Embeds with OpenAI text-embedding-3-small and indexes with FAISS
4. Retrieves top-5 chunks per query
5. Sends chunks + query to Claude Sonnet 4.6 for answer generation
6. Records F1, tokens, and RDS (same metrics as CKG harness)

Usage:
    python evaluation/rag_harness.py --domain calculus
    python evaluation/rag_harness.py --all
    python evaluation/rag_harness.py --all --dry-run
"""

import json
import os
import re
import time
import argparse
import pickle
from collections import defaultdict
from pathlib import Path
from typing import Optional

import numpy as np
import tiktoken
import faiss
import anthropic
import openai

# ── Config ────────────────────────────────────────────────────────────────────

CLAUDE_MODEL    = "claude-sonnet-4-6"
EMBED_MODEL     = "text-embedding-3-small"
CHUNK_TOKENS    = 512
OVERLAP_TOKENS  = 50
TOP_K           = 5

CORPUS_DIR  = Path("corpus")
QUERIES_DIR = Path("benchmark/queries")
RESULTS_DIR = Path("results/rag")
INDEX_DIR   = Path("results/rag_indexes")   # cached FAISS indexes

PRICE_INPUT  = 3.0  / 1_000_000   # Claude Sonnet 4.6: $3 per 1M input
PRICE_OUTPUT = 15.0 / 1_000_000   # $15 per 1M output
PRICE_EMBED  = 0.02 / 1_000_000   # text-embedding-3-small: $0.02 per 1M tokens

SYSTEM_PROMPT = """You are a knowledgeable tutor. Answer the question using ONLY the
provided context passages. Be concise and precise. List concepts as comma-separated
values when asked to enumerate. Do not add information not present in the context."""

STOPWORDS = {
    "what","is","the","a","an","of","for","are","in","and","or","to","with",
    "how","does","related","which","these","those","all","list","describe",
    "explain","between","concept","concepts"
}

# ── Tokenizer ─────────────────────────────────────────────────────────────────

_enc = None

def get_encoder():
    global _enc
    if _enc is None:
        _enc = tiktoken.get_encoding("cl100k_base")
    return _enc


def count_tokens(text: str) -> int:
    return len(get_encoder().encode(text))

# ── Corpus loading ────────────────────────────────────────────────────────────

def strip_markdown(text: str) -> str:
    """Remove MkDocs-specific markup that adds noise but no content."""
    # Remove <details> image prompt blocks (very long, zero information value)
    text = re.sub(r'<details>.*?</details>', '', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove MkDocs admonitions (!!!) — keep the content, drop the directive
    text = re.sub(r'^!!!\s+\w+.*$', '', text, flags=re.MULTILINE)
    # Remove image links
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove bare URLs
    text = re.sub(r'https?://\S+', '', text)
    # Collapse whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def load_corpus_docs(domain: str) -> list[dict]:
    """Return list of {source, text} dicts from chapter index.md files."""
    chapters_dir = CORPUS_DIR / domain / "docs" / "chapters"
    if not chapters_dir.exists():
        return []

    docs = []
    for chapter_path in sorted(chapters_dir.iterdir()):
        if not chapter_path.is_dir():
            continue
        index_file = chapter_path / "index.md"
        if not index_file.exists():
            continue
        raw = index_file.read_text(encoding="utf-8", errors="ignore")
        text = strip_markdown(raw)
        if len(text) > 200:  # skip near-empty files
            docs.append({
                "source": f"{domain}/{chapter_path.name}",
                "text": text
            })

    # Also include glossary and course-description if present
    for extra in ["glossary.md", "course-description.md"]:
        extra_path = CORPUS_DIR / domain / "docs" / extra
        if extra_path.exists():
            raw = extra_path.read_text(encoding="utf-8", errors="ignore")
            text = strip_markdown(raw)
            if len(text) > 200:
                docs.append({"source": f"{domain}/{extra}", "text": text})

    return docs


def chunk_documents(docs: list[dict]) -> list[dict]:
    """Split documents into overlapping token windows."""
    enc = get_encoder()
    chunks = []

    for doc in docs:
        tokens = enc.encode(doc["text"])
        step = CHUNK_TOKENS - OVERLAP_TOKENS
        for start in range(0, len(tokens), step):
            end = min(start + CHUNK_TOKENS, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = enc.decode(chunk_tokens)
            if len(chunk_tokens) < 20:  # skip tiny tail chunks
                continue
            chunks.append({
                "source": doc["source"],
                "text": chunk_text,
                "start_token": start,
                "n_tokens": len(chunk_tokens)
            })
            if end == len(tokens):
                break

    return chunks

# ── Embeddings + FAISS ────────────────────────────────────────────────────────

def embed_texts(texts: list[str], oai_client: openai.OpenAI) -> np.ndarray:
    """Embed a list of texts in batches. Returns (n, 1536) float32 array."""
    BATCH = 100
    all_vecs = []
    for i in range(0, len(texts), BATCH):
        batch = texts[i:i+BATCH]
        resp = oai_client.embeddings.create(model=EMBED_MODEL, input=batch)
        vecs = [item.embedding for item in resp.data]
        all_vecs.extend(vecs)
    return np.array(all_vecs, dtype=np.float32)


def build_or_load_index(domain: str, oai_client) -> tuple:
    """Build FAISS index for a domain, or load cached version.
    Returns (index, chunks). index is None in dry-run mode (no oai_client)."""
    docs   = load_corpus_docs(domain)
    if not docs:
        return None, []

    chunks = chunk_documents(docs)
    if not chunks:
        return None, []

    # Dry-run: skip embedding, return chunks only
    if oai_client is None:
        print(f"    dry-run: {len(chunks)} chunks from {len(docs)} docs (no index)")
        return None, chunks

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_path = INDEX_DIR / f"{domain}.faiss"
    meta_path  = INDEX_DIR / f"{domain}_chunks.pkl"

    if index_path.exists() and meta_path.exists():
        index  = faiss.read_index(str(index_path))
        chunks = pickle.loads(meta_path.read_bytes())
        print(f"    loaded cached index ({len(chunks)} chunks)")
        return index, chunks

    print(f"    embedding {len(chunks)} chunks from {len(docs)} docs...")
    texts  = [c["text"] for c in chunks]
    vecs   = embed_texts(texts, oai_client)

    # L2-normalize for cosine similarity via inner product
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    vecs  = vecs / (norms + 1e-9)

    dim   = vecs.shape[1]
    index = faiss.IndexFlatIP(dim)   # inner product = cosine after normalization
    index.add(vecs)

    faiss.write_index(index, str(index_path))
    meta_path.write_bytes(pickle.dumps(chunks))
    print(f"    indexed {len(chunks)} chunks ({dim}-dim)")

    return index, chunks


def retrieve_chunks(query: str, index, chunks: list[dict], oai_client) -> list[dict]:
    """Return top-K chunks for a query. Falls back to first-K if no index."""
    if index is None or oai_client is None:
        # Dry-run: return first TOP_K chunks
        return [{**c, "score": 0.0} for c in chunks[:TOP_K]]

    q_vec = embed_texts([query], oai_client)
    norm  = np.linalg.norm(q_vec)
    q_vec = q_vec / (norm + 1e-9)

    scores, indices = index.search(q_vec, TOP_K)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        results.append({**chunks[idx], "score": float(score)})
    return results

# ── F1 scoring ────────────────────────────────────────────────────────────────

def token_f1(predicted: str, ground_truth: list[str]) -> dict:
    pred_tokens  = set(predicted.lower().split()) - STOPWORDS
    truth_tokens = set(" ".join(ground_truth).lower().split()) - STOPWORDS
    if not pred_tokens and not truth_tokens:
        return {"f1": 1.0, "precision": 1.0, "recall": 1.0}
    if not pred_tokens or not truth_tokens:
        return {"f1": 0.0, "precision": 0.0, "recall": 0.0}
    tp = len(pred_tokens & truth_tokens)
    p  = tp / len(pred_tokens)
    r  = tp / len(truth_tokens)
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return {"f1": round(f1, 4), "precision": round(p, 4), "recall": round(r, 4)}

# ── Main harness ──────────────────────────────────────────────────────────────

def run_domain(domain: str, ant_client: anthropic.Anthropic,
               oai_client: openai.OpenAI, dry_run: bool = False) -> list[dict]:

    queries_file = QUERIES_DIR / f"queries_{domain}.jsonl"
    if not queries_file.exists():
        print(f"  ✗ no queries file for {domain}")
        return []

    # Build or load FAISS index
    index, chunks = build_or_load_index(domain, oai_client)
    if not chunks:
        print(f"  ✗ no corpus content for {domain}")
        return []

    queries = []
    with open(queries_file) as f:
        for line in f:
            queries.append(json.loads(line))

    print(f"  {domain}: {len(queries)} queries, {len(chunks)} chunks")

    results = []
    for i, q in enumerate(queries):
        query_text = q["query"]

        # Retrieve top-K chunks
        top_chunks = retrieve_chunks(query_text, index, chunks, oai_client)
        context    = "\n\n---\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in top_chunks
        )
        retrieved_tokens = sum(c["n_tokens"] for c in top_chunks)

        user_message = f"Context:\n{context}\n\nQuestion: {query_text}"

        if dry_run:
            result = {
                **q,
                "system": "rag",
                "retrieved_context": context[:300] + "...",
                "predicted_answer": "[DRY RUN]",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "retrieved_tokens": retrieved_tokens,
                "f1": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "rds": 0.0,
                "cost_usd": 0.0,
                "latency_ms": 0
            }
            results.append(result)
            continue

        t0 = time.time()
        try:
            response = ant_client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=512,
                temperature=0,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}]
            )
            latency_ms = int((time.time() - t0) * 1000)
            answer = response.content[0].text
            prompt_tokens     = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
        except Exception as e:
            print(f"    ✗ API error on {q.get('id', q.get('query_id','?'))}: {e}")
            continue

        scores      = token_f1(answer, q.get("ground_truth", []))
        total_tokens = prompt_tokens + completion_tokens
        rds         = scores["f1"] / total_tokens if total_tokens > 0 else 0.0
        cost        = (prompt_tokens * PRICE_INPUT
                       + completion_tokens * PRICE_OUTPUT
                       + retrieved_tokens * PRICE_EMBED)

        result = {
            **q,
            "system": "rag",
            "retrieved_context": context,
            "predicted_answer": answer,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "retrieved_tokens": retrieved_tokens,
            "f1": scores["f1"],
            "precision": scores["precision"],
            "recall": scores["recall"],
            "rds": round(rds, 8),
            "cost_usd": round(cost, 6),
            "latency_ms": latency_ms
        }
        results.append(result)

        if (i + 1) % 25 == 0:
            avg_f1 = sum(r["f1"] for r in results) / len(results)
            avg_tok = sum(r["total_tokens"] for r in results) / len(results)
            print(f"    [{i+1}/{len(queries)}] avg F1={avg_f1:.3f} avg_tokens={avg_tok:.0f}")

        time.sleep(0.2)

    return results


def summarize(results: list[dict]) -> dict:
    if not results:
        return {}
    by_type = defaultdict(list)
    for r in results:
        by_type[r.get("query_type") or r.get("type", "unknown")].append(r)

    type_f1 = {k: round(sum(r["f1"] for r in v) / len(v), 4)
               for k, v in by_type.items()}

    all_f1   = [r["f1"] for r in results]
    all_rds  = [r["rds"] for r in results if r.get("rds", 0) > 0]
    all_tok  = [r.get("total_tokens", 0) for r in results]
    all_cost = [r.get("cost_usd", 0) for r in results]

    by_hop = defaultdict(list)
    for r in results:
        by_hop[r.get("hop_depth", 0)].append(r["f1"])
    hop_f1 = {k: round(sum(v)/len(v), 4) for k, v in by_hop.items()}

    return {
        "n_queries": len(results),
        "macro_f1":  round(sum(all_f1) / len(all_f1), 4),
        "macro_rds": round(sum(all_rds) / len(all_rds), 8) if all_rds else 0,
        "mean_tokens": round(sum(all_tok) / len(all_tok), 1) if all_tok else 0,
        "total_cost_usd": round(sum(all_cost), 4),
        "f1_by_type": type_f1,
        "f1_by_hop":  hop_f1,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain",   help="Single domain to run")
    parser.add_argument("--all",      action="store_true", help="Run all domains with corpus")
    parser.add_argument("--dry-run",  action="store_true", help="Skip Claude calls, test retrieval only")
    parser.add_argument("--reindex",  action="store_true", help="Rebuild FAISS indexes from scratch")
    parser.add_argument("--limit",    type=int, default=0, help="Limit queries per domain (0=all)")
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key    = os.environ.get("OPENAI_API_KEY")

    if not anthropic_key and not args.dry_run:
        raise SystemExit("Set ANTHROPIC_API_KEY or use --dry-run")
    if not openai_key and not args.dry_run:
        raise SystemExit("Set OPENAI_API_KEY (required for embeddings)")

    ant_client = anthropic.Anthropic(api_key=anthropic_key) if not args.dry_run else None
    oai_client = openai.OpenAI(api_key=openai_key) if openai_key else None

    if args.reindex:
        for p in INDEX_DIR.glob("*.faiss"):
            p.unlink()
        for p in INDEX_DIR.glob("*_chunks.pkl"):
            p.unlink()
        print("Cleared cached indexes.")

    if args.domain:
        domains = [args.domain]
    elif args.all:
        # Only domains that have both queries AND corpus content
        domains = []
        for qf in sorted(QUERIES_DIR.glob("queries_*.jsonl")):
            d = qf.stem.replace("queries_", "")
            chapters_dir = CORPUS_DIR / d / "docs" / "chapters"
            if chapters_dir.exists() and any(chapters_dir.iterdir()):
                domains.append(d)
    else:
        parser.print_help()
        return

    print(f"\nRAG Harness — {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Model: {CLAUDE_MODEL}")
    print(f"Embed: {EMBED_MODEL} (top-{TOP_K} chunks, {CHUNK_TOKENS}-token windows)")
    print(f"Domains: {len(domains)}\n")

    all_results     = []
    domain_summaries = {}

    for domain in domains:
        # Skip already-completed domains (unless re-running)
        out_path = RESULTS_DIR / f"rag_{domain}.jsonl"
        if out_path.exists() and not args.dry_run:
            print(f"SKIP {domain} (done)")
            continue

        print(f"── {domain}")
        results = run_domain(domain, ant_client, oai_client, dry_run=args.dry_run)

        if args.limit:
            results = results[:args.limit]

        if results:
            with open(out_path, "w") as f:
                for r in results:
                    f.write(json.dumps(r) + "\n")

            summary = summarize(results)
            domain_summaries[domain] = summary
            all_results.extend(results)

            if not args.dry_run:
                print(f"   F1={summary['macro_f1']}  tokens={summary['mean_tokens']:.0f}  "
                      f"RDS={summary['macro_rds']:.6f}  cost=${summary['total_cost_usd']:.3f}")

    if all_results:
        global_summary = summarize(all_results)
        global_summary["by_domain"] = domain_summaries

        with open(RESULTS_DIR / "rag_summary.json", "w") as f:
            json.dump(global_summary, f, indent=2)

        print(f"\n── GLOBAL SUMMARY ──")
        print(f"   Domains:      {len(domain_summaries)}")
        print(f"   Queries:      {global_summary['n_queries']}")
        print(f"   Macro F1:     {global_summary['macro_f1']}")
        print(f"   Mean tokens:  {global_summary['mean_tokens']:.0f}")
        print(f"   Macro RDS:    {global_summary['macro_rds']:.6f}")
        print(f"   Total cost:   ${global_summary['total_cost_usd']:.3f}")
        print(f"\n   F1 by query type:")
        for qtype, f1 in sorted(global_summary["f1_by_type"].items()):
            print(f"     {qtype}: {f1}")
        print(f"\n   F1 by hop depth:")
        for hop, f1 in sorted(global_summary["f1_by_hop"].items()):
            print(f"     hop={hop}: {f1}")
        print(f"\n   Results written to: {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
