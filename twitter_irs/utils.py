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

def process_txt(txt, stem=True):
    '''
    Processes text by removing stopwords, punctuation, urls and optionally running a stemmer on the text.
    Used to process both documents (tweet bodies) and queries.
    :param txt: a block of text to process
    :param stem: if False, do not run the stemmer when processing text
    :return: A list of words with the aforementioned ones removed
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
    '''
    Processes a query, removing stopwords and doing stemming.  Creates a query vector (list of words in the query)
    and a query frequency vector (a corresponding list of the weight for each word based on frequency)
    :param query: the text of a query
    :param frequency_index: the frequency index for the system, created by the Indexer
    :param corpus_size: the number of words in the corpus
    :return: a tuple containing the query vector  and the query frequency vector
    '''
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
    '''
    Finds the maximum frequency of a term in a document by checking all documents where the term appears
    :param frequency_index: the frequency index created by the Indexer
    :param term: a term to look for frequency of
    :return: the highest frequency the term occurs at across all documents containing the term
    '''
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
    '''
    :param frequency: the frequency of a term in a query or document
    :param max_frequency: the maximum frequency of the term across all documents
    :return: a number representing the frequency of a term compared to its frequency in the entire corpus, or 0 if the term does not appear in the corpus
    '''
    if(max_frequency > 0):
        return float(frequency)/max_frequency
    else:
        return 0

def compute_idf(document_frequency, corpus_size):
    '''
    :param document_frequency: the frequency of a term across the corpus
    :param corpus_size: the size of the corpus
    :return: the idf for the term, or 0 if the term does not appear in the corpus
    '''
    if(document_frequency > 0):
        return log(float(corpus_size)/document_frequency, 2)
    else:
        return 0

def compute_tf_idf_weight(term_frequency, idf):
    '''
    :param term_frequency: the frequency of a term, computed with compute_term_frequency
    :param idf: the idf for a term
    :return: the if-idf weight for a term 
    '''
    return term_frequency*idf




