"""Extract the sentence from the brown corpus into a file."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json
import re
import string

from lib import constants
from nltk.corpus import brown

sentences = []
for sents in brown.sents(categories=brown.categories()):
    sentence = str(' '.join(sents)).translate(
        string.maketrans("",""), string.punctuation).lower().replace(
        '  ', ' ').strip()
    if re.match(r'[A-Za-z ]+$', sentence):
        sentences.append(sentence)

print len(sentences)

with open(constants.DATA_PATH % 'brown.sentences', 'w') as wfptr:
    wfptr.write(json.dumps(sentences))
