"""File to handle processing of individual words."""

import cPickle
import json
import math
import os

import lib
from lib import constants
from lib import huffman_tree

class Words(lib.Singleton):
    """Class that handles all processing of words."""
    def __init__(self, Pb=math.e):
        words = self.read_words_from_file()
        self._encoded_words_by_length = self.get_encoded_words()
        self._encoded_tries_by_length = self.get_encoded_tries()
        self._word_probability = self.get_word_probabilities(words)
        self.Pb = Pb

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
        encoded_tries_by_length = {}
        for filename in os.listdir(constants.DATA_PATH % ''): 
            if not filename.endswith('.trie'): 
                continue
            with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
                encoded_tries_by_length[filename.split('.')[0]] = cPickle.loads(rfptr.read())
        return encoded_tries_by_length

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

    def _trie_util(self, trie, word, m):
        """Checks if the word is in the trie."""
        curr = trie
        has_path = False
        next_node = None
        count = 0

        for bit in word:
            if bit == '0':
                curr = curr.left
            else:
                curr = curr.right
            if not curr:
                break
            if count == m:
                has_path = True
                next_node = curr
            count += 1
        return curr != None, has_path, next_node

    ## Important algorithm to get words from trie ##
    def get_most_probable_words_through_trie(self, error_word):
        """Given a word with bit errors, get the most probable words."""
        word_len = len(error_word)
        if not constants.ALPHA.has_key(word_len):
            return {0: [error_word]}
        self.alpha = word_len * math.log(constants.ALPHA.get(word_len))
        trie = self._encoded_tries_by_length.get(str(word_len), None)
        probable_words = {}
        isword, _, _ = self._trie_util(trie, error_word, 0)
        if isword:
            probable_words.update({0: [error_word]})
#             probable_words.update({0: [(error_word, self._get_word_probability(error_word, 0))]})
        bit_flip_list = [(trie, '', error_word)]
        for n in range(5):
            temp_bit_flip_list = []
            for root, prev, rest in bit_flip_list:
                stream = list(rest)
                stream_len = len(stream)
                for m in range(stream_len):
                    temp = list(stream)
                    # check with flip
                    if temp[m] == '0':
                        temp[m] = '1'
                    else:
                        temp[m] = '0'
                    temp = ''.join(temp)
                    isword, haspath, next_node = self._trie_util(root, temp, m)
                    valid_word = prev + temp
                    if isword:
                        words_list = probable_words.get(n + 1, set())
                        words_list.add(valid_word)
#                         words_list.add((valid_word, self._get_word_probability(valid_word, n + 1)))
                        probable_words[n + 1] = words_list
                    if haspath:
                        temp_bit_flip_list.append((next_node, prev + temp[:m + 1], temp[m + 1:]))
            bit_flip_list = temp_bit_flip_list
        return probable_words

    def _get_word_probability(self, valid_word, Dh):
        print valid_word
        probability = self._word_probability[valid_word]
        print self.alpha
        print probability
        print self.Pb
        return self.alpha + math.log(probability) + Dh * math.log(self.Pb)
