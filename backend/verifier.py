"""
TruthLens - Headline Verifier
Compares user input against the DB of real verified headlines
using TF-IDF cosine similarity.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from news_db import get_all_headlines


# Thresholds
MATCH_THRESHOLD   = 0.60   # >= this → likely verified real news
PARTIAL_THRESHOLD = 0.35   # >= this → partial match / related news found
RELATED_THRESHOLD = 0.15   # >= this → loosely related (used for similar_count only)


def verify_headline(query: str) -> dict:
    """
    Compare query against all stored headlines using TF-IDF cosine similarity.

    Returns:
        {
          "verified": bool,
          "match_score": float (0-100),
          "best_match": str or None,
          "status": "VERIFIED" | "PARTIAL" | "UNVERIFIED",
          "db_count": int,
          "similar_count": int   -- # of DB headlines loosely related to query
        }

    NOTE: similar_count is purely informational and does NOT affect
          verified, match_score, or status.
    """
    headlines = get_all_headlines()

    if not headlines:
        return {
            "verified": False,
            "match_score": 0.0,
            "best_match": None,
            "status": "NO_DB",
            "db_count": 0,
            "similar_count": 0,
        }

    # Build TF-IDF corpus: all headlines + user query at end
    corpus = headlines + [query]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words='english',
        max_features=10000
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except Exception:
        return {
            "verified": False,
            "match_score": 0.0,
            "best_match": None,
            "status": "ERROR",
            "db_count": len(headlines),
            "similar_count": 0,
        }

    # Query vector is the last row
    query_vec = tfidf_matrix[-1]
    headline_vecs = tfidf_matrix[:-1]

    # Compute cosine similarity of query vs all headlines
    scores = cosine_similarity(query_vec, headline_vecs).flatten()

    best_idx   = int(scores.argmax())
    best_score = float(scores[best_idx])
    best_match = headlines[best_idx]

    # --- Verdict (unchanged logic) ---
    if best_score >= MATCH_THRESHOLD:
        status   = "VERIFIED"
        verified = True
    elif best_score >= PARTIAL_THRESHOLD:
        status   = "PARTIAL"
        verified = False
    else:
        status   = "UNVERIFIED"
        verified = False

    # --- Informational: count loosely related headlines ---
    similar_count = int((scores >= RELATED_THRESHOLD).sum())

    return {
        "verified":      verified,
        "match_score":   round(best_score * 100, 1),
        "best_match":    best_match if best_score >= PARTIAL_THRESHOLD else None,
        "status":        status,
        "db_count":      len(headlines),
        "similar_count": similar_count,
    }

