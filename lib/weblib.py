"""Code to assist with the webapp."""

import re
import threading
import time

import lib
from lib import best_sequence
from lib import huffman_tree

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
            error_array.append(lib.add_error(bit_stream, error_pb))
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
    correct_array = bs.get_best_sequence_g(error_array, error_pb)
    if encoded_array == correct_array:
        correctq.append(1)
    else:
        errorq.append(1)

    for word in correct_array:
        decoded_array.append(ht.decode(word))

    corrected_text.append(' '.join(decoded_array))