"""Code to construct the huffman tree for encoding and decoding."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json
import math
import os

import lib
from lib import constants
from lib import node as node_def


class NotLeafException(Exception):
    """Exception to be raised when """
    pass


class HuffmanTree (lib.Singleton):
    """THe Huffman tree."""
    CHILD = {
        '0': 'left',
        '1': 'right'
    }
    MATH_POW = {}

    def __init__(self):
        self._root = node_def.Node(is_root=True)
        for character in constants.HUFFMAN_CODES.keys():
            self._construct_tree(character)

        rfptr = open(constants.DATA_PATH % '/words.count', 'r')
        word_counts = json.loads(rfptr.read())
        rfptr.close()

        self._encoded_word_count = {}
        for word, count in word_counts.items():
            self._encoded_word_count[self.encode(word)] = count

        self._hamming_dict = {}
        for filename in os.listdir(constants.DATA_PATH % ''): 
            if not filename.endswith('.code_length'):
                continue
            with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
                self._hamming_dict[filename.split('.')[0]] = (
                    rfptr.read().split(','))

    def decode(self, bit_stream):
        """Decode the bit_stream."""
        if not self._encoded_word_count.get(bit_stream):
            restored_word = ''
            max_prob = 0
            for x in self._hamming_dict[str(len(bit_stream))]:
                dis = lib.hamming_distance(bit_stream, x)
                wcount = self._encoded_word_count[x]
                temp = HuffmanTree.MATH_POW.get((wcount, dis))
   
                if temp == None:
                    temp = math.pow(wcount, dis)
                    HuffmanTree.MATH_POW[(wcount, dis)] = temp
   
                if temp >= max_prob:
                    max_prob = temp
                    restored_word = x
 
            bit_stream = restored_word

        word = []
        node = self._root
        for bit in bit_stream:
            node = getattr(node, HuffmanTree.CHILD[bit])
            if node.is_leaf:
                word.append(node.value)
                node = self._root
        return ''.join(word)

    def encode(self, word):
        """Encode the word."""
        bit_stream = []
        for char in word:
            bit_stream.append(constants.HUFFMAN_CODES[char])
        return ''.join(bit_stream)

    def _construct_tree (self, character):
        node = self._root
        for bit in constants.HUFFMAN_CODES[character]:
            new_node = getattr(node, HuffmanTree.CHILD[bit]) or node_def.Node()
            setattr(node, HuffmanTree.CHILD[bit], new_node)
            node = new_node
        node.value = character
        node.is_leaf = True
