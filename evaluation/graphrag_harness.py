"""
GraphRAG Harness — Microsoft GraphRAG v3.x baseline.

For each benchmark domain, this harness:
1. Creates a per-domain GraphRAG workspace in results/graphrag_workspaces/{domain}/
2. Copies corpus .md files into workspace input/
3. Runs 'graphrag index' to build the knowledge graph (entity extraction,
   community detection, community reports)
4. Queries using 'graphrag query --method local' per benchmark query
5. Parses the CLI output, scores F1/RDS, and writes results

LLM:        Claude Sonnet 4.6 via Anthropic API (using LiteLLM's anthropic provider)
Embeddings: OpenAI text-embedding-3-small (configurable via --embed-key)
            OR local sentence-transformers via a LiteLLM proxy (see --local-embed)

Usage:
    # Full run (requires ANTHROPIC_API_KEY and OPENAI_API_KEY for embeddings):
    python evaluation/graphrag_harness.py --domain calculus

    # Use local embeddings (no OpenAI key needed — starts a LiteLLM proxy):
    python evaluation/graphrag_harness.py --domain calculus --local-embed

    # Dry run — index only, skip Claude queries (tests pipeline):
    python evaluation/graphrag_harness.py --domain calculus --dry-run

    # All available domains:
    python evaluation/graphrag_harness.py --all

    # Skip re-indexing if workspace already exists:
    python evaluation/graphrag_harness.py --all --skip-index

Architecture note:
    GraphRAG indexes text by extracting entities + relationships via many LLM
    calls, then clusters them into communities. Each query triggers additional
    LLM calls. This makes GraphRAG 30-100x more expensive to index than RAG,
    and 5-10x more expensive per query — the core efficiency gap the paper
    documents.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
import textwrap
import argparse
from collections import defaultdict
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CLAUDE_MODEL   = "claude-haiku-4-5-20251001"
EMBED_MODEL    = "text-embedding-3-small"   # OpenAI (cheapest), configurable
LOCAL_EMBED_PORT = 4001                      # LiteLLM proxy port for local embeds

CORPUS_DIR    = Path("corpus")
QUERIES_DIR   = Path("benchmark/queries")
RESULTS_DIR   = Path("results/graphrag")
WORKSPACE_DIR = Path("results/graphrag_workspaces")

PRICE_INPUT  = 3.0  / 1_000_000   # Claude Sonnet 4.6: $3 per 1M input
PRICE_OUTPUT = 15.0 / 1_000_000   # $15 per 1M output
# Embedding: text-embedding-3-small $0.02/1M tokens
PRICE_EMBED  = 0.02 / 1_000_000

STOPWORDS = {
    "what","is","the","a","an","of","for","are","in","and","or","to","with",
    "how","does","related","which","these","those","all","list","describe",
    "explain","between","concept","concepts","based","on","knowledge","graph",
    "subgraph","prerequisites","prerequisite","following"
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize_text(text: str) -> str:
    text = re.sub(r'\*+', ' ', text)
    text = re.sub(r'_+', ' ', text)
    text = re.sub(r'`+', ' ', text)
    text = re.sub(r'#+\s*', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def token_f1(predicted: str, ground_truth: list[str]) -> dict:
    pred_tokens  = set(normalize_text(predicted).lower().split()) - STOPWORDS
    truth_tokens = set(normalize_text(" ".join(ground_truth)).lower().split()) - STOPWORDS
    if not pred_tokens and not truth_tokens:
        return {"f1": 1.0, "precision": 1.0, "recall": 1.0}
    if not pred_tokens or not truth_tokens:
        return {"f1": 0.0, "precision": 0.0, "recall": 0.0}
    tp = len(pred_tokens & truth_tokens)
    p  = tp / len(pred_tokens)
    r  = tp / len(truth_tokens)
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return {"f1": round(f1, 4), "precision": round(p, 4), "recall": round(r, 4)}


def strip_markdown(text: str) -> str:
    text = re.sub(r'<details>.*?</details>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^!!!\s+\w+.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def load_corpus_docs(domain: str) -> list[dict]:
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
        raw  = index_file.read_text(encoding="utf-8", errors="ignore")
        text = strip_markdown(raw)
        if len(text) > 200:
            docs.append({"source": chapter_path.name, "text": text})
    for extra in ["glossary.md", "course-description.md"]:
        extra_path = CORPUS_DIR / domain / "docs" / extra
        if extra_path.exists():
            raw  = extra_path.read_text(encoding="utf-8", errors="ignore")
            text = strip_markdown(raw)
            if len(text) > 200:
                docs.append({"source": extra, "text": text})
    return docs

# ── Workspace management ──────────────────────────────────────────────────────

SETTINGS_TEMPLATE = """\
### GraphRAG settings — auto-generated by graphrag_harness.py

completion_models:
  default_completion_model:
    model_provider: anthropic
    model: {claude_model}
    auth_method: api_key
    api_key: ${{ANTHROPIC_API_KEY}}
    retry:
      type: exponential_backoff

embedding_models:
  default_embedding_model:
    model_provider: {embed_provider}
    model: {embed_model}
    auth_method: api_key
    api_key: ${{GRAPHRAG_EMBED_KEY}}
{embed_api_base}    retry:
      type: exponential_backoff

input:
  type: text

chunking:
  type: tokens
  size: 1200
  overlap: 100
  encoding_model: o200k_base

input_storage:
  type: file
  base_dir: "input"

output_storage:
  type: file
  base_dir: "output"

reporting:
  type: file
  base_dir: "logs"

cache:
  type: json
  storage:
    type: file
    base_dir: "cache"

vector_store:
  type: lancedb
  db_uri: output/lancedb

embed_text:
  embedding_model_id: default_embedding_model

extract_graph:
  completion_model_id: default_completion_model
  entity_types: [concept, prerequisite, category, skill, topic]
  max_gleanings: 0

summarize_descriptions:
  completion_model_id: default_completion_model
  max_length: 300

cluster_graph:
  max_cluster_size: 10

extract_claims:
  enabled: false

community_reports:
  completion_model_id: default_completion_model
  max_length: 1500
  max_input_length: 6000

local_search:
  completion_model_id: default_completion_model
  embedding_model_id: default_embedding_model

global_search:
  completion_model_id: default_completion_model

snapshots:
  graphml: false
  embeddings: false
"""


def setup_workspace(domain: str, docs: list[dict], args) -> Path:
    """Create a GraphRAG workspace for a domain. Returns workspace path."""
    ws = WORKSPACE_DIR / domain
    ws.mkdir(parents=True, exist_ok=True)
    (ws / "input").mkdir(exist_ok=True)
    (ws / "output").mkdir(exist_ok=True)
    (ws / "logs").mkdir(exist_ok=True)
    (ws / "cache").mkdir(exist_ok=True)

    # Write corpus docs as .txt files into input/
    for i, doc in enumerate(docs):
        fname = ws / "input" / f"{doc['source'].replace('/', '_')}.txt"
        fname.write_text(doc["text"], encoding="utf-8")

    # Determine embedding config
    if args.local_embed:
        embed_provider = "openai"
        embed_model    = "text-embedding-ada-002"   # name LiteLLM proxy accepts
        embed_api_base = f"    api_base: http://localhost:{LOCAL_EMBED_PORT}\n"
        embed_key      = "local"
    else:
        embed_provider = "openai"
        embed_model    = args.embed_model
        embed_api_base = ""
        embed_key      = os.environ.get("OPENAI_API_KEY", "")

    # When using local embeddings, inline the placeholder key directly
    # (avoids env var resolution issues with empty GRAPHRAG_EMBED_KEY)
    if args.local_embed:
        settings_embed_key = "local-embeddings-proxy"
    else:
        settings_embed_key = "${GRAPHRAG_EMBED_KEY}"

    settings = SETTINGS_TEMPLATE.format(
        claude_model      = CLAUDE_MODEL,
        embed_provider    = embed_provider,
        embed_model       = embed_model,
        embed_api_base    = embed_api_base,
    ).replace("${GRAPHRAG_EMBED_KEY}", settings_embed_key if args.local_embed else "${GRAPHRAG_EMBED_KEY}")
    (ws / "settings.yaml").write_text(settings)

    # .env file for API keys
    # GraphRAG validates that api_key is non-empty when auth_method=api_key,
    # so use a placeholder for local embeddings
    env_embed_key = embed_key if embed_key else "placeholder-not-used"
    env_content = (
        f"ANTHROPIC_API_KEY={os.environ.get('ANTHROPIC_API_KEY', '')}\n"
        f"GRAPHRAG_EMBED_KEY={env_embed_key}\n"
    )
    (ws / ".env").write_text(env_content)

    return ws


def run_index(ws: Path, domain: str, timeout: int = 3600) -> bool:
    """Run graphrag index on a workspace. Returns True on success."""
    # Skip if already indexed (output/create/ directory exists)
    if (ws / "output" / "create").exists():
        parquets = list((ws / "output" / "create").glob("*.parquet"))
        if parquets:
            print(f"    [skip index] {domain} — already indexed ({len(parquets)} parquet files)")
            return True

    print(f"    indexing {domain} (this takes several minutes — many LLM calls)...")
    t0 = time.time()
    try:
        result = subprocess.run(
            ["graphrag", "index", "--root", str(ws)],
            capture_output=True, text=True, timeout=timeout,
            env={**os.environ,
                 "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
                 "GRAPHRAG_EMBED_KEY": (os.environ.get("OPENAI_API_KEY", "")
                                        if not hasattr(ws, '_local_embed') else "local")}
        )
        elapsed = int(time.time() - t0)
        if result.returncode != 0:
            print(f"    ERROR indexing {domain} (exit {result.returncode}, {elapsed}s):")
            print(result.stderr[-2000:])
            return False
        print(f"    indexed {domain} in {elapsed}s")
        return True
    except subprocess.TimeoutExpired:
        print(f"    TIMEOUT indexing {domain} after {timeout}s")
        return False
    except Exception as e:
        print(f"    EXCEPTION indexing {domain}: {e}")
        return False


def run_query(ws: Path, query_text: str, method: str = "local", timeout: int = 120) -> dict:
    """Run a single graphrag query. Returns {answer, tokens_estimate, cost_estimate}."""
    t0 = time.time()
    try:
        result = subprocess.run(
            ["graphrag", "query",
             "--root", str(ws),
             "--method", method,
             "--response-type", "Concise list or single sentence",
             query_text],
            capture_output=True, text=True, timeout=timeout,
            env={**os.environ,
                 "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "")}
        )
        latency_ms = int((time.time() - t0) * 1000)

        if result.returncode != 0:
            return {"answer": "", "latency_ms": latency_ms, "error": result.stderr[-500:]}

        # Parse answer from CLI output — graphrag prints "SUCCESS: ..." then the answer
        output = result.stdout + result.stderr
        answer = _parse_graphrag_output(output)

        # GraphRAG doesn't expose per-query token counts via CLI.
        # Estimate based on typical local search behavior:
        #   system prompt ~800t, context ~2500t, query ~50t, answer ~100t = ~3450t
        tokens_estimate = 3450
        cost_estimate   = (tokens_estimate * 0.85 * PRICE_INPUT
                           + tokens_estimate * 0.15 * PRICE_OUTPUT)

        return {
            "answer":         answer,
            "latency_ms":     latency_ms,
            "tokens_estimate": tokens_estimate,
            "cost_estimate":   round(cost_estimate, 6),
            "raw_output":     output[:500],
        }
    except subprocess.TimeoutExpired:
        return {"answer": "", "latency_ms": timeout * 1000, "error": "TIMEOUT"}
    except Exception as e:
        return {"answer": "", "latency_ms": 0, "error": str(e)}


def _parse_graphrag_output(output: str) -> str:
    """Extract the answer text from graphrag CLI output."""
    # Look for the SUCCESS line and everything after it
    lines = output.strip().split("\n")
    answer_lines = []
    capture = False
    for line in lines:
        if "SUCCESS:" in line:
            # The answer typically follows SUCCESS
            after = line.split("SUCCESS:", 1)[-1].strip()
            if after:
                answer_lines.append(after)
            capture = True
            continue
        if capture:
            # Skip log lines (they start with timestamps or INFO/WARNING)
            if re.match(r'^\d{4}-\d{2}|^INFO|^WARNING|^ERROR|^DEBUG', line):
                continue
            answer_lines.append(line)

    if answer_lines:
        return "\n".join(answer_lines).strip()

    # Fallback: return last non-empty, non-log line
    for line in reversed(lines):
        line = line.strip()
        if line and not re.match(r'^\d{4}-\d{2}|^INFO|^WARNING|^ERROR|^DEBUG', line):
            return line
    return ""

# ── Local embedding proxy ─────────────────────────────────────────────────────

_embed_proxy_proc = None

def start_local_embed_proxy(port: int = LOCAL_EMBED_PORT) -> bool:
    """Start the local embed_server.py (OpenAI-compatible) on the given port.
    Returns True if started (or already running)."""
    global _embed_proxy_proc
    import socket

    # Check if already running
    with socket.socket() as s:
        if s.connect_ex(("localhost", port)) == 0:
            print(f"    local embed server already running on port {port}")
            return True

    server_script = Path(__file__).parent / "embed_server.py"
    if not server_script.exists():
        print(f"    ERROR: embed_server.py not found at {server_script}")
        return False

    print(f"    starting local embedding server on port {port} (all-MiniLM-L6-v2)...")
    _embed_proxy_proc = subprocess.Popen(
        [sys.executable, str(server_script), "--port", str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    # Wait up to 30s for server to come up
    for _ in range(30):
        time.sleep(1)
        with socket.socket() as s:
            if s.connect_ex(("localhost", port)) == 0:
                print(f"    local embed server ready on port {port}")
                return True
    print(f"    WARNING: embed server did not start on port {port} after 30s")
    return False


def stop_local_embed_proxy():
    global _embed_proxy_proc
    if _embed_proxy_proc and _embed_proxy_proc.poll() is None:
        _embed_proxy_proc.terminate()
        _embed_proxy_proc = None

# ── Main harness ──────────────────────────────────────────────────────────────

def run_domain(domain: str, args) -> list[dict]:
    queries_file = QUERIES_DIR / f"queries_{domain}.jsonl"
    if not queries_file.exists():
        print(f"  ✗ no queries file for {domain}")
        return []

    docs = load_corpus_docs(domain)
    if not docs:
        print(f"  ✗ no corpus content for {domain}")
        return []

    print(f"── {domain}: {len(docs)} docs")
    ws = setup_workspace(domain, docs, args)

    if not args.skip_index:
        ok = run_index(ws, domain)
        if not ok:
            print(f"  ✗ indexing failed for {domain}")
            return []
    else:
        # Check workspace is ready
        if not any((ws / "output").iterdir()) if (ws / "output").exists() else True:
            print(f"  ✗ no index found for {domain} — run without --skip-index first")
            return []

    queries = []
    with open(queries_file) as f:
        for line in f:
            queries.append(json.loads(line))

    print(f"  querying {len(queries)} queries (method: {args.method})")

    results = []
    for i, q in enumerate(queries):
        query_text = q["query"]

        if args.dry_run:
            result = {
                **q,
                "system":          "graphrag",
                "method":          args.method,
                "predicted_answer": "[DRY RUN]",
                "total_tokens":    3450,
                "f1":              0.0,
                "precision":       0.0,
                "recall":          0.0,
                "rds":             0.0,
                "cost_usd":        0.0,
                "latency_ms":      0,
            }
            results.append(result)
            continue

        qr = run_query(ws, query_text, method=args.method)

        if "error" in qr and not qr.get("answer"):
            print(f"    ✗ query error on {q.get('id','?')}: {qr['error'][:100]}")
            continue

        scores = token_f1(qr["answer"], q.get("ground_truth", []))
        toks   = qr.get("tokens_estimate", 3450)
        rds    = scores["f1"] / toks if toks > 0 else 0.0

        result = {
            **q,
            "system":          "graphrag",
            "method":          args.method,
            "predicted_answer": qr["answer"],
            "total_tokens":    toks,
            "f1":              scores["f1"],
            "precision":       scores["precision"],
            "recall":          scores["recall"],
            "rds":             round(rds, 8),
            "cost_usd":        qr.get("cost_estimate", 0.0),
            "latency_ms":      qr["latency_ms"],
        }
        results.append(result)

        if (i + 1) % 10 == 0:
            avg_f1 = sum(r["f1"] for r in results) / len(results)
            print(f"    [{i+1}/{len(queries)}] avg F1={avg_f1:.3f}")

        time.sleep(0.5)   # rate-limit buffer

    return results


def summarize(results: list[dict]) -> dict:
    if not results:
        return {}
    by_type = defaultdict(list)
    for r in results:
        by_type[r.get("query_type") or r.get("type", "unknown")].append(r)

    type_f1  = {k: round(sum(r["f1"] for r in v) / len(v), 4)
                for k, v in by_type.items()}
    all_f1   = [r["f1"] for r in results]
    all_rds  = [r["rds"] for r in results if r.get("rds", 0) > 0]
    all_tok  = [r.get("total_tokens", 0) for r in results]
    all_cost = [r.get("cost_usd", 0) for r in results]

    return {
        "n_queries":      len(results),
        "macro_f1":       round(sum(all_f1) / len(all_f1), 4),
        "macro_rds":      round(sum(all_rds) / len(all_rds), 8) if all_rds else 0,
        "mean_tokens":    round(sum(all_tok) / len(all_tok), 1) if all_tok else 0,
        "total_cost_usd": round(sum(all_cost), 4),
        "f1_by_type":     type_f1,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain",      help="Single domain to run")
    parser.add_argument("--all",         action="store_true")
    parser.add_argument("--dry-run",     action="store_true", help="Build index only, skip queries")
    parser.add_argument("--skip-index",  action="store_true", help="Skip indexing (workspace must exist)")
    parser.add_argument("--method",      default="local", choices=["local","global","drift","basic"],
                        help="Query method (default: local)")
    parser.add_argument("--embed-model", default=EMBED_MODEL)
    parser.add_argument("--local-embed", action="store_true",
                        help="Use local sentence-transformers via LiteLLM proxy on port 4001")
    parser.add_argument("--limit",       type=int, default=0, help="Limit queries per domain")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY")

    if args.local_embed:
        if not start_local_embed_proxy(LOCAL_EMBED_PORT):
            print("WARNING: local embed proxy failed to start. Embeddings may fail.")
    elif not os.environ.get("OPENAI_API_KEY") and not args.skip_index:
        print("WARNING: No OPENAI_API_KEY. Embeddings will fail unless --local-embed is set.")
        print("         Use: python evaluation/graphrag_harness.py --local-embed <other args>")
        print("         Or set OPENAI_API_KEY for text-embedding-3-small.")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    if args.domain:
        domains = [args.domain]
    elif args.all:
        domains = []
        for qf in sorted(QUERIES_DIR.glob("queries_*.jsonl")):
            d = qf.stem.replace("queries_", "")
            chapters_dir = CORPUS_DIR / d / "docs" / "chapters"
            if chapters_dir.exists() and any(chapters_dir.iterdir()):
                domains.append(d)
    else:
        parser.print_help()
        return

    print(f"\nGraphRAG Harness — {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"LLM: {CLAUDE_MODEL} (Anthropic)")
    print(f"Embed: {'local/sentence-transformers via LiteLLM proxy' if args.local_embed else args.embed_model}")
    print(f"Query method: {args.method}")
    print(f"Domains: {len(domains)}\n")
    print("Note: GraphRAG indexing requires many LLM calls per domain (entity extraction,")
    print("      community reports). Expect 15-30 min and $2-5 per domain in API costs.\n")

    all_results      = []
    domain_summaries = {}

    for domain in domains:
        out_path = RESULTS_DIR / f"graphrag_{domain}.jsonl"
        if out_path.exists() and not args.dry_run:
            print(f"SKIP {domain} (done)")
            continue

        results = run_domain(domain, args)
        if args.limit:
            results = results[:args.limit]
        if results:
            with open(out_path, "w") as f:
                for r in results:
                    f.write(json.dumps(r) + "\n")
            summary = summarize(results)
            domain_summaries[domain] = summary
            all_results.extend(results)
            print(f"   {domain}: F1={summary['macro_f1']}  tokens~{summary['mean_tokens']:.0f}  "
                  f"cost=${summary['total_cost_usd']:.3f}")

    if args.local_embed:
        stop_local_embed_proxy()

    if all_results:
        global_summary = summarize(all_results)
        global_summary["n_domains"] = len(domain_summaries)
        global_summary["by_domain"] = domain_summaries

        with open(RESULTS_DIR / "graphrag_summary.json", "w") as f:
            json.dump(global_summary, f, indent=2)

        print(f"\n── GRAPHRAG GLOBAL SUMMARY ──")
        print(f"   Domains:      {len(domain_summaries)}")
        print(f"   Queries:      {global_summary['n_queries']}")
        print(f"   Macro F1:     {global_summary['macro_f1']}")
        print(f"   Mean tokens:  {global_summary['mean_tokens']:.0f}  (estimate)")
        print(f"   Macro RDS:    {global_summary['macro_rds']:.8f}")
        print(f"   Total cost:   ${global_summary['total_cost_usd']:.3f}  (estimate)")
        print(f"\n   F1 by query type:")
        for qtype, f1 in sorted(global_summary["f1_by_type"].items()):
            print(f"     {qtype}: {f1}")
        print(f"\n   Results: {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
