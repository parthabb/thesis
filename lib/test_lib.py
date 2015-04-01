"""Unit test cases for build trie file."""

import unittest
import lib

class TestLib(unittest.TestCase):
    """Unit test cases for build trie."""
    def _util(self, node, all_leaves, temp):
        if node.is_leaf:
            print temp
            all_leaves.append(''.join(temp))
            return
        if node.left:
            t = list(temp)
            t.append('0')
            self._util(node.left, all_leaves, t)
        if node.right:
            t = list(temp)
            t.append('1')
            self._util(node.right, all_leaves, t)

    def test_build_tries(self):
        """Unit test case for build trie."""
        all_words = ['1111', '0000', '0001', '1011', '1001', '0010']
        root = lib.build_tries(all_words)
        all_leaves = []
        self._util(root, all_leaves, [])
        for x in all_leaves:
            self.assertIn(x, all_words)

if __name__ == '__main__':
    unittest.main()
