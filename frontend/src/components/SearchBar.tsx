import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SearchBar.css";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const wrapperRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const runSearch = (value: string) => {
    const trimmed = value.trim();
    if (!trimmed) return;
    if (trimmed.length === 1) {
      setError("Keep going — add one more character.");
      return;
    }
    setError(null);
    navigate(`/search?q=${encodeURIComponent(trimmed)}`);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      runSearch(query);
    }
  };

  return (
    <div className="search-bar" ref={wrapperRef}>
      <div className="search-bar__input-wrap">
        <svg
          className="search-bar__icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          aria-hidden="true"
        >
          <circle cx="11" cy="11" r="7" />
          <path d="M20 20l-3.5-3.5" />
        </svg>
        <input
          ref={inputRef}
          type="search"
          className="search-bar__input"
          placeholder="What are peoples thoughts on..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          aria-label="Search topics"
          autoComplete="off"
        />

        <button
          type="button"
          className="search-bar__button"
          onClick={() => runSearch(query)}
          disabled={query.trim().length === 0}
        >
          Search
        </button>
      </div>

      {error && (
        <div className="search-bar__error" role="status">
          {error}
        </div>
      )}
    </div>
  );
}
