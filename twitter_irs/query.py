import json
from sets import Set
from numpy.linalg import linalg
from twitter_irs.indexing import load_index
from twitter_irs.preprocessor import parse_corpus
from twitter_irs.utils import process_txt, process_query

__author__ = 'shaughnfinnerty'



def retrieve_limited_set(query_vector, index):
    '''
    :param query: a query vector
    :param index: an index of terms associated to a list of document maps containing ids w/ term frequencys
    :return: a unique set of document ids w/ no duplicates; these documents contain at least one of the query terms
    '''
    limited_set = Set()
    for term in query_vector:
        document_list = index.get(term, {})
        for doc in document_list.keys():
            limited_set.add(doc)
    return limited_set

def create_document_vectors(query_vector, doc_list, index):
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

def compute_cos_similarity(doc_vector, query_vector):
    return linalg.dot(doc_vector, query_vector)/(linalg.norm(doc_vector)*linalg.norm(query_vector))

def rank_vectors(doc_vectors, query_vector):
    ranked_docs = []
    for id in doc_vectors:
        ranked_docs.append({"id":id, "score": compute_cos_similarity(doc_vectors[id], query_vector)})
    return sorted(ranked_docs, key=lambda doc: doc["score"], reverse=True)

def execute_query(query, tf_idf_index, frequency_index, corpus):
    query_vector, query_freq_vector = process_query(query, frequency_index, len(corpus))
    limited_set = retrieve_limited_set(query_vector,tf_idf_index)
    doc_freq_vectors = create_document_vectors(query_vector, limited_set, tf_idf_index)
    results = rank_vectors(doc_freq_vectors, query_freq_vector)
    return results

# print compute_cos_similarity([9.24123639255446], [(0.5+0.5*1/2)])
