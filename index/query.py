"""
query

parameters:
[-k k]      [k value for BM25 algorithm]
[-b b]      [value for BM25 algorithm]
[-q query] 

if no k,b passed, defaults will be used

o   Allows user to run one query by passing a query as a parameter, 
or running the script without parameters which loops to accept and process queries

o   Involves creating a QueryObject that holds the index loaded from memory. 
This improves performance if program is ran interactively (loop), because the index is loaded once to memory, 
and can be used to process queries until user stops program

"""

import argparse
import cPickle as pickle
import pprint
# import string
from nltk.corpus import stopwords


import filestuff
import ranking

from nltk.stem import *

# index_path = './blocks/index.txt'
index_path = './index.txt'


stem = True

class QueryObject:

    def __init__(self, index_file):
        self.index, self.postings_count = filestuff.read_index_into_memory(index_file)


    @staticmethod
    def query_rank(index, term_list):
        #--> pprint.pprint(term_list)

        if len(term_list) >1:
            # get postings of first term
            try:
                # e.g. student={u'https://www.concordia.ca/artsci/science-college/about/lenny.html': 1}
                temp_postings_LoD = index[term_list[0]]       # initialize with first term's docs
                # pprint.pprint(temp_postings_DoD)
                # this simply discards v in each k:v  [{'http://url1': 1}, {'http://url2': 1}] -> ['http://url1','http://url2']
                temp_postings = temp_postings_LoD.keys()
                # print(temp_postings)
            except KeyError:
                temp_postings = list()

            or_postings = temp_postings  

            # print(term_list)
            for t in term_list:
                try:
                    temp_term_LoD = index[t]    # [{'21004': 1}, {'21005': 1}]
                    # this simply discards v in each k:v  [{'21004': 1}, {'21005': 1}] -> ['21004','21005']
                    # temp_term = list({k for d in temp_term_LoD for k in d.keys()})
                    temp_term = temp_term_LoD.keys()
                except KeyError:
                    temp_term = list()

                or_postings = list(set(or_postings) | set(temp_term))

            return or_postings

        else:
            try:
                result = index[term_list[0]]
            except KeyError:
                result = list()
            return result

    def run_ranked_query(self, query):
        index = self.index
        q_terms = query.split() 

        err = ''
        try:
            result = QueryObject.query_rank(index, q_terms)       
        except KeyError:
            result = list()
            err = "no documents found"
        return result, err


"""
compress_query

remove weird things
remove numbers
case-fold
remove stop-words 
"""
def compress_query(q_string):

    # STOP LIST- 150

    stop_words = ['research', 'students', 'science', 'university', 'c', 'de', 'concordia', 'p', 'program', 'faculty',
                  'department', 'environmental', 'student', 'r', 'study', 'course', 'credits', 'b', 'biology', 'h',
                  'studies', 'courses', 'graduate', 'new', 'phd', 'urban', 'chemistry', 'k', 'l', 'one', 'may',
                  'biol', 'physics', 'g', 'information', 'montreal', 'brain', 'work', 'n', 'amir', 'psychology',
                  'canada', 'also', 'development', 'dr', 'journal', 'jaeger', 'environment', 'e', 'health', 'rats',
                  'pfaus', 'college', 'human', 'planning', 'sleep', 'use', 'geography', 'transportation', 'clinical',
                  'jg', 'la', 'effects', 'programs', 'undergraduate', 'canadian', 'change', 'ecology', 'publications',
                  'honours', 'using', 'chem', 'analysis', 'academic', 'conference', 'pm', 'sciences', 'cell',
                  'professor', 'degree', 'pp', 'systems', 'behav', 'international', 'year', 'interests', 'teaching', 'msc', 'v',
                  'life', 'well', 'time', 'back', 'exercise', 'patterson', 'take', 'top', 'molecular', 'lab', 'role', 'current',
                  'w', 'social', 'assessment', 'rat', 'physical', 'system', 'must', 'res', 'sexual', 'engineering', 'pdf',
                  'et', 'two', 'climate', 'project', 'education', 'f', 'arts', 'bsc', 'landscape', 'thesis', 'processes', 'public',
                  'abstract', 'following', 'association', 'neuroscience', 'full', 'energy', 'training', 'applications', 'areas',
                  'first', 'community', 'cognitive', 'people', 'natural', 'montral', 'years', 'including', 'room', 'include',
                  'impact', 'field', 'activities', 'november', 'protein', 'data', 'quantum']

    # stemmer = SnowballStemmer("english")
    stemmer = PorterStemmer()

    # add nltk stop words, for a total of 304
    stop_words += set(stopwords.words("english"))

    punctuations = '!?"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'             # remove punctuations and weird things in query terms

    temp = q_string.split()
    removed_stop_words = []

    q_string_list = []
    for t in temp:
        t = t.translate(None, punctuations)  # remove punctuations

        if t in stop_words:
            removed_stop_words.append(t)

        if not t.isdigit() and t not in stop_words:
            t = t.lower()                                       # case-fold
            if stem:
                t = stemmer.stem(t)                                 # stem
            q_string_list.append(t)

    q_string = " ".join(q_string_list)
    if len(removed_stop_words) > 0:
        print("Removed stop words: ", removed_stop_words)
    if stem:
        print("stemmed: ", q_string_list)


    return q_string


def get_query_results(q_string, q_object):
    # q1= QueryObject('./blocks/index.txt')
    # result, err = q_object.run_query(q_string)

    result, err = q_object.run_ranked_query(q_string)

    # print(q + '->')
    if len(result):
        return result
    else:
        print(err)
        return err

# MAIN
############# QUERY ######################
parser = argparse.ArgumentParser(description='query', add_help=False)
parser.add_argument("-q", "--query")
parser.add_argument("-k", "--k")
parser.add_argument("-b", "--b")
parser.add_argument("-t", "--top")
args = parser.parse_args()

# load document lengths used for ranking
with open('doc_lengths.p', 'rb') as fp:
    doc_length_dict = pickle.load(fp)

N = len(doc_length_dict) 

### print "N: ", N

# get Lave (document length average)
temp_doc_len_sum = 0
for d in doc_length_dict:
    # print(d, ":", doc_length_dict[d])
    temp_doc_len_sum += doc_length_dict[d]

doc_len_ave = temp_doc_len_sum /  N

### print "Doc length avg: ", doc_len_ave

# if query passed as argument, run query
# otherwise, loop to allow user to run queries

if args.k:
    k = float(args.k)
else:
    k = 0.5

if args.b:
    b = float(args.b)
else:
    b = 0.5

if args.top:
    t = int(args.top)
else:
    t = 10

if args.query:
    run_forever = False
else:
    run_forever = True


q1 = QueryObject(index_path)
while True:
    print("Enter query:")
    _q_string = raw_input(">")
    try:
        # query.prepare_query(q)
        _q_string = compress_query(_q_string)
        doc_results = get_query_results(_q_string, q1)
        results_count = len(doc_results)
        # print("results")
        # print(doc_results)
        # k = 1
        # b = 0.5
        RSVd = ranking.get_rsvd(_q_string, doc_results, N, doc_length_dict, doc_len_ave, k, b, q1.index, t)
        # sort results by the ranking
        top_docs = sorted(RSVd, key=RSVd.__getitem__, reverse=True)

        if results_count > 0:
            print str(results_count) + " found "
            if results_count < t:
                print "Displaying top", results_count, ":"
            else:
                print "Displaying top", t, ":"
            for doc in top_docs:
                # print("{:<60} : {:<15}".format(doc, RSVd[doc]))
                print("%-85s : %-15s" % (doc, str(RSVd[doc])))
        else:
            print("No results found")
    except:
        print("No results found")

    print("----------------")
    if run_forever == False:
        break