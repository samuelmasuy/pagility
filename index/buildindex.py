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


# STOP LIST - 150
stop_words = ['research', 'students', 'science', 'university', 'c', 'de', 'concordia', 'p', 'program', 'faculty',
              'department', 'environmental', 'student', 'r', 'study', 'course', 'credits', 'b', 'biology', 'h',
              'studies', 'courses', 'graduate', 'new', 'phd', 'urban', 'chemistry', 'k', 'l', 'one', 'may',
              'biol', 'physics', 'g', 'information', 'montreal', 'brain', 'work', 'n', 'amir', 'psychology',
              'canada', 'also', 'development', 'dr', 'journal', 'jaeger', 'environment', 'e', 'health', 'rats',
              'pfaus', 'college', 'human', 'planning', 'sleep', 'use', 'geography', 'transportation', 'clinical',
              'jg', 'la', 'effects', 'programs', 'undergraduate', 'canadian', 'change', 'ecology', 'publications',
              'honours', 'using', 'chem', 'analysis', 'academic', 'conference', 'pm', 'sciences', 'cell', 'professor',
              'degree', 'pp', 'systems', 'behav', 'international', 'year', 'interests', 'teaching', 'msc', 'v', 'life',
              'well', 'time', 'back', 'exercise', 'patterson', 'take', 'top', 'molecular', 'lab', 'role', 'current', 'w',
              'social', 'assessment', 'rat', 'physical', 'system', 'must', 'res', 'sexual', 'engineering', 'pdf', 'et', 'two',
              'climate', 'project', 'education', 'f', 'arts', 'bsc', 'landscape', 'thesis', 'processes', 'public', 'abstract',
              'following', 'association', 'neuroscience', 'full', 'energy', 'training', 'applications', 'areas', 'first',
              'community', 'cognitive', 'people', 'natural', 'montral', 'years', 'including', 'room', 'include', 'impact',
              'field', 'activities', 'november', 'protein', 'data', 'quantum']

# add nltk stop words
unicode_sw = stopwords.words("english")
str_sw = [str(sw) for sw in unicode_sw]
stop_words += str_sw

index = {}

# get all the .jsonl files and accumulate all term, docID pairs

tokens_list = []
docs_dir = "../output_500_itemcount"
index_file = "index.txt"

doc_ctr = 0
doc_len_ave = 0
doc_length_dict = {}
all_terms = []
department_doc_count = {}

# loop through docs and accumulate scores
# do for each file in the collection
# collect tokens

doc_list = []

for f in os.listdir(docs_dir):
    if f.endswith(".jsonl"):
        with jsonlines.open(os.path.join(docs_dir, f)) as reader:
            for obj in reader:
                field = format(obj['field'])
                # url_string = format(obj['url'])
                url_string = format(obj['url'])
                real_url_path = url_string.split("://")[1]
                if real_url_path in doc_list:       # avoid http:// and https:// version of same doc being recorded twice
                    pass
                else:
                    title = format(obj['title'])
                    text = format(obj['text'])
                    url = real_url_path

                    if field in department_doc_count:
                        department_doc_count[field] += 1
                    else:
                        department_doc_count[field] = 1

                    data = title + " " + text
                    terms = data.encode('ascii', 'ignore')
                    terms = nltk.word_tokenize(terms)   # tokenize SGM doc to a list
                    # ###### COMPRESSION #####
                    terms = compress.remove_weird_things(terms)         # 1 remove punctuations, escape characters, etc
                    terms = compress.remove_numbers(terms)              # 2 remove numbers
                    terms = compress.case_folding(terms)                # 3 convert all to lowercase
                    terms = [t for t in terms if t not in stop_words]   # 4  remove stop words

                    all_terms += terms

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
# stop_words = compress.collect_stop_words(all_terms, 150)
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


# get number of non-positional postings
nonp_postings = 0

for _term in index:
    nonp_postings += len(index[_term])

print("Doc length ave: ", doc_len_ave)
print("Index size: ", len(index))
print("Non-positional postings: ", nonp_postings)

