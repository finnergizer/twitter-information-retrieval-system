# In this file we can test the toolkits and functions that we want to use
# -*- coding: utf-8 -*-
from twitter_irs.utils import process_txt


__author__ = 'shaughnfinnerty'

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.lancaster import LancasterStemmer
import csv
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer, TreebankWordTokenizer, PunktSentenceTokenizer, \
    sent_tokenize
import re
from nltk.tokenize.stanford import StanfordTokenizer
from sets import Set
import string
import nltk


def run():
    corpus = open("trec-microblog11.txt")
    stopword_set = set(stopwords.words("english"))
    stemmer = EnglishStemmer()
    plurals = ['loving','caresses', 'flies', 'dies', 'mules', 'denied', 'deny',
               'don\'t',
               'died', 'agree','agreed', 'owned', 'humbled', 'sized',
               'meeting', 'stating', 'siezing', 'itemization',
               'sensational', 'traditional', 'reference', 'colonizer',
               'plotted']

    singles = []
    for plural in plurals:
        singles.append(stemmer.stem(plural))
    print singles


def tokenize():
    words = Set()
    hyperlink_re = re.compile(
        # protocol identifier
        u"(?:(?:https?|ftp)://)"
        # user:pass authentication
        u"(?:\S+(?::\S*)?@)?"
        u"(?:"
        # IP address exclusion
        # private & local networks
        u"(?!(?:10|127)(?:\.\d{1,3}){3})"
        u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
        u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
        u"|"
        # host name
        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        u")"
        # port number
        u"(?::\d{2,5})?"
        # resource path
        u"(?:/\S*)?", re.UNICODE)

    stemmer = EnglishStemmer()
    tokenizer = RegexpTokenizer(u'\w+\'\w+|\w+', False, False, re.UNICODE)
    tokenizer = TreebankWordTokenizer()
    sentence_tokenizer = PunktSentenceTokenizer()
    with open("test.txt") as f:
        for line in f:
            line = hyperlink_re.sub("", line)
            print line
            try:
                for sent in sentence_tokenizer.tokenize(line):
                    for w in tokenizer.tokenize(sent):
                        print w
                        words.add(w)
            except:
                for w in tokenizer.tokenize(line):
                    print w
                    words.add()
    print words

# tokenize()
# print "(" in Set(string.punctuation)
# nltk.download()


# print set(stopwords.words("english"))


def indexing(corpus, tokens):
    """ Creates an inverted index with message id and frequency."""
    inverted_index = {}
    for token in tokens:
        inverted_index[token] = []
        for document in corpus:
            frequency = document["msg"].count(token)
            if frequency > 0:
                inverted_index[token].append({"id": document["id"], "freq": frequency})

    return inverted_index


def indexToFile(index):
    """ Outputs the inverted index to a text file, tab-separated.  Not very readable."""
    with open("index-output.txt", "wb") as f:
        writer = csv.writer(f, delimiter='\t')
        for word in index:
            writer.writerow([word] + [doc for doc in index[word]])

# Just a few random words to test the inverted index with
# indexToFile(indexing(corpus, ["whenever", "attempt", "new", "index"]))
