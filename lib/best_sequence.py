"""File implementing the logic for correct words of the sentence."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import cPickle
import heapq
import json
import math
import os
import pickle


import lib
from lib import constants

class BestSequence(lib.Singleton):
    """Class to implement the algorithm to determine the best sequence."""
    MATH_POW = {}
    PRODUCT = {}

    def __init__(self, ht):
        rfptr = open(constants.DATA_PATH % '/words.count', 'r')
        word_counts = json.loads(rfptr.read())
        rfptr.close()

        self._encoded_word_count = {}
        for word, count in word_counts.items():
            self._encoded_word_count[ht.encode(word)] = count

        self._hamming_dict = {}
        for filename in os.listdir(constants.DATA_PATH % ''): 
            if not filename.endswith('.code_length'): 
#             if not filename.endswith('.tries'):
                continue
            with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
                self._hamming_dict[filename.split('.')[0]] = (
                    rfptr.read().split(','))
#                 self._hamming_dict[filename.split('.')[0]] = (
#                     cPickle.loads(rfptr.read()))

        with open(constants.DATA_PATH % 'bigram.probs', 'r') as rfptr:
            self.bigram_pb = pickle.loads(rfptr.read())

        with open(constants.DATA_PATH % 'bag_of_tags_by_word.huffman', 'r') as fptr:
            self.bag_of_tags_by_word = cPickle.loads(fptr.read())

        with open(constants.DATA_PATH % 'word_freq_per_bag_of_tag.hufman', 'r') as fptr:
            self.word_freq_per_bag_of_tag = cPickle.loads(fptr.read())

        with open(constants.DATA_PATH % 'bag_of_tag.prob', 'r') as fptr:
            self.bag_of_tag = cPickle.loads(fptr.read())

    def get_best_sequence(self, error_array, error_pb):
        """Get the best sequence. Implements the Viterbi algorithm."""
        prev_word = constants.PAD_SYMBOL
        decored_array = []
        for bit_stream in error_array:
            if not self._encoded_word_count.get(bit_stream):
                heap = []
                for x in self._hamming_dict[str(len(bit_stream))]:
                    dis = lib.hamming_distance(bit_stream, x)
                    if dis > 2 and len(heap) > 0:
                        break
    #                 wcount = self._encoded_word_count[x]
                    wcount = self.bigram_pb.get((prev_word, x), 0.0)
    
                    flip_pb = BestSequence.MATH_POW.get((error_pb, dis))
     
                    non_flip_pb = BestSequence.MATH_POW.get(
                        (1.0 - error_pb), (len(bit_stream) - dis))
    
                    product = BestSequence.PRODUCT.get(
                        (flip_pb, non_flip_pb, wcount))
    
                    if flip_pb == None:
                        flip_pb = math.pow(error_pb, dis)
                        BestSequence.MATH_POW[(error_pb, dis)] = flip_pb
    
                    if non_flip_pb == None:
                        non_flip_pb = math.pow((1.0 - error_pb),
                                               (len(bit_stream) - dis))
                        BestSequence.MATH_POW[
                            ((1.0 - error_pb),
                             (len(bit_stream) - dis))] = non_flip_pb
    
                    if product == None:
                        product = flip_pb * non_flip_pb * wcount * (-1.0)
                        BestSequence.PRODUCT[
                            (flip_pb, non_flip_pb, wcount)] = product
    
                    heapq.heappush(heap, (product, x))
                bit_stream = heapq.heappop(heap)[1]
            decored_array.append(bit_stream)
            prev_word = bit_stream
        return decored_array

#     def get_best_sequence(self, error_array, error_pb):
#         """Get the best sequence. Implements the Viterbi algorithm."""
#         pos = 0
#         bit_stream = error_array[pos]
#         prev_word = constants.PAD_SYMBOL
#         hmm_table = []
#         seq_table = []
#         maximum = 0
#         hmm = {}
#         seq = {}
#         for x in self._hamming_dict[str(len(bit_stream))]:
#             dis = lib.hamming_distance(bit_stream, x)
# #                     if dis > 2 and count > 0:
# #                         break
# #                 wcount = self._encoded_word_count[x]
#             wcount = self.bigram_pb.get((prev_word, x), 0.0)
# 
#             flip_pb = BestSequence.MATH_POW.get((error_pb, dis))
#             if flip_pb == None:
#                 flip_pb = math.pow(error_pb, dis)
#                 BestSequence.MATH_POW[(error_pb, dis)] = flip_pb
# 
#             non_flip_pb = BestSequence.MATH_POW.get(
#                 (1.0 - error_pb), (len(bit_stream) - dis))
#             if non_flip_pb == None:
#                 non_flip_pb = math.pow((1.0 - error_pb),
#                                        (len(bit_stream) - dis))
#                 BestSequence.MATH_POW[
#                     ((1.0 - error_pb),
#                      (len(bit_stream) - dis))] = non_flip_pb
# 
#             product = BestSequence.PRODUCT.get(
#                 (flip_pb, non_flip_pb, wcount))
#             if product == None:
#                 product = flip_pb * non_flip_pb * wcount
#                 BestSequence.PRODUCT[
#                     (flip_pb, non_flip_pb, wcount)] = product
#             hmm[x] = product
#             seq[x] = prev_word
#             if product > maximum:
#                 maximum = product
# 
#         hmm_table.append(hmm)
#         seq_table.append(seq)
# 
#         pos = 0
#         for bit_stream in error_array[1:]:
#             pos += 1
#             hmm = {}
#             seq = {}
#             count = 0
#             for x in self._hamming_dict[str(len(bit_stream))]:
#                 dis = lib.hamming_distance(bit_stream, x)
#                 if dis > 2 and count > 2:
#                     break
#                 flip_pb = BestSequence.MATH_POW.get((error_pb, dis))
#                 if flip_pb == None:
#                     flip_pb = math.pow(error_pb, dis)
#                     BestSequence.MATH_POW[(error_pb, dis)] = flip_pb
# 
#                 non_flip_pb = BestSequence.MATH_POW.get(
#                     (1.0 - error_pb), (len(bit_stream) - dis))
#                 if non_flip_pb == None:
#                     non_flip_pb = math.pow((1.0 - error_pb),
#                                            (len(bit_stream) - dis))
#                     BestSequence.MATH_POW[
#                         ((1.0 - error_pb),
#                          (len(bit_stream) - dis))] = non_flip_pb
# 
#                 for prev_word, pb in hmm_table[pos - 1].items():
#                     if pb == 0:
#                         continue
#                     wcount = self.bigram_pb.get((prev_word, x), 0.0)
# 
#                     product = BestSequence.PRODUCT.get(
#                         (flip_pb, non_flip_pb, wcount))
#                     if product == None:
#                         product = flip_pb * non_flip_pb * wcount
#                         BestSequence.PRODUCT[
#                             (flip_pb, non_flip_pb, wcount)] = product
#                     pb_x = pb * product
#                     if pb_x >= hmm.get(x, 0.0):
#                         hmm[x] = pb_x
#                         seq[x] = prev_word
# 
#                 count += 1
#             hmm_table.append(hmm)
#             seq_table.append(seq)
# 
#         print len(hmm_table)
#         maximum = 0
#         word = ''
#         t = max(hmm_table[-1].values())
#         print t
#         for k, v in hmm_table[-1].items():
#             if v == t:
#                 print k
# #         print hmm_table[-1]
#         for x, pb in hmm_table[-1].items():
#             if pb > maximum:
#                 maximum = pb
#                 word = x
#         decoded_str = [word]
#         seq_table.reverse()
# #         print seq_table[0]
#         decoded_str.reverse()
# #         print decoded_str
#         return decoded_str
