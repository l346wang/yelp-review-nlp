
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))

tokens = ['I', 'do', 'not', 'like', 'the', 'movie']
for w in tokens:
    print(w)
    if w not in stopWords and len(w) != 1:
        print(w)