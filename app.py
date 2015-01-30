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
        with open(constants.DATA_PATH % 'brown.sentences', 'r') as rfptr:
            sentences.extend(json.loads(rfptr.read()))

        now = time.time()
        other = 0.0
        no_error = 0
        for val in sentences[:17000]:
#         for _ in range(1):
            other_time = time.time()
            encoded_array = []
            for word in val.split():
                encoded_array.append(ht.encode(word.lower()))

            error_array = []
            for bit_stream in encoded_array:
                error_array.append(lib.add_error(bit_stream, error_pb))
            if error_array == encoded_array:
                no_error += 1
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
        print (time.time() - now - other) / 17000.0
        print len(correctq) + len(errorq)
        print 'correct: %s' % sum(correctq)
        print 'wrong: %s' % sum(errorq)

    @staticmethod
    def decode(ht, bs, error_array, val, error_pb, correctq, errorq):
        decoded_array = []
        correct_array = bs.get_best_sequence_ug(error_array, error_pb)
        for word in correct_array:
            decoded_array.append(ht.decode(word))

        decoded_str = ' '.join(decoded_array)

        if val.lower() == decoded_str:
            correctq.append(1)
        else:
            errorq.append(1)


if __name__ == '__main__':
#     cProfile.run('app.run()')
    app.run()
