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
#         with open(constants.DATA_PATH % 'word_prob_per_bag_of_tag.hufman', 'r') as fptr:
#             self.word_freq_per_bag_of_tag = cPickle.loads(fptr.read())  # For Data Structure refer generate_hmm.py.
#  
#         with open(constants.DATA_PATH % 'bag_of_tag_prev.prob', 'r') as fptr:
#             self.bag_of_tag_prob_prev = cPickle.loads(fptr.read())  # For Data Structure refer generate_hmm.py.
#  
#         with open(constants.DATA_PATH % 'bag_of_tag_next.prob', 'r') as fptr:
#             self.bag_of_tag_prob_next = cPickle.loads(fptr.read())  # For Data Structure refer generate_hmm.py.

    # Unigram frequencies
    def get_best_sequence_ug(self, error_array, error_pb):
        """Get the best sequence."""
        decoded_array = []
        for bit_stream in error_array:
#             if self._encoded_word_count.get(bit_stream):
#                 decoded_array.append(bit_stream)
#                 continue
            dis = 2
            possible_words = set(lib.get_possible_words(bit_stream, dis))
            actual_words = set(self._bit_len_dict[str(len(bit_stream))])
            possible_words = actual_words.intersection(possible_words)

            heap = []
            for x in possible_words:
                dis = lib.hamming_distance(bit_stream, x)
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
            decoded_array.append(heapq.heappop(heap)[1])
        return decoded_array

    # Bigram frequencies
    def get_best_sequence_g(self, error_array, error_pb):
        """Get the best sequence. Greedy approach."""
        prev_word = constants.PAD_SYMBOL
        decoded_array = []
        for bit_stream in error_array:
#             if self._encoded_word_count.get(bit_stream):
#                 prev_word = bit_stream
#                 decoded_array.append(bit_stream)
#                 continue
            dis = 2
            possible_words = set(lib.get_possible_words(bit_stream, dis))
            actual_words = set(self._bit_len_dict[str(len(bit_stream))])
            possible_words = actual_words.intersection(possible_words)

            heap = []
            for x in possible_words:
                dis = lib.hamming_distance(bit_stream, x)
                wcount = self.bigram_pb.get((prev_word, x), self.ugram_pb.get(x, 0.0))

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
            prev_word = heapq.heappop(heap)[1]
            decoded_array.append(prev_word)
        return decoded_array

    # Bigram frequencies
    def get_best_sequence_dp(self, error_array, error_pb):
        """Get the best sequence. Implemented in Dynamic programming."""
        prev_word = constants.PAD_SYMBOL
        prob_list = {prev_word: (1, [])}
        for bit_stream in error_array:
            if self._encoded_word_count.get(bit_stream):
                maximum = 0
                max_path = []
                for prev_word, (prob, path) in prob_list.items():
                    if prob > maximum:
                        maximum = prob
                        max_path = path
                prob_list = {bit_stream: (1, max_path + [bit_stream])}
                continue
            dis = 2
            possible_words = set(lib.get_possible_words(bit_stream, dis))
            actual_words = set(self._bit_len_dict[str(len(bit_stream))])
            possible_words = actual_words.intersection(possible_words)

            temp = {}
#             print '========================================'
#             print prob_list
#             print '========================================'
            for prev_word, (prob, path) in prob_list.items():
                for x in possible_words:
                    dis = lib.hamming_distance(bit_stream, x)
                    wcount = self.bigram_pb.get((prev_word, x), self.ugram_pb.get(x, 0.0))

                    flip_pb = BestSequence.MATH_POW.get((error_pb, dis))

                    non_flip_pb = BestSequence.MATH_POW.get(
                        ((1.0 - error_pb), (len(bit_stream) - dis)))

                    product = BestSequence.PRODUCT.get(
                        (flip_pb, non_flip_pb, wcount, prob))

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
                        if wcount == 0.0:
                            wcount = 0.00001  # add a bias.
                        product = flip_pb * non_flip_pb * wcount * prob
                        BestSequence.PRODUCT[
                            (flip_pb, non_flip_pb, wcount, prob)] = product
#                     print '==============================='
#                     print error_pb
#                     print wcount, flip_pb, non_flip_pb, product
#                     print '==============================='

                    if temp.get(x, (0, []))[0] <= product:
                        temp[x] = (product, path + [x])
            prob_list = temp


        maximum = 0
        max_path = []
        for prev_word, (prob, path) in prob_list.items():
            if prob > maximum:
                maximum = prob
                max_path = path

        return max_path

    def get_best_sequence_true_hmm(self, error_array, error_pb):
        """Get the best sequence. Using True HMM and fb for each state."""
        prev_word = constants.PAD_SYMBOL
        prob_hmm_a = {}
        pos = 0
        prev_states = [(prev_word, constants.PAD_SYMBOL)]

        # Forward
        for bit_stream in error_array:
            temp = []
            pos += 1
            dis = 1
            possible_words = set(lib.get_possible_words(bit_stream, dis))
            actual_words = set(self._bit_len_dict[str(len(bit_stream))])
            possible_words = actual_words.intersection(possible_words)

            for x in possible_words:
                bot = self.bag_of_tags_by_word.get(x, ())
                curr_state = (x, bot)

                dis = lib.hamming_distance(bit_stream, x)
                temp.append(curr_state)

                for prev_state in prev_states:  # option for parallelism.
                    transition = self.bag_of_tag_prob_prev.get((
                        prev_state[1], curr_state[1]), 0.0)
                    emission = self.word_freq_per_bag_of_tag.get(
                        curr_state[1], {}).get(curr_state[0], 0)
                    state_prob = BestSequence.PRODUCT.get((transition,
                                                           emission))
                    if state_prob == None:
                        state_prob = transition * emission
                        BestSequence.PRODUCT[(transition, emission)] = (
                            state_prob)

                    prob_hmm_a[(prev_state,
                                curr_state, pos, bit_stream)] = state_prob
            prev_states = temp

        error_array_rev = []
        error_array_rev.extend(error_array)
        error_array_rev.reverse()

        pos += 1
        prob_hmm_b = {}
        next_states = prev_states

        # Backward
        for bit_stream in error_array_rev[:-1]:
            temp = []
            pos -= 1
            dis = 1
            possible_words = set(lib.get_possible_words(bit_stream, dis))
            actual_words = set(self._bit_len_dict[str(len(bit_stream))])
            possible_words = actual_words.intersection(possible_words)

            for x in possible_words:
                bot = self.bag_of_tags_by_word.get(x, ())
                curr_state = (x, bot)

                dis = lib.hamming_distance(bit_stream, x)
                temp.append(curr_state)

                for next_state in next_states:  # option for parallelism.
                    transition = self.bag_of_tag_prob_next.get((
                        next_state[1], curr_state[1]), 0.0)
                    emission = self.word_freq_per_bag_of_tag.get(
                        curr_state[1], {}).get(curr_state[0], 0)
                    state_prob = BestSequence.PRODUCT.get((transition,
                                                           emission))
                    if state_prob == None:
                        state_prob = transition * emission
                        BestSequence.PRODUCT[(transition, emission)] = (
                            state_prob)

                    prob_hmm_b[(curr_state, next_state, pos)] = state_prob
            next_states = temp

        prob_hmm = {}
        states = {}
        for k, v in prob_hmm_a.items():
#             prev_word = k[0][0]
#             x = k[1][0]
#             error_word = k[3]
#             dis = lib.hamming_distance(error_word, x)
# 
#             wcount = self.bigram_pb.get((prev_word, x), 0.0)
# 
#             flip_pb = BestSequence.MATH_POW.get((error_pb, dis))
# 
#             non_flip_pb = BestSequence.MATH_POW.get(
#                 (1.0 - error_pb), (len(error_word) - dis))
# 
#             product = BestSequence.PRODUCT.get(
#                 (flip_pb, non_flip_pb, wcount))
# 
#             if flip_pb == None:
#                 flip_pb = math.pow(error_pb, dis)
#                 BestSequence.MATH_POW[(error_pb, dis)] = flip_pb
# 
#             if non_flip_pb == None:
#                 non_flip_pb = math.pow((1.0 - error_pb),
#                                        (len(error_word) - dis))
#                 BestSequence.MATH_POW[
#                     ((1.0 - error_pb),
#                      (len(error_word) - dis))] = non_flip_pb
# 
#             if product == None:
#                 product = flip_pb * non_flip_pb * wcount * (-1.0)
#                 BestSequence.PRODUCT[
#                     (flip_pb, non_flip_pb, wcount)] = product

            transition = self.bag_of_tag_prob_prev.get((k[0][1], k[1][1]), 0.0)
            emission = self.word_freq_per_bag_of_tag.get(k[1][1], {}).get(
                k[1][0], 0)
            # TODO possible use of more Hashing.
            state_prob = BestSequence.PRODUCT.get((transition, emission))
            prob_hmm[k] = v * state_prob * prob_hmm_b.get(k[:3], 0) * (-1.0)
            states[k[2]] = states.get(k[2], [])
            heapq.heappush(states[k[2]], (prob_hmm[k], k[1][0]))

        decoded_array = []
        for x in range(len(error_array)):
            decoded_array.append(heapq.heappop(states[x + 1])[1])

        return decoded_array
