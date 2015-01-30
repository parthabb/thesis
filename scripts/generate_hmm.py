"""Create HMM model based on Parts-Of-Speech tags."""

import cPickle
import json
import re
import string

import nltk
from nltk.corpus import brown
from nltk.util import ngrams

from lib import constants
from lib import huffman_tree


# HuffmanTree object.
ht = huffman_tree.HuffmanTree()

# A dict with a bag of tags for each word.
words = {}
words_huffman_encoded = {}  # A dict with a bag of tags for each huffman encoded word.

# All raw text of brown corpus.
txt = brown.raw()

# Raw sentences from brown corpus.
tagged_sentences = txt.split('./.')

# Get all tags for all words
for tagged_sentence in tagged_sentences:
    tagged_sentence = tagged_sentence.strip()
    if re.match(r'[0-9 ]+$', tagged_sentence):
        continue
    for word in tagged_sentence.split():
        word = word.strip()
        word = word.split('/')
        if len(word) < 2:
            continue
        word[0] = str(word[0]).translate(string.maketrans("",""),
                                         string.punctuation)
        if not re.match(r'[A-Za-z ]+$', word[0]):
            continue
        tags = words.get(word[0].lower(), set())
        tags.add(word[1])
        words[word[0].lower()] = tags
        words_huffman_encoded[ht.encode(word[0].lower())] = tags  # [<encoded_word>] = Set of all tags for that word.

with open(constants.DATA_PATH % 'bag_of_tags_by_word.huffman', 'w') as fptr:
    fptr.write(cPickle.dumps(words_huffman_encoded))


word_count_by_bag_of_tags = {}

for word, bot in words.items():
    bot = tuple(bot)  # Convert set to tuple.
    word_dict = word_count_by_bag_of_tags.get(bot, {})
    count = word_dict.get(word, 0.0)
    count += 1.0
    word_dict[word] = count
    word_count_by_bag_of_tags[bot] = word_dict

# print word_count_by_bag_of_tags

word_freq_bot = {}
for bot, word_dict in word_count_by_bag_of_tags.items():
    total = sum(word_dict.values())
    for word, count in word_dict.items():
        word_dict[word] = count / total
    word_freq_bot[bot] = word_dict

# print word_freq_bot




word_count_by_bag_of_tags_huffman = {}

for word, bot in words_huffman_encoded.items():
    bot = tuple(bot)  # Convert set to tuple.
    word_dict = word_count_by_bag_of_tags_huffman.get(bot, {})
    count = word_dict.get(word, 0.0)
    count += 1.0
    word_dict[word] = count
    word_count_by_bag_of_tags_huffman[bot] = word_dict

word_prob_per_bot_huffman = {}  # Probability of word in a Bag of Tags. 
for bot, word_dict in word_count_by_bag_of_tags_huffman.items():
    total = sum(word_dict.values())
    for word, count in word_dict.items():
        word_dict[word] = count / total
    word_prob_per_bot_huffman[bot] = word_dict

with open(constants.DATA_PATH % 'word_freq_per_bag_of_tag.hufman', 'w') as fptr:
    fptr.write(cPickle.dumps(word_prob_per_bot_huffman))




clean_sentences = []
with open(constants.DATA_PATH % 'brown.sentences', 'r') as fptr:
    clean_sentences = json.loads(fptr.read())

ugs = []
bgs = []
for clean_sentence in clean_sentences:
    temp = []
    for word in clean_sentence.split():
        if words.has_key(word.lower()):
            temp.append(json.dumps(tuple(words[word.lower()])))
    if len(temp) == 0:
        continue
    clean_sentence = 'nlp'.join(temp)
    ugs.append(constants.PAD_SYMBOL)
    ugs.extend(temp)
    bgs.extend(list(ngrams(clean_sentence.split('nlp'), n=2, pad_left=True,
                           pad_right=False,
                           pad_symbol=constants.PAD_SYMBOL)))

fdist_ugs = nltk.FreqDist(ugs)
fdist_bgs = nltk.FreqDist(bgs)

probs = {}
for sample, count in fdist_bgs.items():
    # [(<bag_of_tag_1>, <bag_of_tag_2>)] = Probability of (<bag_of_tag_1>, <bag_of_tag_2>) given <bag_of_tag_1>.
    probs[sample] = count / float(fdist_ugs.get(sample[1]))


with open(constants.DATA_PATH % 'bag_of_tag.prob', 'w') as fptr:
    fptr.write(cPickle.dumps(probs))
