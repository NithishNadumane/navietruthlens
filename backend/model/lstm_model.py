"""
TruthLens - Naive Bayes Model Definition
Machine Learning model for fake news classification using
TF-IDF vectorization and Multinomial Naive Bayes.
"""

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


class NaiveBayesClassifier:
    """
    Naive Bayes based classifier for fake news detection.

    Architecture:
        - TF-IDF Vectorizer: Converts text into numerical feature vectors
        - Multinomial Naive Bayes: Performs probabilistic classification
    """

    def __init__(
        self,
        max_features=5000,
        ngram_range=(1, 2)
    ):

        # TF-IDF feature extractor
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range
        )

        # Naive Bayes classifier
        self.model = MultinomialNB()

    def fit(self, texts, labels):
        """
        Train the model on text data.
        """

        # Convert text → TF-IDF vectors
        X = self.vectorizer.fit_transform(texts)

        # Train Naive Bayes
        self.model.fit(X, labels)

    def predict(self, texts):
        """
        Predict labels for input texts.
        """

        X = self.vectorizer.transform(texts)

        return self.model.predict(X)

    def predict_proba(self, texts):
        """
        Return prediction probabilities.
        """

        X = self.vectorizer.transform(texts)

        return self.model.predict_proba(X)

    def save(self, model_path, vectorizer_path):
        """
        Save trained model and vectorizer.
        """

        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)

    def load(self, model_path, vectorizer_path):
        """
        Load trained model and vectorizer.
        """

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)