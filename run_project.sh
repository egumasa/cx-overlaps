#!/usr/bin/env bash
# Runs the full pipeline for a project folder.
# Usage: bash run_project.sh project/PROJECT1
set -euo pipefail
PROJECT_DIR="${1:?Usage: $0 <project-directory>}"

echo "=== Step 1: Extracting n-grams ==="
uv run python src/cx-extraction.py --project "$PROJECT_DIR"

echo "=== Step 2: Running similarity analysis ==="
uv run python src/SimilarityAnalysis.py --project "$PROJECT_DIR"

echo "=== Done. Results in $PROJECT_DIR/output/ ==="
