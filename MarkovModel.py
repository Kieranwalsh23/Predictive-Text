"""
    Functions to Generate a Markov Model
    Path: MarkovModel.py
"""
import pickle
from collections import Counter
from nltk.corpus import stopwords


def create_model(sentences: list, markov_model=None):
    """ Given a training set of sentences, create or update a markov model """
    # if no model is given, create a new one
    if markov_model is None:
        markov_model = {}
    # go through each sentence
    for sentence in sentences:
        # split the sentence into words
        words = sentence.split()
        # remove stop words from words
        words = [word for word in words if word not in stopwords.words('english')]
        print('words: ' + str(words))
        # go through each word until the second to last word
        for i in range(len(words) - 1):
            print('i: ' + str(i))
            # get word and next word
            word = words[i]
            next_word = words[i + 1]
            print('word: ' + word)
            print('next_word: ' + next_word)
            # if word is in the markov model
            if word in markov_model.keys():
                values = markov_model[word]
                # if next word is in the values increment the count
                if next_word in values.keys():
                    values[next_word] += 1
                # else add the next word to the values
                else:
                    values[next_word] = 1
            # else add the word and next word to the markov model with count 1
            else:
                markov_model[word] = Counter({next_word: 1})
    return markov_model


def predict_next_word(model, word: str):
    """ Given a model and a word, predict the next word """
    # get the next word
    five_most_common = model[word].most_common(5)
    return five_most_common


def create_pickle(model, save_name: str):
    """ Given a model and a save name, create a pickle file """
    # create pickle file
    with open(save_name, 'wb') as f:
        pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)


def read_pickle(file_path: str):
    """ Given a file path, read the pickle file and return the model """
    # read pickle file
    with open(file_path, 'rb') as f:
        model = pickle.load(f)
    return model
