"""
Metrics for the CKG Benchmark.

Implements:
- Token-level F1 (SQuAD-style)
- Edge F1
- Reasoning Density Score (RDS)
- Context Utilization Rate (CUR)
- Cost Per Correct Answer (CPCA)
- Hop-Depth F1 tracking
- Relationship Precision
- Hallucination Rate
"""

from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional
import statistics


# Claude Sonnet 4.6 pricing (April 2026)
PRICE_INPUT_PER_TOKEN = 3.0 / 1_000_000   # $3 per 1M input tokens
PRICE_OUTPUT_PER_TOKEN = 15.0 / 1_000_000  # $15 per 1M output tokens


@dataclass
class QueryResult:
    query_id: str
    domain: str
    query_type: str         # T1_entity | T2_dependency | T3_path | T4_aggregate | T5_cross_concept
    system: str             # rag | graphrag | ckg
    predicted: list[str]    # Tokenized predicted answer
    ground_truth: list[str] # Tokenized ground truth
    hop_depth: int          # 0 = direct, 1 = one hop, etc.
    prompt_tokens: int
    completion_tokens: int
    retrieved_tokens: int   # Tokens in the retrieval context
    relevant_retrieved_tokens: int  # Retrieved tokens that appear in ground truth
    hallucinated_concepts: list[str] = field(default_factory=list)  # Concepts not in corpus


def token_f1(predicted: list[str], ground_truth: list[str]) -> dict:
    """SQuAD-style token-level F1."""
    pred_tokens = set(" ".join(predicted).lower().split())
    truth_tokens = set(" ".join(ground_truth).lower().split())

    if not pred_tokens and not truth_tokens:
        return {"f1": 1.0, "precision": 1.0, "recall": 1.0}
    if not pred_tokens or not truth_tokens:
        return {"f1": 0.0, "precision": 0.0, "recall": 0.0}

    tp = len(pred_tokens & truth_tokens)
    precision = tp / len(pred_tokens)
    recall = tp / len(truth_tokens)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {"f1": f1, "precision": precision, "recall": recall}


def edge_f1(predicted_edges: list[tuple], truth_edges: list[tuple]) -> float:
    """F1 over edge sets for path/relationship queries."""
    pred_set = set(map(tuple, predicted_edges))
    truth_set = set(map(tuple, truth_edges))
    if not pred_set and not truth_set:
        return 1.0
    if not pred_set or not truth_set:
        return 0.0
    tp = len(pred_set & truth_set)
    p = tp / len(pred_set)
    r = tp / len(truth_set)
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0


def reasoning_density_score(f1: float, total_tokens: int) -> float:
    """RDS = F1 / tokens. Core compound metric."""
    return f1 / total_tokens if total_tokens > 0 else 0.0


def context_utilization_rate(retrieved_tokens: int, relevant_retrieved_tokens: int) -> float:
    """CUR = relevant tokens in context / total tokens in context."""
    return relevant_retrieved_tokens / retrieved_tokens if retrieved_tokens > 0 else 0.0


def cost_per_correct_answer(
    prompt_tokens: int,
    completion_tokens: int,
    f1: float
) -> Optional[float]:
    """CPCA = cost_per_query / F1. None if F1 = 0."""
    cost = (prompt_tokens * PRICE_INPUT_PER_TOKEN +
            completion_tokens * PRICE_OUTPUT_PER_TOKEN)
    return cost / f1 if f1 > 0 else None


def hallucination_rate(results: list[QueryResult]) -> float:
    """Fraction of queries where system returned ≥1 hallucinated concept."""
    if not results:
        return 0.0
    hallucinated = sum(1 for r in results if r.hallucinated_concepts)
    return hallucinated / len(results)


class BenchmarkEvaluator:
    """Aggregate metrics across a set of QueryResults."""

    def __init__(self, results: list[QueryResult]):
        self.results = results

    def compute_all(self) -> dict:
        """Compute all metrics and return summary dict."""
        f1_scores = []
        rds_scores = []
        cur_scores = []
        cpca_scores = []
        hop_f1 = defaultdict(list)
        hop_rds = defaultdict(list)

        for r in self.results:
            scores = token_f1(r.predicted, r.ground_truth)
            f1 = scores["f1"]
            total_tokens = r.prompt_tokens + r.completion_tokens

            f1_scores.append(f1)
            rds = reasoning_density_score(f1, total_tokens)
            rds_scores.append(rds)

            cur = context_utilization_rate(r.retrieved_tokens, r.relevant_retrieved_tokens)
            cur_scores.append(cur)

            cpca = cost_per_correct_answer(r.prompt_tokens, r.completion_tokens, f1)
            if cpca is not None:
                cpca_scores.append(cpca)

            hop_f1[r.hop_depth].append(f1)
            hop_rds[r.hop_depth].append(rds)

        macro_f1 = statistics.mean(f1_scores) if f1_scores else 0.0
        macro_rds = statistics.mean(rds_scores) if rds_scores else 0.0
        macro_cur = statistics.mean(cur_scores) if cur_scores else 0.0
        mean_cpca = statistics.mean(cpca_scores) if cpca_scores else None
        hr = hallucination_rate(self.results)

        # F1 by query type
        type_f1 = defaultdict(list)
        for r, f1 in zip(self.results, f1_scores):
            type_f1[r.query_type].append(f1)
        type_f1_means = {k: statistics.mean(v) for k, v in type_f1.items()}

        # F1 and RDS by hop depth
        hop_f1_means = {k: statistics.mean(v) for k, v in hop_f1.items()}
        hop_rds_means = {k: statistics.mean(v) for k, v in hop_rds.items()}

        # Token stats
        total_tokens_list = [r.prompt_tokens + r.completion_tokens for r in self.results]
        mean_tokens = statistics.mean(total_tokens_list) if total_tokens_list else 0

        return {
            "n_queries": len(self.results),
            "macro_f1": round(macro_f1, 4),
            "macro_rds": round(macro_rds, 8),
            "macro_cur": round(macro_cur, 4),
            "mean_tokens": round(mean_tokens, 1),
            "mean_cpca_usd": round(mean_cpca, 6) if mean_cpca else None,
            "hallucination_rate": round(hr, 4),
            "f1_by_type": {k: round(v, 4) for k, v in type_f1_means.items()},
            "f1_by_hop": {k: round(v, 4) for k, v in hop_f1_means.items()},
            "rds_by_hop": {k: round(v, 8) for k, v in hop_rds_means.items()},
        }

    def rds_ratio(self, other: "BenchmarkEvaluator") -> float:
        """Compute RDS ratio: self / other. >1 means self is more efficient."""
        self_metrics = self.compute_all()
        other_metrics = other.compute_all()
        if other_metrics["macro_rds"] == 0:
            return float("inf")
        return self_metrics["macro_rds"] / other_metrics["macro_rds"]

    def precision_at_token_budget(self, budget: int) -> float:
        """Mean F1 over queries where total tokens ≤ budget."""
        in_budget = []
        for r in self.results:
            if r.prompt_tokens + r.completion_tokens <= budget:
                scores = token_f1(r.predicted, r.ground_truth)
                in_budget.append(scores["f1"])
        return statistics.mean(in_budget) if in_budget else 0.0
