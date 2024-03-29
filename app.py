"""Main application file."""

import cProfile
import json
import threading
import time

import lib
from lib import constants
from lib import best_sequence
from lib import huffman_tree


class app (object):
    """Application entry point."""
    @staticmethod
    def run():
        ht = huffman_tree.HuffmanTree()
        bs = best_sequence.BestSequence(ht)
        sentences = []
        correctq = []
        errorq = []
        error_pb = .01
        threads = []
        with open(constants.DATA_PATH % 'brown_test.sentences', 'r') as rfptr:
            sentences.extend(json.loads(rfptr.read()))

        now = time.time()
        other = 0.0
        no_error = 0
        sentences = sentences[:100]
#         sentences = ['his eyes had the same dreadful rigid stare as dr grimesby roylotts when he was found before his open safe wearing the speckled band',
#                      'the doors of the d train slid shut and as i dropped into a seat and exhaling looked up across the aisle the whole aviary in my head burst into song']
        for val in sentences:
#         for _ in range(1):
#             val = 'this is a test sentence to the test the program'
            other_time = time.time()
            encoded_array = []
            for word in val.split():
                encoded_array.append(ht.encode(word.lower()))

            error_array = []
            for bit_stream in encoded_array:
                error_array.append(lib.add_error(bit_stream, error_pb, 2))

            other += time.time() - other_time

            t = threading.Thread(target=app.decode,
                                 args=(ht, bs, error_array, val, error_pb,
                                       correctq, errorq))
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print '=================time taken================='
        print no_error
        print time.time() - now - other
        print (time.time() - now - other) / (len(sentences) * 1.0)
        print len(correctq) + len(errorq)
        print 'correct: %s (%s)' % (sum(correctq), (sum(correctq) / (len(sentences) * 0.01)))
        print 'wrong: %s (%s)' % (sum(errorq), sum(errorq) / (len(sentences) * 0.01))

    @staticmethod
    def decode(ht, bs, error_array, val, error_pb, correctq, errorq):
        decoded_array = []
#         print error_array
        correct_array = bs.get_bs_hmm_g(error_array, error_pb)
#         print correct_array
        for word in correct_array:
            decoded_array.append(ht.decode(word))

        decoded_str = ' '.join(decoded_array)

        if val.lower() == decoded_str:
            correctq.append(1)
        else:
            print '============================================================'
            print val.lower()
            print '+++++++++++++++++++++++++++++++++'
            print ' '.join(map(ht.decode, error_array))
            print '+++++++++++++++++++++++++++++++++'
            print decoded_str
            print '============================================================'
            errorq.append(1)


if __name__ == '__main__':
#     cProfile.run('app.run()')
    app.run()
