"""
TruthLens - Bulk Headline Fetcher
==================================
Scrapes headlines from multiple reliable sources using RSS feeds
and the existing Inshorts scraper to populate the DB with 400+ entries.

Sources:
  - BBC News (RSS)            ~30 headlines
  - Reuters (RSS)             ~30 headlines
  - Al Jazeera (RSS)          ~30 headlines
  - The Hindu (RSS)           ~30 headlines
  - NDTV (RSS)                ~30 headlines
  - Times of India (RSS)      ~30 headlines
  - India Today (RSS)         ~30 headlines
  - NPR News (RSS)            ~30 headlines
  - CNN (RSS)                 ~30 headlines
  - Google News Top Stories   ~20 headlines
  - Inshorts (HTML scrape)    ~70 headlines (7 categories × ~10 each)

Run:
    cd backend
    python bulk_fetch.py
"""

import sys
import os
import time

# Force UTF-8 output on Windows to avoid cp1252 codec errors
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Make sure sibling modules (news_db, news_fetcher) are importable
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))

from news_db import init_db, insert_headlines, get_headline_count
from news_fetcher import refresh_news_db   # reuse existing Inshorts fetcher


# ---------------------------------------------------------------------------
# RSS Feed Sources
# Each entry: (friendly_name, rss_url, source_label)
# ---------------------------------------------------------------------------

RSS_FEEDS = [
    # International
    ("BBC News - Top Stories",
     "http://feeds.bbci.co.uk/news/rss.xml",
     "BBC News"),

    ("BBC News - World",
     "http://feeds.bbci.co.uk/news/world/rss.xml",
     "BBC News"),

    ("BBC News - Technology",
     "http://feeds.bbci.co.uk/news/technology/rss.xml",
     "BBC News"),

    ("Reuters - Top News",
     "https://feeds.reuters.com/reuters/topNews",
     "Reuters"),

    ("Reuters - World News",
     "https://feeds.reuters.com/Reuters/worldNews",
     "Reuters"),

    ("Reuters - Business",
     "https://feeds.reuters.com/reuters/businessNews",
     "Reuters"),

    ("Al Jazeera - All News",
     "https://www.aljazeera.com/xml/rss/all.xml",
     "Al Jazeera"),

    ("NPR - Top Stories",
     "https://feeds.npr.org/1001/rss.xml",
     "NPR"),

    ("NPR - World",
     "https://feeds.npr.org/1004/rss.xml",
     "NPR"),

    ("CNN - Top Stories",
     "http://rss.cnn.com/rss/edition.rss",
     "CNN"),

    ("CNN - World",
     "http://rss.cnn.com/rss/edition_world.rss",
     "CNN"),

    ("CNN - Technology",
     "http://rss.cnn.com/rss/edition_technology.rss",
     "CNN"),

    # Indian Sources
    ("The Hindu - News",
     "https://www.thehindu.com/news/feeder/default.rss",
     "The Hindu"),

    ("The Hindu - National",
     "https://www.thehindu.com/news/national/feeder/default.rss",
     "The Hindu"),

    ("The Hindu - International",
     "https://www.thehindu.com/news/international/feeder/default.rss",
     "The Hindu"),

    ("The Hindu - Business",
     "https://www.thehindu.com/business/feeder/default.rss",
     "The Hindu"),

    ("NDTV - Latest",
     "https://feeds.feedburner.com/ndtvnews-latest",
     "NDTV"),

    ("NDTV - India",
     "https://feeds.feedburner.com/ndtvnews-india-news",
     "NDTV"),

    ("NDTV - World",
     "https://feeds.feedburner.com/ndtvnews-world-news",
     "NDTV"),

    ("Times of India - Top Stories",
     "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
     "Times of India"),

    ("Times of India - India",
     "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
     "Times of India"),

    ("Times of India - World",
     "https://timesofindia.indiatimes.com/rssfeeds/296589545.cms",
     "Times of India"),

    ("Times of India - Business",
     "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
     "Times of India"),

    ("India Today - Latest",
     "https://www.indiatoday.in/rss/home",
     "India Today"),

    ("India Today - India",
     "https://www.indiatoday.in/rss/1206578",
     "India Today"),

    ("India Today - World",
     "https://www.indiatoday.in/rss/1206614",
     "India Today"),

    # Tech & Science
    ("TechCrunch",
     "https://techcrunch.com/feed/",
     "TechCrunch"),

    ("Wired",
     "https://www.wired.com/feed/rss",
     "Wired"),

    ("Ars Technica",
     "https://feeds.arstechnica.com/arstechnica/index",
     "Ars Technica"),

    # Google News
    ("Google News - Top",
     "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
     "Google News"),

    ("Google News - World",
     "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN:en",
     "Google News"),

    ("Google News - Business",
     "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TWpRU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN:en",
     "Google News"),

    ("Google News - Technology",
     "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN:en",
     "Google News"),

    ("Google News - Science",
     "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN:en",
     "Google News"),
]


HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
}

REQUEST_TIMEOUT = 12   # seconds per feed
SLEEP_BETWEEN  = 0.3   # seconds between requests (polite crawling)
TARGET_TOTAL   = 400   # stop early if we hit this


# ---------------------------------------------------------------------------
# RSS Parser
# ---------------------------------------------------------------------------

def _extract_title_from_item(item) -> str:
    """Pull the <title> text from an RSS <item> element."""
    title_el = item.find('title')
    if title_el is None:
        return ''
    # Google News wraps titles in CDATA; ET handles that automatically
    return (title_el.text or '').strip()


def fetch_rss_feed(name: str, url: str, source: str) -> list:
    """
    Fetch an RSS feed and return a list of article dicts compatible
    with news_db.insert_headlines().

    Returns [] on any error so the caller can continue.
    """
    articles = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        # Parse XML
        root = ET.fromstring(resp.content)

        # Standard RSS 2.0: /rss/channel/item  or  /channel/item
        items = root.findall('.//item')

        for item in items:
            title = _extract_title_from_item(item)
            if not title or len(title) < 10:
                continue

            # Remove source attribution appended by Google News e.g. " - Reuters"
            if ' - ' in title:
                title = title.rsplit(' - ', 1)[0].strip()

            # Skip very short titles after cleanup
            if len(title) < 10:
                continue

            # Try to grab link
            link_el = item.find('link')
            link = (link_el.text or '').strip() if link_el is not None else ''

            # Try to infer category from feed name
            cat = 'general'
            name_lower = name.lower()
            for kw in ('world', 'india', 'national', 'business', 'technology',
                       'tech', 'science', 'sports', 'politics'):
                if kw in name_lower:
                    cat = kw
                    break

            articles.append({
                'title':    title,
                'category': cat,
                'source':   source,
                'url':      link,
            })

    except ET.ParseError:
        # Try BeautifulSoup as XML fallback (handles malformed feeds)
        articles = _fetch_rss_bs4(url, source, name)
    except requests.exceptions.RequestException as e:
        print(f"  [SKIP] {name}: network error — {e}")
    except Exception as e:
        print(f"  [SKIP] {name}: unexpected error — {e}")

    return articles


def _fetch_rss_bs4(url: str, source: str, name: str) -> list:
    """Fallback RSS parser using BeautifulSoup for malformed feeds."""
    articles = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'xml')

        for item in soup.find_all('item'):
            title_tag = item.find('title')
            title = title_tag.get_text(strip=True) if title_tag else ''
            if not title or len(title) < 10:
                continue

            if ' - ' in title:
                title = title.rsplit(' - ', 1)[0].strip()

            link_tag = item.find('link')
            link = link_tag.get_text(strip=True) if link_tag else ''

            cat = 'general'
            for kw in ('world', 'india', 'national', 'business', 'technology',
                       'tech', 'science', 'sports', 'politics'):
                if kw in name.lower():
                    cat = kw
                    break

            articles.append({
                'title':    title,
                'category': cat,
                'source':   source,
                'url':      link,
            })
    except Exception as e:
        print(f"  [SKIP-BS4] {name}: {e}")

    return articles


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def bulk_fetch(target: int = TARGET_TOTAL) -> int:
    """
    Fetch headlines from all RSS sources + Inshorts until `target` is reached.
    Returns the number of new headlines inserted in this run.
    """
    print("=" * 60)
    print(f"  TruthLens — Bulk Headline Fetcher")
    print(f"  Target: {target} total headlines in DB")
    print("=" * 60)

    # Ensure DB is initialised
    init_db()

    before = get_headline_count()
    print(f"\n[DB] Headlines before run : {before}")

    if before >= target:
        print(f"[DB] Already have {before} headlines — target met. Exiting.")
        return 0

    total_new = 0

    # ------------------------------------------------------------------
    # Step 1: Inshorts (HTML scraper — already implemented)
    # ------------------------------------------------------------------
    print("\n-- Step 1/2 : Inshorts HTML scraper --")
    try:
        inshorts_new = refresh_news_db(verbose=True)
        total_new += inshorts_new
        print(f"  Inshorts inserted: {inshorts_new}")
    except Exception as e:
        print(f"  [WARN] Inshorts failed: {e}")

    # ------------------------------------------------------------------
    # Step 2: RSS Feeds
    # ------------------------------------------------------------------
    print("\n-- Step 2/2 : RSS feeds --")

    for name, url, source in RSS_FEEDS:
        current = get_headline_count()
        if current >= target:
            print(f"\n[DB] Reached {current} headlines — target met. Stopping early.")
            break

        articles = fetch_rss_feed(name, url, source)
        inserted = insert_headlines(articles) if articles else 0
        total_new += inserted

        status = f"fetched {len(articles):>3}, new {inserted:>3}"
        print(f"  {source:<20} | {name:<40} | {status}")

        time.sleep(SLEEP_BETWEEN)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    after = get_headline_count()
    print("\n" + "=" * 60)
    print(f"  Run complete.")
    print(f"  Headlines before : {before}")
    print(f"  Headlines after  : {after}")
    print(f"  New this run     : {after - before}")
    print(f"  Target           : {target}")

    if after >= target:
        print(f"  [OK] Target reached!")
    else:
        print(f"  [WARN] Only {after} fetched -- some feeds may be down.")
        print(f"         Re-run the script to retry failed sources.")
    print("=" * 60)

    return after - before


if __name__ == '__main__':
    bulk_fetch(target=TARGET_TOTAL)
