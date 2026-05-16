#!/usr/bin/env bash
mkdir -p output
uv run python src/SimilarityAnalysis.py -t trigram -d input/trigram --begin-line 6 -oname output/result_trigram.csv
