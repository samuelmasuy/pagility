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
    token_score = afinn.score(text)
    # sum_score = title_score + text_score
    # print(title)

    # if "mystery" in field:
    #     print(field,title,text)
    #     print(":", text_score)
    #return text_score, len(text)
    return token_score


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
department_token_scores = {}  # department is the key, values are dictionaries for each text in that department

# loop through docs and accumulate scores
for f in glob.glob("*.jsonl"):
    with jsonlines.open(f) as reader:
        for obj in reader:
            field = format(obj['field'])
            url = format(obj['url'])
            title = format(obj['title'])
            text = format(obj['text'])

            data = title + text
            #data = data.encode("ascii", "ignore")
            data_score = get_score(field, title, data)  # call method to get a score for all data

            if field not in department_scores:
                department_scores[field] = data_score
            else:
                department_scores[field] += data_score

            if field not in department_token_scores:
                URL_token_scores = {}
                department_token_scores[field] = {}

            token_scores = []
            tokens = data.split()
            length = len(data)
            #length = 0
            for token in tokens:
                score = get_score(field, title, token)  # call method to get a score for the token
                #length += 1
                if score != 0:
                    token_score_tuple = (token, score)
                    token_scores.append(token_score_tuple)

            URL_token_scores[url] = token_scores
            department_token_scores[field] = URL_token_scores

            """if field in department_scores:
                department_scores[field] += score
            else:
                department_scores[field] = score"""

            if field in department_lengths:
                department_lengths[field] += length
            else:
                department_lengths[field] = length

            if field in department_page_count:
                department_page_count[field] += 1
            else:
                department_page_count[field] = 1

for dep in department_token_scores:
    print()
    print(dep, ":")
    score = 0
    for doc in department_token_scores[dep]:
        print(doc, ":")
        print(department_token_scores[dep][doc])
        for token_tuple in department_token_scores[dep][doc]:
            score += token_tuple[1]
    print("Total score:", score)

for d_s in department_scores:

    denominator = (department_lengths[d_s] / department_page_count[d_s]) / 100

    normalized_score = department_scores[d_s] / denominator

    print(d_s, '_Count:', department_page_count[d_s], ':',  department_scores[d_s], ':', normalized_score, ':', department_lengths[d_s])


