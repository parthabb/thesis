"""Code to assist with the webapp."""

import re
import threading
import time

import lib
from lib import best_sequence
from lib import huffman_tree
from lib import words

class WebLib(lib.Singleton):
    """Weblib class to handle all methods related to web server view."""
    def __init__(self):
        self.ht = huffman_tree.HuffmanTree()
        self.words = words.Words()

    def get_word_probability(self, word):
        """Get the count of that word."""
        return self.words._word_probability.get(word, 0)

    def get_encoded_word(self, word):
        return self.ht.encode(word)

    def get_probable_words(self, word):
#         now = time.time()
#         pwords_m = self.words.get_most_probable_words_through_setops(word)
#         time_taken = time.time() - now
#         decoded_words = []
#         for dis, temp in pwords_m.items():
#             for w in temp:
#                 decoded_words.append(self.ht.decode(w))
#             pwords_m[dis] = decoded_words
#             decoded_words = []

        now = time.time()
        pwords_m = self.words.get_most_probable_words_through_trie(word)
        time_taken = time.time() - now
        decoded_words = []
        for dis, temp in pwords_m.items():
            for w in temp:
                decoded_words.append(self.ht.decode(w))
            pwords_m[dis] = decoded_words
            decoded_words = []

        return pwords_m, time_taken


def initialize ():
    best_sequence.BestSequence(huffman_tree.HuffmanTree())

def add_error_and_correct (text, error_pb):
    sentences = []
    for sentence in text.split('. '):
        sentence = lib.clean_data(sentence.split())
        if re.match(r'[A-Za-z ]+$', sentence):
            sentences.append(sentence)

    ht = huffman_tree.HuffmanTree()
    bs = best_sequence.BestSequence(ht)
    correctq = []
    errorq = []
    threads = []

    now = time.time()
    other = 0.0
    no_error = 0

    error_text = []
    corrected_text = []
    for val in sentences:
        other_time = time.time()
        encoded_array = []
        for word in val.split():
            encoded_array.append(ht.encode(word.lower()))

        error_array = []
        for bit_stream in encoded_array:
            error_array.append(lib.add_error(bit_stream, error_pb, 2))
        if error_array == encoded_array:
            no_error += 1

        err = []
        for x in error_array:
            err.append(ht.decode(x))

        error_text.append(' '.join(err))
        other += time.time() - other_time

        t = threading.Thread(target=decode,
                             args=(ht, bs, error_array, encoded_array, error_pb,
                                   corrected_text, correctq, errorq))
        t.daemon = True
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return ('. '.join(error_text),
            '. '.join(corrected_text),
            (time.time() - now - other) / ((len(sentences)) * 1.0),
            ((sum(correctq) - no_error) / ((len(sentences)) * 0.01)),
            sum(errorq) / (len(sentences) * 0.01))

def decode(ht, bs, error_array, encoded_array, error_pb, corrected_text,
           correctq, errorq):
    decoded_array = []
    correct_array = bs.get_best_sequence_dp(error_array, error_pb)
    if encoded_array == correct_array:
        correctq.append(1)
    else:
        errorq.append(1)

    for word in correct_array:
        decoded_array.append(ht.decode(word))

    corrected_text.append(' '.join(decoded_array))
