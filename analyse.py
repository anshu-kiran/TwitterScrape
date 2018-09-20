# Finding out which terms and hashtags are most common. Also, looking at most common occurrences of a pair of words
# and plot of most common words

import json
import operator

from collections import Counter

from nltk.corpus import stopwords
from nltk import bigrams, defaultdict
import string
import matplotlib.pyplot as plt

from tokenizer import preprocess

com = defaultdict(lambda: defaultdict(int))

search_word = 'fun'
count_search = Counter()

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', '…', '’', 'ั', '่', 'ี', '้', '∙', '#uselesstriviathatiknow',
                                                   'ِ', '”', '“']

with open('tweets.json', 'r') as f:
    count_all = Counter()
    hash_all = Counter()
    term_all = Counter()
    bigram_all = Counter()

    for line in f:
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

        for i in range(len(terms_only) - 1):
            for j in range(i + 1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1

        if search_word in terms_only:
            count_search.update(terms_only)

    print('Most Common Terms:\n')
    print(count_all.most_common(20))
    print('\n')
    print('Most Common Hashtags:\n')
    print(hash_all.most_common(20))
    print('\n')
    print('Most Common Terms after removal of hastags and mentions:\n')
    print(term_all.most_common(50))
    print('\n')
    print('Most Common co-occurrences:\n')
    print(bigram_all.most_common(20))

    # Bar graph
    word_freq = term_all.most_common(5)
    labels, freq = zip(*word_freq)
    plt.bar(labels, freq)
    plt.show()

com_max = []

for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))

terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print("\n\n\nCommon Co-occurrences:")
print(terms_max[:40])

print("\n\n\nCo-occurrence for %s:" % search_word)
print(count_search.most_common(50))
