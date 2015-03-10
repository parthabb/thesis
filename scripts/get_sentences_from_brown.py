"""Extract the sentence from the brown corpus into a file."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json
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

test_data = sentences[:len(sentences) / 3]
train_data = sentences[len(sentences) / 3:]

with open(constants.DATA_PATH % 'brown.sentences', 'w') as wfptr:
    wfptr.write(json.dumps(train_data))

with open(constants.DATA_PATH % 'brown_test.sentences', 'w') as wfptr:
    wfptr.write(json.dumps(test_data))
