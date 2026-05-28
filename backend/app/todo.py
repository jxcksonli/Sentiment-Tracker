from __future__ import annotations

import httpx

from app.models import KeywordBubble, SentimentScore
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


_analyser = SentimentIntensityAnalyzer()

# Stop words for sentiment analysis
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "is", "it", "this", "that", "was", "are",
    "be", "as", "by", "from", "have", "has", "had", "not", "they",
    "you", "we", "i", "he", "she", "its", "his", "her", "their",
    "what", "which", "who", "will", "would", "could", "should",
    "there", "been", "more", "also", "when", "about", "up", "out",
    "lol", "lmao", "rofl", "omg", "wtf", "idk", "smh", "tbh", "fwiw",
    "imho", "afaik", "brb", "btw", "ftw", "gg", "np", "thx", "ty",
    "yw", "afk", "bff", "cya", "gr8", "hbu", "jk", "k", "nvm", "sry", "w/", "w/o",
}

async def fetch_hn_comment_texts(topic: str, *, hits_per_page: int = 100) -> list[str]:
    """
    Fetch comments from HackerNews via Algolia Search API.
    Returns a list of comment texts strings.

    Endpoint:
      https://hn.algolia.com/api/v1/search?query=<topic>&tags=comment
    """
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": topic,
        "tags": "comment",
        "hitsPerPage": hits_per_page,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        comments = [hit["comment_text"] for hit in data.get("hits", []) if hit.get("comment_text")]
    return comments


def tokenize(text: str) -> list[str]:
    """Lowercase + split into words (clean punctuation)"""
    words = text.lower().split()
    cleaned: list[str] = []
    for word in words:
        cleaned_word = "".join(char for char in word if char.isalnum())
        if cleaned_word:
            cleaned.append(cleaned_word)
    return cleaned

def remove_stopwords(tokens: list[str]) -> list[str]:
    """Remove common words like 'the', 'and', 'is', etc"""
    return [t for t in tokens if t and t not in STOPWORDS]

def top_keywords(comment_texts: list[str], *, top_n: int = 60) -> list[tuple[str, int]]:
    """Return top N (word, count) pairs"""
    word_freq: dict[str, int] = {}
    for comment in comment_texts:
        tokens = remove_stopwords(tokenize(comment))
        for token in tokens:
            word_freq[token] = word_freq.get(token, 0) + 1

    sorted_words = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)
    return sorted_words[:top_n]

def label_sentiment_for_word(word: str) -> SentimentScore:
    """Return a SentimentScore for the word using VADER sentiment analysis"""
    scores = _analyser.polarity_scores(word)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return SentimentScore(score=round(compound, 3), label=label)

# Restored name from your original search.py (kept for familiarity)
def calculate_sentiment_for_keyword(keyword: str, comments: list[str]) -> SentimentScore:
    """
    Calculate a sentiment score for a given keyword based on the comments it appears in.
    Maybe improve this later to consider the context around the keyword, but for now just score the keyword itself.
    """
    return label_sentiment_for_word(keyword)


def extract_bubbles(comments: list[str], top_n: int = 10) -> list[KeywordBubble]:
    """
    Extract top keywords from comments, score each one, and return as KeywordBubble objects.
    """
    pairs = top_keywords(comments, top_n=top_n)

    bubbles: list[KeywordBubble] = []
    for keyword, count in pairs:
        sentiment = calculate_sentiment_for_keyword(keyword, comments)
        bubbles.append(KeywordBubble(keyword=keyword, count=count, sentiment=sentiment))

    return bubbles

def build_bubbles(comment_texts: list[str], *, top_n: int = 60) -> list[KeywordBubble]:
    """
    Build bubbles for the UI.
    """
    return extract_bubbles(comment_texts, top_n=top_n)


def calculate_overall_sentiment(bubbles: list[KeywordBubble]) -> SentimentScore:
    """
    Calculate overall sentiment by averaging bubble sentiment scores weighted by count.
    """
    if not bubbles:
        return SentimentScore(score=0.0, label="neutral")

    total = sum(b.count for b in bubbles)
    weighted = sum(b.sentiment.score * b.count for b in bubbles)
    average_score = weighted / total if total > 0 else 0.0

    if average_score >= 0.05:
        label = "positive"
    elif average_score <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return SentimentScore(score=round(average_score, 3), label=label)