from pydantic import BaseModel, Field


class SearchSuggestion(BaseModel):
    """A single autocomplete suggestion."""

    label: str = Field(..., description="Display text shown in the dropdown")
    value: str = Field(..., description="Canonical topic value used for search")
    category: str | None = Field(
        default=None,
        description="Optional grouping, e.g. 'Industry', 'Ticker', 'Topic'",
    )


class SearchSuggestionsResponse(BaseModel):
    query: str
    suggestions: list[SearchSuggestion]


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Topic to analyze")


class SearchResponse(BaseModel):
    """
    TEMPLATE — extend this with sentiment scores, sources, time series, etc.
    """

    query: str
    message: str
    # TODO: add fields like sentiment_score, sources, trend, etc.
