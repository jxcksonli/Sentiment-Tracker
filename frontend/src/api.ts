export type SentimentLabel = "positive" | "neutral" | "negative";

export interface KeywordBubble {
  word: string;
  count: number;
  sentiment: SentimentLabel;
  score?: number;
}

// Backend (current) shape: bubbles -> keyword/count/sentiment(score+label)
export interface BackendSentimentScore {
  score: number;
  label: SentimentLabel;
}

export interface BackendKeywordBubble {
  keyword: string;
  count: number;
  sentiment: BackendSentimentScore;
}

/**
 * NOTE: Backend is still being implemented.
 * This type supports both the current placeholder response (message)
 * and the bubble-cloud response (keywords) plus the backend's current (bubbles) shape.
 */
export type SearchResponse =
  | { query: string; message: string }
  | { query: string; keywords: KeywordBubble[] }
  | {
      query: string;
      bubbles: BackendKeywordBubble[];
      overall_sentiment?: BackendSentimentScore;
      sources?: string[];
      total_comments_analysed?: number;
    };

const API_BASE = import.meta.env.VITE_API_URL ?? "";

export async function searchTopic(query: string): Promise<SearchResponse> {
  const res = await fetch(`${API_BASE}/api/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error("Search failed");
  return res.json();
}
