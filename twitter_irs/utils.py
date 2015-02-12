from collections import Counter
from math import log
import re
import string
from nltk import TreebankWordTokenizer, sent_tokenize
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

tokenizer = TreebankWordTokenizer()

stopword_set = set(stopwords.words("english"))
punctuation_set = set(string.punctuation)

stemmer = EnglishStemmer()

# remove URLs, punctuation, stopwords, and stem
def process_txt(txt, stem=True):
    '''
    :param txt:
    :param stem:
    :return:
    '''
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

def process_query(query, frequency_index, corpus_size):
    formatted_query = process_txt(query);
    word_counter = Counter(formatted_query);
    vector = []
    freq_vector = []
    for key in word_counter:
        vector.append(key)
        max_freq = find_max_frequency(frequency_index,key);
        term_freq = compute_term_frequency(word_counter[key], max_freq)
        idf = compute_idf(len(frequency_index.get(key, [])), corpus_size)
        query_term_weight = (0.5 + 0.5*term_freq)*idf
        freq_vector.append(query_term_weight)
    return (vector, freq_vector)

def find_max_frequency(frequency_index, term):
    doc_list = frequency_index.get(term, {})
    if len(doc_list) > 0:
        freq = 0
        for doc in doc_list:
            if doc_list[doc] > freq:
                freq = doc_list[doc]
    else:
        freq = 0
    return freq

def compute_term_frequency(frequency, max_frequency):
    if(max_frequency > 0):
        return float(frequency)/max_frequency
    else:
        return 0

def compute_idf(document_frequency, corpus_size):
    if(document_frequency > 0):
        return log(float(corpus_size)/document_frequency, 2)
    else:
        return 0

def compute_tf_idf_weight(term_frequency, idf):
    return term_frequency*idf




