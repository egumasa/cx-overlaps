#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This program extracts constructions for overlap calculation.
'''
import ntpath
import glob
import os
import re
import spacy

__author__ = 'Masaki Eguchi'

nlp = spacy.load("en_core_web_trf")

TRIGRAM_DIR = 'input/trigram/'
UNIGRAM_DIR = 'input/unigram/'


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
    s = re.sub(r'_[Tt]extgrid\.txt$', '', s)
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
    files = sorted(glob.glob('input/rawtexts/*.txt'))
    print(f"Found {len(files)} files.")
    for i, file in enumerate(files):
        print(f"[{i+1}/{len(files)}] {file}")
        text_to_ngrams(file, length=3, output_dir=TRIGRAM_DIR)
        text_to_ngrams(file, length=1, output_dir=UNIGRAM_DIR)
    print("Done.")
