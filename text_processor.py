"""
    Run this file to extract sentences from the emails
    This really only needs to be done once.
    Path: text_processor.py
"""
import os
import re
import time
from email.parser import Parser
import nltk
from nltk.tokenize import sent_tokenize
import enchant

nltk.download('punkt')
nltk.download('stopwords')
d = enchant.Dict("en_US")

DATASET_DIR = '../../enron-email-dataset/maildir'

# Get all users
users = os.listdir(DATASET_DIR)


def read_and_format_email(file_path: str):
    with open(file_path, 'r') as f:
        data = f.read()
        email = Parser().parsestr(data)
        email_message = email.get_payload()
        return preprocess_text(email_message)


def preprocess_text(text_to_process: str):
    # set email_message to lowercase
    text_to_process = text_to_process.lower()
    # remove non-alphanumeric characters except spaces and punctuation
    text_to_process = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?]', '', text_to_process)
    # remove newlines
    text_to_process = text_to_process.replace('\n', ' ')
    # remove multiple spaces
    text_to_process = re.sub(' +', ' ', text_to_process)
    # remove leading and trailing whitespace
    text_to_process = text_to_process.strip()
    # remove numbers
    text_to_process = re.sub(r'\d+', '', text_to_process)
    # Use nltk to tokenize the email message into sentences
    email_sentences = sent_tokenize(text_to_process)
    # remove punctuation from sentences
    email_sentences = [re.sub(r'([?.!,"])', r'', sent) for sent in email_sentences]
    return email_sentences


def write_sentences_to_file(sentences, output_file: str = 'sentences.txt'):
    with open(output_file, 'w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')
        f.close()


def extract_sentences():
    # Get all users' inbox files
    sentences = []
    for user_idx, user in enumerate(users):
        print('Processing user {} of {}'.format(user_idx, len(users)))
        # for each directory in the user's directory
        user_dir = DATASET_DIR + '/' + user
        # Use a lot of try/excepts to avoid errors
        # Restarting the program due to small error would be a pain
        try:
            for directory in os.listdir(user_dir):
                directory_path = user_dir + '/' + directory
                try:
                    for file in os.listdir(directory_path):
                        file_path = directory_path + '/' + file
                        if os.path.isfile(file_path):
                            try:
                                # read the email and add sentences to sentences list
                                file_sentences = read_and_format_email(file_path,)
                                sentences.extend(file_sentences)
                            except Exception as e:
                                print('Error reading file: ' + file_path)
                                print(e)
                                pass
                except Exception as e:
                    print('Error reading user directory: ' + user_dir)
                    print(e)
                    pass
        except Exception as e:
            print('Error reading user: ' + user)
            print(e)
            pass
    # write sentences to file
    write_sentences_to_file(sentences)


def main():
    start_time = time.time()
    extract_sentences()
    end_time = time.time()
    print('Time elapsed: {} seconds'.format(end_time - start_time))


if __name__ == '__main__':
    main()
