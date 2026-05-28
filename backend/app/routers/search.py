from fastapi import APIRouter

from app.models import (
    SearchRequest,
    SearchResponse,
    SentimentScore,
)
from app.hn_pipeline import (
    build_bubbles,
    calculate_overall_sentiment,
    fetch_hn_comment_texts,
)

router = APIRouter(prefix="/search", tags=["search"])

@router.post("", response_model=SearchResponse)
async def search_topic(body: SearchRequest) -> SearchResponse:
    """
    Run a full sentiment search for a topic.
    """
    comment_texts = await fetch_hn_comment_texts(body.query)
    bubbles = build_bubbles(comment_texts)
    overall_sentiment = calculate_overall_sentiment(bubbles)
    total = len(comment_texts)
    return SearchResponse(
        query=body.query,
        bubbles=bubbles,
        overall_sentiment=overall_sentiment,
        sources=["hackernews"],
        total_comments_analysed=total,
    )