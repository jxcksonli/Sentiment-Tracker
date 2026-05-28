import { useEffect, useMemo, useRef, useState } from "react";
import * as d3 from "d3";
import type { KeywordBubble, SentimentLabel } from "../api";

type NodeDatum = KeywordBubble & {
  r: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
};

function colorFor(sentiment: SentimentLabel) {
  switch (sentiment) {
    case "positive":
      return "rgba(90, 255, 170, 0.55)";
    case "negative":
      return "rgba(255, 90, 120, 0.55)";
    case "neutral":
    default:
      return "rgba(220, 228, 255, 0.40)";
  }
}

function strokeFor(sentiment: SentimentLabel) {
  switch (sentiment) {
    case "positive":
      return "rgba(120, 255, 190, 0.55)";
    case "negative":
      return "rgba(255, 120, 145, 0.55)";
    case "neutral":
    default:
      return "rgba(255, 255, 255, 0.18)";
  }
}

export default function WordBubbleCloud({
  keywords,
  height = 420,
}: {
  keywords: KeywordBubble[];
  height?: number;
}) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(640);

  useEffect(() => {
    if (!wrapRef.current) return;
    const ro = new ResizeObserver(() => {
      setWidth(Math.max(320, Math.floor(wrapRef.current?.clientWidth ?? 640)));
    });
    ro.observe(wrapRef.current);
    return () => ro.disconnect();
  }, []);

  const nodes = useMemo<NodeDatum[]>(() => {
    const cleaned = keywords
      .filter((k) => k.word && Number.isFinite(k.count) && k.count > 0)
      .slice(0, 60);

    const counts = cleaned.map((k) => k.count);
    const min = Math.min(...counts);
    const max = Math.max(...counts);
    const radius = d3
      .scaleSqrt<number, number>()
      .domain([min, max])
      .range([18, 58]);

    return cleaned.map((k) => ({
      ...k,
      r: radius(k.count),
    }));
  }, [keywords]);

  const [positions, setPositions] = useState<NodeDatum[]>([]);

  useEffect(() => {
    if (nodes.length === 0) {
      setPositions([]);
      return;
    }

    const sim = d3
      .forceSimulation<NodeDatum>(nodes.map((n) => ({ ...n })))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("charge", d3.forceManyBody<NodeDatum>().strength(1))
      .force("collide", d3.forceCollide<NodeDatum>().radius((d: NodeDatum) => d.r + 2))
      .force("x", d3.forceX<NodeDatum>(width / 2).strength(0.05))
      .force("y", d3.forceY<NodeDatum>(height / 2).strength(0.05))
      .stop();

    // Run a fixed number of ticks for deterministic-ish layout
    sim.tick(240);

    setPositions(sim.nodes());
    sim.stop();
  }, [nodes, width, height]);

  return (
    <div ref={wrapRef} style={{ width: "100%" }}>
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="Keyword bubble cloud"
        style={{ display: "block" }}
      >
        <defs>
          <filter id="glassBlur" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="0.6" />
          </filter>
        </defs>

        {positions.map((d) => {
          const label =
            d.word.length > 14 ? `${d.word.slice(0, 13)}…` : d.word;
          const fontSize = Math.max(11, Math.min(18, d.r * 0.42));

          return (
            <g key={`${d.word}-${d.count}`} transform={`translate(${d.x},${d.y})`}>
              <circle
                r={d.r}
                fill={colorFor(d.sentiment)}
                stroke={strokeFor(d.sentiment)}
                strokeWidth={1.2}
                filter="url(#glassBlur)"
              />
              <circle
                r={d.r - 1.2}
                fill="none"
                stroke="rgba(255,255,255,0.10)"
                strokeWidth={1}
              />
              <text
                textAnchor="middle"
                dominantBaseline="middle"
                style={{
                  fill: "rgba(255,255,255,0.92)",
                  fontWeight: 650,
                  letterSpacing: "-0.01em",
                  fontSize,
                  userSelect: "none",
                }}
              >
                {label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

