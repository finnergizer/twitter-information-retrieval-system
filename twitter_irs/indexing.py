from collections import Counter
from twitter_irs.preprocessor import pre_process, parse_corpus
import twitter_irs.utils
import json
from twitter_irs.utils import find_max_frequency, compute_term_frequency, compute_idf, compute_tf_idf_weight

__author__ = 'shaughnfinnerty'


def corpus_counter(corpus):
    corpus_counter = []
    for doc in corpus:
        corpus_counter.append({"id": doc["id"], "msg_counter": Counter(doc["msg"])})
    return corpus_counter

def create_frequency_index(corpus_counter, tokens):
    """ Creates an inverted index with hashes using message id as key and frequency as value"""
    inverted_index = {}
    i=1
    for token in tokens:
        inverted_index[token] = {}
        if (i % 1000 == 0):
            print(str(float(i)/len(tokens)*100) + "% Complete Creating Frequency Index")
            with open("index/index-output"+str(i)+".txt", "w") as f:
                f.write(json.dumps(inverted_index))
        i=i+1
        for document in corpus_counter:
            # msg_tokens = process_txt(document["msg"])
            counter = document["msg_counter"]
            freq = counter[token]
            if freq > 0:
                # inverted_index[token].append({"id": document["id"], "freq": freq})
                inverted_index[token].update({document["id"]: freq})

    return inverted_index

def create_tf_idf_index(frequency_index, corpus_size):
    tf_idf_index = frequency_index
    for term in tf_idf_index:
        max_frequency = find_max_frequency(frequency_index, term)
        doc_list = frequency_index[term]
        doc_frequency = len(doc_list)
        idf = compute_idf(doc_frequency, corpus_size)
        for id in doc_list:
            term_frequency = compute_term_frequency(doc_list[id], max_frequency)
            tf_idf_weight = compute_tf_idf_weight(term_frequency, idf)
            doc_list[id] = tf_idf_weight
    return tf_idf_index


def index_to_file(index, path):
    """ Outputs the inverted index to a text file, tab-separated.  Not very readable."""
    with open(path, "wb") as f:
        f.write(json.dumps(index))

def load_index(path):
    index = {}
    with open(path, "rb") as f:
        index = json.loads(f.read())
    return index;
#

# #Creating the index... Will need to package this more gracefully in a function
# corpus = parse_corpus();
# print len(parse_corpus())
# frequency_index = loadIndex("frequency-index.txt")
# print "freq index loaded"
# tf_idf_index = create_tf_idf_index(frequency_index,45389)
# print "print tf-idf-index created"
# indexToFile(tf_idf_index, "tf-idf-index.txt")
# print len(corpus)
# tokens = pre_process(corpus);
# print "tokens created";
#
# corpus_counter = corpus_counter(corpus);
# print "created corpus_counter" + str(len(corpus_counter))
# index = indexing(corpus_counter, tokens);
# print "index created"
# indexToFile(index)
# print "index saved"

