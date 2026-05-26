import { useState } from "react";
import SearchBar from "./components/SearchBar";
import "./App.css";

export default function App() {
  const [resultMessage, setResultMessage] = useState<string | null>(null);

  return (
    <div className="app">
      <div className="app__glow app__glow--sun" aria-hidden="true" />
      <div className="app__glow app__glow--horizon" aria-hidden="true" />
      <div
        className="app__bubble"
        aria-hidden="true"
        style={{
          top: "12%",
          left: "8%",
          width: "170px",
          height: "170px",
          animationDelay: "-7s",
          animationDuration: "22s",
          ["--bubble-opacity" as any]: 0.55,
          ["--bubble-blur" as any]: "20px",
        }}
      />
      <div
        className="app__bubble"
        aria-hidden="true"
        style={{
          top: "28%",
          right: "10%",
          width: "120px",
          height: "120px",
          animationDelay: "-3s",
          animationDuration: "26s",
          ["--bubble-opacity" as any]: 0.4,
          ["--bubble-blur" as any]: "18px",
        }}
      />
      <div
        className="app__bubble"
        aria-hidden="true"
        style={{
          bottom: "22%",
          left: "12%",
          width: "150px",
          height: "150px",
          animationDelay: "-12s",
          animationDuration: "24s",
          ["--bubble-opacity" as any]: 0.48,
          ["--bubble-blur" as any]: "22px",
        }}
      />
      <div
        className="app__bubble"
        aria-hidden="true"
        style={{
          bottom: "8%",
          right: "16%",
          width: "190px",
          height: "190px",
          animationDelay: "-9s",
          animationDuration: "28s",
          ["--bubble-opacity" as any]: 0.35,
          ["--bubble-blur" as any]: "16px",
        }}
      />
      <div
        className="app__bubble"
        aria-hidden="true"
        style={{
          top: "50%",
          left: "20%",
          width: "90px",
          height: "90px",
          animationDelay: "-5s",
          animationDuration: "20s",
          ["--bubble-opacity" as any]: 0.5,
          ["--bubble-blur" as any]: "18px",
        }}
      />
      <div
        className="app__bubble"
        aria-hidden="true"
        style={{
          top: "40%",
          right: "26%",
          width: "110px",
          height: "110px",
          animationDelay: "-14s",
          animationDuration: "30s",
          ["--bubble-opacity" as any]: 0.38,
          ["--bubble-blur" as any]: "19px",
        }}
      />

      <main className="app__content">
        <header className="app__header">
          <h1 className="app__title">Sentiment Tracker</h1>
          <p className="app__subtitle">
            Track and visualise public sentiment on any topic
          </p>
        </header>

        <SearchBar onSearchResult={setResultMessage} />

        {resultMessage && (
          <p className="app__result" role="status">
            {resultMessage}
          </p>
        )}

        <footer className="app__footer">
          <span className="app__footer-main">© 2026 Sentiment Tracker</span>
        </footer>
      </main>
    </div>
  );
}
