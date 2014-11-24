"""Constants values library."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'


DATA_PATH = '/projects/researchv2/data/%s'


STOP_WORDS = (
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
    'will', 'with')


# Huffman code taken from http://www.yorku.ca/mack/uist2011.html.
HUFFMAN_CODES = {
    ' ': '111',
    'a': '1011',
    'b': '011000',
    'c': '00001',
    'd': '01101',
    'e': '010',
    'f': '110011',
    'g': '011001',
    'h': '0010',
    'i': '1000',
    'j': '1100001011',
    'k': '11000011',
    'l': '10101',
    'm': '110010',
    'n': '0111',
    'o': '1001',
    'p': '101000',
    'q': '11000010101',
    'r': '0001',
    's': '0011',
    't': '1101',
    'u': '00000',
    'v': '1100000',
    'w': '110001',
    'x': '110000100',
    'y': '101001',
    'z': '11000010100',
}

# Start and Stop params for use in bigram and trigram ML
PAD_SYMBOL = '*'