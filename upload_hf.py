from huggingface_hub import HfApi, create_repo
import os
from pathlib import Path

api = HfApi()
repo_id = "danyarm/ckg-benchmark"
bench_root = Path(__file__).parent

# Create dataset repo
try:
    create_repo(repo_id, repo_type="dataset", exist_ok=True)
    print(f"Repo ready: {repo_id}")
except Exception as e:
    print(f"Repo: {e}")

# Upload domain CSVs
domains_dir = bench_root / "benchmark" / "domains"
for domain_dir in sorted(domains_dir.iterdir()):
    csv = domain_dir / "learning-graph.csv"
    if csv.exists():
        api.upload_file(
            path_or_fileobj=str(csv),
            path_in_repo=f"domains/{domain_dir.name}/learning-graph.csv",
            repo_id=repo_id,
            repo_type="dataset",
        )
        print(f"  uploaded {domain_dir.name}")

# Upload query files
queries_dir = bench_root / "benchmark" / "queries"
if queries_dir.exists():
    for f in sorted(queries_dir.glob("*.jsonl")):
        api.upload_file(
            path_or_fileobj=str(f),
            path_in_repo=f"queries/{f.name}",
            repo_id=repo_id,
            repo_type="dataset",
        )
        print(f"  uploaded queries/{f.name}")

# Upload results tables
tables_dir = bench_root / "results" / "tables"
if tables_dir.exists():
    for f in sorted(tables_dir.glob("*.csv")):
        api.upload_file(
            path_or_fileobj=str(f),
            path_in_repo=f"results/{f.name}",
            repo_id=repo_id,
            repo_type="dataset",
        )
        print(f"  uploaded results/{f.name}")

# Upload README
readme_path = bench_root / "HF_README.md"
api.upload_file(
    path_or_fileobj=str(readme_path),
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type="dataset",
)
print("  uploaded README.md")

print("\nDone. Dataset live at huggingface.co/datasets/danyarm/ckg-benchmark")
