"""
buildindex.py

o   Builds index using SPIMI and compression methods, and block size as a parameter
o   After getting documents from the collection, this module iterates through all documents and collects all (term, docID) pairs
o   Multiple indexes can be generated with different levels of compression
"""

import nltk
import pprint
import cPickle as pickle
import os, jsonlines, sys
from collections import OrderedDict
import compress

from nltk.corpus import stopwords


# STOP LIST
stop_words = ['the', 'and', 'of', 'in', 'a', 'to', 'for', 'on', 'is', 'with', 'at',
              'j', 'are', 'as', 'by', 's', 'or', 'that', 'an', 'from', 'm', 'pubmed',
              'content', 'be', 'this', 'will']

# add nltk stop words
unicode_sw = stopwords.words("english")
str_sw = [str(sw) for sw in unicode_sw]
stop_words += str_sw

index = {}

# get all the .jsonl files and accumulate all term, docID pairs

tokens_list = []
docs_dir = "../sample_output"
index_file = "index.txt"

doc_ctr = 0
doc_len_ave = 0
doc_length_dict = {}
all_terms = []
department_doc_count = {}

# loop through docs and accumulate scores
# do for each file in the collection
# collect tokens

for f in os.listdir(docs_dir):
    if f.endswith(".jsonl"):
        with jsonlines.open(os.path.join(docs_dir, f)) as reader:
            for obj in reader:
                field = format(obj['field'])
                url = format(obj['url'])
                title = format(obj['title'])
                text = format(obj['text'])

                if field in department_doc_count:
                    department_doc_count[field] += 1
                else:
                    department_doc_count[field] = 1

                data = title + " " + text
                terms = data.encode('ascii', 'ignore')
                terms = nltk.word_tokenize(terms)   # tokenize SGM doc to a list
                # ###### COMPRESSION #####
                terms = compress.remove_weird_things(terms)         # 1 remove puntuations, escape characters, etc
                terms = compress.remove_numbers(terms)              # 2 remove numbers
                terms = compress.case_folding(terms)                # 3 convert all to lowercase
                terms = [t for t in terms if t not in stop_words]   # 4  remove stop words

                terms = compress.snowball_stemmer(terms)            # 5 stem words

                doc_length = len(terms)
                doc_length_dict[url] = doc_length                   # save doc length in a dict
                doc_ctr += 1

                # collect all term,docID pairs to a list
                for term in terms:
                    token_obj = {"term": term, "docID": url}
                    tokens_list.append(token_obj)

print("N: " + str(doc_ctr))

# do only once to get stop words list -----------------------------
# stop_words = compress.collect_stop_words(all_terms, 30)
# print("stop words")
# pprint.pprint(stop_words)
# -----------------------------------------------------------------
# pprint.pprint(tokens_list)

# index sample
# { 'word': {'http:url1':1, 'http:url2':2 },   'wordy':  {'http:url1':1, 'http:url2':2 }    }

# build simple inverted index
for t in tokens_list:
    _term = t['term']
    _docID = t['docID']

    if _term in index:

        if _docID in index[_term]:
            index[_term][_docID] += 1
        else:
            index[_term][_docID] = 1
    else:
        postings = {}
        postings[_docID] = 1
        index[_term] = postings

# pprint.pprint(index)
# pprint.pprint(department_doc_count)
# pprint.pprint(doc_length_dict)

# print index to file
with open(index_file, "w") as out_file:
    for _term in index:
        out_file.write(_term + "->" + str(index[_term]) + "\n")

# doc length array and doc length average
temp_doc_len_sum = 0
for d in doc_length_dict:
    # print(d, ":", doc_length_dict[d])
    temp_doc_len_sum += doc_length_dict[d]

doc_len_ave = temp_doc_len_sum /doc_ctr

# save some necessary info for querying
# to save space and computing, only write doc_length_dict to a file
# from which we can derive N and doc_len_ave
# use Pickle for speed

with open('doc_lengths.p','wb') as fp:
    pickle.dump(doc_length_dict, fp)


print("Doc length ave: ", doc_len_ave)
