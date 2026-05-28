import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { searchTopic, type BackendKeywordBubble, type KeywordBubble } from "../api";
import WordBubbleCloud from "../components/WordBubbleCloud";

export default function ResultsPage() {
  const [params] = useSearchParams();
  const query = (params.get("q") ?? "").trim();

  const [message, setMessage] = useState<string | null>(null);
  const [keywords, setKeywords] = useState<null | KeywordBubble[]>(null);
  const [isLoading, setIsLoading] = useState(false);

  const validationMessage = useMemo(() => {
    if (query.length === 0) return "Type a topic, then search.";
    if (query.length === 1) return "Keep going — add one more character.";
    return null;
  }, [query]);

  const isPlaceholderMode = useMemo(() => {
    return message?.startsWith("TEMPLATE:") ?? false;
  }, [message]);

  useEffect(() => {
    let cancelled = false;

    async function run() {
      if (validationMessage) {
        setMessage(validationMessage);
        setKeywords(null);
        return;
      }

      setIsLoading(true);
      setMessage(null);
      setKeywords(null);

      try {
        const res = await searchTopic(query);
        if (cancelled) return;

        if ("keywords" in res) {
          setKeywords(res.keywords);
          setMessage(null);
        } else if ("bubbles" in res) {
          const mapped: KeywordBubble[] = (res.bubbles as BackendKeywordBubble[]).map(
            (b) => ({
              word: b.keyword,
              count: b.count,
              sentiment: b.sentiment.label,
              score: b.sentiment.score,
            }),
          );
          setKeywords(mapped);
          setMessage(null);
        } else {
          setKeywords(null);
          setMessage(res.message);
        }
      } catch {
        if (!cancelled) setMessage("Something went wrong. Is the backend running?");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [query, validationMessage]);

  return (
    <div className="app__results">
      <div className="app__results-top">
        <Link className="app__back" to="/">
          ← Back
        </Link>
        <div className="app__query">
          <div className="app__query-label">Topic</div>
          <div className="app__query-value">{query || "—"}</div>
        </div>
      </div>

      {keywords && keywords.length > 0 ? (
        <div className="results-grid">
          <div className="glass-card glass-card--chart">
            <div className="glass-card__header">
              <div className="glass-card__label">Word cloud</div>
              <div className="glass-card__chip">size = frequency • color = sentiment</div>
            </div>
            <div style={{ marginTop: "0.85rem" }}>
              <WordBubbleCloud keywords={keywords} />
            </div>
          </div>
        </div>
      ) : isPlaceholderMode ? (
        <div className="results-grid">
          <div className="glass-card glass-card--metric">
            <div className="glass-card__label">Overall mood</div>
            <div className="glass-card__value">—</div>
            <div className="glass-card__sub">Waiting for live signals</div>
          </div>

          <div className="glass-card glass-card--metric">
            <div className="glass-card__label">Sentiment rating</div>
            <div className="glass-card__value">—</div>
            <div className="glass-card__sub">Score will appear here</div>
          </div>

          <div className="glass-card glass-card--chart">
            <div className="glass-card__header">
              <div className="glass-card__label">Trend</div>
              <div className="glass-card__chip">Last 7 days</div>
            </div>
            <div className="chart-skeleton" aria-hidden="true" />
          </div>

          <div className="glass-card glass-card--sources">
            <div className="glass-card__header">
              <div className="glass-card__label">Sources</div>
              <div className="glass-card__chip">HackerNews</div>
            </div>
            <ul className="sources-skeleton" aria-hidden="true">
              <li />
              <li />
              <li />
              <li />
            </ul>
          </div>

          <div className="app__result" role="status">
            Results will show here once your backend is hooked up.
          </div>
        </div>
      ) : (
        <div className="app__result" role="status">
          {isLoading ? "Loading…" : message ?? "—"}
        </div>
      )}
    </div>
  );
}

