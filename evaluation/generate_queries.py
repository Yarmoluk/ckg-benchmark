"""
Generate benchmark queries from a McCreary learning-graph.csv file.

Usage:
    python generate_queries.py \
        --csv corpus/calculus/docs/learning-graph/learning-graph.csv \
        --domain calculus \
        --output benchmark/queries_calculus.jsonl
"""

import csv
import json
import argparse
import random
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Concept:
    id: int
    label: str
    dependencies: list[int]
    taxonomy_id: str


def load_csv(path: str) -> dict[int, Concept]:
    concepts = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = int(row["ConceptID"])
            deps = []
            if row.get("Dependencies", "").strip():
                deps = [int(d) for d in row["Dependencies"].split("|") if d.strip()]
            concepts[cid] = Concept(
                id=cid,
                label=row["ConceptLabel"].strip(),
                dependencies=deps,
                taxonomy_id=row["TaxonomyID"].strip()
            )
    return concepts


def build_reverse_map(concepts: dict[int, Concept]) -> dict[int, list[int]]:
    """Map concept -> list of concepts that depend on it."""
    rev = defaultdict(list)
    for c in concepts.values():
        for dep in c.dependencies:
            rev[dep].append(c.id)
    return rev


def bfs_path(concepts: dict, start_id: int, end_id: int) -> Optional[list[int]]:
    """Find shortest path from start to end in DAG."""
    from collections import deque
    visited = {start_id}
    queue = deque([[start_id]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end_id:
            return path
        for dep in concepts[node].dependencies:
            if dep not in visited:
                visited.add(dep)
                queue.append(path + [dep])
    return None


def generate_queries(
    concepts: dict[int, Concept],
    domain: str,
    seed: int = 42
) -> list[dict]:
    random.seed(seed)
    queries = []
    concept_list = list(concepts.values())
    rev_map = build_reverse_map(concepts)
    taxonomy_groups = defaultdict(list)
    for c in concept_list:
        taxonomy_groups[c.taxonomy_id].append(c)

    # T1: Entity lookup — one per concept (sample 50)
    sample_t1 = random.sample(concept_list, min(50, len(concept_list)))
    for c in sample_t1:
        queries.append({
            "id": f"{domain}_T1_{c.id}",
            "domain": domain,
            "type": "T1_entity",
            "query": f"What is {c.label}?",
            "ground_truth": [c.label, c.taxonomy_id],
            "concept_id": c.id,
            "hop_depth": 0
        })

    # T2: Direct dependency — concepts with ≥1 prerequisite (sample 50)
    with_deps = [c for c in concept_list if c.dependencies]
    sample_t2 = random.sample(with_deps, min(50, len(with_deps)))
    for c in sample_t2:
        dep_labels = [concepts[d].label for d in c.dependencies if d in concepts]
        queries.append({
            "id": f"{domain}_T2_{c.id}",
            "domain": domain,
            "type": "T2_dependency",
            "query": f"What are the prerequisites for {c.label}?",
            "ground_truth": dep_labels,
            "concept_id": c.id,
            "hop_depth": 1
        })

    # T3: Multi-hop path — find pairs with path length 2-5 (sample 25)
    foundational = [c for c in concept_list if not c.dependencies]
    terminal = [c for c in concept_list if not rev_map[c.id]]
    path_queries = []
    attempts = 0
    while len(path_queries) < 25 and attempts < 500:
        attempts += 1
        if not foundational or not terminal:
            break
        start = random.choice(foundational)
        end = random.choice(terminal)
        if start.id == end.id:
            continue
        path = bfs_path(concepts, end.id, start.id)  # follow deps back to root
        if path and 2 <= len(path) <= 6:
            path_labels = [concepts[pid].label for pid in path if pid in concepts]
            path_queries.append({
                "id": f"{domain}_T3_{start.id}_{end.id}",
                "domain": domain,
                "type": "T3_path",
                "query": f"What is the prerequisite chain from {start.label} to {end.label}?",
                "ground_truth": path_labels,
                "concept_id": end.id,
                "hop_depth": len(path) - 1,
                "path_ids": path
            })
    queries.extend(path_queries)

    # T4: Category aggregate — one per taxonomy category
    for tax_id, members in taxonomy_groups.items():
        queries.append({
            "id": f"{domain}_T4_{tax_id}",
            "domain": domain,
            "type": "T4_aggregate",
            "query": f"List all {tax_id} concepts in this knowledge graph",
            "ground_truth": [c.label for c in members],
            "taxonomy_id": tax_id,
            "hop_depth": 0
        })

    # T5: Cross-concept relationship — pairs sharing a direct dependency (sample 38)
    pairs = []
    for c in concept_list:
        for dep in c.dependencies:
            if dep in concepts:
                pairs.append((c, concepts[dep]))
    sample_t5 = random.sample(pairs, min(38, len(pairs)))
    for a, b in sample_t5:
        # Ground truth: shared neighbors
        a_neighbors = set(a.dependencies)
        b_neighbors = set(b.dependencies)
        shared = a_neighbors & b_neighbors
        shared_labels = [concepts[s].label for s in shared if s in concepts]
        queries.append({
            "id": f"{domain}_T5_{a.id}_{b.id}",
            "domain": domain,
            "type": "T5_cross_concept",
            "query": f"How does {a.label} relate to {b.label}?",
            "ground_truth": shared_labels + [b.label],  # b is direct dep of a
            "concept_id_a": a.id,
            "concept_id_b": b.id,
            "hop_depth": 1
        })

    return queries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to learning-graph.csv")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. calculus)")
    parser.add_argument("--output", required=True, help="Output .jsonl path")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    concepts = load_csv(args.csv)
    queries = generate_queries(concepts, args.domain, args.seed)

    with open(args.output, "w") as f:
        for q in queries:
            f.write(json.dumps(q) + "\n")

    type_counts = {}
    for q in queries:
        type_counts[q["type"]] = type_counts.get(q["type"], 0) + 1

    print(f"Generated {len(queries)} queries for domain '{args.domain}'")
    for qtype, count in sorted(type_counts.items()):
        print(f"  {qtype}: {count}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
