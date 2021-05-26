# import wordninja
from nltk.corpus import wordnet

textwords = open("test.txt").read()
newwords = list()
print(textwords)

# print(maxword)
# print(wordninja.split("thelongestlistofthelongeststuffatthelongestdomainnameatlonglast.com"))
str = ""
for i in textwords:
    str = str + i
    print(str)

    if wordnet.synsets(str):
        newwords.append(str)
        str = ''
print(newwords)
