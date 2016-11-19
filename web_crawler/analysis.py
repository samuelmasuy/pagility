from __future__ import print_function, division

import glob, os
from collections import defaultdict
import operator

import jsonlines

if __name__ == '__main__':
    sentiments = defaultdict(int)
    os.chdir("output")
    for f in glob.glob("*.jsonl"):
        with jsonlines.open(f) as reader:
            total_docs = 0
            for obj in reader:
                sentiments[obj['field']] += obj['sentiment']
                total_docs += 1
            sentiments[obj['field']] = sentiments[obj['field']] / total_docs

    for k, v in sorted(sentiments.iteritems(), key=operator.itemgetter(1), reverse=True):
        print(k, v)
