import collections
import math
import nltk


class IRSystemHelper:
    """
    This class contains methods that do the actual computations.
    """
    def JaccardSimilarityFromTokens(self, tokens1, tokens2):
        union = tokens1.union(tokens2)
        intersection = tokens1.intersection(tokens2)
        return len(intersection) / len(union)

    def Length(self, v):
        return math.sqrt(self.DotProduct(v, v))

    def DotProduct(self, v1, v2):
        sumSquared = 0
        for e1 in v1.keys():
            if e1 in v2:
                sumSquared += v1[e1] * v2[e1]
        return sumSquared

    def getTokens(self, text):
        return nltk.word_tokenize(text)

    def getTf(self, tokens):
        tf = collections.defaultdict(int)
        for t in tokens:
            tf[t] += 1
        return tf

    def getTrigrams(self, text):
        return list(nltk.ngrams(self.getTokens(text), 3))

    def getFreqDict(self, text):
        freq = collections.defaultdict(int)
        for token in self.getTokens(text):
            freq[token] += 1
        return freq

    def getFreqDictTrigrams(self, text):
        freq = collections.defaultdict(int)
        for trigram in self.getTrigrams(text):
            freq[" ".join(trigram)] += 1
        return freq

    def getIdf(self, token, docs, idf):
        if token in idf.keys():
            return idf[token]
        nrOfDocs = len(docs.keys())
        appearances = 0
        for filePath in docs.keys():
            if token in docs[filePath]:
                appearances += 1
        if appearances == 0:
            idf[token] = 1.0  # log(1,2)=0, so source-only tokens contribute nothing
            return idf[token]
        idf[token] = nrOfDocs / appearances
        return idf[token]

    def getTfIdfVector(self, doIdf, getIdf, tokenFreqDict):
        v = collections.defaultdict(lambda: 0.0)
        for token in tokenFreqDict.keys():
            v[token] = (1 + math.log(tokenFreqDict[token], 2))
            if doIdf:
                v[token] = v[token] * math.log(getIdf(token), 2)
        # normalize this vector
        length = self.Length(v)
        for token in tokenFreqDict.keys():
            v[token] = v[token] / length
        return v