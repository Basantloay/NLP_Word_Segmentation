#import wordninja


words = open("test.txt").read()
newwords=list()
print(words)

#print(maxword)
#print(wordninja.split("thelongestlistofthelongeststuffatthelongestdomainnameatlonglast.com"))
str=""
for i in words:
    str=str+i
    print(str)
    if len(str)!=1 & str.isalpha():
        newwords.append(str)
        str='\0'

print(newwords)
