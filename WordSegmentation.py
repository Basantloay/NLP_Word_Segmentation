import math
import functools

# ##############################################################
# all numbers and constants taken from http://norvig.com/ngrams/ch14.pdf

# ############################ Unigram #####################################
"""
 File count_1w.txt is taken from http://norvig.com/ngrams/count_1w.txt that represents frequency of common unigram words
"""
unigrams = dict()

file = open("count_1w.txt", "r")
lines = file.readlines()
for line in lines:
    if line != "\n" or line != '':
        line = line.partition('\t')
        str = line[2].partition("\n")
        unigrams[line[0]] = float(str[0])

file.close()
# print(unigrams)
N = 1024908267229  ## Number of tokens in corpus
unigram_probability = dict()
for word, frequency in unigrams.items():
    unigram_probability[word] = frequency / N
# ############################ bigram #####################################
"""
 File count_2w.txt is taken from http://norvig.com/ngrams/count_2w.txt that represents frequency of common bigram words
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
bigram_probability = dict()
for word, frequency in bigrams.items():
    bigram_probability[word] = frequency / N


# print(bigrams)


# ########################### Unigram and Bigram probability (conditional probability) #################################

def UniBigramprob(word, prev):
    try:
        return bigram_probability[prev + ' ' + word] / float(unigram_probability[prev])
    except KeyError:
        if word in unigram_probability:
            return unigram_probability[word]
        else:
            return 10. / (N * 10 ** len(word))


# ####################### cost #################################
def cost(string, prev):
    if str == "" or not str:
        return 0.0
    return math.log10(UniBigramprob(string, prev))


# ##################### spacing using viterbi algorithm ##########################################
@functools.lru_cache(maxsize=None)
def spacing(str, remainstr='<S>'):
    L = 20
    if str == "" or not str:
        return 0.0, []
    list1 = []
    length = min(L, len(str))
    for i in range(length):
        list1.append((str[0:i + 1], str[i + 1:len(str)]))
    # print(list1)
    candidates = []
    for left, right in list1:
        coststr = cost(left, remainstr)
        costright, right = spacing(right, left)

        candidates.append((coststr + costright, [left] + right))

    return max(candidates)

# ##################### remove first element (cost) and calculate accuracy ##########################################

def slice_result(original,string):
    result = list(spacing(string))
    result.remove(result.__getitem__(0))
    print("The Output List : ",*result)
    listresult=result[0]
    list_difference = []

    for item in original:
        if item not in listresult:
            #print(item)
            list_difference.append(item)

    return (len(original)-len(list_difference))*100/len(original),listresult

# ##################### calling function ##########################################
#text = open("test.txt").read()
#slice_result(text)
#slice_result("faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun")
