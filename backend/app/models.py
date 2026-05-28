from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Topic to analyze")


class SearchResponse(BaseModel):
    """
    TEMPLATE — extend this with sentiment scores, sources, time series, etc.
    """

    query: str
    message: str
    # TODO: add fields like sentiment_score, sources, trend, etc.
