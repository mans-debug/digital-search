import math

import lemmamizer.lemma_utils as lu
from itertools import groupby
import os


def groupBy_count(tokens):
    return [(term, len(list(group))) for term, group in groupby(sorted(tokens))]


def number_of_docs_contain_term(doc_unique_terms, term):
    return len(list(filter(lambda x: x, map(lambda entry: term in entry[1], doc_unique_terms.items()))))


def calculate_values(tf_dict, doc_unique_tokens, doc_token_count):
    term_res = {}
    for doc_id, terms_with_count in tf_dict.items():
        term_res[doc_id] = list()
        for term, count in terms_with_count:
            idf = math.log(100 / number_of_docs_contain_term(doc_unique_tokens, term), 10)
            tf = count / doc_token_count[doc_id]
            term_res[doc_id].append((term, idf, idf * tf))
    return term_res


def write_res(token_res, root):
    for filename, results in token_res.items():
        with open(root + '/' + filename, 'w') as file:
            for term, idf, tf_idf in results:
                print(term, idf, tf_idf, file=file)


if __name__ == '__main__':
    file_dir = '/Users/mansurminnikaev/PycharmProjects/crawler/crawler/files'
    _, _, html_paths = next(os.walk(file_dir))
    htmls = map(open, map(lambda path: file_dir + '/' + path, html_paths))

    term_tf_dict = {}  # docId - [(term, tf)]
    lemma_tf_dict = {}  # docId - [(lemma, tf)]

    doc_unique_terms = {}  # docId - set(terms)  # used for idf calculation
    doc_unique_lemmas = {}  # docId - set(terms) # used for idf calculation

    doc_term_count = {}
    doc_lemma_count = {}

    counter = 0
    for html in htmls:
        doc_id = os.path.basename(html.name)

        tokens = lu.clear_redundant_terms(html)
        term_tf_dict[doc_id] = groupBy_count(tokens)

        lemmas = lu.lemmatize_tokens(tokens)
        lemma_tf_dict[doc_id] = groupBy_count(lemmas)

        doc_unique_terms[doc_id] = set(tokens)
        doc_unique_lemmas[doc_id] = set(lemmas)

        doc_term_count[doc_id] = len(tokens)
        doc_lemma_count[doc_id] = len(lemmas)

        print("Progress", counter)
        counter += 1

    term_res = calculate_values(term_tf_dict, doc_unique_terms, doc_term_count)
    lemmas_res = calculate_values(lemma_tf_dict, doc_unique_lemmas, doc_lemma_count)

    write_res(term_res, '/Users/mansurminnikaev/PycharmProjects/crawler/tf-idf-ier/terms')
    write_res(lemmas_res, '/Users/mansurminnikaev/PycharmProjects/crawler/tf-idf-ier/lemmas')
