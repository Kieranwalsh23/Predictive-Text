import os
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QPlainTextEdit, QFileDialog, QListWidget, QLabel
from nltk.corpus import stopwords

import MarkovModel
import text_processor

VERSION = '0.0.1'
markov_model = None


def open_file_explorer():
    """ Open the file explorer to select a file """
    print("Open file explorer")
    filename = QFileDialog.getOpenFileName()
    print(filename)
    return filename[0]


def exit_button_handler():
    """ Event handler for the exit button """
    print("Exit button clicked")
    sys.exit()


class MainWindow(QMainWindow):
    """ Window for the GUI """

    def __init__(self):
        QMainWindow.__init__(self)

        self.markov_model = markov_model

        # set window to fixed size (not resizable)
        self.setFixedSize(1450, 800)

        # set window title
        self.setWindowTitle("Next Word Prediction - " + VERSION)
        # set window to dark theme
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff")

        # add a text area that is 1200x800
        self.text_area = QPlainTextEdit(self)
        self.text_area.setFixedSize(1200, 700)
        self.text_area.move(10, 10)
        # set text area font to 16
        self.text_area.setFont(QtGui.QFont("Arial", 16))

        # add a train model button to the right of the text area
        self.train_model_button = QPushButton('Train Model', self)
        self.train_model_button.setFixedSize(200, 50)
        self.train_model_button.move(1220, 10)
        self.train_model_button.setStyleSheet("font-size: 20px")
        self.train_model_button.setStyleSheet("border: 3px solid #ffffff")

        # add a save button to the right of the text area
        self.save_button = QPushButton('Save', self)
        self.save_button.setFixedSize(200, 50)
        self.save_button.move(1220, 70)
        self.save_button.setStyleSheet("font-size: 20px")
        self.save_button.setStyleSheet("border: 3px solid #ffffff")

        # add a load button to the right of the text area
        self.load_button = QPushButton('Load', self)
        self.load_button.setFixedSize(200, 50)
        self.load_button.move(1220, 130)
        self.load_button.setStyleSheet("font-size: 20px")
        self.load_button.setStyleSheet("border: 3px solid #ffffff")

        # add an exit button to the right of the text area
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setFixedSize(200, 50)
        self.exit_button.move(1220, 190)
        self.exit_button.setStyleSheet("font-size: 20px")
        self.exit_button.setStyleSheet("border: 3px solid #ffffff")

        # add a 'Predictions' Label to the right of the text area
        self.predictions_label = QLabel('Predictions', self)
        self.predictions_label.setFixedSize(200, 50)
        self.predictions_label.move(1220, 250)
        self.predictions_label.setStyleSheet("font-size: 20px")

        # add a selectable listbox to the right of the text area
        self.predictions_listbox = QListWidget(self)
        self.predictions_listbox.setFixedSize(200, 300)
        self.predictions_listbox.move(1220, 300)
        self.predictions_listbox.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.predictions_listbox.setStyleSheet("border: 3px solid #ffffff")

        # set up the event handlers
        self.train_model_button.clicked.connect(lambda: self.train_model())
        self.save_button.clicked.connect(lambda: self.save())
        self.load_button.clicked.connect(lambda: self.load_button_handler())
        self.exit_button.clicked.connect(lambda: exit_button_handler())
        self.text_area.textChanged.connect(lambda: self.text_changed())
        self.predictions_listbox.itemClicked.connect(lambda it: self.prediction_clicked(it.text()))

    def load_button_handler(self):
        """ Event handler for the load button """
        print("Load button clicked")
        filename = open_file_explorer()
        if filename != '' and filename.endswith('.txt'):
            with open(filename, 'r') as f:
                text = f.read()
                f.close()
                self.text_area.insertPlainText(text)
        return

    def save(self):
        """ Event handler for the save button """
        name = QFileDialog.getSaveFileName(self, 'Save File')
        # if name is not empty
        if name[0]:
            file = open(name[0], 'w+')
            text = self.text_area.toPlainText()
            file.write(text)
            file.close()
            print("File Saved Successfully")
            # update model
            print('Adding new data to model')
            self.train_model()

    def prediction_clicked(self, word):
        """ Event handler for the prediction box """
        # clear first, as adding will trigger event handler to add next predictions
        # This ensures no race condition for clearing predictions that we want
        self.predictions_listbox.clear()
        self.text_area.insertPlainText(word)
        self.text_area.setFocus()
        # Trigger automatic next prediction
        self.text_area.insertPlainText(" ")

    def train_model(self):
        global markov_model
        """ Event handler for the train model button """
        # get text from text area
        text = self.text_area.toPlainText()
        # preprocess text
        text = text_processor.preprocess_text(text)
        markov_model = MarkovModel.create_model(text, markov_model=self.markov_model)
        self.markov_model = markov_model
        print('New model created')
        MarkovModel.create_pickle(markov_model, 'markov_model.pickle')

    def text_changed(self):
        """ Event handler for the text area """
        # TODO: error handling not perfect, but works for first release
        text = self.text_area.toPlainText()
        # if text is empty do nothing
        try:
            if text == '':
                return
            # if last key was a space, grab the word before the space
            if text[-1] == ' ':
                word = text.split(' ')[-2]
                # if word is empty or ends with period, do nothing
                if word == '' or word[-1] == '.':
                    return
                # if word is a stop word, get the word before that
                if word in stopwords.words('english'):
                    word = text.split(' ')[-3]
                    # if word is empty or ends with period, do nothing
                    if word == '' or word[-1] == '.':
                        return

            # predict the next word and display it in the prediction box
            predictions = MarkovModel.predict_next_word(markov_model, word.lower())
            # get the top 5 predictions and display them in the prediction box
            self.predictions_listbox.clear()
            for prediction in predictions:
                self.predictions_listbox.addItem(prediction[0])
        except Exception:
            return


if __name__ == "__main__":
    # instantiate the model
    if not os.path.exists('markov_model.pickle'):
        markov_model = MarkovModel.create_pickle('sentences.txt', 'markov_model.pickle')
    else:
        markov_model = MarkovModel.read_pickle('markov_model.pickle')

    # create application
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # execute application
    sys.exit(app.exec_())
