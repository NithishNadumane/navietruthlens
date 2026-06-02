"""
TruthLens - Dual Model Training Script
Trains TWO Naive Bayes models from the same dataset:
  1. Article model  → uses title + full text  → saved as naive_bayes_article.pkl
  2. Headline model → uses title only         → saved as naive_bayes_headline.pkl

The article model is also saved as naive_bayes.pkl (backward compatibility).

Usage:
    python train.py
"""

import os
import json
import time
import joblib

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from model.preprocess import TextPreprocessor


# =========================
# Configuration
# =========================

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'data', 'dataset.csv')
SAVE_DIR     = os.path.join(os.path.dirname(__file__), 'saved_model')
TEST_SIZE    = 0.2
RANDOM_STATE = 42
MAX_FEATURES = 5000


def load_dataset():
    """Load and validate the dataset. Returns the full DataFrame."""
    print("[1/6] Loading dataset...")

    if not os.path.exists(DATASET_PATH):
        print(f"\n[ERROR] Dataset not found: {DATASET_PATH}")
        print("  -> Download Fake.csv and True.csv from:")
        print("     https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        print("  -> Place them in backend/data/")
        print("  -> Run: python download_dataset.py")
        return None

    df = pd.read_csv(DATASET_PATH)

    required_cols = ['title', 'text', 'label']
    for col in required_cols:
        if col not in df.columns:
            print(f"[ERROR] Missing column: {col}")
            return None

    # Remove rows with missing title or text
    df = df.dropna(subset=['title', 'text'])

    # Shuffle
    df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

    print(f"  Total samples : {len(df)}")
    print(f"  Fake          : {len(df[df.label == 1])}")
    print(f"  Real          : {len(df[df.label == 0])}")

    return df


def preprocess_texts(texts: list, preprocessor: TextPreprocessor, label: str) -> list:
    """Run the NLP preprocessing pipeline on a list of texts."""
    print(f"[2/6] Preprocessing {label} texts...")
    processed = []
    for i, text in enumerate(texts):
        processed.append(preprocessor.preprocess(str(text)))
        if (i + 1) % 5000 == 0:
            print(f"  Processed {i + 1}/{len(texts)}...")
    return processed


def train_and_evaluate(X_train, X_test, y_train, y_test, label: str) -> tuple:
    """Train a MultinomialNB and return (model, metrics_dict)."""
    print(f"[4/6] Training {label} model...")
    model = MultinomialNB()
    model.fit(X_train, y_train)

    print(f"[5/6] Evaluating {label} model...")
    predictions = model.predict(X_test)

    accuracy  = accuracy_score(y_test, predictions)  * 100
    precision = precision_score(y_test, predictions) * 100
    recall    = recall_score(y_test, predictions)    * 100
    f1        = f1_score(y_test, predictions)        * 100
    cm        = confusion_matrix(y_test, predictions)

    print(f"\n  === {label} Results ===")
    print(f"  Accuracy  : {accuracy:.2f}%")
    print(f"  Precision : {precision:.2f}%")
    print(f"  Recall    : {recall:.2f}%")
    print(f"  F1 Score  : {f1:.2f}%")
    print(f"  TN={cm[0][0]} FP={cm[0][1]} FN={cm[1][0]} TP={cm[1][1]}")

    metrics = {
        "accuracy"         : round(accuracy, 2),
        "precision"        : round(precision, 2),
        "recall"           : round(recall, 2),
        "f1_score"         : round(f1, 2),
        "confusion_matrix" : {
            "true_positive"  : int(cm[1][1]),
            "true_negative"  : int(cm[0][0]),
            "false_positive" : int(cm[0][1]),
            "false_negative" : int(cm[1][0]),
        },
        "training_samples" : int(X_train.shape[0]),
        "test_samples"     : int(X_test.shape[0]),
        "model_architecture": {
            "type"        : "TF-IDF + Multinomial Naive Bayes",
            "max_features": MAX_FEATURES,
            "ngram_range" : "(1, 2)",
            "input"       : label,
        },
        "dataset" : "Kaggle Fake News Dataset",
        "mode"    : "trained",
    }
    return model, metrics


def vectorize(processed_texts: list, label: str):
    """Fit a TF-IDF vectorizer on processed texts. Returns (vectorizer, X)."""
    print(f"[3/6] Vectorizing {label} texts (TF-IDF)...")

    vectorizer = TfidfVectorizer(
        max_features = MAX_FEATURES,
        ngram_range  = (1, 2),    # unigrams + bigrams
        stop_words   = 'english',
        max_df       = 0.7,
        min_df       = 2,
        dtype        = 'float32',
    )
    X = vectorizer.fit_transform(processed_texts)
    print(f"  TF-IDF shape: {X.shape}")
    return vectorizer, X


def save_model(model, vectorizer, metrics, model_filename, vec_filename, metrics_filename):
    """Persist model, vectorizer, and metrics to disk."""
    os.makedirs(SAVE_DIR, exist_ok=True)

    joblib.dump(model,      os.path.join(SAVE_DIR, model_filename))
    joblib.dump(vectorizer, os.path.join(SAVE_DIR, vec_filename))

    with open(os.path.join(SAVE_DIR, metrics_filename), 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"[6/6] Saved → {model_filename}, {vec_filename}, {metrics_filename}")


def main():
    print("=" * 60)
    print(" TruthLens — Dual Model Training (Article + Headline)")
    print("=" * 60)

    start = time.time()

    # --- Load ---
    df = load_dataset()
    if df is None:
        return

    preprocessor = TextPreprocessor()
    labels       = df['label'].values

    # ================================================================
    # MODEL 1: ARTICLE  (title + body)
    # ================================================================
    print("\n" + "─" * 40)
    print(" Training ARTICLE model (title + body)")
    print("─" * 40)

    article_texts = (
        df['title'].astype(str) + ' ' + df['text'].astype(str)
    ).tolist()

    proc_article = preprocess_texts(article_texts, preprocessor, "article")
    vec_article, X_article = vectorize(proc_article, "article")

    X_tr_a, X_te_a, y_tr, y_te = train_test_split(
        X_article, labels,
        test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=labels
    )

    model_article, metrics_article = train_and_evaluate(X_tr_a, X_te_a, y_tr, y_te, "Article")

    save_model(
        model_article, vec_article, metrics_article,
        'naive_bayes_article.pkl', 'tfidf_article.pkl', 'metrics_article.json'
    )
    # Backward-compat alias
    save_model(
        model_article, vec_article, metrics_article,
        'naive_bayes.pkl', 'tfidf.pkl', 'metrics.json'
    )

    # ================================================================
    # MODEL 2: HEADLINE  (title only — no stop-word removal in TF-IDF)
    # ================================================================
    print("\n" + "─" * 40)
    print(" Training HEADLINE model (title only)")
    print("─" * 40)

    headline_texts = df['title'].astype(str).tolist()

    # For headlines, preprocess without stop-word removal
    # (headlines are short — removing words hurts more than helps)
    print("[2/6] Preprocessing headline texts (lemmatize-only)...")
    proc_headlines = []
    for i, text in enumerate(headline_texts):
        cleaned = preprocessor.clean_text(text)
        tokens  = preprocessor.tokenize(cleaned)
        tokens  = preprocessor.lemmatize(tokens)
        proc_headlines.append(' '.join(tokens))

    print("[3/6] Vectorizing headline texts (TF-IDF, no stop_words filter)...")
    vec_headline = TfidfVectorizer(
        max_features = MAX_FEATURES,
        ngram_range  = (1, 2),
        # No stop_words here — headlines are already short
        max_df       = 0.85,   # slightly more lenient for short texts
        min_df       = 1,      # lower min_df since fewer words per doc
        dtype        = 'float32',
    )
    X_headline = vec_headline.fit_transform(proc_headlines)
    print(f"  TF-IDF shape: {X_headline.shape}")

    X_tr_h, X_te_h, y_tr_h, y_te_h = train_test_split(
        X_headline, labels,
        test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=labels
    )

    model_headline, metrics_headline = train_and_evaluate(
        X_tr_h, X_te_h, y_tr_h, y_te_h, "Headline"
    )

    save_model(
        model_headline, vec_headline, metrics_headline,
        'naive_bayes_headline.pkl', 'tfidf_headline.pkl', 'metrics_headline.json'
    )

    # ================================================================
    # Summary
    # ================================================================
    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f" Training complete in {elapsed / 60:.2f} minutes")
    print(f" Article  model accuracy : {metrics_article['accuracy']}%")
    print(f" Headline model accuracy : {metrics_headline['accuracy']}%")
    print(f" Models saved to        : {SAVE_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()