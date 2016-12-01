from __future__ import print_function

import glob, os
import sys
import jsonlines

from afinn import Afinn
afinn = Afinn()

"""
get_score

for now, just return length
we're supposed to do sentiment analysis here and return the text's score
"""
def get_score(title, text):

    # title_score = afinn.score(title)
    text_score = afinn.score(text)
    # sum_score = title_score + text_score
    print(title,text)
    print(":", text_score)
    return text_score


PYTHONIOENCODING="UTF-8"
# reload(sys)
# sys.setdefaultencoding("utf-8")

os.chdir("../sample_output")

# for f in glob.glob("*.jsonl"):
#     with jsonlines.open(f) as reader:
#         for obj in reader:
#             # WARNING: The string in obj are encoded with unicode.
#             print(u"Field: {}".format(obj['field']))
#             print(u"url: {}".format(obj['url']))
#             print(u"title: {}".format(obj['title']))
#             print(u"text: {}".format(obj['text']))

# each department will have its own accumulated score
# e.g. artsci_biology
department_scores = {}

# loop through docs and accumulate scores
for f in glob.glob("*.jsonl"):
    with jsonlines.open(f) as reader:
        for obj in reader:
            field = format(obj['field'])
            url = format(obj['url'])
            title = format(obj['title'])
            text = format(obj['text'])

            try:
                department_scores[field] += get_score(title, text)         # call method to get scores for text
            except KeyError:  # department score not initialized yet
                department_scores[field] = 0         # init

for d_s in department_scores:
    print(d_s, ':',  department_scores[d_s])


