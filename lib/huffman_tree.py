"""Code to construct the huffman tree for encoding and decoding."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

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

    def __init__(self):
        self._root = node_def.Node(is_root=True)
        for character in constants.HUFFMAN_CODES.keys():
            self._construct_tree(character)

    def decode(self, bit_stream):
        """Decode the bit_stream."""
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
