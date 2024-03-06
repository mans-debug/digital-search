import re
import os
import lemma_utils
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


def write_results(root_dir, global_tokens, lemmas):
    global word
    with open(root_dir + '/tokens.txt', 'w') as tokens_file:
        for token in global_tokens:
            print(token, file=tokens_file)
    with open(root_dir + '/lemmas.txt', 'w') as lemmas_file:
        for key in lemmas.keys():
            print(key, file=lemmas_file)
    with open(root_dir + '/lemmas-with-words.txt', 'w') as lemmas_with_words_file:
        for key, words in lemmas.items():
            print(key, file=lemmas_with_words_file, end=' ')
            for word in words:
                print(word, file=lemmas_with_words_file, end=' ')
            print(file=lemmas_with_words_file)


if __name__ == '__main__':
    file_dir = '/Users/mansurminnikaev/PycharmProjects/crawler/crawler/files'
    lemmas = dict()
    _, _, htmls = next(os.walk(file_dir))
    global_tokens = set()
    for html_path in htmls:
        path = file_dir + '/' + html_path
        html_file = open(path)
        filtered_tokens = lemma_utils.clear_tokens(html_file)
        global_tokens = global_tokens.union(filtered_tokens)
        for word in filtered_tokens:
            lemmatized_word = lemmatizer.lemmatize(word, pos='v')
            if lemmatized_word not in lemmas:
                lemmas[lemmatized_word] = set()
            lemmas[lemmatized_word].add(word)

    root = '/Users/mansurminnikaev/PycharmProjects/crawler/lemmamizer'
    write_results(root, global_tokens, lemmas)
