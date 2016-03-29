"""
A module for coordinating the classification of the POS in a sentence or body
of text.

The tags being used are currently those in use for the brown corpus
"""
WEIGHT_FILE = 'data/weights.csv'
DEFAULT_TRAINING_FILE = 'data/train.txt'


class POSClassifier(object):
    """
    Classifier that manages the POS Classification
    """
    weights_file = None

    def __init__(self):
        self.weights_file = open(WEIGHT_FILE, 'r+')

    def __del__(self):
        self.weights_file.close()

    def train(self, file_name = DEFAULT_TRAINING_FILE):
        """
        Takes in a training file formatted where the entire body of text is
        parsed each individual word or punctuation. On each line, there is
        also an identification stating the actual part of speech for that word.

        Args:
            file_name (str): The path to the file contain the training data
        """
        self.training_data = open(file_name)



        self.training_data.close()

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
        classification = []

        return classification
