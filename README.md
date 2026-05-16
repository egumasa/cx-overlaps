# construction (cx) overlap codes
This is a forked repo from [Philip Tillman's fluencysimilarity repo](https://bitbucket.org/philtillman/fluencysimilarity/src/master/). The original code is used to measure Jaccard and Cosine similarities between two sets of texts (i.e., overlapping unigrams, trigrams, etc.). We are extending their approach mainly in two ways:

1) Adding measures of source text overlap, in addition to the comparison between performances.
2) Adding more fine-grained measures of lingusitic constructions (which require more advanced Natural Language Processing component beyond simple ngrams).

The original Tillman's code is used in their publication.

- de Jong, N., & Tillman, P. (2018). Chapter 2. Grammatical structures and oral fluency in immediate task repetition: Trigrams across repeated performances. In M. Bygate (Ed.), Task-Based Language Teaching (Vol. 11, pp. 43–73). John Benjamins Publishing Company. https://doi.org/10.1075/tblt.11.02jon

My colleague and I have reused the code in the following publication:

- Suzuki, Y., Eguchi, M., & de Jong, N. (2022). Does the Reuse of Constructions Promote Fluency Development in Task Repetition? A Usage‐Based Perspective. TESOL Quarterly, tesq.3103. https://doi.org/10.1002/tesq.3103

## TODO
- [x] Refactor Tillman's code to allow a single, specified text file to compare to.
  - [x] change ParseFileName
  - [x] Add CompareToSource method.
  - [ ] Refactor output file writing pipeline.
  - [ ] More flexible study design and fileformat.
- [x] Refactor Tillman's code to allow different formatting of input files.
- [x] Simple construction (cx) extraction code using spaCy pipeline
  - [x] Simple N-grams and POS-ngrams 
  - [ ] More complex constituency-based constructions
  - [ ] More complex Verb-argument constructions

# FluencySimilarity (Readme from Tillman's repo)

This repository contains scripts to compare textual similarity using trigrams and unigram (words) using two metrics 
for similarity: Jaccard Similarity and Cosine Similarity of tf-idf vectors. These measures are used to compare
unigrams and trigrams of words and/or parts of speech tokens. The idea is that we can measure the relative fluency
of a pair of text using these measures.

### How do I get set up? ###

* Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
* Open a terminal and `cd` to the project root.
* Run `uv sync` to create a virtual environment and install all dependencies (including the spaCy model).
* Run `uv run python src/SimilarityAnalysis.py -h` to verify the setup.
* On Windows run `SimilarityAnalysis.bat`; on macOS/Linux run `bash run_similarity.sh`.
  Both output `result.csv` in the project root.

**Notes**

* Requires Python 3.9+. uv manages the environment automatically — no manual venv or conda setup needed.
* To run unit tests: `uv run python -m pytest tests/`

To see help from the command line run the command

`$ python "src\SimilarityAnalysis.py" -h`

## Expected file format
**File name format:** {condition}_{session}_{studentId}_{story}{delivery}_blah_blah.cex

Ex) "NoTP_918_1_a1_10250_checked_AS-mlv_trans.str.fix.fxb.mor.pst_err-jms.chstr.coocr.cex"
`condition = "NoTP", session = 1, sudentId = 918, story = "a", delivery = 1`

Note that the story and delivery must be one character. If you want to change this behavior then
see file `BaseFreqDictReader.py` method `ParseFileName()`

**Contents** The contents of the file should contain lines of the form "    {freq}  {word1} {word2} {word3}"
where freq is the frequency of the trigram and words 1 through 3 are the words in the trigram. For example,
given the text `my_text = "This is my text. This is my new text."` the file would contain the trigrams:

    2  . . this
    2 . this is
    2  this is my
    1  is my text
    1  my text .
    2  text . .
    1  is my new
    1  my new text
    1  new text .

Note that we use the convention tbat the "." means the end and beginning of a sentence.

**How we compare files:** Comparison are made between files with same {condition, studentId, delivery} unless the 
"abc" flag is set in which
the comparisons are made between files with same {condition, studentId, session}.

### Examples

There are two comparison approaches, each available in trigram and unigram variants.

**Approach 1 — Between performances** (default): compares each student's performances against each other.

Ex1a) Trigram similarity between performances. (`SimilarityAnalysis.bat` / `run_similarity.sh`)

    uv run python src/SimilarityAnalysis.py -t trigram -d input/sample_data --begin-line 7 -oname result.csv

Ex1b) Unigram similarity between performances. (`SimilarityAnalysisUnigram.bat` / `run_similarity_unigram.sh`)

    uv run python src/SimilarityAnalysis.py -t unigram -d input/sample_data_unigram --begin-line 7 -oname result_unigram.csv

**Approach 2 — Compare to source text**: compares each performance against a single source/model text file.

Ex2a) Trigram similarity against a source text.

    uv run python src/SimilarityAnalysis.py -t trigram -d input/sample_data --begin-line 7 --compare-to-source True -s path/to/source.txt -oname result_source.csv

Ex2b) Unigram similarity against a source text.

    uv run python src/SimilarityAnalysis.py -t unigram -d input/sample_data_unigram --begin-line 7 --compare-to-source True -s path/to/source.txt -oname result_source_unigram.csv

### Documentation of SimilarityAnalysis

To understand how Similarity in SimilarityAnalysis is computed one should start by running and inspecting the unit 
tests in SimpleTests.py. These tests should give a basic understanding of what this core of the code does. The other 
code in this  is mainly for performance and unpacking the data from the form it is in so that we can compute the 
 imilarity (i.e., plumbing)

The raw methods that compute the compute the Jaccard Similarity and Cosine Similarity are in
IRSystemHelper.py. IRSystem.py and IRSystemSimple.py are wrapper classes around methods of this class that adds 
caching for performance and methods to read files from disk. If you want to understand how these basic methods 
can be used, look at SimpleTests.py. Here there are unit tests that set up very simple test documents and compute 
all the desired similarities.

### Who do I talk to? ###

* admin: Philip Tillman <phil.tillman@gmail.com>
* researcher: Nel de Jong <c.a.m.dejong@uva.nl>

### Publishing using our code ###
Please cite our paper if you use this code:

de Jong, N., & Tillman, P. C. (2018). Grammatical structures and oral fluency in immediate task repetition: 
trigrams across repeated performances. In M. Bygate (Ed.), Learning language through task repetition (pp. 43-73). 
Amsterdam: John Benjamins.

```
@article{deJongTillman2018,
  title={ Grammatical structures and oral fluency in immediate task repetition: trigrams across repeated performances},
  author={de Jong, N., & Tillman, P. C.},
  journal={Learning language through task repetition},
  editor={M. Bygate},
  publisher={John Benjamins},
  location={Amsterdam},
  year={2018}
}
```

### License ###
Copyright 2019 Philip Tillman

Licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html) (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

