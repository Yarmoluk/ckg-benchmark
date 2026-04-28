#!/bin/bash
set -e
cd /Users/danielyarmoluk/Desktop/projects/ckg-benchmark

DOMAINS=(
  algebra-1
  chemistry
  computer-science
  data-science-course
  Dementia
  digital-electronics
  economics-course
  ethics-course
  fft-benchmarking
  functions
  infographics
  intro-to-graph
  intro-to-physics-course
  it-management-graph
  learning-linux
  linear-algebra
  microsims
  personal-finance
  reading-for-kindergarten
  signal-processing
)

mkdir -p /tmp/rag_logs

for d in "${DOMAINS[@]}"; do
  count=$(ls corpus/"$d"/*.md 2>/dev/null | wc -l | tr -d ' ')
  if [ "$count" -gt 0 ]; then
    echo "Launching $d ($count chapters)"
    python evaluation/rag_harness.py --domain "$d" > /tmp/rag_logs/rag_${d}.log 2>&1 &
  else
    echo "Skipping $d (no corpus)"
  fi
done

echo "Waiting for all jobs..."
wait
echo "Done. Results:"
ls results/rag/*.jsonl | wc -l
