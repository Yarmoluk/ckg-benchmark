"""
LangChain RAG retriever for KRB benchmark.

Uses: FAISS + HuggingFaceEmbeddings (all-MiniLM-L6-v2) — standard LangChain RAG stack.
Builds one FAISS index per domain from the learning-graph CSV, retrieves top-5 chunks.

Usage:
    python evaluation/langchain_retriever.py --domain calculus --dry-run
    python evaluation/langchain_retriever.py --domain calculus biology
    python evaluation/langchain_retriever.py --all
"""

import csv
import sys
import argparse
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from evaluation.krb_eval import Retriever, run_eval


class LangChainRetriever(Retriever):
    """
    Standard LangChain RAG: FAISS vector store over domain CSV concepts,
    HuggingFace sentence-transformers embeddings, top-5 retrieval.
    """

    def __init__(self, embed_model: str = "all-MiniLM-L6-v2", top_k: int = 5):
        self._retrievers = {}
        self._embed_model = embed_model
        self._top_k = top_k
        self._embeddings = None

    def _get_embeddings(self):
        if self._embeddings is None:
            from langchain_huggingface import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self._embed_model,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        return self._embeddings

    def setup(self, domain: str, graph_path: Path):
        from langchain_community.vectorstores import FAISS

        docs = []
        with open(graph_path) as f:
            for row in csv.DictReader(f):
                label = row["ConceptLabel"].strip()
                tax   = row.get("TaxonomyID", "GEN").strip()
                deps  = row.get("Dependencies", "").strip()
                dep_labels = deps.replace("|", ", ") if deps else "none"
                docs.append(
                    f"[{tax}] {label} | prerequisites: {dep_labels}"
                )

        embeddings = self._get_embeddings()
        vs = FAISS.from_texts(docs, embeddings)
        self._retrievers[domain] = vs.as_retriever(
            search_kwargs={"k": self._top_k}
        )

    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        r = self._retrievers.get(domain)
        if not r:
            return ""
        chunks = r.invoke(query_text)
        context = "\n".join(c.page_content for c in chunks)
        return f"RETRIEVED CONTEXT:\n{context}"


def main():
    p = argparse.ArgumentParser(
        description="Run LangChain RAG baseline against KRB benchmark"
    )
    p.add_argument("--domain", nargs="+", help="Domains to evaluate")
    p.add_argument("--all", action="store_true", help="Run all domains")
    p.add_argument("--dry-run", action="store_true", help="Skip API calls")
    p.add_argument("--limit", type=int, default=0, help="Max queries per domain")
    p.add_argument("--embed-model", default="all-MiniLM-L6-v2")
    p.add_argument("--top-k", type=int, default=5)
    args = p.parse_args()

    if not args.domain and not args.all:
        p.print_help()
        return

    retriever = LangChainRetriever(
        embed_model=args.embed_model,
        top_k=args.top_k,
    )

    results = run_eval(
        retriever=retriever,
        system_name=f"langchain-faiss-{args.embed_model.split('/')[-1]}",
        domains=args.domain if args.domain else None,
        dry_run=args.dry_run,
        limit=args.limit,
        output_dir=Path("krb_results"),
    )

    return results


if __name__ == "__main__":
    main()
