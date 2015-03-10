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
        # [<encoded_word>] = Set of all tags for that word.
        words_huffman_encoded[ht.encode(word[0].lower())] = tuple(tags)

with open(constants.DATA_PATH % 'bag_of_tags_by_word.huffman', 'w') as fptr:
    fptr.write(cPickle.dumps(words_huffman_encoded))


# For each bag of tag, count the words in that bag of tag.
word_count_by_bag_of_tags = {}

for word, bot in words.items():
    bot = tuple(bot)
    word_dict = word_count_by_bag_of_tags.get(bot, {})
    count = word_dict.get(word, 0.0)
    count += 1.0
    word_dict[word] = count
    word_count_by_bag_of_tags[bot] = word_dict

# For each bag of tag, calculate the probability of the words in that bag of tag
word_prob_per_bot = {}

for bot, word_dict in word_count_by_bag_of_tags.items():
    total = sum(word_dict.values())
    for word, count in word_dict.items():
        word_dict[word] = count / total
    word_prob_per_bot[bot] = word_dict

# For each bag of tag, count the words in that bag of tag, words in huffman code
word_count_by_bag_of_tags_huffman = {}

for word, bot in words_huffman_encoded.items():
    word_dict = word_count_by_bag_of_tags_huffman.get(bot, {})
    count = word_dict.get(word, 0.0)
    count += 1.0
    word_dict[word] = count
    word_count_by_bag_of_tags_huffman[bot] = word_dict

# For each bag of tag, calculate the probability of the words in that bag of tag
# Words are in huffman code.
word_prob_per_bot_huffman = {}  # Probability of word in a Bag of Tags. 
for bot, word_dict in word_count_by_bag_of_tags_huffman.items():
    total = sum(word_dict.values())
    for word, count in word_dict.items():
        word_dict[word] = count / total
    word_prob_per_bot_huffman[bot] = word_dict

with open(constants.DATA_PATH % 'word_prob_per_bag_of_tag.hufman', 'w') as fptr:
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
            temp.append(tuple(words[word.lower()]))
    if len(temp) == 0:
        continue
    ugs.append(constants.PAD_SYMBOL)
    ugs.extend(tuple(temp))
    bgs.extend(list(ngrams(tuple(temp), n=2, pad_left=True,
                           pad_right=False,
                           pad_symbol=constants.PAD_SYMBOL)))

fdist_ugs = nltk.FreqDist(ugs)
total_bots = len(fdist_ugs)

all_bgs = set()
for ug1 in fdist_ugs.keys():
    for ug2 in fdist_ugs.keys():
        all_bgs.add((ug1, ug2))

fdist_bgs = nltk.FreqDist(bgs)

# Probability of each bot with frequency 1 or less are made equal.
UNKNOWN_BOTS = {}
for k in all_bgs:
    if fdist_bgs.get(k, 0.0) < 2:
        UNKNOWN_BOTS[k] = 1

# Implement kneser-ney smoothing.

# Total bigrams with frequency greater than 0.
total_bgs_with_frequency_gt_zero = len(fdist_bgs)

# Discount value.
D = 0.75

# Modify the bigram counts by subtracting 0.75 (Refer coursera slides by manning
# on absolute discounting).
for k, v in fdist_bgs.items():
    fdist_bgs[k] = max(v - D, 0)

P_continuation = {}

temp_continuation = {}
for (_, w), c in fdist_bgs.items():
    if c > 0:
        temp_continuation[w] = temp_continuation.get(w, 0) + 1

# Continuation probability (P_continuation).
for k, v in fdist_ugs.items():
    if k == constants.PAD_SYMBOL:
        continue
    P_continuation[k] = temp_continuation.get(k, 0) * 1.0 / total_bgs_with_frequency_gt_zero

temp_prob = 0
for k, v in P_continuation.items():
    if UNKNOWN_BOTS.has_key(k):
        temp_prob += v

for k, v in P_continuation.items():
    if UNKNOWN_BOTS.has_key(k):
        P_continuation[k] = temp_prob


temp_coefficient = {}
for (w, _), c in fdist_bgs.items():
    if c > 0:
        temp_coefficient[w] = temp_coefficient.get(w, 0) + 1

# Interpolation co-efficient.(lambda_coefficient).
lambda_coefficient = {}
for (w, _), v in fdist_bgs.items():
    lambda_coefficient[w] = D * temp_coefficient.get(w, 0) * 1.0 / fdist_ugs[w]



probs_prev = {}
for sample in all_bgs:
    # [(<bag_of_tag_1>, <bag_of_tag_2>)] = Probability of (<bag_of_tag_1>, <bag_of_tag_2>) given <bag_of_tag_1>.
    probs_prev[sample] = (fdist_bgs.get(sample, 0.0) / float(fdist_ugs.get(sample[0]))) + (lambda_coefficient.get(sample[0], 0.0) * P_continuation.get(sample[1], 0.0))


with open(constants.DATA_PATH % 'bag_of_tag_prev.prob', 'w') as fptr:
    fptr.write(cPickle.dumps(probs_prev))



probs_next = {}
for sample, count in fdist_bgs.items():
    # [(<bag_of_tag_1>, <bag_of_tag_2>)] = Probability of (<bag_of_tag_1>, <bag_of_tag_2>) given <bag_of_tag_2>.
    probs_next[sample] = count / float(fdist_ugs.get(sample[1]))


with open(constants.DATA_PATH % 'bag_of_tag_next.prob', 'w') as fptr:
    fptr.write(cPickle.dumps(probs_next))
