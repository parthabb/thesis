"""Calculate the unigram probabilities for the words."""

import cPickle
import json

import nltk

from lib import constants
from lib import huffman_tree

sentences = []

with open(constants.DATA_PATH % 'brown.sentences', 'r') as rfptr:
    sentences.extend(json.loads(rfptr.read()))

ugs = []

for sentence in sentences:
    ugs.extend(sentence.split())

fdist_ug = nltk.FreqDist(ugs)

ht = huffman_tree.HuffmanTree()

# prob[(<huffman_encoded_word_1>)] = P[(<huffman_encoded_word_1>)]
prob = {}
count = 1
total_words = len(ugs) * 1.0

for sample in fdist_ug.keys():
    w1 = ht.encode(sample)
    prob[w1] = fdist_ug.get(sample) / total_words

with open(constants.DATA_PATH % 'ugram.probs', 'w') as wfptr:
    wfptr.write(cPickle.dumps(prob))
