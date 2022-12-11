import os
import MarkovModel
import random
import enchant
from nltk.corpus import stopwords

d = enchant.Dict("en_US")


def read_sentences(file_path: str):
    """ Given a file path, read the file line by line and return a list of sentences """
    with open(file_path, 'r') as f:
        sentences = f.readlines()
        f.close()
    return sentences


def random_indices(end: int):
    """ Given an end number, return a list of random numbers between 0 and end """
    sentence_indices = []
    for i in range(0, 1000):
        n = random.randrange(end)
        sentence_indices.append(n)
    # return unique values only
    return list(set(sentence_indices))


def create_pickle(sent_file_path: str, pickle_file_name: str):
    """ Create a pickle file of the markov model """
    sentences = read_sentences(sent_file_path)
    model = MarkovModel.create_model(sentences)
    MarkovModel.create_pickle(model, pickle_file_name)
    return model


def load_pickle(file_path: str):
    """ Load the pickle file of the markov model """
    # read pickle file
    return MarkovModel.read_pickle(file_path)


def manual_accuracy(model):
    correct_predictions = 0
    total_predictions = 0
    print('To exit, type "exit_script"')
    run = True
    while run:
        user_input = input('Enter 2 words that would fit next to each other in a sentence: ')
        if user_input == 'exit_script':
            run = False
        else:
            words = user_input.split()
            first_word = words[0]
            second_word = words[1]
            prediction_tuples = MarkovModel.predict_next_word(model, first_word)
            total_predictions += 1
            prediction_words = [tup[0] for tup in prediction_tuples]
            print(prediction_words)
            if second_word in prediction_words:
                print('Prediction was correct!')
                correct_predictions += 1
            else:
                print('Incorrect prediction')
    print('Accuracy: ' + str(correct_predictions / total_predictions))


def automated_accuracy(markov_model):
    # read sentences
    sentences = read_sentences('sentences.txt')
    # get random indices
    indices = random_indices(len(sentences))
    # get random sentences
    random_sentences = [sentences[i] for i in indices]
    # remove stop words from sentences
    random_sentences = [' '.join([word for word in sentence.split() if word not in stopwords.words('english')]) for
                        sentence in random_sentences]

    # for each sentence get a random word that is not the last word and get the next word
    correct_predictions = 0
    total_predictions = 0
    for sentence in random_sentences:
        words = sentence.split()
        # if words is less than 3, skip
        if len(words) < 3:
            continue
        # get random word
        random_word = random.choice(words[:-2])
        # if word is in the model
        if random_word in markov_model.keys():
            # get prediction
            prediction_tuples = MarkovModel.predict_next_word(markov_model, random_word)
            total_predictions += 1
            prediction_words = [tup[0] for tup in prediction_tuples]
            # get next word
            next_word = words[words.index(random_word) + 1]
            if next_word in prediction_words:
                correct_predictions += 1
    return correct_predictions, total_predictions


def manual_data_cleaning(model: dict, pickle_file_name: str):
    """ Clean the data manually """

    # Automated Section
    print('Model key length: ' + str(len(model.keys())))
    idx = 0
    keys_to_remove = []
    for key, value in model.items():
        # Remove any keys that are stop words
        if key in stopwords.words('english'):
            keys_to_remove.append(key)
            continue
        # Remove any stopwords from value
        if any(word in value for word in stopwords.words('english')):
            # remove stop word from value
            for word in stopwords.words('english'):
                if word in value:
                    del value[word]

        # Remove any values that have a count less than 10
        values_to_remove = []
        for word, count in value.items():
            if count < 10:
                values_to_remove.append(word)
        for word in values_to_remove:
            del value[word]

        # Remove any keys that have less than 10 values
        if len(value) < 10:
            keys_to_remove.append(key)
    # remove keys
    for key in keys_to_remove:
        del model[key]

    print('Model key length: ' + str(len(model.keys())))
    print()
    print('Automated data cleaning complete. Starting Manual Section')
    print()

    # # Manual Section
    for key, value in model.items():
        # Print Key and Value
        print('Key:', key)
        print('Value:', sorted(value.items(), key=lambda item: (-item[1], item[0])))

        # ask user if they want to remove the key or value
        user_input = input('Enter value(s) to remove (separated by spaces):')
        if user_input == 'exit_script':
            break
        values_to_remove = user_input.split()
        for value_to_remove in values_to_remove:
            try:
                del value[value_to_remove]
            except KeyError:
                print('Value does not exist:', value_to_remove)

    # save model to pickle file
    MarkovModel.create_pickle(model, pickle_file_name)
    return model


def main():
    # if markov_model.pickle does not exist, create it
    if not os.path.exists('markov_model.pickle'):
        print('markov_model.pickle does not exist. Creating it now...')
        markov_model = MarkovModel.create_pickle('sentences.txt', 'markov_model.pickle')
    else:
        print('markov_model.pickle exists. Loading it now...')
        markov_model = load_pickle('markov_model.pickle')
    # Get accuracy of model
    total_correct_predictions, all_total_predictions = 0, 0
    max_accuracy = 0
    min_accuracy = 0
    run_times = 100
    for i in range(0, run_times):
        correct_predictions, total_predictions = automated_accuracy(markov_model)
        print('Run {}/{} '.format(i, run_times) + 'Accuracy: ' + str(correct_predictions / total_predictions))
        # set max and min accuracy
        if i == 0:
            max_accuracy = correct_predictions / total_predictions
            min_accuracy = correct_predictions / total_predictions
        else:
            if correct_predictions / total_predictions > max_accuracy:
                max_accuracy = correct_predictions / total_predictions
            if correct_predictions / total_predictions < min_accuracy:
                min_accuracy = correct_predictions / total_predictions

        total_correct_predictions += correct_predictions
        all_total_predictions += total_predictions
    print()
    print()
    print('Max Accuracy: ' + str(max_accuracy))
    print('Min Accuracy: ' + str(min_accuracy))
    print('Average Accuracy: ' + str(total_correct_predictions / all_total_predictions))


if __name__ == '__main__':
    main()
