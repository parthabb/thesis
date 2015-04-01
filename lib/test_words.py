"""Unit test cases for words.py"""

import time
import unittest

import lib
from lib import words


class TestWords(unittest.TestCase):
    """Unit test case class for Words."""
    def test_get_most_probable_words(self):
        pass

    def test_get_most_probable_words_through_trie(self):
        self.w = words.Words()
        error_word = '00100'
        actual_words = ['10101', '00000', '01101', '00001']
        trie = lib.build_tries(actual_words)
        self.w._encoded_tries_by_length = {str(len(error_word)): trie}
        now = time.time()
        res_words = self.w.get_most_probable_words_through_trie(error_word)
        print time.time() - now
        temp = []
        for v in res_words.values():
            temp.extend(list(v))
        res_words = temp
        print res_words
        for x in res_words:
            self.assertIn(x, actual_words)
        for x in actual_words:
            self.assertIn(x, res_words)


if __name__ == '__main__':
    unittest.main()