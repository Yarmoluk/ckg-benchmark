#!/usr/bin/env python3
"""
Parallel GraphRAG runner — 4 domains simultaneously.

Usage:
    cd /Users/danielyarmoluk/Desktop/projects/ckg-benchmark
    python run_parallel.py

Starts the local embed server once, then runs graphrag_harness.py
for each domain in batches of 4. Already-completed domains are skipped
automatically (harness checks results/graphrag/graphrag_{domain}.jsonl).
"""

import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Config ─────────────────────────────────────────────────────────────────────
WORKERS       = 8

# These 3 domains are excluded from GraphRAG due to indexing cost ($59 combined).
# They remain in CKG and RAG benchmarks. Note in paper:
# "GraphRAG indexing cost scales prohibitively with corpus size — three largest
#  domains (learning-linux 3MB, microsims 2MB, tracking-ai 1MB) excluded."
EXCLUDE = {"learning-linux", "microsims", "tracking-ai-course"}
PROJECT_ROOT  = Path(__file__).parent
HARNESS       = PROJECT_ROOT / "evaluation" / "graphrag_harness.py"
RESULTS_DIR   = PROJECT_ROOT / "results" / "graphrag"
QUERIES_DIR   = PROJECT_ROOT / "benchmark" / "queries"
CORPUS_DIR    = PROJECT_ROOT / "corpus"
EMBED_PORT    = 4001
LOG_DIR       = PROJECT_ROOT / "results" / "parallel_logs"

# ── Helpers ────────────────────────────────────────────────────────────────────

def embed_server_running(port: int) -> bool:
    with socket.socket() as s:
        return s.connect_ex(("localhost", port)) == 0


def start_embed_server() -> subprocess.Popen:
    """Start the local sentence-transformer embed server on port 4001."""
    if embed_server_running(EMBED_PORT):
        print(f"[embed] server already running on port {EMBED_PORT}")
        return None
    server_script = PROJECT_ROOT / "evaluation" / "embed_server.py"
    print(f"[embed] starting local embed server on port {EMBED_PORT}...")
    proc = subprocess.Popen(
        [sys.executable, str(server_script), "--port", str(EMBED_PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for i in range(60):
        time.sleep(1)
        if embed_server_running(EMBED_PORT):
            print(f"[embed] ready after {i+1}s")
            return proc
    print("[embed] WARNING: server did not start after 60s — embeddings may fail")
    return proc


def get_domains() -> list[str]:
    """All domains that have both a queries file and corpus chapters."""
    domains = []
    for qf in sorted(QUERIES_DIR.glob("queries_*.jsonl")):
        domain = qf.stem.replace("queries_", "")
        chapters_dir = CORPUS_DIR / domain / "docs" / "chapters"
        if chapters_dir.exists() and any(chapters_dir.iterdir()):
            domains.append(domain)
    return domains


def already_done(domain: str) -> bool:
    return (RESULTS_DIR / f"graphrag_{domain}.jsonl").exists()


def run_domain(domain: str) -> tuple[str, bool, str]:
    """Run harness for one domain. Returns (domain, success, summary)."""
    log_file = LOG_DIR / f"{domain}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, str(HARNESS),
        "--domain", domain,
        "--local-embed",
    ]

    env = {
        **os.environ,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
        "GRAPHRAG_EMBED_KEY": "local",
    }

    with open(log_file, "w") as log:
        try:
            result = subprocess.run(
                cmd,
                stdout=log,
                stderr=subprocess.STDOUT,
                env=env,
                cwd=str(PROJECT_ROOT),
                timeout=7200,  # 2hr max per domain
            )
            success = result.returncode == 0 and already_done(domain)
            summary = "OK" if success else f"exit={result.returncode}"
        except subprocess.TimeoutExpired:
            success = False
            summary = "TIMEOUT (2hr)"
        except Exception as e:
            success = False
            summary = str(e)

    return domain, success, summary


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        # Try loading from calculus .env
        env_file = PROJECT_ROOT / "results" / "graphrag_workspaces" / "calculus" / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip()
                    print(f"[env] loaded ANTHROPIC_API_KEY from calculus .env")
                    break
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit("ERROR: ANTHROPIC_API_KEY not set")

    domains = get_domains()
    domains = [d for d in domains if d not in EXCLUDE]
    todo    = [d for d in domains if not already_done(d)]
    done    = [d for d in domains if already_done(d)]

    print(f"\n{'='*60}")
    print(f"  GraphRAG Parallel Runner — {WORKERS} workers")
    print(f"  Total domains:     {len(domains)}")
    print(f"  Excluded (cost):   {', '.join(sorted(EXCLUDE))}")
    print(f"  Already done:      {len(done)}")
    print(f"  Queued to run:     {len(todo)}")
    print(f"  Est. cost:         ~$110  (budget: $121.89)")
    print(f"{'='*60}\n")

    if done:
        print(f"[skip] {', '.join(done)}\n")

    if not todo:
        print("All domains complete!")
        return

    # Start embed server once for all workers
    embed_proc = start_embed_server()
    time.sleep(2)  # small buffer

    t_start   = time.time()
    succeeded = []
    failed    = []

    try:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(run_domain, d): d for d in todo}
            for i, future in enumerate(as_completed(futures), 1):
                domain, success, summary = future.result()
                elapsed = int(time.time() - t_start)
                status  = "✓" if success else "✗"
                remaining = len(todo) - i
                eta_min = int((elapsed / i) * remaining / 60) if i > 0 else "?"
                print(f"  {status} [{i}/{len(todo)}] {domain:<40} {summary}  "
                      f"| elapsed {elapsed//60}m | ~{eta_min}m remaining")
                (succeeded if success else failed).append(domain)
    finally:
        if embed_proc:
            embed_proc.terminate()
            print("\n[embed] server stopped")

    total = int(time.time() - t_start)
    print(f"\n{'='*60}")
    print(f"  Done in {total//3600}h {(total%3600)//60}m")
    print(f"  Succeeded: {len(succeeded)}")
    print(f"  Failed:    {len(failed)}")
    if failed:
        print(f"  Failed domains: {', '.join(failed)}")
        print(f"  Re-run:  python run_parallel.py  (failed domains auto-retry)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
