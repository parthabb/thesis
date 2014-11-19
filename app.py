"""Main application file."""

import cProfile
import json
import time

import lib
from lib import constants
from lib import huffman_tree


class app (object):
    """Application entry point."""
    @staticmethod
    def run():
        ht = huffman_tree.HuffmanTree()
        sentences = []
        time_taken = 0.0
        correct = 0
        wrong = 0
        with open(constants.DATA_PATH % 'brown.sentences', 'r') as rfptr:
            sentences.extend(json.loads(rfptr.read()))

#         val = ('The inference has been too widely accepted that because the '
#                'Communists have succeeded in building barricades across '
#                'Berlin the free world must acquiesce in dismemberment of that'
#                ' living city')

        for val in sentences[:17000]:
#         for _ in range(1):
            encoded_array = []
            for word in val.split():
                encoded_array.append(ht.encode(word.lower()))

            error_array = []
            for bit_stream in encoded_array:
                error_array.append(lib.add_error(bit_stream, .01))


            decoded_array = []
            for word in error_array:
#             for word in encoded_array:
                now = time.time()
                decoded_word = ht.decode(word)
                time_taken += time.time() - now
                decoded_array.append(decoded_word)

            decoded_str = ' '.join(decoded_array)

            if val.lower() == decoded_str:
                correct += 1
            else:
                wrong += 1

#             print val.lower()
#             print ' '.join(decoded_array)
        print '=================time taken================='
        print time_taken
        print 'correct: %s' % correct
        print 'wrong: %s' % wrong


if __name__ == '__main__':
#     cProfile.run('app.run()')
    app.run()
