"""
A module for coordinating the classification of the POS in a sentence or body
of text.

The tags being used are currently those in use for the brown corpus
"""
from __future__ import print_function
import sqlite3
from pandas import DataFrame
import os
import re

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

def array_column_filter(matrix, index, value):
    rows = []
    for row in matrix:
        if row[index] == value:
            rows.append(row)

    return rows

def array_max(matrix, index):
    """
    Returns a specific columns max from an array base on some index
    """
    max = None
    for row in matrix:
        if max == None or row[index] > max:
            max = row[index]
    return max

def get_max_word(word_rows):
    optimal_tag = 'NP'
    max = 0
    for row in word_rows:
        if max < row['Occurrences']:
            max = row['Occurrences']
            optimal_tag = row['Tag']
    return optimal_tag


def get_tags_by_word(word_emissions, word):
    word_options = []
    for row in word_emissions:
        if row['Word'] == word:
            word_options.append(row)
    return word_options

def get_tags_by_tag(tag_transitions, origin_tag):
    tag_options = []
    for row in tag_transitions:
        if row['OriginTag'] == origin_tag:
            tag_options.append(row)
    return tag_options

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
                    context = word.rsplit('/', maxsplit=1)
                    word = context[0].lower().strip()
                    if word not in vocabulary:
                        vocabulary.add(word)

        # Prepare necessary data structures
        emission = DataFrame(index=vocabulary, columns=tags)
        transition = DataFrame(index=tags, columns=tags)
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
                    context = word.rsplit('/', maxsplit=1)
                    word = context[0].lower().strip()
                    context_tags = context[1].split('+')

                    # Update the emission matrix
                    for context_tag in context_tags:
                        emission[context_tag][word] += 1

                    # Update the transition
                    if last_class != None:
                        for context_tag in context_tags:
                            for last_tag in last_class:
                                transition[last_tag][context_tag] += 1

                    # Update the last_class
                    last_class = context_tags

        # Pull info from the database that needs to be updated & merge arrays
        cursor = self.connection.cursor()
        word_totals = {}
        tag_totals = {}
        for dest_tag, row in transition.iteritems():
            for origin_tag, occurrence in row.iteritems():
                # Retrieve total occurence data if it could not be found
                if origin_tag not in tag_totals:
                    cursor.execute('SELECT TotalOccurrences FROM Tags WHERE Tag = ?', (origin_tag.upper().strip(),))
                    tag_totals[origin_tag] = cursor.fetchone()
                    if tag_totals[origin_tag] == None:
                        cursor.execute('INSERT INTO Tags (Tag, TotalOccurrences) VALUES (?, ?)', (origin_tag.upper().strip(), 1))
                        tag_totals[origin_tag] = 1
                    else:
                        tag_totals[origin_tag] = int(tag_totals[origin_tag]['TotalOccurrences'])
                tag_totals[origin_tag] += int(occurrence)

                # Grab data for this specific transition
                cursor.execute('SELECT Occurrences FROM Transitions WHERE OriginTag = ? AND DestTag = ?', (origin_tag.upper().strip(), dest_tag))
                db_occurrence = cursor.fetchone()
                if db_occurrence == None:
                    # We need to add one if it doesn't exists
                    cursor.execute('INSERT INTO Transitions (OriginTag, DestTag, Occurrences) VALUES (?, ?, ?)', (origin_tag.upper().strip(), dest_tag, 0))
                    db_occurrence = 0
                else:
                    db_occurrence = db_occurrence['Occurrences']

                # Update the data
                db_occurrence += int(occurrence)
                cursor.execute('UPDATE Transitions SET Occurrences = ? WHERE OriginTag = ? AND DestTag = ?', (int(db_occurrence), origin_tag.upper().strip(), dest_tag))

        for tag, row in emission.iteritems():
            for word, occurrence in row.iteritems():
                # Retrieve total occurence data if it could not be found
                if word not in word_totals:
                    cursor.execute('SELECT TotalOccurrences FROM Words WHERE Word = ?', (word,))
                    word_totals[word] = cursor.fetchone()
                    if word_totals[word] == None:
                        cursor.execute('INSERT INTO Words (Word, TotalOccurrences) VALUES (?, ?)', (word, 1))
                        word_totals[word] = 1
                    else:
                        word_totals[word] = int(word_totals[word]['TotalOccurrences'])
                word_totals[word] += int(occurrence)

                # Grab data for this specific emission
                cursor.execute('SELECT Occurrences FROM Emissions WHERE Word = ? AND Tag = ?', (word, tag.upper().strip()))
                db_occurrence = cursor.fetchone()
                if db_occurrence == None:
                    # We need to add the entry
                    cursor.execute('INSERT INTO Emissions (Word, Tag, Occurrences) VALUES (?, ?, ?)', (word, tag.upper().strip(), 0))
                    db_occurrence = 0
                else:
                    db_occurrence = db_occurrence['Occurrences']

                # Update the data
                db_occurrence += int(occurrence)
                cursor.execute('UPDATE Emissions SET Occurrences = ? WHERE Word = ? AND Tag = ?', (int(db_occurrence), word, tag.upper().strip()))

        # Update totals in general
        for word, occurence in word_totals.items():
            cursor.execute('UPDATE Words SET TotalOccurrences = ? WHERE Word = ?', (int(occurence), word))
        for tag, occurence in tag_totals.items():
            cursor.execute('UPDATE Tags SET TotalOccurrences = ? WHERE tag = ?', (int(occurence), (tag.upper().strip())))

        # Close unnecessary resources
        cursor.close()
        self.connection.commit()
        training_file.close()

    def mass_train(self):
        # Reset database
        cursor = self.connection.cursor()

        cursor.execute('UPDATE Tags SET TotalOccurrences = 0')
        cursor.execute('DELETE FROM Words')
        cursor.execute('DELETE FROM Emissions')
        cursor.execute('DELETE FROM Transitions')

        cursor.close()
        self.connection.commit()

        for f in os.listdir(DEFAULT_TRAINING_PATH):
            print('Training w/ ' + f)
            self.train(DEFAULT_TRAINING_PATH + '/' + f)

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
        cursor = self.connection.cursor()

        # Pad the sentence itself & Parse into our vocabulary
        vocabulary = re.sub('([.,!?()])', r' \1 ', text)
        vocabulary = re.sub('\s{2,}', ' ', vocabulary).strip().split(' ')
        parsed_sentence = vocabulary
        vocabulary = [x.lower() for x in vocabulary]

        # Format the vocabulary appropriately
        words = ''
        if len(vocabulary) > 0:
            words = "'" + "', '".join(vocabulary) + "'"
        words = '(' + words + ')'

        # Grab Word Totals
        cursor.execute('SELECT * FROM Words WHERE Word IN '+ words)
        word_totals = cursor.fetchall()

        # Grab Word Emissions
        cursor.execute('SELECT * FROM Emissions WHERE Occurrences > 0 AND Word IN ' + words)
        word_emissions = cursor.fetchall()

        # Retrieve tags into a consolidated
        tag_set = array_column(word_emissions, 'Tag')
        tags = ''
        if len(tag_set) > 0:
            tags = "'" + "', '".join(tag_set) + "'"
        tags = '(' + tags + ')'

        # Grab Tag totals
        cursor.execute('SELECT * FROM Tags WHERE Tag IN ' + tags)
        tag_totals = cursor.fetchall()

        # Grab Tag Transitions
        cursor.execute('SELECT * FROM Transitions WHERE Occurrences > 0 AND OriginTag IN ' + tags + ' AND DestTag IN ' + tags)
        tag_transitions = cursor.fetchall()

        # Start searching for the best path
        last_tag = None
        optimal_tags = []
        for word in vocabulary:
            # Pull the important nodes
            word_tags = get_tags_by_word(word_emissions, word)
            tag_tags = []
            optimal_tag = ''

            # Either pick the best combo or max word
            if last_tag != None:
                tag_tags = get_tags_by_tag(tag_transitions, last_tag)
                optimal_combo_value = 0
                optimal_combo_tag = ''
                transition_seen = False
                for transition_row in word_tags:
                    tag_tests = array_column_filter(tag_tags, 'DestTag', transition_row['Tag'])
                    for emission_row in tag_tests:
                        transition_seen = True
                        combo_value = emission_row['Occurrences'] * transition_row['Occurrences']
                        if combo_value > optimal_combo_value:
                            optimal_combo_tag = transition_row['Tag']
                            optimal_combo_value = combo_value
                if not transition_seen:
                    optimal_tag = get_max_word(word_tags)
                else:
                    optimal_tag = optimal_combo_tag
            else:
                optimal_tag = get_max_word(word_tags)

            # Add to list
            last_tag = optimal_tag
            optimal_tags.append(optimal_tag)

        # Format the sentence
        tagged_corpus = []
        for index in range(len(parsed_sentence)):
            tagged_corpus.append(parsed_sentence[index] + '/' + optimal_tags[index].lower())
        tagged_sentence = " ".join(tagged_corpus)

        return tagged_sentence
