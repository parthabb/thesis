"""Main application file."""

import cProfile
import json
import Queue
import threading
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
        correctq = []
        wrong = 0
        errorq = []
        error_pb = .01
        threads = []
        with open(constants.DATA_PATH % 'brown.sentences', 'r') as rfptr:
            sentences.extend(json.loads(rfptr.read()))

#         val = ('The inference has been too widely accepted that because the '
#                'Communists have succeeded in building barricades across '
#                'Berlin the free world must acquiesce in dismemberment of that'
#                ' living city')

        now = time.time()
        other = 0.0
        for val in sentences[:17000]:
#         for _ in range(1):
            other_time = time.time()
            encoded_array = []
            for word in val.split():
                encoded_array.append(ht.encode(word.lower()))

            error_array = []
            for bit_stream in encoded_array:
                error_array.append(lib.add_error(bit_stream, error_pb))
            other += time.time() - other_time

            t = threading.Thread(target=app.decode,
                                 args=(ht, error_array, val, error_pb,
                                       correctq, errorq))
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

            decoded_array = []
            for word in error_array:
#             for word in encoded_array:
                now = time.time()
                decoded_word = ht.decode(word, error_pb)
                time_taken += time.time() - now
                decoded_array.append(decoded_word)
 
            decoded_str = ' '.join(decoded_array)
#             print val
#             print decoded_str
 
            if val.lower() == decoded_str:
#                 print 'Correct'
                correct += 1
            else:
#                 print 'wrong'
                wrong += 1
 
#             print val.lower()
#             print ' '.join(decoded_array)
        print '=================time taken================='
        print time.time() - now - other
        print (time.time() - now - other) / 17000.0
        print len(correctq) + len(errorq)
        print sum(correctq)
        print sum(errorq)
        print 'correct: %s' % correct
        print 'wrong: %s' % wrong

#     @staticmethod
#     def decode(ht, error_array, val, error_pb, correctq, errorq):
#         decoded_array = []
#         for word in error_array:
# #             for word in encoded_array:
#             decoded_word = ht.decode(word, error_pb)
#             decoded_array.append(decoded_word)
# 
#         decoded_str = ' '.join(decoded_array)
# #             print val
# #             print decoded_str
# 
#         if val.lower() == decoded_str:
# #                 print 'Correct'
#             correctq.append(1)
#         else:
# #                 print 'wrong'
#             errorq.append(1)


if __name__ == '__main__':
#     cProfile.run('app.run()')
    app.run()
