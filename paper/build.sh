#!/bin/bash
# Build the CKG Benchmark paper using Tectonic
#
# Usage:
#   ./build.sh          Build main.pdf
#   ./build.sh clean    Remove build artifacts
#
# Install Tectonic:
#   brew install tectonic    (macOS)
#   cargo install tectonic   (via Rust)

set -e

PAPER_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PAPER_DIR"

if [ "$1" = "clean" ]; then
    echo "Cleaning build artifacts..."
    rm -f main.aux main.bbl main.blg main.log main.out main.pdf
    rm -f sections/*.aux
    echo "Done."
    exit 0
fi

echo "Building CKG Benchmark paper..."
echo "================================"

if command -v tectonic &> /dev/null; then
    tectonic main.tex
else
    echo "Tectonic not found. Falling back to pdflatex + bibtex..."
    pdflatex -interaction=nonstopmode main.tex
    bibtex main
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex
fi

if [ -f main.pdf ]; then
    SIZE=$(ls -lh main.pdf | awk '{print $5}')
    if command -v pdfinfo &> /dev/null; then
        PAGES=$(pdfinfo main.pdf | grep Pages | awk '{print $2}')
        echo "================================"
        echo "Success: main.pdf ($SIZE, $PAGES pages)"
    else
        echo "================================"
        echo "Success: main.pdf ($SIZE)"
    fi
else
    echo "ERROR: main.pdf was not generated."
    exit 1
fi
