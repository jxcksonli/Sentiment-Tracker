from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Post:
    source: str  # e.g. "reddit"
    url: str
    title: str
    body: str
    created_at: datetime


@dataclass(frozen=True)
class SentimentPoint:
    ts: datetime
    score: float  # -1..+1
    volume: int


def fetch_posts(topic: str, *, limit: int = 100) -> list[Post]:
    """
    TODO: Pull raw posts for a topic from your sources (Reddit, etc.).

    Return a normalized list of Post objects.
    """
    raise NotImplementedError


def score_posts(posts: list[Post]) -> list[float]:
    """
    TODO: Convert each post to a sentiment score (-1..+1).

    Keep it deterministic so debugging is easier.
    """
    raise NotImplementedError


def aggregate_overall(scores: list[float]) -> float:
    """
    TODO: Convert post scores into a single overall score.
    """
    raise NotImplementedError


def aggregate_timeseries(
    posts: list[Post], scores: list[float], *, bucket: str = "day"
) -> list[SentimentPoint]:
    """
    TODO: Build a time series for graphing (daily/hourly buckets).
    """
    raise NotImplementedError


def pick_top_sources(posts: list[Post], *, limit: int = 5) -> list[str]:
    """
    TODO: Return URLs (or ids) to show as 'top posts' on the results page.
    """
    raise NotImplementedError

