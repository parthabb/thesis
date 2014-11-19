"""Read words from the wordnet database and store pos word in file."""

__author__ = 'Partha Baruah (parthabb@gmail.com)'

import json
from nltk.corpus import wordnet as wn

POS = ('noun', 'verb', 'adj', 'adv')
ABBR = {
    'noun': 'n',
    'verb': 'v',
    'adj': 'a',
    'adv': 'r'
}

words = {}
count = 0

for pos in POS:
    with open('dict/index.%s' % pos, 'r') as fptr:
        for line in fptr:
            if line.startswith(' ') or line.startswith('\t'):
                continue
            count += 1
            line.rstrip()
            words[line.split(' %s ' % ABBR[pos], 2)[0]] = words.get(
                line.rsplit(' %s ' % ABBR[pos], 2)[0], set())
            words[line.rsplit(' %s ' % ABBR[pos], 2)[0]].add(pos)


# if word has a '/' then it is replaced by _forwardslash_
for word, pos in words.iteritems():
    fname = word
    if '/' in fname:
        fname = fname.replace('/', '_forwardslash_')
    with open('database_pos/%s_pos.txt' % fname, 'w') as fptr:
        fptr.write(json.dumps({word: list(pos)}))
