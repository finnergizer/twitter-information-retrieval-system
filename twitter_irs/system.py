from twitter_irs.indexing import load_index, corpus_counter, create_frequency_index, index_to_file, create_tf_idf_index, \
    load_index
from twitter_irs.preprocessor import parse_corpus, pre_process
from twitter_irs.query import retrieve_limited_set, create_document_vectors, rank_vectors, execute_query
from twitter_irs.utils import process_query
from xml.etree import ElementTree

__author__ = 'shaughnfinnerty'




def test_system(run_name, tf_idf_index, frequency_index, corpus):
    query_tree = ElementTree.parse("topics_MB1-50.xml")
    with open("results.txt", 'wb') as f:
        for child in query_tree.getroot():
            query_results = execute_query(child[1].text, tf_idf_index, frequency_index, corpus)
            for i in range(len(query_results)):
                if i >= 1000:
                    break
                print_out = child[0].text + "\t" + "Q0" + "\t" + query_results[i].get("id") + "\t" + str(i+1) + "\t" + \
                            str(query_results[i].get("score")) + "\t" + run_name + "\n"
                f.write(print_out)
            f.write("====================================================================\n")


def run(createIndex=False):
    corpus = {}
    frequency_index = {}
    tf_idf_index = {}
    if createIndex:
        c_counter = []
        tokens = []
        corpus = parse_corpus()
        c_counter = corpus_counter(corpus)
        tokens = pre_process(corpus)
        frequency_index = create_frequency_index(c_counter, tokens)
        index_to_file(frequency_index, "frequency-index.txt")
        tf_idf_idx = create_tf_idf_index(frequency_index, len(corpus))
        index_to_file(tf_idf_index, "tf-idf-index.txt")
    else:
        corpus = parse_corpus(True)
        frequency_index = load_index("frequency-index.txt")
        tf_idf_index = load_index("tf-idf-index.txt")

    test_system("myRun", tf_idf_index, frequency_index, corpus)

run()