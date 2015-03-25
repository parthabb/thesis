"""Unit test cases to check if create huffman code file works"""

__author__ = "Partha Baruah (parthabb@gmail.com)"

import unittest

import create_huffman_code


class TestStringMethods(unittest.TestCase):

    def test_generate_huffman_code(self):
        chc = create_huffman_code.CreateHuffmanCode()
        data = {'1': 5, '2': 7, '3': 10, '4': 15, '5': 20, '6': 45}
        expected = {'6': '0', '3': '100', '1': '1010', '2': '1011', '4': '110', '5': '111'}
        result = chc.generate_huffman_code(data)
        self.assertDictEqual(result, expected)

    def test_count_characters(self):
        chc = create_huffman_code.CreateHuffmanCode('scripts/test_count.txt')
        expected = {'1': 5, '2': 7, '3': 10, '4': 15, '5': 20, '6': 45}
        result = chc.char_counts
        self.assertDictEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
