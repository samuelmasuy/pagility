"""
buildindex.py

o   Builds index using SPIMI and compression methods, and block size as a parameter
o   After getting documents from the collection, this module iterates through all documents and collects all (term, docID) pairs
o   Multiple indexes can be generated with different levels of compression
"""

import nltk
import pprint
import argparse
import cPickle as pickle
import os, jsonlines, glob, sys

import filestuff
import spimi
import compress
# import merge
# import query
import ranking
from nltk.corpus import stopwords

####### Memory management ########
memory_size = 1000000000
default_block_size = 1315000  # whole corpus 26.3 MB/10 blocks = 2.63 MB

# good values 2630000-> ~ 5 blocks
#             1315000-> ~9 blocks
#              657500-> ~ 20 blocks

# parse arguments from command-line
# parser = argparse.ArgumentParser(description='build index', add_help=False)
# parser.add_argument("block_size")
# args = parser.parse_args()
#
# if args.block_size:
#     block_size = int(args.block_size)
# else:
#     block_size = default_block_size

block_size = default_block_size

print ("Using block size " + str(block_size))

# STOP LIST
stop_words = ['the', 'and', 'of', 'in', 'a', 'to', 'for', 'on', 'is', 'research', 'with', 'at',
              'j', 'are', 'as', 'students', 'by', 's', 'or', 'that', 'an', 'from', 'm', 'pubmed',
              'science', 'university', 'content', 'be', 'this', 'will']

index = {}

# # add nltk stop words, for a total of 304
# unicode_sw = stopwords.words("english")
# str_sw = [str(sw) for sw in unicode_sw]
# stop_words += str_sw

# get all the .jsonl files and accumulate all term, docID pairs

tokens_list = []
# doc_path = './docs'
# docs, sgm_docID_map = filestuff.get_reuters(doc_path)

os.chdir("../sample_output")
index_file = './blocks/index.txt'

doc_ctr = 0
doc_len_ave = 0
doc_length_dict = {}

all_terms = []

department_doc_count = {}

# loop through docs and accumulate scores

# do for each file in the collection
os.chdir("../sample_output")

for f in glob.glob("*.jsonl"):
    with jsonlines.open(f) as reader:
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
            terms = nltk.word_tokenize(terms)  # tokenize SGM doc to a list
            # ###### COMPRESSION #####
            terms = compress.remove_weird_things(terms)  # 1 remove puntuations, escape characters, etc
            terms = compress.remove_numbers(terms)  # 2 remove numbers
            terms = compress.case_folding(terms)  # 3 convert all to lowercase

            all_terms += terms

            terms = [t for t in terms if t not in stop_words]  # 4  remove stop words
            doc_length = len(terms)
            doc_length_dict[url] = doc_length  # save doc length in a dict
            doc_ctr += 1

            # collect all term,docID pairs to a list
            for term in terms:
                token_obj = {"term": term, "docID": url}
                tokens_list.append(token_obj)

print("N: " + str(doc_ctr))

# stop_words = compress.collect_stop_words(all_terms, 30)
# print("stop words")
# pprint.pprint(stop_words)

### we don't need this if the stop words are already eliminated before even forming the tokens_list
# tokens_list = compress.remove_stop_words(tokens_list, 30)       # 4 remove 30 most common words
# tokens_list = compress.remove_stop_words(tokens_list, 150)        # 5 remove 30 most common words


# doc length array and doc length average
temp_doc_len_sum = 0
for d in doc_length_dict:
    # print(d, ":", doc_length_dict[d])
    temp_doc_len_sum += doc_length_dict[d]

doc_len_ave = temp_doc_len_sum / doc_ctr

# pprint.pprint(tokens_list)
# pprint.pprint(doc_length_dict)


# { 'word': {'http:url1':1, 'http:url2':2 },   'wordy':  {'http:url1':1, 'http:url2':2 }           }

for t in tokens_list:
    _term = t['term']
    _docID = t['docID']

    if _term in index:

        if _docID in index[_term]:
            index[_term][_docID] += 1
        else:
            # postings = {}
            # postings[_docID] = 1
            index[_term][_docID] = 1
    else:
        postings = {}
        postings[_docID] = 1
        index[_term] = postings

pprint.pprint(index)

# save some necessary info for querying

# to save space and computing, only write doc_length_dict to a file
# from which we can derive N and doc_len_ave
# use Pickle for speed

# with open('doc_lengths.p','wb') as fp:
#     pickle.dump(doc_length_dict, fp)
#
#
# ########## SPIMI ####################
# spimi_files = spimi.SPIMI(tokens_list, block_size)
# print(spimi_files)
#
# ########## MERGING ##################
# index_file = spimi.block_merge(spimi_files, index_file)
# #print(index_file)
#
# index, postings_count = filestuff.read_index_into_memory(index_file)
# print("Term count: " + str(len(index)))


# index :

# word = {{'http://www.concordia.ca/artsci/science-college/news/public-lecture-series/past-lectures/core-social-cognition.html': 1}, {'http://www.concordia.ca/artsci/science-college/news/public-lecture-series/past-lectures/core-social-cognition.html': 2}}
