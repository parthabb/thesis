"""Utility functions for use in research."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json
import re
import random
import string

from nltk import probability


class Singleton (object):
    """Singleton super class"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


def get_word_count (words):
    """Get the count of each alpha word for the list of words 'words'.

    Example: 
        import lib
        from nltk.corpus import brown
        lib.get_word_count(brown.words())

     Args:
        words: A list of words.

    Returns:
        A dict with words as key and their count as value.
    """
    fd = probability.FreqDist(words)
    words = {}

    for word, freq in fd.items():
        if re.match(r'[A-Za-z]+$', word):
            words[word.lower()] = freq + words.get(word.lower(), 0)

    total_words = sum(words.values())

    for word, count in words.iteritems():
        words[word] = count / float(total_words)

    return words


def clean_data(sents):
    """Function to clean the data from the corpus files."""
    words = []
    for x in sents:
        words.append(x.strip())
    sentence = str(' '.join(words))
    sentence = sentence.replace('-', ' ')
    return ' '.join(sentence.translate(
        string.maketrans("",""), string.punctuation).lower().split())


def add_error(bitstream, p, nob):
    """Flips the bits in the bit stream with a probability p."""
    random.seed()
    new_bitstream = []
    for bit in bitstream:
        val = random.random()
        if val < p and nob > 0:
            nob = nob - 1
            if bit == '1':
                bit = '0'
            else:
                bit = '1'
        new_bitstream.append(bit)
    return ''.join(new_bitstream)


def hamming_distance(word_1, word_2):
    """The words with 'hamming_dist' order Hamming distance."""
    bitlen = len(word_1)
    dist = 0
    for x in range(bitlen):
        if word_1[x] != word_2[x]:
            dist += 1
    return dist


def filter_by_hamming_distance(bitstream):
    """The words with 'hamming_dist' order Hamming distance."""
    bitlen = len(bitstream)
    all_words = []
    with open('huffman_code_all_words/%s.code_length' % bitlen, 'r') as rfptr:
        all_words.extend(rfptr.read().split(','))
    selected_words = []
    for word in all_words:
        dist = hamming_distance(bitstream, word)
        selected_words.append((word, dist))
    return selected_words


def get_possible_words (bit_stream, dis, index=None, dp=None):
    """Get all possible words which are dis bit-flips away from bit_stream."""
    # Implement in Dynamic programming.
    if len(bit_stream) == 0:
        return ['']
    if dis <= 0:
        return [bit_stream]
    possible_words = []
    bit = '1'
    if bit_stream[0] == '1':
        bit = '0'
    words = get_possible_words(bit_stream[1:], dis - 1)  # flip current bit.
    for word in words:
        possible_words.append(bit + word)
    words = get_possible_words(bit_stream[1:], dis)  # don't flip current bit.
    for word in words:
        possible_words.append(bit_stream[0] + word)
    try:
        possible_words.remove(bit_stream)
    except ValueError:
        pass
    return possible_words
