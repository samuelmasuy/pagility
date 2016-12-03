from __future__ import print_function
from afinn import Afinn
import glob
import os
import sys
import jsonlines


# function calculates the afinn score for a title and the text of 1 document
def get_score(title, text, afinn):
    doc_data = title + ' ' + text
    #doc_data = doc_data.encode("ascii", "ignore")
    token_score = afinn.score(doc_data)  # calculating the afinn score for the document text
    return token_score


# function calculates the total afinn score for each department
def calculate_department_scores():
    os.chdir("../sample_output")
    afinn = Afinn()
    afinn.setup_from_file(os.path.join(afinn.data_dir(), 'AFINN-111.txt'), word_boundary=False)

    # dictionary where the keys are departments, values are lists of tuples containing a url, doc score and doc length
    # for each document in the department
    department_scores = {}
    # loop through documents and accumulate scores for each department
    for f in glob.glob("*.jsonl"):
        with jsonlines.open(f) as reader:
            for obj in reader:
                dep = format(obj['field'])
                url = format(obj['url'])
                title = format(obj['title'])
                text = format(obj['text'])

                doc_score = get_score(title, text, afinn)
                doc_length = len(title + text)
                doc_tuple = (url, doc_score, doc_length)
                if dep not in department_scores:  # checking if the department is present in the d
                    department_scores[dep] = [doc_tuple]
                else:
                    department_scores[dep].append(doc_tuple)

    return department_scores


# function takes in a dictionary of department scores and returns a dictionary of normalized department scores
def normalize_scores(dep_scores):
    norm_scores = {}
    # iterating through all the departments
    for department in dep_scores:
        dep_score = 0
        dep_doc_total_length = 0
        dep_doc_count = 0
        # iterating through each document in the current department
        for doc in dep_scores[department]:
            dep_score += doc[1]
            dep_doc_total_length += doc[2]
            dep_doc_count += 1

        denominator = (dep_doc_total_length / dep_doc_count) / 100
        normalized_score = dep_score / denominator
        norm_scores[department] = normalized_score

    return norm_scores


# takes in a dictionary of normalized department scores
# ranks and classifies them between negative, neutral and positive
def three_way_classifier(scores):
    lowest_score = 0
    highest_score = 0
    # iterating through dep scores to get the lowest and highest score
    for dep in scores:
        score = scores[dep]
        if score < lowest_score:
            lowest_score = score
        if score > highest_score:
            highest_score = score
    # calculating the score range of each class
    rng = (highest_score - lowest_score) / 3
    neg_upper_bound = lowest_score + rng
    pos_lower_bound = highest_score - rng

    dep_scores_classified = []
    # classifying the departments by checking what range their score falls into
    for dep in scores:
        score = scores[dep]
        if score < neg_upper_bound:
            dep_tuple = (dep, score, "negative")
            dep_scores_classified.append(dep_tuple)
        elif score < pos_lower_bound:
            dep_tuple = (dep, score, "neutral")
            dep_scores_classified.append(dep_tuple)
        else:
            dep_tuple = (dep, score, "positive")
            dep_scores_classified.append(dep_tuple)

    sorted_by_score = sorted(dep_scores_classified, key=lambda x: x[1])
    return sorted_by_score

dep_scores = calculate_department_scores()
normalized_scores = normalize_scores(dep_scores)
sorted_dep = three_way_classifier(normalized_scores)

for d in sorted_dep:
    print(d[0], ":", d[1], ":", d[2])


