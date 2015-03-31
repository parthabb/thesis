"""File to handle processing of individual words."""

import cPickle
import json
import os

import lib
from lib import constants
from lib import huffman_tree

class Words(lib.Singleton):
    """Class that handles all processing of words."""
    def __init__(self):
        words = self.read_words_from_file()
        self._encoded_words_by_length = self.get_encoded_words()
        self._encoded_tries_by_length = self.get_encoded_tries()
        self._word_probability = self.get_word_probabilities(words)

    def read_words_from_file(self):
        """Read the words into memory from words.count"""
        words = {}
        with open(constants.DATA_PATH % '/words.count', 'r') as rfptr:
            words.update(json.loads(rfptr.read()))
        return words

    def get_encoded_words(self):
        """Return a dictionary of encoded words."""
        encoded_words_by_length = {}
        for filename in os.listdir(constants.DATA_PATH % ''): 
            if not filename.endswith('.code_length'): 
                continue
            with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
                encoded_words_by_length[filename.split('.')[0]] = rfptr.read().split(',')
        return encoded_words_by_length

    def get_encoded_tries(self):
        """Return a dictionary of encoded tries."""
        encoded_words_by_length = {}
        for filename in os.listdir(constants.DATA_PATH % ''): 
            if not filename.endswith('.trie'): 
                continue
            with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
                encoded_words_by_length[filename.split('.')[0]] = cPickle.loads(rfptr.read())
        return encoded_words_by_length

    def get_word_probabilities(self, words):
        """Assign probabilities to the words."""
        word_probability = {}
        word_probs = {}
        with open(constants.DATA_PATH % 'ugram.probs', 'r') as rfptr:
            word_probs.update(json.loads(rfptr.read()))

        ht = huffman_tree.HuffmanTree()
        for w, _ in words.items():
            encoded_word = ht.encode(w)
            word_probability[encoded_word] = word_probs.get(encoded_word, 0)
        return word_probability

    def get_most_probable_words_through_setops(self, error_word):
        """Given a word with bit errors, get the most probable words."""
        count = 0
        word_len = len(error_word)
        words = self._encoded_words_by_length.get(str(word_len), [])
        probable_words = {0: list(set([error_word]).intersection(set(words)))}
        count += len(probable_words.get(0))
        for dis in xrange(1, word_len):
            if count > 10:
                break
            probable_words[dis] = list(set(lib.get_possible_words(error_word, dis)).intersection(words))
            count += len(probable_words.get(dis))
        return probable_words

    def _trie_util(self, trie, word):
        """Checks if the word is in the trie."""
        curr = trie
        for bit in word:
            if bit == '0':
                curr = curr.left
            else:
                curr = curr.right
            if not curr:
                break
        return curr != None

    def get_most_probable_words_through_trie(self, error_word):
        """Given a word with bit errors, get the most probable words."""
        pass
