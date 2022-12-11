# Next Word Prediction
Using a Markov Chain to generate text based on a given word. The markov chain is trained from the enron email dataset.
The application will feature a GUI that will allow the user to customize their experience. The user will be able to do
the following:
### 1. Change their model preference (EDIT: Application now - ALWAYS REMOVES STOP WORDS)
Predictions will no longer be made on stop words, but will retrieve the previous word and predict on that.
### 2. Use the application as a text editor
Enter text into a text area (next word predictions will be displayed in a list as the user types)
### 3. Update their model
The user will be able to update their model with their own entered-text. Or load and existing file into the text area.
Clicking the train button will update the model.
### 4. Save text to a file
The user will be able to save the text in the text area to a file.

#
#
### Single click item in prediction to add to text area. (Ensure that the cursor has not been moved and the next word and no letters have been added


