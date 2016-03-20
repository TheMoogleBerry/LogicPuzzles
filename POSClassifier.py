"""
A module for coordinating the classification of the POS in a sentence or body
of text.
"""

class POSClassifier:
    """
    Classifier that manages the POS Classification
    """
    weights = []

    def train(self, file_name):
        """
        Takes a file name where each line is formatted with a single sentence, -, and
        finally followed by the classification of each work. For example a line from
        the file may be:
        The boy is happy. - Article Noun Linking_Verb Adjective

        Args:
            file_name (str): The path to the file contain the training data
        """
        training_data = open(file_name)

        training_data.close()

    def classify(self, text):
        """
        Takes a body of text and transforms it to an array of classification for each
        word in the body of text, where its position in the returned array is determined
        by its position in the text.

        Args:
            text (str): The body of text that needs to be classified

        Returns:
            str[]: The classifcation of each word in the body of text
        """
        classification = []

        return classification
