"""
A module for coordinating the classification of the POS in a sentence or body
of text.

The tags being used are currently those in use for the brown corpus
"""
from __future__ import print_function
import sqlite3
import pandas
import os.path

WEIGHT_FILE = 'data/viterbi.sqlite3'
DEFAULT_TRAINING_PATH = 'data/brown'
DEFAULT_TRAINING_FILE = 'data/brown/ca01'

def associative_factory(cursor, row):
    """
    Returns associative arrays for data from db connections
    """
    assoc = {}
    for idx, col in enumerate(cursor.description):
        assoc[col[0]] = row[idx]
    return assoc

def array_column(matrix, index):
    """
    Returns a specific column from an array based on some index
    """
    column = []
    for row in matrix:
        column.append(row[index])
    return column

class POSClassifier(object):
    """
    Classifier that manages the POS Classification
    """
    connection = None
    tags = {}

    def __init__(self):
        # Open connection to the sqlite db
        self.connection = sqlite3.connect(WEIGHT_FILE)
        self.connection.row_factory = associative_factory

        # Retrieve the current tag set
        cursor = self.connection.cursor()
        cursor.execute("SELECT lower(Tag) as Tag, Occurrences FROM Tags")
        self.tags = cursor.fetchall()

    def __del__(self):
        self.connection.close()

    def train(self, file_name=DEFAULT_TRAINING_FILE):
        """
        Takes in a training file formatted where the entire body of text is
        parsed each individual word or punctuation. On each line, there is
        also an identification stating the actual part of speech for that word.

        Args:
            file_name (str): The path to the file contain the training data
        """
        # Create connection to the file
        training_file = None

        # Open the specific training file
        if os.path.exists(file_name):
            try:
                training_file = open(file_name)
            except IOError:
                print("Unable to open the file at " + file_name + ".")

        # Pull probablistic data from these files
        tags = array_column(self.tags, "Tag")
        emission = pandas.DataFrame(columns=tags)
        transition = pandas.DataFrame(index=tags, columns=tags)
        emission.fillna(0, inplace=True)
        transition.fillna(0, inplace=True)
        last_class = None
        for line in training_file:
            # Ensure this doesn't just return an empty line
            line = line.strip()
            if len(line) > 0:
                # Parse line into observation/classification
                words = line.split(' ')

                # Iterate over each word to get the word and classification
                for word in words:
                    # Separate into tag & classification
                    context = word.split('/')
                    context_tags = context[1].split('+')

                    # Update the emission matrix
                    if context[0] not in emission.index:
                        # If not found, create and append
                        row = pandas.DataFrame(index=[context[0]], columns=tags)
                        row.fillna(0, inplace=True)
                        for context_tag in context_tags:
                            row[context_tag] += 1
                        emission = emission.append(other=row)
                    else:
                        # Update the necessary columns
                        for context_tag in context_tags:
                            emission[context[0]][context_tag] += 1

                    # Update the transition
                    if last_class != None:
                        for context_tag in context_tags:
                            for last_tag in last_class:
                                transition[last_tag][context_tag] += 1

                    # Update the last_class
                    last_class = context_tags

                    print(emission)

        # Pull info from the database that needs to be updated & merge arrays

        # Push information to the database

        # Close unnecessary resources
        training_file.close()

    def classify(self, text):
        """
        Takes a body of text and transforms it to an array of classification for
        each word in the body of text, where its position in the returned array
        is determined by its position in the text.

        Args:
            text (str): The body of text that needs to be classified

        Returns:
            str[]: The classifcation of each word in the body of text
        """
        pass
