"""Extract the sentence from the brown corpus into a file."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json
import random
import re

import lib
from lib import constants
from nltk.corpus import brown

sentences = []
for sents in brown.sents(categories=brown.categories()):
    sentence = lib.clean_data(sents)
    if re.match(r'[A-Za-z ]+$', sentence):
        sentences.append(sentence)

###############################################################################
#
# Format: [sentence1, sentence2, sentence3....]
#
###############################################################################

total_sentences = len(sentences)
test_sentence_indices = random.sample(range(total_sentences),
                                      total_sentences / 3)

test_sentence_indices.sort()
test_sentence_indices.reverse()

test_data = []
for x in test_sentence_indices:
    test_data.append(sentences.pop(x))

train_data = sentences

with open(constants.DATA_PATH % 'brown.sentences', 'w') as wfptr:
    wfptr.write(json.dumps(train_data))

with open(constants.DATA_PATH % 'brown_test.sentences', 'w') as wfptr:
    wfptr.write(json.dumps(test_data))
