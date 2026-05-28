from fastapi import APIRouter

from app.models import (
    SearchRequest,
    SearchResponse,
)

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search_topic(body: SearchRequest) -> SearchResponse:
    """
    Run a full sentiment search for a topic.

    TODO: Wire up NLP pipeline, data ingestion, and scoring here.
    """
    return SearchResponse(
        query=body.query,
        message=(
            f"TEMPLATE: sentiment analysis for '{body.query}' not yet implemented. "
            "Connect your backend logic in app/routers/search.py."
        ),
    )
