from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import WordNetLemmatizer
import re
import nltk

unwanted_tokens = ['TO', 'IN', 'CD', 'CC', '.', ':', 'PRP', '(', ')']
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
lemmatizer = WordNetLemmatizer()

tag_dict = {
    'NN': 'n',
    'NNS': 'n'
}


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


def contains_symbols(word):
    symbols = set(") ` ~ ! @ # $ % ^ & * - + = | \\ { } [ ] : ; \" ' < > , . ? / _ . ” ’".split(" "))
    if len(word) == 1:
        return True
    for ch in word:
        if ch in symbols:
            return True
    return False


def tokenize_html(html_file):
    html_text = ' '.join(re.split('\\s+', text_from_html(html_file))).lower()
    return tokenize_str(html_text)


def tokenize_str(text):
    tokens = list(filter(lambda x: not contains_symbols(x), nltk.word_tokenize(text)))
    tagged = nltk.pos_tag(tokens)
    return list(map(lambda x: x[0], filter(lambda x: x[1] not in unwanted_tokens, tagged)))


def clear_tokens(html_file):
    html_text = ' '.join(re.split('\\s+', text_from_html(html_file))).lower()
    tokens = set(filter(lambda x: not contains_symbols(x), set(nltk.word_tokenize(html_text))))
    tagged = nltk.pos_tag(tokens)
    return set(map(lambda x: x[0], filter(lambda x: x[1] not in unwanted_tokens, tagged)))


def lemmatize_tokens(tokens):
    tokens = nltk.pos_tag(tokens)
    return [lemmatizer.lemmatize(token, pos=tag_dict.get(tag, 'v')) for token, tag in tokens]
