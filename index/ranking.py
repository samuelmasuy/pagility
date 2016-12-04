"""
ranking

ranks the gathered documents using BM25 algorithm
BM25 provides a rank for each document (RSVd) based on the terms in the query

overview: RSVd = idf * tftd_len.norm

idf : inverse document frequency, which attenuates effect of terms that occur too often
tftd : term frequency with length normalization that depends on 2 constants

k - positive tuning parameter that calibrates term frequency scaling
b - tuning parameter for document length

If a term occurs in over half the documents in the collecction, this formula would not
give a negative weight, which is desirable.

"""

import math
import operator
import pprint

"""
get_rvsd

calculates RSV for each document, aggregate in a RSV dictionary

inputs:
q - query string
docs - docs which are the result of the query
N - number of docs in the colletion
doc_length_dict - doc. lengths in a dictionary data structure
Lave - average length of all documents
k - positive tuning parameter that calibrates tftd scaling
b - tuning parameter for document length

"""

def get_rsvd(q, docs, N, doc_length_dict, Lave, k, b, index, j):
    # print "Doc length avg: ", Lave
    RSVd = {}

    terms = q.split()

    # this simply discards v in each k:v  [{'21004': 1}, {'21005': 1}] -> ['21004','21005']
    try:
        # docs_list = list({key for d in docs for key in d.keys()})
        docs_list = docs.keys()
    except:
        docs_list = docs

    for d in docs_list:
        Ld = doc_length_dict[d]

        # calculate RSV for this document
        tf_idf_sum = 0  # init. tf_idf sum to 0

        for t in terms:
            try:  # if term not found in dictionary, dft will be 0 so just skip so
                postings = index[t]  # this term wont contribute to the score of this document
            except KeyError:
                postings = {}
                continue
            dft = len(postings)
            tftd = 0
            # print("postings of ", t)
            # pprint.pprint(postings)

            # get tftd
            for doc in postings:
                # print "postings:"
                # print doc, ':', postings[doc]
                # print "docID", d
                if doc == d:
                    tftd = postings[doc]

            # print d, ':' , t, " DFT: " + str(dft), " TFTD: " + str(tftd)

            # BM2 formula
            idf = (math.log10(N / dft))
            tftd_norm = ((k + 1) * tftd) / ((k * ((1 - b) + (b * (Ld / Lave)))) + tftd)
            tf_idf = idf * tftd_norm
            tf_idf_sum += tf_idf

        RSVd[d] = tf_idf_sum

    # get top values
    top_j = dict(sorted(RSVd.iteritems(), key=operator.itemgetter(1), reverse=True)[:j])

    return top_j
