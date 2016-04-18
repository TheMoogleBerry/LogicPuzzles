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
        cursor.execute("SELECT lower(Tag) as Tag, TotalOccurrences FROM Tags")
        self.tags = cursor.fetchall()
        cursor.close()

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
        vocabulary = set()

        # Pandas copies memory over for appending so must iterate for unique
        # words first
        for line in training_file:
            # Ensure this doesn't just return an empty line
            line = line.strip()
            if len(line) > 0:
                # Parse line into 'observation/classification'
                words = line.split(' ')

                # Iterate over each word to get the word and classification
                for word in words:
                    # Separate into tag & classification
                    context = word.split('/')
                    vocabulary.add(context[0].lower())

        # Prepare necessary data structures
        emission = pandas.DataFrame(index=vocabulary, columns=tags)
        transition = pandas.DataFrame(index=tags, columns=tags)
        emission.fillna(0, inplace=True)
        transition.fillna(0, inplace=True)
        last_class = None

        # Iterate to update the emissions and
        training_file.seek(0)
        for line in training_file:
            # Ensure this doesn't just return an empty line
            line = line.strip()
            if len(line) > 0:
                # Parse line into 'observation/classification'
                words = line.split(' ')

                # Iterate over each word to get the word and classification
                for word in words:
                    # Separate into tag & classification
                    context = word.split('/')
                    word = context[0].lower()
                    context_tags = context[1].split('+')

                    # Update the emission matrix
                    for context_tag in context_tags:
                        print(emission.index.values)
                        emission[context_tag][word] += 1

                    # Update the transition
                    if last_class != None:
                        for context_tag in context_tags:
                            for last_tag in last_class:
                                transition[last_tag][context_tag] += 1

                    # Update the last_class
                    last_class = context_tags

        # Pull info from the database that needs to be updated & merge arrays
        # TODO: Need to optimize
        cursor = self.connection.cursor()
        word_totals = {}
        tag_totals = {}
        for dest_tag, row in transition.iteritems():
            for origin_tag, occurrence in row.iteritems():
                # Retrieve total occurence data if it could not be found
                if origin_tag not in tag_totals:
                    cursor.execute('SELECT TotalOccurrences FROM Tags WHERE Tag = ?', (origin_tag,))
                    tag_totals[origin_tag] = cursor.fetchone()
                    if tag_totals[origin_tag] == None:
                        cursor.execute('INSERT INTO Tags (Tag, TotalOccurrences) VALUES (?, ?)', (origin_tag, 1))
                        tag_totals[origin_tag] = 1
                    else:
                        tag_totals[origin_tag] = tag_totals[origin_tag]['TotalOccurrences']
                tag_totals[origin_tag] = tag_totals[origin_tag] + int(occurrence)

                # Grab data for this specific transition
                cursor.execute('SELECT Occurrences FROM Transitions WHERE OriginTag = ? AND DestTag = ?', (origin_tag, dest_tag))
                db_occurrence = cursor.fetchone()
                if db_occurrence == None:
                    # We need to add one if it doesn't exists
                    cursor.execute('INSERT INTO Transitions (OriginTag, DestTag, Occurrences) VALUES (?, ?, ?)', (origin_tag, dest_tag, 0))
                    db_occurrence = 0
                else:
                    db_occurrence = db_occurrence['Occurrences']

                # Update the data
                db_occurrence += int(occurrence)
                cursor.execute('UPDATE Transitions SET Occurrences = ? WHERE OriginTag = ? AND DestTag = ?', (int(db_occurrence), origin_tag, dest_tag))

        for tag, row in emission.iteritems():
            for word, occurrence in row.iteritems():
                # Retrieve total occurence data if it could not be found
                if word not in word_totals:
                    cursor.execute('SELECT TotalOccurrences FROM Words WHERE Word = ?', (word,))
                    word_totals[origin_tag] = cursor.fetchone()
                    if word_totals[origin_tag] == None:
                        cursor.execute('INSERT INTO Words (Word, TotalOccurrences) VALUES (?, ?)', (word, 1))
                        word_totals[origin_tag] = 1
                    else:
                        word_totals[origin_tag] = word_totals[origin_tag]['TotalOccurrences']
                word_totals[origin_tag] = word_totals[origin_tag] + int(occurrence)

                # Grab data for this specific emission
                cursor.execute('SELECT Occurrences FROM Emissions WHERE Word = ? AND Tag = ?', (word, tag))
                db_occurrence = cursor.fetchone()
                if db_occurrence == None:
                    # We need to add the entry
                    cursor.execute('INSERT INTO Emissions (Word, Tag, Occurrences) VALUES (?, ?, ?)', (word, tag, 0))
                    db_occurrence = 0
                else:
                    db_occurrence = db_occurrence['Occurrences']

                # Update the data
                db_occurrence += int(occurrence)
                cursor.execute('UPDATE Emissions SET Occurrences = ? WHERE Word = ? AND Tag = ?', (int(db_occurrence), word, tag))

        # Update totals in general
        for word, occurence in word_totals:
            cursor.execute('UPDATE Words SET TotalOccurrences = ? WHERE Word = ?', (int(occurence), word))
        for tag, occurence in tag_totals:
            cursor.execute('UPDATE Tags SET TotalOccurrences = ? WHERE tag = ?', (int(occurence), tag))

        # Close unnecessary resources
        cursor.close()
        self.connection.commit()
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

test = POSClassifier()
test.train()
