import numpy as np
import lemmamizer.lemma_utils as lu
from itertools import groupby


def groupBy_count(tokens):
    return [(term, len(list(group))) for term, group in groupby(sorted(tokens))]


def read_tokens(path):
    with open(path) as words_file:
        return words_file.readline().split()


def read_idf_map(path):
    res = {}
    with open(path) as idf_map:
        for line in idf_map.readlines():
            splits = line.split()
            res[splits[0]] = float(splits[1])
    return res


def build_query_vector(tf, token_pos_map, token_idf_map):
    res = np.zeros(len(token_pos_map))
    for token, frequency in tf:
        if token in token_pos_map:
            res[token_pos_map[token]] = frequency * token_idf_map[token]
    return res


def cosine_sim(a, b):
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim


def find_matches(query_vec, matrix):
    return [cosine_sim(query_vec, doc_vec) for doc_vec in matrix]


path = '/Users/mansurminnikaev/PycharmProjects/crawler/search_engine'
doc_matrix = np.loadtxt(path + '/matrix.txt')
tokens = read_tokens(path + '/tokens.txt')
token_count = len(tokens)
token_pos_map = dict([(word, i) for i, word in enumerate(tokens)])
token_idf_map = read_idf_map(path + '/tokens-idf-map.txt')


def search(query, show_top_n=5):
    query_tokens = lu.tokenize_str(query)
    lemmas = lu.lemmatize_tokens(query_tokens)
    tf = groupBy_count(lemmas)
    query_idf_vector = build_query_vector(tf, token_pos_map, token_idf_map)
    matches = find_matches(query_idf_vector, doc_matrix)
    return list(sorted(enumerate(matches), key=lambda x: x[1], reverse=True))[:show_top_n]

# if __name__ == '__main__':
#     while True:
#         q = input()
#         matches = search(q)
#         print(list(sorted(enumerate(matches), key=lambda x: x[1], reverse=true))[:5])
