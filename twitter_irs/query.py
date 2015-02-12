from sets import Set
from numpy.linalg import linalg
from utils import process_query

__author__ = 'shaughnfinnerty'


class Query:

    def __init__(self, frequency_index, tf_idf_index, corpus):
        self.frequency_index = frequency_index
        self.tf_idf_index = tf_idf_index
        self.corpus = corpus
        self.corpus_size = len(corpus)

    def retrieve_limited_set(self, query_vector, index):
        '''
        :param query_vector: a query vector
        :param index: an index of terms associated to a list of document maps containing ids w/ term frequencys
        :return: a unique set of document ids w/ no duplicates; these documents contain at least one of the query terms
        '''
        limited_set = Set()
        for term in query_vector:
            document_list = index.get(term, {})
            for doc in document_list.keys():
                limited_set.add(doc)
        return limited_set

    def create_document_vectors(self, query_vector, doc_list, index):
        '''
        :param query_vector: a query vector
        :param doc_list: a set of document ids for documents containing at least one query term
        :param index: an index of terms associated to a list of document maps containing ids w/ term frequencys
        :return: the document frequency vectors for the query
        '''
        doc_vectors = {}
        for doc_id in doc_list:
            doc_vectors[doc_id]=[]
        i = 0
        for term in query_vector:
            term_list = index.get(term,{})
            for doc_id in doc_list:
                doc_vectors[doc_id].insert(i, term_list.get(doc_id,0))
            i = i + 1;
        return doc_vectors

    def compute_cos_similarity(self, doc_vector, query_vector):
        '''
        Uses the dot produt to compute cosine similarity between vectors
        :param doc_vector: a document vector
        :param query_vector: a query vector
        :return: the cosine similarity between the document and query vectors
        '''
        return linalg.dot(doc_vector, query_vector)/(linalg.norm(doc_vector)*linalg.norm(query_vector))

    def rank_vectors(self, doc_vectors, query_vector):
        '''
        Ranks document vectors by sorting them based on cosine similarity to a query vector
        :param doc_vectors: the document vectors hashed by id
        :param query_vector: a query vector
        :return: a sorted list of docs ranked by cosine similarity
        '''
        ranked_docs = []
        for id in doc_vectors:
            ranked_docs.append({"id":id, "score": self.compute_cos_similarity(doc_vectors[id], query_vector)})
        return sorted(ranked_docs, key=lambda doc: doc["score"], reverse=True)

    def execute_query(self, query):
        '''
        Executes the query.  Processes it to deal with stemming and stopwords, and creates a query vector and frequency vector.
        Creates document frequency vectors for all documents containing at least one word from the query, then ranks these
        documents based on cosine similarity with the query frequency vector.
        :param query: The text of a query.
        :return: A list of all documents matching at least one word from the query, sorted and ranked by cosine similarity.
        '''
        query_vector, query_freq_vector = process_query(query, self.frequency_index, self.corpus_size)
        limited_set = self.retrieve_limited_set(query_vector, self.tf_idf_index)
        doc_freq_vectors = self.create_document_vectors(query_vector, limited_set, self.tf_idf_index)
        results = self.rank_vectors(doc_freq_vectors, query_freq_vector)
        return results


