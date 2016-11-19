from __future__ import print_function, division

import glob, os
from collections import defaultdict
import operator
from datetime import datetime

import jsonlines

def find_latest_run(output_dir):
    dirs = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]
    dirs_datetime = [datetime.strptime(dt, "%Y-%m-%dT%H-%M-%S") for dt in dirs]
    return os.path.join(output_dir, max(dirs_datetime).strftime("%Y-%m-%dT%H-%M-%S"))

if __name__ == '__main__':
    sentiments = defaultdict(int)
    os.chdir(find_latest_run("output"))
    for f in glob.glob("*.jsonl"):
        with jsonlines.open(f) as reader:
            total_docs = 0
            for obj in reader:
                sentiments[obj['field']] += obj['sentiment']
                total_docs += 1
            sentiments[obj['field']] = sentiments[obj['field']] / total_docs

    for k, v in sorted(sentiments.iteritems(), key=operator.itemgetter(1), reverse=True):
        print(k, v)
