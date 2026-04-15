#!/bin/bash
set -e
export PYTHONUNBUFFERED=1

completed=$(ls results/ckg/ckg_*.jsonl 2>/dev/null | xargs -I{} basename {} .jsonl | sed 's/ckg_//')

total=0
success=0
for f in benchmark/queries/queries_*.jsonl; do
  domain=$(basename $f .jsonl | sed 's/queries_//')
  if echo "$completed" | grep -q "^${domain}$"; then
    echo "SKIP $domain (done)"
    continue
  fi
  echo "── $domain"
  if python3 -u evaluation/ckg_harness.py --domain "$domain" 2>&1; then
    success=$((success+1))
  fi
  total=$((total+1))
  echo "   done ($success/$total)"
done

echo ""
echo "=== COMPLETE: $success/$total domains ==="
