import functools
import math

# ############################ class pdis ##################################
class Pdist(dict):
    # probability distribution estimated from counts in datafile
    # N = 1024908267229 ## Number of tokens in corpus
    def __init__(self, dictionary, N=None, missingfn=None):
        for key, frequency in dictionary.items():
            # print(self.get(key, 0))
            self[key] = self.get(key, 0) + float(frequency)
            self.N = float(N or sum(self.itervalues()))
            self.missingfn = missingfn or (lambda k, N: 1. / N)

    def __call__(self, key):
        if key in self:
            return self[key] / self.N
        else:
            return self.missingfn(key, self.N)


def avoid_long_words(word, N):
    "Estimate the probability of an unknown word."
    return 10. / (N * 10 ** len(word))


# ############################ Unigram #####################################
"""
 File count_1w.txt is taken from http://norvig.com/ngrams/count_1w.txt that represents frequency of  common unigram words
"""
unigrams = dict()

file = open("count_1w.txt", "r")
lines = file.readlines()
for line in lines:
    if line != "\n" or line != '':
        k, v = line.rstrip().split('\t')
        line = line.partition('\t')
        str = line[2].partition("\n")
        unigrams[line[0]] = float(str[0])

file.close()
# print(unigrams)
N = 1024908267229  ## Number of tokens in corpus
pdis_unigrams = Pdist(unigrams, N, avoid_long_words)

# ############################ bigram #####################################
"""
 File count_2w.txt is taken from http://norvig.com/ngrams/count_2w.txt that represents frequency of  common bigram words
"""
bigrams = dict()
file = open("count_2w.txt", "r")
lines = file.readlines()
for line in lines:
    if line != "\n" or line != '':
        line = line.partition('\t')
        str = line[2].partition("\n")
        bigrams[line[0]] = float(str[0])
file.close()
N = 1024908267229  ## Number of tokens in corpus
pdis_bigrams = Pdist(bigrams, N, avoid_long_words)


# print(bigrams)


# ########################### Conditional probability #####################################

def conitionalprobablity(word, prev):
    try:
        return pdis_bigrams[prev + ' ' + word] / float(pdis_unigrams[prev])
    except KeyError:
        return pdis_bigrams(word)


# ####################### cost #################################
def cost(string, prev='<S>'):
    if string == "" or not string:
        return 0.0, []
    return math.log10(conitionalprobablity(string, prev))


# ##################### using viterbi algorithm ##########################################
@functools.lru_cache(maxsize=2 ** 10)
def spacing(str, remainstr='<S>'):
    L = 20
    if str == "":
        return 0.0, []
    else:
        length = min(L, len(str))
        list1 = []
        for i in range(length):
            list1.append((str[0:i + 1], str[i + 1:len(str)]))
        # print(list1)
        candidates = []
        for left, right in list1:
            coststr = cost(left,remainstr)
            costright, right = spacing(right, left)

            candidates.append((coststr + costright, [left] + right))

        return max(candidates)

text = open("test.txt").read()
result = list(spacing(text))
result.remove(result.__getitem__(0))
for items in result:
    print(*items)
