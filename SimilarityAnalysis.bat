@echo off
uv run python "src/SimilarityAnalysis.py" -t trigram -d "input/sample_data" --begin-line 7 > "result.csv"