import re
import string
from nltk import RegexpTokenizer, TreebankWordTokenizer, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer

__author__ = 'shaughnfinnerty'

url_regex = re.compile(
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

# punctuation_tokenizer = RegexpTokenizer(u'\w+\'\w+|\w+')
tokenizer = TreebankWordTokenizer()

stopword_set = set(stopwords.words("english"))
punctuation_set = set(string.punctuation)

stemmer = EnglishStemmer()

# remove URLs, punctuation, stopwords, and stem
def process_txt(txt, stem=True):
    words = []
    txt_stripped = url_regex.sub("", txt)
    try:
        for sentence in sent_tokenize(txt_stripped):
            for w in tokenizer.tokenize(sentence):
                w_lower = w.lower()
                if w_lower not in stopword_set and w_lower not in punctuation_set:
                    if stem:
                        try:
                            words.append(stemmer.stem(w_lower))
                        except:
                            words.append(w_lower)
                    else:
                        words.append(w_lower)

    except:
        for w in tokenizer.tokenize(txt_stripped):
            w_lower = w.lower()
            if w_lower not in stopword_set and w_lower not in punctuation_set:
                if stem:
                    try:
                        words.append(stemmer.stem(w_lower))
                    except:
                        words.append(w_lower)
                else:
                    words.append(w_lower)
    return words
