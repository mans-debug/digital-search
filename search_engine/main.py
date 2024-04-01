import numpy as np
import os
import re


def load_indexes():
    doc_map = dict()
    file_dir = '/Users/mansurminnikaev/PycharmProjects/crawler/tf-idf-ier/lemmas'
    _, _, indexes_path = next(os.walk(file_dir))
    idf_indexes = map(open, map(lambda path: file_dir + '/' + path, indexes_path))
    unique_tokens_idf = set()
    for idf_i in idf_indexes:
        doc_id = os.path.basename(idf_i.name)
        doc_map[doc_id] = dict()
        for line in idf_i.readlines():
            splits = line.rstrip().split(" ")
            token = splits[0]
            idf = splits[1]
            tf_idf = splits[2]
            doc_map[doc_id][token] = float(tf_idf)
            unique_tokens_idf.add((token, idf))
    return doc_map, list(unique_tokens_idf)


def write_matrix(path, matrix):
    with open(path, 'w') as matrix_file:
        for row in matrix:
            for el in row:
                print(el, end=" ", file=matrix_file)
            print(file=matrix_file)


if __name__ == '__main__':
    idf_indexes, unique_tokens_idf = load_indexes()
    unique_tokens = [token for token, _ in unique_tokens_idf]
    matrix = np.zeros((len(idf_indexes.keys()), len(unique_tokens)))
    path = '/search_engine'
    write_matrix(path + '/tokens.txt', [unique_tokens])
    write_matrix(path + '/tokens-idf-map.txt', unique_tokens_idf)
    for doc_id, doc_idf_map in idf_indexes.items():
        doc_num = int(re.findall('\\d+', doc_id)[0])
        for i, token in enumerate(unique_tokens):
            matrix[doc_num][i] = doc_idf_map.get(token, 0)

    write_matrix(path + '/matrix.txt', matrix)
