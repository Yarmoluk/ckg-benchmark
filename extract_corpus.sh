#!/bin/bash
repos=(
  "calculus" "biology" "genetics" "bioinformatics"
  "statistics-course" "quantum-computing" "circuits"
  "geometry-course" "ecology" "functions" "economics-course"
  "organizational-analytics" "modeling-healthcare-data"
  "database-selection" "conversational-ai"
  "automating-instructional-design" "blockchain"
  "systems-thinking" "theory-of-knowledge"
  "digital-citizenship" "prompt-class" "tracking-ai-course"
  "us-geography" "asl-book" "moss" "unicorns" "claude-skills"
)

mkdir -p corpus benchmark/domains

for repo in "${repos[@]}"; do
  echo "── $repo"
  # Clone shallow
  gh repo clone "dmccreary/$repo" "corpus/$repo" -- --depth=1 --quiet 2>&1
  mkdir -p "benchmark/domains/$repo"

  # Try standard path first
  csv_path="corpus/$repo/docs/learning-graph/learning-graph.csv"
  if [ -f "$csv_path" ]; then
    cp "$csv_path" "benchmark/domains/$repo/learning-graph.csv"
    count=$(tail -n +2 "$csv_path" | wc -l | tr -d ' ')
    echo "   ✓ $count concepts"
  else
    # Try alternate paths
    found=$(find "corpus/$repo" -name "learning-graph.csv" 2>/dev/null | head -1)
    if [ -n "$found" ]; then
      cp "$found" "benchmark/domains/$repo/learning-graph.csv"
      count=$(tail -n +2 "$found" | wc -l | tr -d ' ')
      echo "   ✓ $count concepts (alt path: $found)"
    else
      echo "   ✗ no CSV found"
    fi
  fi
done

echo ""
echo "── Extraction complete"
echo "── Domains with CSV:"
ls benchmark/domains/*/learning-graph.csv 2>/dev/null | wc -l
