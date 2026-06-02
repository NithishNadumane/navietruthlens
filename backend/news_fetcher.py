"""
TruthLens - Inshorts News Fetcher
Scrapes headlines from Inshorts website directly (no API key needed).
Stores them in SQLite DB for verification purposes.
"""

import requests
from bs4 import BeautifulSoup
from news_db import insert_headlines, init_db

INSHORTS_CATEGORIES = [
    'national',
    'business',
    'politics',
    'technology',
    'world',
    'science',
    'sports',
]

INSHORTS_URL = "https://inshorts.com/en/read/{category}"

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )
}


def fetch_category(category: str) -> list:
    """
    Scrape headlines for a given Inshorts category.
    Returns list of article dicts: {title, category, source, url}

    Note: Inshorts uses obfuscated CSS module class names that change
    frequently. We use the stable `itemprop="headline"` attribute instead.
    """
    url = INSHORTS_URL.format(category=category)
    articles = []

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

        # itemprop="headline" is stable across Inshorts HTML changes
        for title_el in soup.find_all('span', itemprop='headline'):
            title = title_el.get_text(strip=True)
            if not title:
                continue

            # Try to grab the source URL from a sibling/ancestor <a> tag
            parent = title_el.parent
            link_el = parent.find('a') if parent else None
            url_href = link_el['href'] if link_el and link_el.get('href') else ''

            articles.append({
                'title': title,
                'category': category,
                'source': 'Inshorts',
                'url': url_href,
            })

    except Exception as e:
        print(f"[Fetcher] Failed to fetch '{category}': {e}")

    return articles


def refresh_news_db(verbose: bool = True) -> int:
    """
    Fetch all categories and update the SQLite DB.
    Returns total number of new headlines inserted.
    """
    init_db()
    total_inserted = 0

    for category in INSHORTS_CATEGORIES:
        articles = fetch_category(category)
        inserted = insert_headlines(articles)
        total_inserted += inserted

        if verbose:
            print(
                f"[Fetcher] {category}: "
                f"fetched {len(articles)}, "
                f"new {inserted}"
            )

    if verbose:
        print(f"[Fetcher] Done. Total new headlines: {total_inserted}")

    return total_inserted


if __name__ == '__main__':
    refresh_news_db()
