#!/usr/bin/env bash
# Small-Model CKG Benchmark Suite
# Runs CKG + baseline for all 4 models, then generates the gap-closed report + chart.
#
# Usage:
#   ./run_small_model_suite.sh             # full run
#   ./run_small_model_suite.sh --resume    # skip already-completed domains
#   ./run_small_model_suite.sh --dry-run   # test without calling models

set -euo pipefail

RESUME=""
DRY_RUN=""
for arg in "$@"; do
  case "$arg" in
    --resume)   RESUME="--resume" ;;
    --dry-run)  DRY_RUN="--dry-run" ;;
  esac
done

PY="python3 evaluation/small_model_harness.py"
LOG_DIR="results/small_model/logs"
mkdir -p "$LOG_DIR"

run_model() {
  local model="$1"
  local backend="${2:-ollama}"
  local no_think="${3:-}"
  local slug="${model//:/-}"
  slug="${slug//\//-}"

  echo ""
  echo "════════════════════════════════════════════════════════"
  echo " MODEL: $model   backend=$backend"
  echo "════════════════════════════════════════════════════════"

  # CKG mode
  echo "[$(date '+%H:%M:%S')] Starting CKG mode for $model..."
  $PY --model "$model" --backend "$backend" --mode ckg \
      $no_think $RESUME $DRY_RUN \
      2>&1 | tee "$LOG_DIR/${slug}_ckg.log"
  echo "[$(date '+%H:%M:%S')] CKG done."

  # Baseline (no context)
  echo "[$(date '+%H:%M:%S')] Starting baseline mode for $model..."
  $PY --model "$model" --backend "$backend" --mode baseline \
      $no_think $RESUME $DRY_RUN \
      2>&1 | tee "$LOG_DIR/${slug}_baseline.log"
  echo "[$(date '+%H:%M:%S')] Baseline done."

  echo "[$(date '+%H:%M:%S')] $model complete."
}

echo "▶ Small-Model CKG Benchmark Suite — $(date)"
echo "  Options: resume=$RESUME dry_run=$DRY_RUN"
echo ""

# Wait for a model to be available in Ollama, polling every 30s
wait_for_model() {
  local model="$1"
  echo -n "  Waiting for $model..."
  while ! ollama list 2>/dev/null | grep -q "^${model%%:*}"; do
    echo -n "."
    sleep 30
  done
  echo " ready."
}

# ── Model 1: qwen3:8b (already installed, non-thinking for speed) ──────────────
wait_for_model "qwen3"
run_model "qwen3:8b" "ollama" "--no-think"

# ── Model 2: deepseek-r1:8b (already installed) ────────────────────────────────
wait_for_model "deepseek-r1"
run_model "deepseek-r1:8b" "ollama" "--no-think"

# ── Model 3: phi4-mini (3.8B — smallest, fastest) ──────────────────────────────
wait_for_model "phi4-mini"
run_model "phi4-mini" "ollama" ""

# ── Model 4: mistral:7b ────────────────────────────────────────────────────────
wait_for_model "mistral"
run_model "mistral:latest" "ollama" ""

echo ""
echo "════════════════════════════════════════════════════════"
echo " All models complete. Generating gap-closed report..."
echo "════════════════════════════════════════════════════════"

python3 evaluation/small_model_harness.py --gap-report

echo ""
echo "Generating chart..."
python3 evaluation/chart_small_model.py

echo ""
echo "▶ Suite done. Results at results/small_model/"
echo "  Chart: results/small_model/gap_closed_chart.html"
