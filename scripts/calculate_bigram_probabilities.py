"""Calculate the bigram probabilities for the words."""

import json
import pickle
import threading

import nltk
from nltk import probability
from nltk.util import ngrams

from lib import constants
from lib import huffman_tree

sentences = []

with open(constants.DATA_PATH % 'brown.sentences', 'r') as rfptr:
    sentences.extend(json.loads(rfptr.read()))

bgs = []
for sentence in sentences:
    bgs.extend(list(ngrams(sentence.split(), n=2, pad_left=True,
                               pad_right=False,
                               pad_symbol=constants.PAD_SYMBOL)))

fdist = nltk.FreqDist(bgs)
mle = probability.MLEProbDist(fdist)

ht = huffman_tree.HuffmanTree()

prob = {}
count = 1

def organize_probs(w1, w2):
    temp = [w1, w2]
    if temp[0] != constants.PAD_SYMBOL:
        temp[0] = ht.encode(temp[0])
    temp[1] = ht.encode(temp[1])
    prob[tuple(temp)] = mle.prob((w1, w2))

threads = []

for sample in mle.samples():
    print count
    t = threading.Thread(target=organize_probs, args=sample)
    t.daemon = True
    threads.append(t)
    t.start()
    count += 1

for t in threads:
    t.join()

with open(constants.DATA_PATH % 'bigram.probs', 'w') as wfptr:
    wfptr.write(pickle.dumps(prob))
