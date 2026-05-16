"""
TruthLens - Text Preprocessing Module
NLP pipeline for cleaning and preprocessing news article text.
Optimized for TF-IDF + Naive Bayes classification.
"""

import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


class TextPreprocessor:
    """
    NLP preprocessing pipeline for fake news detection.

    Steps:
        1. Lowercase conversion
        2. URL removal
        3. HTML removal
        4. Special character removal
        5. Tokenization
        6. Stop-word removal
        7. Lemmatization
        8. Rejoin tokens
    """

    def __init__(self):

        # Load stopwords
        self.stop_words = set(stopwords.words('english'))

        # Keep important negation words
        self.important_words = {
            'not', 'no', 'nor', 'never',
            'none', 'nothing'
        }

        self.stop_words -= self.important_words

        # Lemmatizer
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text: str) -> str:
        """
        Clean raw text.
        """

        if not isinstance(text, str):
            return ""

        # Lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)

        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)

        # Remove emails
        text = re.sub(r'\S+@\S+', '', text)

        # Keep only letters
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def tokenize(self, text: str) -> list:
        """
        Convert sentence into tokens.
        """

        return word_tokenize(text)

    def remove_stopwords(self, tokens: list) -> list:
        """
        Remove unnecessary words.
        """

        return [
            token
            for token in tokens
            if token not in self.stop_words
            and len(token) > 1
        ]

    def lemmatize(self, tokens: list) -> list:
        """
        Convert words to root form.
        """

        return [
            self.lemmatizer.lemmatize(token)
            for token in tokens
        ]

    def preprocess_to_tokens(self, text: str) -> list:
        """
        Full preprocessing pipeline returning token list.
        """

        cleaned = self.clean_text(text)

        tokens = self.tokenize(cleaned)

        tokens = self.remove_stopwords(tokens)

        tokens = self.lemmatize(tokens)

        return tokens

    def preprocess(self, text: str) -> str:
        """
        Full preprocessing pipeline returning string.
        """

        tokens = self.preprocess_to_tokens(text)

        return ' '.join(tokens)

    def get_preprocessing_steps(self, text: str) -> dict:
        """
        Return preprocessing stages for frontend visualization.
        """

        original = text

        cleaned = self.clean_text(text)

        tokens = self.tokenize(cleaned)

        after_stopwords = self.remove_stopwords(tokens)

        after_lemma = self.lemmatize(after_stopwords)

        final_text = ' '.join(after_lemma)

        return {
            "original": original[:500],

            "after_cleaning": cleaned[:500],

            "tokens": tokens[:50],

            "after_stopword_removal": after_stopwords[:50],

            "after_lemmatization": after_lemma[:50],

            "final_text": final_text[:500],

            "original_word_count": len(original.split()),

            "final_word_count": len(after_lemma),

            "words_removed":
                len(original.split()) - len(after_lemma)
        }