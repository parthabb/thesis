"""Code to create Huffman code for all characters found in the text"""

__author__ = "Partha Baruah (parthabb@gmail.com)"

import heapq

from lib import node

class CreateHuffmanCode(object):
    """Utility class that reads data from the files and creates Huffman code for the symbols"""
    def __init__(self, filename='scripts/test_data.txt'):
        data = ''
        with open(filename, 'r') as rfptr:
            data = rfptr.read().split('. ')
        self.char_counts = {}
        for sentence in data:
            self._count_characters(sentence.lower())
        self._hc = self.generate_huffman_code(self.char_counts)

    def get_huffman_code(self, character):
        """Returns the huffman code for that character"""
        return self._hc.get(character, None)

    def _count_characters(self, text):
        """Counts the characters in the text and returns a dictionary with the counts."""
        for char in text:
            self.char_counts[char] = self.char_counts.get(char, 0) + 1

    def generate_huffman_code(self, char_counts):
        """Based on the char counts, generate the huffman codes."""
        huffman_code = {}
        heap = []
        for k, v in char_counts.items():
            heapq.heappush(heap, (v, k))
        while True:
            char_1 = heapq.heappop(heap)
            if isinstance(char_1[1], str):
                node_1 = node.Node()
                node_1.is_leaf = True
                node_1.value = char_1[1]
            else:
                node_1 = char_1[1]

            char_2 = heapq.heappop(heap)
            if isinstance(char_2[1], str):
                node_2 = node.Node()
                node_2.is_leaf = True
                node_2.value = char_2[1]
            else:
                node_2 = char_2[1]

            parent = node.Node()
            parent.left = node_1
            parent.right = node_2
            parent.value = char_1[0] + char_2[0]

            heapq.heappush(heap, (parent.value, parent))

            if len(heap) <= 1:
                break
        root = heapq.heappop(heap)[1]
        root.is_root = True

        code_word = []
        nodes = []
        nodes.append(root)
        curr = None
        while nodes:
            curr = nodes.pop()
            if not curr.is_leaf:
                nodes.append(curr)
                nodes.append(curr.left)
                code_word.append('0')
            else:
                huffman_code[curr.value] = ''.join(code_word)
                try:
                    parent = nodes.pop()
                except IndexError:
                    break
                prev = code_word.pop()
                if curr != parent.left:
                    while prev != '0':
                        prev = code_word.pop()
                code_word.append('1')
                nodes.append(parent.right)

        return huffman_code
