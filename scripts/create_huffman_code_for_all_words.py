"""Create Huffman encoded bit-streams for all words."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json
import os
import re

from lib import constants
from lib import huffman_tree


def create_huffman():
    """Create their Huffman codes for words in wsd_paper_1_imp/senses."""
    huffman_code_lengths = {}
    ht = huffman_tree.HuffmanTree()
    with open(constants.DATA_PATH % 'words.count', 'r') as rfptr:
        all_words = json.loads(rfptr.read())
        for word, count in all_words.iteritems():
            if word.isdigit():
                continue
            encoded_word = ht.encode(word)
            len_encoded_word = len(encoded_word)
            huffman_code_lengths[len_encoded_word] = huffman_code_lengths.get(
                len_encoded_word, [])
            huffman_code_lengths[len_encoded_word].append(encoded_word)

    for k, v in huffman_code_lengths.iteritems():
        with open(constants.DATA_PATH % ('%s.code_length' % k), 'w') as wfptr:
            wfptr.write(','.join(v))


create_huffman()
