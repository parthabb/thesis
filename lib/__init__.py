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


def clean_data(text):
    """Function to clean the data from the corpus files."""
    text = text.split('/')
    if not text:
        return ''
    text = text[0].split('\'')[0]
    return text.translate(string.maketrans("",""), string.punctuation).lower()


def add_error(bitstream, p):
    """Flips the bits in the bit stream with a probability p."""
    random.seed()
    new_bitstream = []
    for bit in bitstream:
        val = random.random()
        if val < p:
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
