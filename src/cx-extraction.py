#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This program extracts constructions for overlap calculation.
'''
import argparse
import glob
import ntpath
import os
import re
import yaml
from pathlib import Path

import spacy

__author__ = 'Masaki Eguchi'

nlp = spacy.load("en_core_web_trf")


def preprocess(text):
    text = text.strip()
    text = re.sub("\n+", "\n", text)
    text = re.sub("(-\n)+", " ", text)
    text = re.sub("\t+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(";", ".")
    text = text.replace(":", ".")
    return text


def ngrammer(tokenized, number, connect=" ", stop_list=['.', ',', '!', '?']):
    ngram_list = []
    last_index = len(tokenized) - 1
    for i, token in enumerate(tokenized):
        if i + number > last_index:
            continue
        ngram = tokenized[i:i + number]
        ngram_string = connect.join(ngram)
        if any(s in ngram_string for s in stop_list):
            continue
        ngram_list.append(ngram_string)
    return ngram_list


def tokenizer(text, sent_bound=True, lemmatize=False, pos=False):
    doc = nlp(text)
    tok_list = []
    for sent in doc.sents:
        sent_tok = []
        for tok in sent:
            if lemmatize:
                sent_tok.append(tok.lemma_)
            elif pos:
                sent_tok.append(tok.tag_)
            else:
                sent_tok.append(tok.norm_)
        if sent_bound:
            tok_list.append(sent_tok)
        else:
            if len(tok_list) == 0:
                tok_list.append([])
            tok_list[0].extend(sent_tok)
    return tok_list


def counter(items):
    res = {}
    for item in items:
        res[item] = res.get(item, 0) + 1
    return res


def dict_to_cex(freq_dict, output_dir, stem, header):
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, stem + '.cex')
    with open(out_path, 'w') as outf:
        outf.write(header)
        for item, freq in freq_dict.items():
            outf.write(f"{freq} {item}\n")


def stem_filename(filename):
    """Remove _TextGrid.txt (case-insensitive) or bare .txt extension."""
    s = ntpath.basename(filename)
    s = re.sub(r'_[Tt]ext[Gg]rid\.txt$', '', s)
    if s.endswith('.txt'):
        s = s[:-4]
    return s


def text_to_ngrams(filename, length, output_dir):
    stem = stem_filename(filename)
    text = open(filename, 'r').read()
    text = preprocess(text)
    tok = tokenizer(text, sent_bound=False)
    if not tok or not tok[0]:
        print(f"  WARNING: no tokens found in {filename}")
        return
    ngrams = ngrammer(tok[0], length)
    ngram_dict = counter(ngrams)
    header = "#\n" * 6
    dict_to_cex(ngram_dict, output_dir, stem, header)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract trigram/unigram .cex files from raw transcripts.")
    parser.add_argument('--project', '-p', dest='projectDir', default=None,
                        help='Path to a project folder containing config.yaml.')
    parser.add_argument('--input-dir', dest='rawtextDir', default=None,
                        help='Directory of raw .txt transcript files.')
    parser.add_argument('--trigram-dir', dest='trigramDir', default=None,
                        help='Output directory for trigram .cex files.')
    parser.add_argument('--unigram-dir', dest='unigramDir', default=None,
                        help='Output directory for unigram .cex files.')
    args = parser.parse_args()

    project_dir = None
    yaml_config = {}
    if args.projectDir:
        project_dir = Path(args.projectDir).resolve()
        config_path = project_dir / 'config.yaml'
        if config_path.exists():
            with open(config_path) as f:
                yaml_config = yaml.safe_load(f) or {}

    def _resolve(cli_val, yaml_key, fallback):
        raw = cli_val or yaml_config.get(yaml_key) or fallback
        p = Path(raw)
        return str(project_dir / p) if project_dir and not p.is_absolute() else str(p)

    rawtext_dir = _resolve(args.rawtextDir, 'rawtext_directory', 'input/rawtexts')
    trigram_dir = _resolve(args.trigramDir, 'trigram_directory', 'input/trigram')
    unigram_dir = _resolve(args.unigramDir, 'unigram_directory', 'input/unigram')

    files = sorted(glob.glob(os.path.join(rawtext_dir, '*.txt')))
    print(f"Found {len(files)} files in {rawtext_dir}.")
    for i, file in enumerate(files):
        print(f"[{i+1}/{len(files)}] {file}")
        text_to_ngrams(file, length=3, output_dir=trigram_dir)
        text_to_ngrams(file, length=1, output_dir=unigram_dir)
    print("Done.")
