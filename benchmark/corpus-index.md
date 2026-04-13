# McCreary Intelligent Textbook Corpus — Domain Index

All repos at: https://github.com/dmccreary/

## Confirmed Domains (27 identified)

| # | Domain | Repo | Category | Est. Concepts |
|---|--------|------|----------|---------------|
| 1 | Calculus | dmccreary/calculus | STEM | 380 |
| 2 | Biology | dmccreary/biology | STEM | ~200 |
| 3 | Genetics | dmccreary/genetics | STEM | ~200 |
| 4 | Bioinformatics | dmccreary/bioinformatics | STEM | ~200 |
| 5 | Statistics | dmccreary/statistics-course | STEM | ~200 |
| 6 | Quantum Computing | dmccreary/quantum-computing | STEM | ~200 |
| 7 | Circuits | dmccreary/circuits | STEM | ~200 |
| 8 | Geometry | dmccreary/geometry-course | STEM | ~200 |
| 9 | Ecology | dmccreary/ecology | STEM | ~200 |
| 10 | Functions (Algebra) | dmccreary/functions | STEM | ~200 |
| 11 | Economics | dmccreary/economics-course | Professional | ~200 |
| 12 | Organizational Analytics | dmccreary/organizational-analytics | Professional | ~200 |
| 13 | Modeling Healthcare Data | dmccreary/modeling-healthcare-data | Professional | ~200 |
| 14 | Database Selection | dmccreary/database-selection | Professional | ~200 |
| 15 | Conversational AI | dmccreary/conversational-ai | Professional | ~200 |
| 16 | Automating Instructional Design | dmccreary/automating-instructional-design | Professional | ~200 |
| 17 | Blockchain | dmccreary/blockchain | Professional | ~200 |
| 18 | Systems Thinking | dmccreary/systems-thinking | Foundational | ~200 |
| 19 | Theory of Knowledge | dmccreary/theory-of-knowledge | Foundational | ~200 |
| 20 | Digital Citizenship | dmccreary/digital-citizenship | Foundational | ~200 |
| 21 | Prompt Engineering | dmccreary/prompt-class | Foundational | ~200 |
| 22 | Tracking AI | dmccreary/tracking-ai-course | Foundational | ~200 |
| 23 | US Geography | dmccreary/us-geography | Foundational | ~200 |
| 24 | ASL | dmccreary/asl-book | Foundational | ~200 |
| 25 | Moss (Botany) | dmccreary/moss | STEM | ~200 |
| 26 | Unicorns | dmccreary/unicorns | Misc | ~200 |
| 27 | Claude Skills | dmccreary/claude-skills | Professional | ~200 |

## Schema (identical across all repos)

```
docs/learning-graph/learning-graph.csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
```

## Corpus Extraction Script

```bash
#!/bin/bash
# Clone all McCreary textbook repos and extract CSVs
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

mkdir -p corpus
for repo in "${repos[@]}"; do
  echo "Cloning $repo..."
  gh repo clone "dmccreary/$repo" "corpus/$repo" -- --depth=1 --quiet
  mkdir -p "benchmark/domains/$repo"
  # Copy learning graph CSV
  if [ -f "corpus/$repo/docs/learning-graph/learning-graph.csv" ]; then
    cp "corpus/$repo/docs/learning-graph/learning-graph.csv" \
       "benchmark/domains/$repo/learning-graph.csv"
    echo "  ✓ CSV extracted"
  else
    echo "  ✗ CSV not found — check path"
  fi
done
```

## Notes on Validation

- Calculus has 380 concepts (larger than standard ~200)
- Some repos may have DAG validation warnings — document per domain
- All repos MIT licensed — safe to redistribute in HuggingFace dataset
- Cite: McCreary, D. (2024). Intelligent Textbooks. github.com/dmccreary
