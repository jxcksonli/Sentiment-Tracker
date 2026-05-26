import { useCallback, useRef, useState } from "react";
import { searchTopic } from "../api";
import "./SearchBar.css";

interface SearchBarProps {
  onSearchResult?: (message: string) => void;
}

export default function SearchBar({ onSearchResult }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const runSearch = useCallback(
    async (value: string) => {
      const trimmed = value.trim();
      if (!trimmed) return;
      if (trimmed.length === 1) {
        onSearchResult?.("Keep going — add one more character.");
        return;
      }

      setQuery(trimmed);
      setIsSearching(true);

      try {
        const result = await searchTopic(trimmed);
        onSearchResult?.(result.message);
      } catch {
        onSearchResult?.("Something went wrong. Is the backend running?");
      } finally {
        setIsSearching(false);
      }
    },
    [onSearchResult],
  );

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
        {isSearching && <span className="search-bar__spinner" aria-hidden="true" />}

        <button
          type="button"
          className="search-bar__button"
          onClick={() => runSearch(query)}
          disabled={isSearching || query.trim().length === 0}
        >
          Search
        </button>
      </div>
    </div>
  );
}
