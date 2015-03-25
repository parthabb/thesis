"""File to handle processing of individual words."""

import json

import lib
from lib import constants
from lib import huffman_tree

class Words(lib.Singleton):
    """Class that handles all processing of words."""
    def __init__(self):
        self._words = self.read_words_from_file()
        self._encoded_words = self.get_encoded_words(self._words)

    def read_words_from_file(self):
        """Read the words into memory from words.count"""
        words_counts = {}
        with open(constants.DATA_PATH % '/words.count', 'r') as rfptr:
            word_counts = json.loads(rfptr.read())
        return words_counts

    def get_encoded_words(self, words):
        """Return a dictionary of encoded words."""
        encoded_words = {}
        if isinstance(words, dict):
            ht = huffman_tree.HuffmanTree()
            for word, _ in words.items():
                encoded_words[word] = ht.encode(word)
        return encoded_words
