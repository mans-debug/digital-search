from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import os
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def extract_words_using_find(input_string):
    words = [input_string[start:space_index] for start, space_index in enumerate(input_string.split(' '))]
    return words


def contains_symbols(word):
    symbols = set(") ` ~ ! @ # $ % ^ & * - + = | \\ { } [ ] : ; \" ' < > , . ? / _ . ” ’".split(" "))
    if len(word) == 1:
        return True
    for ch in word:
        if ch in symbols:
            return True
    return False


if __name__ == '__main__':
    unwanted_tokens = ['TO', 'IN', 'CD', 'CC', '.', ':', 'PRP', '(', ')']
    file_dir = '/Users/mansurminnikaev/PycharmProjects/crawler/crawler/files'
    lemmas = dict()
    _, _, htmls = next(os.walk(file_dir))
    global_tokens = set()
    for body in htmls:
        path = file_dir + '/' + body
        html = open(path)
        # print(html.read())
        html_text = ' '.join(re.split('\\s+', text_from_html(html))).lower()
        tokens = set(filter(lambda x: not contains_symbols(x), set(nltk.word_tokenize(html_text))))
        tagged = nltk.pos_tag(tokens)
        filtered_words = set(map(lambda x: x[0], filter(lambda x: x[1] not in unwanted_tokens, tagged)))
        global_tokens = global_tokens.union(filtered_words)
        for word in filtered_words:
            lemmatized_word = lemmatizer.lemmatize(word, pos='v')
            if lemmatized_word not in lemmas:
                lemmas[lemmatized_word] = set()
            lemmas[lemmatized_word].add(word)

    root = '/Users/mansurminnikaev/PycharmProjects/crawler/lemmamizer'
    with open(root + '/tokens.txt', 'w') as tokens_file:
        for token in global_tokens:
            print(token, file=tokens_file)

    with open(root + '/lemmas.txt', 'w') as lemmas_file:
        for key in lemmas.keys():
            print(key, file=lemmas_file)

    with open(root + '/lemmas-with-words.txt', 'w') as lemmas_with_words_file:
        for key, words in lemmas.items():
            print(key, file=lemmas_with_words_file, end=' ')
            for word in words:
                print(word, file=lemmas_with_words_file, end=' ')
            print(file=lemmas_with_words_file)
