#!/usr/bin/env python3
"""
RAGAS-stack RAG retriever for KRB benchmark.

Retrieval:  ChromaDB (ephemeral) + sentence-transformers MiniLM, top-5.
Evaluation: standard KRB token F1 + optional RAGAS metrics
            (Faithfulness, ResponseRelevancy, LLMContextRecall).

Install:
    pip install chromadb sentence-transformers langchain-anthropic langchain-huggingface
    pip install ragas  # only needed for --ragas-eval

Usage:
    # Test retrieval pipeline — no API calls
    python evaluation/ragas_retriever.py --domain calculus --dry-run

    # Full KRB eval — 2 domains (~$0.30 Haiku)
    ANTHROPIC_API_KEY=sk-ant-... python evaluation/ragas_retriever.py --domain calculus biology

    # Full benchmark — all domains (~$5 Haiku)
    ANTHROPIC_API_KEY=sk-ant-... python evaluation/ragas_retriever.py --all

    # KRB eval + RAGAS metrics (Faithfulness / Relevancy / Context Recall)
    ANTHROPIC_API_KEY=sk-ant-... python evaluation/ragas_retriever.py --domain calculus --ragas-eval

Submit results:
    github.com/Yarmoluk/ckg-benchmark/issues/new?template=submission.md
    Attach: krb_results/krb_submission_chromadb-minilm-top5.json
"""

import csv
import sys
import argparse
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

sys.path.insert(0, str(Path(__file__).parent.parent))
from evaluation.krb_eval import Retriever, run_eval


# ── Retriever ─────────────────────────────────────────────────────────────────

class RAGASRetriever(Retriever):
    """
    ChromaDB + sentence-transformers dense retrieval.

    Mirrors the retrieval stack recommended in RAGAS documentation.
    Override retrieve() or setup() to swap in your own vector store.

    With --ragas-eval, also scores the (query, contexts, answer) triples
    with RAGAS v0.2 metrics after the KRB eval completes.
    """

    def __init__(
        self,
        embed_model: str = "all-MiniLM-L6-v2",
        top_k: int = 5,
        collect_ragas: bool = False,
    ):
        self._embed_model   = embed_model
        self._top_k         = top_k
        self._collect_ragas = collect_ragas
        self._collections   = {}   # domain → chromadb collection
        self._client        = None
        self._embed_fn      = None
        self._ragas_triples: list[tuple[str, list[str], str]] = []

    # ── ChromaDB helpers ──────────────────────────────────────────────────────

    def _chroma_client(self):
        if self._client is None:
            import chromadb
            self._client = chromadb.EphemeralClient()
        return self._client

    def _embedding_fn(self):
        if self._embed_fn is None:
            from chromadb.utils.embedding_functions import (
                SentenceTransformerEmbeddingFunction,
            )
            self._embed_fn = SentenceTransformerEmbeddingFunction(
                model_name=self._embed_model
            )
        return self._embed_fn

    # ── Retriever interface ───────────────────────────────────────────────────

    def setup(self, domain: str, graph_path: Path):
        """Index one domain's concept CSV into an ephemeral ChromaDB collection."""
        client   = self._chroma_client()
        embed_fn = self._embedding_fn()

        coll_name = domain.replace("-", "_")[:63]
        try:
            client.delete_collection(coll_name)
        except Exception:
            pass

        collection = client.create_collection(
            name=coll_name,
            embedding_function=embed_fn,
        )

        docs, ids, metas = [], [], []
        with open(graph_path) as f:
            for i, row in enumerate(csv.DictReader(f)):
                label = row["ConceptLabel"].strip()
                tax   = row.get("TaxonomyID", "GEN").strip()
                deps  = row.get("Dependencies", "").replace("|", ", ") or "none"
                docs.append(f"[{tax}] {label} | prerequisites: {deps}")
                ids.append(f"{domain}_{i}")
                metas.append({"domain": domain, "label": label})

        if docs:
            collection.add(documents=docs, ids=ids, metadatas=metas)

        self._collections[domain] = collection

    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        """Dense retrieval: top-k concept strings from ChromaDB."""
        collection = self._collections.get(domain)
        if not collection:
            return ""

        n = min(self._top_k, collection.count())
        results = collection.query(query_texts=[query_text], n_results=n)
        chunks  = results["documents"][0] if results["documents"] else []
        return "RETRIEVED CONTEXT:\n" + "\n".join(chunks)

    def generate(
        self, context: str, query_text: str, client, model: str
    ) -> tuple[str, int, int]:
        """
        Wraps the default Claude generation.
        When --ragas-eval is on, captures (query, contexts, answer) for RAGAS scoring.
        """
        answer, pt, ct = super().generate(context, query_text, client, model)

        if self._collect_ragas:
            chunks = [
                line for line in context.splitlines()
                if line.strip() and not line.startswith("RETRIEVED CONTEXT")
            ]
            self._ragas_triples.append((query_text, chunks, answer))

        return answer, pt, ct

    # ── RAGAS evaluation pass ─────────────────────────────────────────────────

    def run_ragas_eval(
        self,
        output_path: Path,
        model: str = "claude-haiku-4-5-20251001",
    ) -> dict:
        """
        Score collected (query, contexts, answer) triples with RAGAS v0.2 metrics.
        Writes per-sample CSV to output_path. Returns mean scores dict.

        Requires: pip install ragas langchain-anthropic langchain-huggingface
        """
        try:
            from ragas import SingleTurnSample, EvaluationDataset, evaluate
            from ragas.llms import LangchainLLMWrapper
            from ragas.embeddings import LangchainEmbeddingsWrapper
            from ragas.metrics import (
                Faithfulness,
                ResponseRelevancy,
                LLMContextRecall,
            )
            from langchain_anthropic import ChatAnthropic
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError as exc:
            print(f"\nRAGAS eval skipped — missing package: {exc}")
            print("  pip install ragas langchain-anthropic langchain-huggingface")
            return {}

        if not self._ragas_triples:
            print("\nRAGAS eval skipped — no triples collected (used --dry-run?).")
            return {}

        print(f"\nRunning RAGAS v0.2 eval on {len(self._ragas_triples)} samples…")

        llm = LangchainLLMWrapper(ChatAnthropic(model=model, temperature=0))
        emb = LangchainEmbeddingsWrapper(
            HuggingFaceEmbeddings(
                model_name=self._embed_model,
                encode_kwargs={"normalize_embeddings": True},
            )
        )

        samples = [
            SingleTurnSample(
                user_input=query,
                retrieved_contexts=contexts if contexts else [""],
                response=answer,
                reference=answer,   # KRB ground truth not surfaced here; use answer as ref
            )
            for query, contexts, answer in self._ragas_triples
        ]

        dataset = EvaluationDataset(samples=samples)
        result  = evaluate(
            dataset=dataset,
            metrics=[Faithfulness(), ResponseRelevancy(), LLMContextRecall()],
            llm=llm,
            embeddings=emb,
        )

        df = result.to_pandas()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

        cols  = [c for c in ["faithfulness", "response_relevancy", "llm_context_recall"] if c in df.columns]
        means = df[cols].mean().to_dict()

        print(f"\nRAGAS metrics (mean across {len(df)} samples):")
        for k, v in means.items():
            print(f"  {k:<26} {v:.4f}")
        print(f"\nPer-sample scores → {output_path}")

        return means


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="KRB benchmark — ChromaDB/RAGAS RAG retriever",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--domain",      nargs="+", help="Domains to evaluate")
    p.add_argument("--all",         action="store_true", help="Run all domains")
    p.add_argument("--dry-run",     action="store_true", help="Skip API calls")
    p.add_argument("--limit",       type=int, default=0, help="Max queries per domain")
    p.add_argument("--top-k",       type=int, default=5, help="Retrieval top-k (default 5)")
    p.add_argument("--embed-model", default="all-MiniLM-L6-v2",
                   help="sentence-transformers model name")
    p.add_argument("--ragas-eval",  action="store_true",
                   help="Run RAGAS v0.2 metrics after KRB eval (requires ragas package)")
    p.add_argument("--output",      default="krb_results", help="Output directory")
    args = p.parse_args()

    if not args.domain and not args.all:
        p.print_help()
        return

    system_name = f"chromadb-{args.embed_model.split('/')[-1]}-top{args.top_k}"

    retriever = RAGASRetriever(
        embed_model=args.embed_model,
        top_k=args.top_k,
        collect_ragas=args.ragas_eval and not args.dry_run,
    )

    summary = run_eval(
        retriever=retriever,
        system_name=system_name,
        domains=args.domain if args.domain else None,
        dry_run=args.dry_run,
        limit=args.limit,
        output_dir=Path(args.output),
    )

    if args.ragas_eval and not args.dry_run and summary:
        ragas_path = Path(args.output) / f"ragas_{system_name}.csv"
        retriever.run_ragas_eval(ragas_path)

    if summary and not args.dry_run:
        print(
            f"\nSubmit at: github.com/Yarmoluk/ckg-benchmark/issues/new"
            f"?template=submission.md&title=Submission%3A+{system_name}"
        )

    return summary


if __name__ == "__main__":
    main()
