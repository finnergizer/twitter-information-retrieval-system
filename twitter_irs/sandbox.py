# In this file we can test the toolkits and functions that we want to use
__author__ = 'shaughnfinnerty'

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import csv

def run():
    corpus = open("trec-microblog11.txt")
    stopword_set = set(stopwords.words("english"))
    stemmer = PorterStemmer("english")

    # plurals = ['caresses', 'flies', 'dies', 'mules', 'denied',
    #            'died', 'agreed', 'owned', 'humbled', 'sized',
    #            'meeting', 'stating', 'siezing', 'itemization',
    #            'sensational', 'traditional', 'reference', 'colonizer',
    #            'plotted']

    singles = []
    for plural in plurals:
        singles.append(stemmer.stem(plural))
    print singles

    # for line in corpus:
    #     for w in line.split():
    #         if w.lower() not in stopword_set:
    #             print w
#Parse the corpus text document into a list of dictionaries (each dict having an id and msg)
corpus = []

with open("trec-microblog11.txt") as f:
     reader=csv.reader(f,delimiter='\t')
     for id, msg in reader:
         corpus.append({"id": id, "msg": msg})
# print set(stopwords.words("english"))
