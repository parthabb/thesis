"""Calculate the bigram probabilities for the words."""

import cPickle
import json
import threading

import nltk
from nltk.util import ngrams

from lib import constants
from lib import huffman_tree

sentences = []

with open(constants.DATA_PATH % 'brown.sentences', 'r') as rfptr:
    sentences.extend(json.loads(rfptr.read()))

ugs = [constants.PAD_SYMBOL]

bgs = []
for sentence in sentences:
    ugs.extend(sentence.split())
    ugs.append(constants.PAD_SYMBOL)
    bgs.extend(list(ngrams(sentence.split(), n=2, pad_left=True,
                           pad_right=False,
                           pad_symbol=constants.PAD_SYMBOL)))

fdist_ug = nltk.FreqDist(ugs)
fdist_bg = nltk.FreqDist(bgs)

ht = huffman_tree.HuffmanTree()
 
prob = {}
count = 1

def organize_probs(w1, w2):
    temp = [w1, w2]
    if temp[0] != constants.PAD_SYMBOL:
        temp[0] = ht.encode(temp[0])
    temp[1] = ht.encode(temp[1])
    prob[tuple(temp)] = fdist_bg.get(tuple([w1, w2])) / float(fdist_ug.get(w1))
 
threads = []

for sample in fdist_bg.keys():
    print count
    organize_probs(sample[0], sample[1])
    t = threading.Thread(target=organize_probs, args=sample)
    t.daemon = True
    threads.append(t)
    t.start()
    count += 1

for t in threads:
    t.join()

with open(constants.DATA_PATH % 'bigram.probs', 'w') as wfptr:
    wfptr.write(cPickle.dumps(prob))
