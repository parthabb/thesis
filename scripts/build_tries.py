"""Create Huffman encoded bit-streams for all words and store them in tries."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import cPickle
import os

import lib
from lib import constants

if __name__ == '__main__':
    for filename in os.listdir(constants.DATA_PATH % ''):
        if not filename.endswith('.code_length'): 
            continue
        all_words = []
        print filename
        with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
            all_words.extend(rfptr.read().split(','))

        root = lib.build_tries(all_words)

        with open(constants.DATA_PATH % ('%s.trie' % filename.split('.')[0]), 'w') as wfptr:
            wfptr.write(cPickle.dumps(root))
