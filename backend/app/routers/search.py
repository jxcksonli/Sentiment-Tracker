from fastapi import APIRouter
import httpx
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.models import (
    SearchRequest,
    SearchResponse,
    SentimentScore,
    KeywordBubble,
)

router = APIRouter(prefix="/search", tags=["search"])

@router.post("", response_model=SearchResponse)
async def search_topic(body: SearchRequest) -> SearchResponse:
    """
    Run a full sentiment search for a topic.
    TODO: Wire up HackerNews ingestion, keyword extraction, and sentiment scoring.
    """

    comments = await fetch_hackernews_comments(body.query)
    bubbles = extract_bubbles(comments)
    overall_sentiment = calculate_overall_sentiment(comments)

    return SearchResponse(
        query=body.query,
        bubbles=bubbles,
        overall_sentiment=overall_sentiment,
        sources=["hackernews"],
        total_comments_analysed=len(comments),
    )

async def fetch_hackernews_comments(query: str, max_results: int = 100) -> list[str]:
    """
    Fetch comments from HackerNews via Algolia Search API.
    Returns a list of comment texts.
    """
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": query,
        "tags": "comment",
        "hitsPerPage": max_results,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        comments = [hit["comment_text"] for hit in data.get("hits", []) if hit.get("comment_text")]
    return comments

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "is", "it", "this", "that", "was", "are",
    "be", "as", "by", "from", "have", "has", "had", "not", "they",
    "you", "we", "i", "he", "she", "its", "his", "her", "their",
    "what", "which", "who", "will", "would", "could", "should",
    "there", "been", "more", "also", "when", "about", "up", "out",
    "lol", "lmao", "rofl", "omg", "wtf", "idk", "smh", "tbh", "fwiw",
    "imho", "afaik", "brb", "btw", "ftw", "gg", "np", "thx", "ty",
    "yw", "afk", "bff", "cya", "gr8", "hbu", "jk", "k", "nvm", "sry", "w/", "w/o",}

def extract_bubbles(comments: list[str], top_n: int = 10) -> list[str]:
    """
    Extract top keywords from comments, score each one, and return as a list of KeywordBubble Objects
    """
    word_freq = {}
    for comment in comments:
        words = comment.lower().split() # Split comment into words and convert to lowercase
        for word in words:
            cleaned_word = ''.join(char for char in word if char.isalnum())
            if cleaned_word and cleaned_word not in STOPWORDS: # Filter out stopwords and empty strings
                word_freq[cleaned_word] = word_freq.get(cleaned_word, 0) + 1

    sorted_words = sorted(word_freq.items(), key=lambda item: item[1], reverse=True) # Sort words by frequency
    top_keywords = [word for word, freq in sorted_words[:top_n]]

    bubbles = []
    for keyword, count in top_keywords:
        sentiment = calculate_sentiment_for_keyword(keyword, comments)
        bubbles.append(KeywordBubble(keyword=keyword, count=count, sentiment=sentiment))

    return bubbles

analyser = SentimentIntensityAnalyzer()

def calculate_sentiment_for_keyword(keyword: str, comments: list[str]) -> SentimentScore:
    """
    Calculate a sentiment score for a given keyword based on the comments it appears in.
    """
    scores = analyser.polarity_scores(keyword)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return SentimentScore(score=round(compound, 3), label=label)

def calculate_overall_sentiment(comments: list[str]) -> SentimentScore:
    """
    Calculate overall sentiment by averaging scores across all comments.
    """

    if not comments:
        return SentimentScore(score=0.0, label="neutral")
    
    total_score = sum(b.count for b in comments)
    weighted_score = sum(calculate_sentiment_for_keyword(b.keyword, comments).score * b.count for b in extract_bubbles(comments))
    average_score = weighted_score / total_score if total_score > 0 else 0.

    if average_score >= 0.05:
        label = "positive"
    elif average_score <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return SentimentScore(score=round(average_score, 3), label=label)
