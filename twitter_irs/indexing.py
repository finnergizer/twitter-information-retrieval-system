import json
from utils import find_max_frequency, compute_term_frequency, compute_idf, compute_tf_idf_weight

__author__ = 'shaughnfinnerty'


class Indexer:
    def __init__(self, corpus_counter=None, tokens=None):
        self.corpus_counter = corpus_counter
        self.tokens = tokens

    def create_frequency_index(self):
        """ Creates an inverted index with hashes using message id as key and frequency as value"""
        inverted_freq_index = {}
        i = 1
        for token in self.tokens:
            inverted_freq_index[token] = {}
            if (i % 1000 == 0):
                print(str(float(i)/len(self.tokens)*100) + "% complete creating frequency index.")
            i = i+1
            for document in self.corpus_counter:
                counter = self.corpus_counter[document]
                freq = counter[token]
                if freq > 0:
                    inverted_freq_index[token].update({document: freq})

        return inverted_freq_index

    def create_frequency_index_optimized(self):
        """ Creates an inverted index with hashes using message id as key and frequency as value"""
        inverted_freq_index = {}
        i = 1
        for document in self.corpus_counter:
            counter = self.corpus_counter[document]
            if (i % 1000 == 0):
                print(str(float(i)/len(self.corpus_counter)*100) + "% complete creating frequency index.")
            for word in counter:
                if len(inverted_freq_index.get(word, {})) == 0:
                    inverted_freq_index[word] = {}
                inverted_freq_index[word].update({document: counter[word]});
            i = i+1
        return inverted_freq_index

    def create_tf_idf_index(self, frequency_index, corpus_size):
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


    def index_to_file(self, index, path):
        """ Outputs the inverted index as JSON to a file"""
        with open(path, "wb") as f:
            f.write(json.dumps(index))

    def load_index(self, path):
        index = {}
        with open(path, "rb") as f:
            index = json.loads(f.read())
        return index;
