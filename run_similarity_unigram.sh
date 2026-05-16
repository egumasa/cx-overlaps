#!/usr/bin/env bash
mkdir -p output
uv run python src/SimilarityAnalysis.py -t unigram -d input/unigram --begin-line 6 -oname output/result_unigram.csv
