import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  async redirects() {
    return [
      { source: "/landing", destination: "/", permanent: true },
      { source: "/agents", destination: "/app/agents", permanent: true },
      { source: "/opportunities", destination: "/app/opportunities", permanent: true },
      { source: "/opportunities/:id", destination: "/app/opportunities/:id", permanent: true },
      { source: "/hypotheses", destination: "/app/hypotheses", permanent: true },
      { source: "/risks", destination: "/app/risks", permanent: true },
      { source: "/evidence", destination: "/app/evidence", permanent: true },
      { source: "/reports", destination: "/app/reports", permanent: true },
      { source: "/reports/:id", destination: "/app/reports/:id", permanent: true },
      { source: "/simulator", destination: "/app/simulator", permanent: true },
      { source: "/simulator/:id", destination: "/app/simulator?opp=:id", permanent: true },
      { source: "/settings", destination: "/app/settings", permanent: true },
      { source: "/history", destination: "/app/history", permanent: true },
      { source: "/research", destination: "/app/research/new", permanent: true },
      { source: "/research/new", destination: "/app/research/new", permanent: true },
      { source: "/research/history", destination: "/app/history", permanent: true },
      { source: "/research/active/:id", destination: "/app/research/:id", permanent: true },
      { source: "/intelligence", destination: "/app/intelligence", permanent: true },
      { source: "/intelligence/:slug", destination: "/app/intelligence/:slug", permanent: true },
    ];
  },
};

export default nextConfig;
