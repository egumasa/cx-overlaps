@echo off
uv run python "src\SimilarityAnalysis.py" -t unigram -d "input\sample_data_unigram" --begin-line 7 > "result_unigram.csv"