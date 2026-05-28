export type SentimentLabel = "positive" | "neutral" | "negative";

export interface KeywordBubble {
  word: string;
  count: number;
  sentiment: SentimentLabel;
  score?: number;
}

/**
 * NOTE: Backend is still being implemented.
 * This type supports both the current placeholder response (message)
 * and the future bubble-cloud response (keywords).
 */
export type SearchResponse =
  | { query: string; message: string }
  | { query: string; keywords: KeywordBubble[] };

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
