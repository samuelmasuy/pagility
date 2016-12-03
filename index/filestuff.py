"""
filestuff

o   Handles getting files in a specified directory and file type, preparing files for writing, loading index file to memory
"""

from os import listdir
from os.path import isfile, join
from collections import OrderedDict
import ast


def get_files(doc_path, file_ext):

    only_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
    file_types = [(doc_path + '/' + f) for f in only_files if f.endswith(file_ext)]

    # print(reuter_files)
    return file_types


def read_index_into_memory(index_file):
    index = OrderedDict()
    index_f = open(index_file)
    postings_count = 0
    for line in index_f:
        t_split = line.split('->')
        term = t_split[0]
        postings = ast.literal_eval(t_split[1])         # convert postings string to list e.g. '[7,9]\n' -> [7,9]
        postings_count += len(postings)
        index.update({term:postings})
    # print("Term count: " + str(len(index)))
    return index, postings_count

def delete_content(f_name):
    with open(f_name, "w"):
        pass
