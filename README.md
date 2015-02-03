thesis
======

Thesis / Research code



Steps:

1) Get the sentences from the corpus and separate them into training and test data. (brown.sentences + brown_test.sentences)

File: scripts/get_sentences_from_brown.py

####################################################
##
# File: brown.sentences + brown_test.sentences
# Format: [sentence1, sentence2, sentence3....]
##
####################################################

2) Count the words in the training + test data and store them in words.count

File: scripts/count_words_and_write_to_file.py

####################################################
##
# File: words.count
# Format: {word1: count1, word2, count2, ...}
##
####################################################

3) Create Huffman code for the words in words.count and store them in files as per their bit word lengths.

File: scripts/create_huffman_code_for_all_words.py

####################################################
##
# File name: <word_len>.code_length
# Format: word1, word2, word3, ...
##
####################################################

4) Calculate unigram and bigram probabilities for the words on brown.sentences

File: scripts/calculate_unigram_probabilities.py

####################################################
##
# File: ugram.probs
# Format: prob[(<huffman_encoded_word_1>)] = P[(<huffman_encoded_word_1>)]
##
####################################################

File: scripts/calculate_bigram_probabilities.py

####################################################
##
# File: bigram.probs
# probability of word2 following word1 appearing together given word1
# Format: prob[(<huffman_encoded_word_1>, <huffman_encoded_word_2>)] = P[(<huffman_encoded_word_1>, <huffman_encoded_word_2>) / <huffman_encoded_word_1>)]
##
####################################################


