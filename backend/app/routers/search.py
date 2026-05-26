from fastapi import APIRouter, Query

from app.models import (
    SearchRequest,
    SearchResponse,
    SearchSuggestion,
    SearchSuggestionsResponse,
)

router = APIRouter(prefix="/search", tags=["search"])

# ---------------------------------------------------------------------------
# TEMPLATE DATA — replace with your own topic index, DB lookup, or NLP pipeline
# ---------------------------------------------------------------------------
_MOCK_TOPICS: list[SearchSuggestion] = [
    SearchSuggestion(label="Artificial Intelligence", value="artificial-intelligence", category="Topic"),
    SearchSuggestion(label="Bitcoin (BTC)", value="bitcoin", category="Ticker"),
    SearchSuggestion(label="Climate Change", value="climate-change", category="Topic"),
    SearchSuggestion(label="Consumer Inflation", value="consumer-inflation", category="Topic"),
    SearchSuggestion(label="Electric Vehicles", value="electric-vehicles", category="Topic"),
    SearchSuggestion(label="Federal Reserve", value="federal-reserve", category="Topic"),
    SearchSuggestion(label="NVIDIA (NVDA)", value="nvda", category="Ticker"),
    SearchSuggestion(label="Renewable Energy", value="renewable-energy", category="Topic"),
    SearchSuggestion(label="Semiconductor", value="semiconductor", category="Industry"),
    SearchSuggestion(label="SMT (Surface Mount Technology)", value="smt", category="Industry"),
]


def _filter_suggestions(query: str, limit: int = 8) -> list[SearchSuggestion]:
    """
    TEMPLATE — implement fuzzy matching, Elasticsearch, or your own logic here.
    """
    needle = query.strip().lower()
    if not needle:
        return []

    matches: list[tuple[int, SearchSuggestion]] = []
    for topic in _MOCK_TOPICS:
        haystack = f"{topic.label} {topic.value} {topic.category or ''}".lower()
        if needle in haystack:
            # Prefer prefix matches on label/value
            score = 0
            if topic.label.lower().startswith(needle) or topic.value.startswith(needle):
                score += 10
            if needle in topic.label.lower():
                score += 5
            matches.append((score, topic))

    matches.sort(key=lambda item: (-item[0], item[1].label))
    return [topic for _, topic in matches[:limit]]


@router.get("/suggestions", response_model=SearchSuggestionsResponse)
async def get_suggestions(
    q: str = Query("", description="Partial search text for autocomplete"),
    limit: int = Query(8, ge=1, le=20),
) -> SearchSuggestionsResponse:
    """
    Return autocomplete suggestions for the given partial query.

    TODO: Replace _filter_suggestions with real data source.
    """
    suggestions = _filter_suggestions(q, limit=limit)
    return SearchSuggestionsResponse(query=q, suggestions=suggestions)


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
