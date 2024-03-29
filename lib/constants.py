"""Constants values library."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'


DATA_PATH = '/projects/research_test/data/%s'


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

ALPHA = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5, 20: 5, 21: 5, 22: 5, 23: 5, 24: 5, 25: 5, 26: 5, 27: 5, 28: 5, 29: 5, 30: 5, 31: 5, 32: 5, 33: 5, 34: 5, 35: 5, 36: 5, 37: 5, 38: 5, 39: 5, 40: 5, 41: 5, 42: 5, 43: 5, 44: 5, 45: 5, 46: 5, 47: 5, 48: 5, 49: 5, 50: 5, 51: 5, 52: 5, 53: 5, 54: 5, 55: 5, 56: 5, 57: 5, 58: 5, 59: 5, 60: 5, 61: 5, 62: 5, 63: 5, 64: 5, 65: 5, 66: 5, 67: 5, 68: 5, 69: 5, 70: 5, 71: 5, 72: 5, 73: 5, 74: 5, 75: 5, 76: 5, 77: 5, 78: 5, 79: 5, 80: 5, 81: 5, 82: 5, 83: 5, 84: 5, 85: 5, 86: 5, 87: 5, 88: 5, 89: 5, 90: 5, 91: 5, 92: 5, 93: 5, 94: 5, 95: 5, 96: 5, 97: 5, 98: 5, 99: 5}
