from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import search

app = FastAPI(
    title="Sentiment Tracker API",
    description="Backend template — implement sentiment analysis and data sources here.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
