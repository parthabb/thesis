"""Main file for collecting word counts."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json

import lib
from lib import constants
# from nltk.corpus import brown

words = []
with open(constants.DATA_PATH % 'brown.sentences', 'r') as fptr:
    sentences = json.loads(fptr.read())
    for sentence in sentences:
        words.extend(sentence.split())

with open(constants.DATA_PATH % 'brown_test.sentences', 'r') as fptr:
    sentences = json.loads(fptr.read())
    for sentence in sentences:
        words.extend(sentence.split())

###############################################################################
##
# Format: {word1: count1, word2, count2, ...}
##
###############################################################################

# Print the word_counts
with open(constants.DATA_PATH % 'words.count', 'w') as fptr:
    fptr.write(json.dumps(lib.get_word_count(words)))
