# CKG Benchmark Paper

LaTeX source for the ArXiv paper:

> **"Benchmarking Knowledge Retrieval Architectures Across 25 Domains:
> RAG, GraphRAG, and Compressed Knowledge Graphs on the
> McCreary Intelligent Textbook Corpus"**

## Structure

```
paper/
├── main.tex                   # Entry point (imports all sections)
├── build.sh                   # Build script (Tectonic or pdflatex)
├── outline.md                 # Original paper outline (reference)
├── abstract.txt               # Plain-text abstract
├── STATUS.md                  # Section-by-section progress
├── sections/
│   ├── 01-abstract.tex
│   ├── 02-introduction.tex
│   ├── 03-related-work.tex
│   ├── 04-corpus.tex
│   ├── 05-architecture.tex
│   ├── 06-benchmark-design.tex
│   ├── 07-metrics.tex
│   ├── 08-results.tex
│   ├── 09-discussion.tex
│   ├── 10-conclusion.tex
│   └── references.bib
├── figures/
│   └── README.md              # Figure conventions and status
└── logs/                      # Collaborative edit logs
```

## Building

### With Tectonic (recommended)

```bash
brew install tectonic   # macOS
./build.sh              # produces main.pdf
./build.sh clean        # remove artifacts
```

### With pdflatex

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Conventions

- **Section files:** Numeric prefix `NN-name.tex`, matching `\input{}` order
- **Labels:** `\label{sec:...}`, `\label{fig:...}`, `\label{tab:...}`
- **TODOs:** `% TODO:` inline LaTeX comments mark incomplete content
- **Figures:** PNG only, 300 DPI, colorblind-friendly (see `figures/README.md`)
- **Bibliography:** IEEE transactions style (`ieeetr`)
- **Version snapshots:** Save as `ckg-benchmark-vN.NN.pdf` at milestones

## ArXiv Submission

- **Categories:** cs.IR (primary), cs.AI (secondary)
- **Dataset:** `graphify-md/ckg-benchmark` on HuggingFace
- For submission, flatten to single file: combine all `\input{}` directives into `arxiv-submission.tex`
