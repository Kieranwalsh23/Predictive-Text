import re
import string
import contractions as contractions
from nltk.corpus import stopwords
import requests as requests


# TODO: get data from personal stuff
def get_data(url: str, start_str: str, end_str: str):
    """Get text from http request"""
    raw = requests.get(url).text
    start = re.search(start_str, raw).start()
    stop = re.search(end_str, raw).end()
    text = raw[start:stop]
    return text


def preprocess(text):
    """Keep alphanumeric values and set all to lower case"""
    text = replace_contractions(text)
    return re.sub('[^A-Za-z0-9.]+', ' ', text).lower()


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for w in words:
        if w not in stopwords.words('english'):
            new_words.append(w)
    return new_words


def remove_punctuation(sentence):
    return sentence.translate(str.maketrans('', '', string.punctuation))