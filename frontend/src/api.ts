export interface SearchSuggestion {
  label: string;
  value: string;
  category?: string | null;
}

export interface SearchSuggestionsResponse {
  query: string;
  suggestions: SearchSuggestion[];
}

export interface SearchResponse {
  query: string;
  message: string;
}

const API_BASE = import.meta.env.VITE_API_URL ?? "";

export async function fetchSuggestions(
  query: string,
  signal?: AbortSignal,
): Promise<SearchSuggestion[]> {
  const params = new URLSearchParams({ q: query });
  const res = await fetch(`${API_BASE}/api/search/suggestions?${params}`, {
    signal,
  });
  if (!res.ok) throw new Error("Failed to fetch suggestions");
  const data: SearchSuggestionsResponse = await res.json();
  return data.suggestions;
}

export async function searchTopic(query: string): Promise<SearchResponse> {
  const res = await fetch(`${API_BASE}/api/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error("Search failed");
  return res.json();
}
