from fastapi import APIRouter
import httpx``

from app.models import (
    SearchRequest,
    SearchResponse,
    SentimentScore,
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

def extract_bubbles(comments: list[str]) -> list[str]:
    """
    Extract top keywords from comments, score each one, and return as a list of KeywordBubble Objects
    """