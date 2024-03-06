import lemmamizer.lemma_utils as lu
from nltk.stem import WordNetLemmatizer
import nltk
import os
import json

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


def lemma_distinct(tokens):
    distinct_lemmas = set()
    for token in tokens:
        lemmatized_word = lemmatizer.lemmatize(token, pos='v')
        distinct_lemmas.add(lemmatized_word)
    return distinct_lemmas


if __name__ == '__main__':
    file_dir = '/Users/mansurminnikaev/PycharmProjects/crawler/crawler/files'
    _, _, html_paths = next(os.walk(file_dir))
    htmls = map(open, map(lambda path: file_dir + '/' + path, html_paths))
    lemma_index = dict()
    for html in htmls:
        tokens = lu.clear_tokens(html)
        unique_lemmas = lemma_distinct(tokens)
        for lemma in unique_lemmas:
            if lemma not in lemma_index:
                lemma_index[lemma] = []
            lemma_index[lemma].append(os.path.basename(html.name))

    json.dump(lemma_index, open('inverted_index.json', 'w'))
