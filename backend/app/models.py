from pydantic import BaseModel, Field
from typing import Literal, List
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Topic to analyse")
class SentimentScore(BaseModel):
    score: float # -1 to 1
    label: Literal["positive", "negative", "neutral"]
class KeywordBubble(BaseModel):
    keyword: str
    count: int # Controls bubble size
    sentiment: SentimentScore # Controls bubble colour
class SearchResponse(BaseModel):
    query: str
    bubbles: List[KeywordBubble]
    overall_sentiment: SentimentScore # From bubbles
    sources: List[str]
    total_comments_analysed: int