"""The node of the Huffman tree."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'


class UnknownNodeTypeException(Exception):
    pass


class Node(object):
    """Node class for the Huffman tree."""
    def __init__(self, is_root=False):
        self._is_root = is_root
        self._value = None
        self._is_leaf = False
        self._left = None
        self._right = None

    @property
    def is_root(self):
        return self._is_root

    @is_root.setter
    def is_root(self, root):
        self._is_root = root

    @property
    def is_leaf(self):
        return self._is_leaf

    @is_leaf.setter
    def is_leaf(self, leaf):
        self._is_leaf = leaf

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        if type(left) is not self.__class__:
            raise UnknownNodeTypeException
        self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        if type(right) is not self.__class__:
            raise UnknownNodeTypeException
        self._right = right
