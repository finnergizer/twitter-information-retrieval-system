import codecs
import csv
from sets import Set

import utils

__author__ = 'shaughnfinnerty'

# Parse the corpus text document into a list of dictionaries (each dict having an id and msg)
def parse_corpus(raw=False):
    corpus = {}
    with open("trec-microblog11.txt") as f:

        reader=csv.reader(f,delimiter='\t')
        for id, msg in reader:
            # corpus.append({"id": int(unicode(id, "utf-8-sig")), "msg": msg})
            if raw:
                corpus[int(unicode(id, "utf-8-sig"))] = unicode(msg,errors="replace")
            else:
                corpus[int(unicode(id, "utf-8-sig"))] = utils.process_txt(unicode(msg,errors="replace"))
    return corpus;



def pre_process(corpus):
    corpus_tokens = Set()
    for doc in corpus:
        # for w in utils.process_txt(doc["msg"], True):
        for w in doc["msg"]:
            corpus_tokens.add(w)
    return corpus_tokens


# pre_process()
# with open("tokens.txt", "w") as f:
#     for w in pre_process():
#         f.write(w + "\n")
# print len(pre_process());
