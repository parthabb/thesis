"""Create Huffman encoded bit-streams for all words and store them in tries."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import cPickle
import os

from lib import constants
from lib import node


def build_tries(all_words):
    """Read all words from the *.code_length and generate tries."""
    root = node.Node(True)
    for word in all_words:
        prev = root
        curr = None
        for char in word:
            if (char == '0'):
                curr = prev.left
                if not curr:
                    prev.left = node.Node()
                    curr = prev.left
            else:
                curr = prev.right
                if not curr:
                    prev.right = node.Node()
                    curr = prev.right
            prev = curr
        curr.is_leaf = True
    return root


if __name__ == '__main__':
    for filename in os.listdir(constants.DATA_PATH % ''):
        if not filename.endswith('.code_length'): 
            continue
        all_words = []
        print filename
        with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
            all_words.extend(rfptr.read().split(','))

        root = build_tries(all_words)

        with open(constants.DATA_PATH % ('%s.trie' % filename.split('.')[0]), 'w') as wfptr:
            wfptr.write(cPickle.dumps(root))
