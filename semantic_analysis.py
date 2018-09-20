# Semantic analysis using Pointwise Mutual Information(PMI) points

import json
import operator

from collections import Counter

import math
from nltk.corpus import stopwords
from nltk import bigrams, defaultdict
import string

from analyse import com
from tokenizer import preprocess

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', '…', '’', 'ั', '่', 'ี', '้', '∙', '#baddecisionsihavemade',
                                                   'ِ', '”', '“']
n_docs = 0

with open('tweets.json', 'r') as f:
    count_all = Counter()
    hash_all = Counter()
    term_all = Counter()
    bigram_all = Counter()

    for line in f:
        n_docs += 1
        if line is not "\n":
            tweet = json.loads(line)

            terms_all = [term for term in preprocess(tweet['text']) if term not in stop]
            count_all.update(terms_all)

            terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
            hash_all.update(terms_hash)

            terms_only = [term for term in preprocess(tweet['text'])
                          if term not in stop and
                          not term.startswith(('#', '@', 'https:'))]
            term_all.update(terms_only)

            terms_bigram = bigrams(term_all)
            bigram_all.update(terms_bigram)

    p_t = {}
    p_t_com = defaultdict(lambda: defaultdict(int))

    for term, n in count_all.items():
        p_t[term] = n / n_docs
        for t2 in com[term]:
            p_t_com[term][t2] = com[term][t2] / n_docs

    positive_vocab = [
        'good', 'nice', 'great', 'awesome', 'outstanding', 'happy', 'fantastic', 'terrific', ':)', ':-)', 'like',
        'love', 'fun', 'funny'
    ]
    negative_vocab = [
        'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(', 'racist', 'nazi', 'sloppy', 'hate', 'hopeless',
        'fear'
    ]

    pmi = defaultdict(lambda: defaultdict(int))
    for t1 in p_t:
        for t2 in com[t1]:
            denom = p_t[t1] * p_t[t2]
            pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)

    semantic_orientation = {}
    for term, n in p_t.items():
        positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
        negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
        semantic_orientation[term] = positive_assoc - negative_assoc

    semantic_sorted = sorted(semantic_orientation.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
    top_pos = semantic_sorted[:50]
    top_neg = semantic_sorted[-50:]

    print('\n Top positive terms')
    print(top_pos)
    print('\n Top negative terms')
    print(top_neg)
