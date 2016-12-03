from __future__ import print_function

import glob, os
import sys
import jsonlines

from afinn import Afinn
afinn = Afinn()

# afinn.setup_from_file(os.path.join(afinn.data_dir(), 'AFINN-165.txt'),
#                       word_boundary=False)

afinn.setup_from_file(os.path.join(afinn.data_dir(), 'AFINN-111.txt'),
                      word_boundary=False)

"""
get_score

for now, just return length
we're supposed to do sentiment analysis here and return the text's score
"""
def get_score(field, title, text):

    # title_score = afinn.score(title)
    text_score = afinn.score(text)
    # sum_score = title_score + text_score
    # print(title)

    # if "mystery" in field:
    #     print(field,title,text)
    #     print(":", text_score)
    return text_score, len(text)


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
department_lengths = {}
department_page_count = {}

# loop through docs and accumulate scores
for f in glob.glob("*.jsonl"):
    with jsonlines.open(f) as reader:
        for obj in reader:
            field = format(obj['field'])
            url = format(obj['url'])
            title = format(obj['title'])
            text = format(obj['text'])

            try:
                department_scores[field]
                department_lengths[field]
                department_page_count[field]
            except KeyError:
                department_scores[field] = 0         # init
                department_lengths[field] = 0
                department_page_count[field] = 0

            score, length = get_score(field, title, text)         # call method to get scores for text
            department_scores[field] += score
            department_lengths[field] += length
            department_page_count[field] += 1


for d_s in department_scores:

    denominator = (department_lengths[d_s] / department_page_count[d_s] ) / 100

    normalized_score = department_scores[d_s] / denominator

    print(d_s, '_Count:', department_page_count[d_s], ':',  department_scores[d_s], ':', normalized_score)


