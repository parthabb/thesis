"""Calculate the bigram probabilities for the words."""

import cPickle
import json
import math
import threading

import nltk
from nltk.util import ngrams

from lib import constants
from lib import huffman_tree

sentences = []

with open(constants.DATA_PATH % 'brown.sentences', 'r') as rfptr:
    sentences.extend(json.loads(rfptr.read()))

ugs = []
bgs = []

for sentence in sentences:
    ugs.append(constants.PAD_SYMBOL)
    ugs.extend(sentence.split())
    bgs.extend(list(ngrams(sentence.split(), n=2, pad_left=True,
                           pad_right=False,
                           pad_symbol=constants.PAD_SYMBOL)))

fdist_ug = nltk.FreqDist(ugs)
total_words = len(fdist_ug)

fdist_bg = nltk.FreqDist(bgs)

# Probability of each word with frequency 1 or less are made equal.
UNKNOWN_WORDS = {}
for k, v in fdist_ug.items():
    if v < 2:
        UNKNOWN_WORDS[k] = 1

# Implement kneser-ney smoothing.

# Total bigrams with frequency greater than 0.
total_bgs_with_frequency_gt_zero = len(fdist_bg)

# Discount value.
D = 0.75

# Modify the bigram counts by subtracting 0.75 (Refer coursera slides by manning
# on absolute discounting).
for k, v in fdist_bg.items():
    fdist_bg[k] = max(v - D, 0)

P_continuation = {}

temp_continuation = {}
for (_, w), c in fdist_bg.items():
    if c > 0:
        temp_continuation[w] = temp_continuation.get(w, 0) + 1

# Continuation probability (P_continuation).
for k, v in fdist_ug.items():
    if k == constants.PAD_SYMBOL:
        continue
    P_continuation[k] = temp_continuation.get(k, 0) * 1.0 / total_bgs_with_frequency_gt_zero

temp_prob = 0
for k, v in P_continuation.items():
    if UNKNOWN_WORDS.has_key(k):
        temp_prob += v

for k, v in P_continuation.items():
    if UNKNOWN_WORDS.has_key(k):
        P_continuation[k] = temp_prob

with open(constants.DATA_PATH % 'unknown_prob.txt', 'w') as wfptr:
    wfptr.write(str(temp_prob))

temp_coefficient = {}
for (w, _), c in fdist_bg.items():
    if c > 0:
        temp_coefficient[w] = temp_coefficient.get(w, 0) + 1

# Interpolation co-efficient.(lambda_coefficient).
lambda_coefficient = {}
for (w, _), v in fdist_bg.items():
    lambda_coefficient[w] = D * temp_coefficient.get(w, 0) * 1.0 / fdist_ug[w]


ht = huffman_tree.HuffmanTree()

# prob[(<huffman_encoded_word_1>, <huffman_encoded_word_2>)] = P[(<huffman_encoded_word_1>, <huffman_encoded_word_2>) / <huffman_encoded_word_1>)]
P_kn = {}

def organize_probs(w1, w2):
    temp = [w1, w2]
    if temp[0] != constants.PAD_SYMBOL:
        temp[0] = ht.encode(temp[0])
    temp[1] = ht.encode(temp[1])
    P_kn[tuple(temp)] = (fdist_bg.get(tuple([w1, w2])) / float(fdist_ug.get(w1))) + (lambda_coefficient[w1] * P_continuation[w2])
 
threads = []

for sample in fdist_bg.keys():
    t = threading.Thread(target=organize_probs, args=sample)
    t.daemon = True
    threads.append(t)
    t.start()

for t in threads:
    t.join()

###############################################################################
##
# File: bigram.probs
# probability of word2 following word1 appearing together given word1
# Format: prob[(<huffman_encoded_word_1>, <huffman_encoded_word_2>)] = P[(<huffman_encoded_word_1>, <huffman_encoded_word_2>) / <huffman_encoded_word_1>)]
##
###############################################################################

with open(constants.DATA_PATH % 'bigram.probs', 'w') as wfptr:
    wfptr.write(cPickle.dumps(P_kn))
