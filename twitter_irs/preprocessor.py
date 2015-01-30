__author__ = 'shaughnfinnerty'
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv

# Parse the corpus text document into a list of dictionaries (each dict having an id and msg)
def parse_corpus():
    corpus = []
    with open("trec-microblog11.txt") as f:
         reader=csv.reader(f,delimiter='\t')
         for id, msg in reader:
             corpus.append({"id": int(unicode(id, "utf-8-sig")), "msg": msg})
    return corpus;

def pre_process():
    corpus = open("test.txt")
    stopword_set = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    unstemmed = []
    for line in corpus:
        for w in line.split():
            w_lower = w.lower()
            if w_lower not in stopword_set:
                unstemmed.append(w_lower)

    print(unstemmed)

# pre_process();
print parse_corpus();
# print set(stopwords.words("english"))
