#!/bin/bash
# Package the CKG Benchmark paper for ArXiv submission.
#
# ArXiv accepts a single .zip (or .tar.gz) of the LaTeX source tree.
# Requirements this script enforces:
#   - main.tex and all \input'd section files
#   - figures referenced by \includegraphics (plus the \input'd table file)
#   - main.bbl (arxiv does NOT run bibtex; it needs the compiled .bbl)
#   - NO build artifacts (.aux, .log, .out, .blg, .pdf)
#   - NO extraneous files (python scripts, CSVs, HTML drafts, markdown)
#
# Usage:
#   ./arxiv-submit.sh                 # produces arxiv-submit-<version>.zip
#   ./arxiv-submit.sh --name foo.zip  # custom output name
#
# After running, upload the zip at https://arxiv.org/submit

set -e

PAPER_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PAPER_DIR"

# --- Parse args ---------------------------------------------------------
OUT_NAME=""
while [ $# -gt 0 ]; do
    case "$1" in
        --name) OUT_NAME="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

# --- Extract version from main.tex for default filename -----------------
if [ -z "$OUT_NAME" ]; then
    VERSION=$(grep -E '^\\newcommand\{\\paperversion\}' main.tex \
              | sed -E 's/.*\{([0-9]+\.[0-9]+\.[0-9]+)\}.*/\1/')
    if [ -z "$VERSION" ]; then
        echo "ERROR: could not parse \\paperversion from main.tex"
        exit 1
    fi
    OUT_NAME="arxiv-submit-${VERSION}.zip"
fi

# --- Preflight: make sure main.bbl exists -------------------------------
if [ ! -f main.bbl ]; then
    echo "ERROR: main.bbl not found. ArXiv does not run bibtex."
    echo "Run ./build.sh first to produce main.bbl, then re-run this script."
    exit 1
fi

# --- Preflight: warn if main.pdf is older than any source --------------
if [ -f main.pdf ]; then
    NEWER=$(find main.tex sections figures -type f \
            \( -name '*.tex' -o -name '*.png' -o -name '*.pdf' -o -name '*.bib' \) \
            -newer main.pdf 2>/dev/null | head -5)
    if [ -n "$NEWER" ]; then
        echo "WARNING: source files are newer than main.pdf:"
        echo "$NEWER" | sed 's/^/  /'
        echo "Consider running ./build.sh before packaging."
        echo
    fi
fi

# --- Stage files in a temp dir ------------------------------------------
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

echo "Staging files in $STAGE ..."

# Top-level tex + compiled bibliography
cp main.tex "$STAGE/"
cp main.bbl "$STAGE/"

# Section sources (only .tex, skip anything else)
mkdir -p "$STAGE/sections"
cp sections/*.tex "$STAGE/sections/"

# Figures: only files actually referenced by LaTeX.
# Scan for \includegraphics{figures/FOO} and \input{figures/FOO}.
mkdir -p "$STAGE/figures"

# Referenced image basenames (without extension, after 'figures/')
REFS=$(grep -rhoE '\\includegraphics(\[[^]]*\])?\{figures/[^}]+\}' main.tex sections \
       | sed -E 's/.*\{figures\/([^}]+)\}.*/\1/' \
       | sort -u)

# Referenced \input files from figures/ (e.g. lg_generation_cost_table)
INPUT_REFS=$(grep -rhoE '\\input\{figures/[^}]+\}' main.tex sections \
             | sed -E 's/.*\{figures\/([^}]+)\}.*/\1/' \
             | sort -u)

MISSING=0
for ref in $REFS; do
    # \includegraphics may omit the extension; try common ones.
    if [ -f "figures/$ref" ]; then
        cp "figures/$ref" "$STAGE/figures/"
    elif [ -f "figures/${ref}.png" ]; then
        cp "figures/${ref}.png" "$STAGE/figures/"
    elif [ -f "figures/${ref}.pdf" ]; then
        cp "figures/${ref}.pdf" "$STAGE/figures/"
    elif [ -f "figures/${ref}.jpg" ]; then
        cp "figures/${ref}.jpg" "$STAGE/figures/"
    else
        echo "MISSING figure: figures/$ref"
        MISSING=1
    fi
done

for ref in $INPUT_REFS; do
    if [ -f "figures/${ref}.tex" ]; then
        cp "figures/${ref}.tex" "$STAGE/figures/"
    elif [ -f "figures/$ref" ]; then
        cp "figures/$ref" "$STAGE/figures/"
    else
        echo "MISSING \\input: figures/$ref"
        MISSING=1
    fi
done

if [ "$MISSING" -ne 0 ]; then
    echo "ERROR: one or more referenced files are missing. Aborting."
    exit 1
fi

# --- Build the zip ------------------------------------------------------
OUT_PATH="$PAPER_DIR/$OUT_NAME"
rm -f "$OUT_PATH"

( cd "$STAGE" && zip -r "$OUT_PATH" . -x '*.DS_Store' > /dev/null )

# --- Report -------------------------------------------------------------
SIZE=$(ls -lh "$OUT_PATH" | awk '{print $5}')
COUNT=$(unzip -l "$OUT_PATH" | tail -1 | awk '{print $2}')

echo
echo "================================"
echo "Created: $OUT_NAME ($SIZE, $COUNT files)"
echo "================================"
echo
echo "Contents:"
unzip -l "$OUT_PATH" | sed -n '4,$p' | sed '$d' | sed '$d' | awk '{print "  " $NF}'
echo
echo "Next steps:"
echo "  1. Verify the zip compiles cleanly (optional sanity check):"
echo "       mkdir /tmp/arxiv-test && cd /tmp/arxiv-test"
echo "       unzip $PAPER_DIR/$OUT_NAME && tectonic main.tex"
echo "  2. Upload at https://arxiv.org/submit"
echo "     - Primary category: cs.IR (or cs.AI if endorsement blocks cs.IR)"
echo "     - Cross-list: cs.AI"
