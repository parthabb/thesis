"""File implementing the logic for correct words of the sentence."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import cPickle
import heapq
import json
import math
import os


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

        self._bit_len_dict = {}  # Words with same bit-string length.
        for filename in os.listdir(constants.DATA_PATH % ''): 
            if not filename.endswith('.code_length'): 
#             if not filename.endswith('.tries'):
                continue
            with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
                self._bit_len_dict[filename.split('.')[0]] = (
                    rfptr.read().split(','))
#                 self._bit_len_dict[filename.split('.')[0]] = (
#                     cPickle.loads(rfptr.read()))

        with open(constants.DATA_PATH % 'ugram.probs', 'r') as rfptr:
            self.ugram_pb = cPickle.loads(rfptr.read())  # For Data Structure refer calculate_unigram_probabilities.py.

        with open(constants.DATA_PATH % 'bigram.probs', 'r') as rfptr:
            self.bigram_pb = cPickle.loads(rfptr.read())  # For Data Structure refer calculate_bigram_probabilities.py.

#         with open(constants.DATA_PATH % 'bag_of_tags_by_word.huffman', 'r') as fptr:
#             self.bag_of_tags_by_word = cPickle.loads(fptr.read())  # For Data Structure refer generate_hmm.py.
# 
#         with open(constants.DATA_PATH % 'word_freq_per_bag_of_tag.hufman', 'r') as fptr:
#             self.word_freq_per_bag_of_tag = cPickle.loads(fptr.read())  # For Data Structure refer generate_hmm.py.
# 
#         with open(constants.DATA_PATH % 'bag_of_tag.prob', 'r') as fptr:
#             self.bag_of_tag = cPickle.loads(fptr.read())  # For Data Structure refer generate_hmm.py.

    # Unigram frequencies
    def get_best_sequence_ug(self, error_array, error_pb):
        """Get the best sequence."""
        decored_array = []
        for bit_stream in error_array:
            if not self._encoded_word_count.get(bit_stream):
                heap = []
                for x in self._bit_len_dict[str(len(bit_stream))]:
                    dis = lib.hamming_distance(bit_stream, x)
                    if dis > 2 and len(heap) > 0:
                        continue
                    wcount = self.ugram_pb.get((x), 0.0)

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
        return decored_array

    # Bigram frequencies
    def get_best_sequence_g(self, error_array, error_pb):
        """Get the best sequence. Greedy approach."""
        prev_word = constants.PAD_SYMBOL
        decored_array = []
        for bit_stream in error_array:
            if not self._encoded_word_count.get(bit_stream):
                heap = []
                for x in self._bit_len_dict[str(len(bit_stream))]:
                    dis = lib.hamming_distance(bit_stream, x)
                    if dis > 2 and len(heap) > 0:
                        continue
#                     wcount = self._encoded_word_count[x]
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

    # Bigram frequencies
    def get_best_sequence_dp(self, error_array, error_pb):
        """Get the best sequence. Implemented in Dynamic programming."""
        prev_word = constants.PAD_SYMBOL
        prob_list = {prev_word: (1, [])}
        for bit_stream in error_array:
            if not self._encoded_word_count.get(bit_stream):
                temp = {}
                for prev_word, (prob, path) in prob_list.items():
                    for x in self._bit_len_dict[str(len(bit_stream))]:
                        dis = lib.hamming_distance(bit_stream, x)
                        if dis > 2 and len(prob_list) > 0:
                            continue
#                         wcount = self._encoded_word_count[x]
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
                            product = flip_pb * non_flip_pb * wcount * prob
                            BestSequence.PRODUCT[
                                (flip_pb, non_flip_pb, wcount)] = product

                        if temp.get(x, (0, []))[0] < product:
                            temp[x] = (product, path + [x])
                prob_list = temp
            else:
                maximum = 0
                max_path = []
                for prev_word, (prob, path) in prob_list.items():
                    if prob > maximum:
                        maximum = prob
                        max_path = path
                prob_list = {bit_stream: (1, max_path + [bit_stream])}

        maximum = 0
        max_path = []
        for prev_word, (prob, path) in prob_list.items():
            if prob > maximum:
                maximum = prob
                max_path = path

        return max_path

    def get_best_sequence_hmm(self, error_array, error_pb):
        """Get the best sequence. Using HMM."""
        pass

    
