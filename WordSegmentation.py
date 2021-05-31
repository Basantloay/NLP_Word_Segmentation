import math

import functools
from math import log

# load all dictionary words
word_dictionary = set((open("words.txt").read().split()))
# print('true' in word_dictionary)
text = open("test.txt").read()

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
# words = open("words-by-frequency.txt").read().split()
wordcost = dict((k, log((i + 1) * log(len(word_dictionary)))) for i, k in enumerate(word_dictionary))
maxword = max(len(x) for x in word_dictionary)
# ##########################################################################
DBvector = dict()  # for memoization key for unspaced string and value for spaced string

# ############################ Unigram #####################################
unigrams = dict()
file = open("unigram.txt", "r")
lines = file.readlines()
for line in lines:
    if line != "\n" or line != '':
        line = line.partition('\t')
        str = line[2].partition("\n")
        unigrams[line[0]] = float(str[0])

# print(unigrams)

# ############################ bigram #####################################
bigrams = dict()
file = open("bigram.txt", "r")
lines = file.readlines()
for line in lines:
    if line != "\n" or line != '':
        line = line.partition('\t')
        str = line[2].partition("\n")
        bigrams[line[0]] = float(str[0])


# print(bigrams)

# ########################### cost #########################################

def get_cost_unigram(str):
    cost = 0.0
    if str in unigrams:
        cost = math.log10(unigrams[str])
    return cost


def get_cost_bigram(str1, str2):
    cost = 0.0
    str = str1 + " " + str2
    if str in bigrams:
        cost = math.log10((bigrams[str] / unigrams[str2]))
    return cost


def conditionalProb(word_curr, word_prev):
    ### Conditional probability of current word given the previous word.
    try:
        return bigrams[word_prev + ' ' + word_curr]*len(str)/unigrams[word_prev]
    except KeyError:
        if word_curr in unigrams:
            return unigrams[word_curr]*len(str)
        else :
            return 0.0000000000000000001

# using viterbi algorithm
@functools.lru_cache(maxsize=2**10)
def spacing(str, remainstr='<S>'):
    L = 20
    if str == "":
        return 0.0, []
    else:
        length = min(L, len(str))
        list1 = []
        j = 0
        list1 = [(str[:i + 1], str[i + 1:]) for i in range(length)]
        #print(list1)
        candidates = []
        for left, right in list1:
            cost = math.log10(conditionalProb(left, remainstr))
            costright, right = spacing(right, left)

            candidates.append((cost + costright, [left] + right))

        return max(candidates)


print((spacing(text)))


def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        return min((c + wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s) + 1):
        c, k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i - k:i])
        i -= k

    return " ".join(reversed(out))


print(infer_spaces(text))
