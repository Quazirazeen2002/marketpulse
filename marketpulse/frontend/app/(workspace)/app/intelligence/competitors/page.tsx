"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import {
  Target,
  RefreshCw,
  Search,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { ResearchRunSummary } from "@/lib/types";

export default function CompetitorIntelligencePage() {
  const [runs, setRuns] = useState<ResearchRunSummary[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string>("");
  const [report, setReport] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function init() {
      try {
        setLoading(true);
        const data = await api.getResearchHistory(20);
        setRuns(data || []);
        if (data && data.length > 0) {
          const firstId = data[0].id;
          setSelectedRunId(firstId);
          const rep = await api.getReport(firstId).catch(() => null);
          setReport(rep);
        }
      } catch {
        // handle fallback
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  const handleSelectRun = async (id: string) => {
    setSelectedRunId(id);
    try {
      setLoading(true);
      const rep = await api.getReport(id).catch(() => null);
      setReport(rep);
    } finally {
      setLoading(false);
    }
  };

  const selectedRun = runs.find((r) => r.id === selectedRunId);
  const competitorContent = report?.competitor_intelligence || report?.competitor_analysis || null;

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#0D1117] text-[#FFFFFF] text-xs font-display font-black uppercase">
            <Target className="w-3.5 h-3.5 text-[#08B0D5]" />
            <span>META SPARK 1.3 SPECIALIST</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Competitor Intelligence
          </h1>
          <p className="text-sm text-[#64748B] font-medium max-w-2xl">
            Competitor benchmarking, pricing models, positioning maps, distribution channels, strengths, and capability blind spots.
          </p>
        </div>

        {/* Run Selector */}
        {runs.length > 0 && (
          <div className="space-y-1">
            <label className="text-[11px] font-display font-black uppercase text-[#0D1117] block">
              Active Investigation:
            </label>
            <select
              value={selectedRunId}
              onChange={(e) => handleSelectRun(e.target.value)}
              className="px-4 py-2.5 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-display font-bold uppercase text-[#0D1117] focus:outline-none focus:ring-2 focus:ring-[#08B0D5]"
            >
              {runs.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.objective.slice(0, 36)}... ({r.id.slice(0, 8)})
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-6">
        <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-4">
          <div className="space-y-1">
            <span className="text-[11px] font-display font-black text-[#08B0D5] uppercase">
              COMPETITIVE MATRIX
            </span>
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117]">
              {selectedRun?.objective || "Competitor Landscape"}
            </h2>
          </div>
          <span className="px-3 py-1 rounded bg-[#08B0D5] border border-[#0D1117] text-xs font-display font-black text-[#0D1117]">
            {selectedRun?.industry || "Competitive Analysis"}
          </span>
        </div>

        {loading ? (
          <div className="py-16 text-center space-y-3">
            <Target className="w-8 h-8 text-[#64748B] animate-pulse mx-auto" />
            <p className="text-xs font-display font-bold uppercase text-[#64748B]">
              Loading competitor benchmarking...
            </p>
          </div>
        ) : competitorContent ? (
          <div className="prose prose-slate max-w-none text-sm leading-relaxed space-y-4 text-[#0D1117]">
            <ReactMarkdown>
              {typeof competitorContent === "string"
                ? competitorContent
                : JSON.stringify(competitorContent, null, 2)}
            </ReactMarkdown>
          </div>
        ) : (
          <div className="p-8 rounded-xl bg-[#F4F8FA] border-2 border-[#0D1117] text-center space-y-3">
            <p className="font-display font-bold uppercase text-xs text-[#64748B]">
              No standalone competitor intelligence section recorded for this run.
            </p>
            <Link
              href={`/app/reports/${selectedRunId}`}
              className="inline-block px-4 py-2 rounded-lg bg-[#08B0D5] text-xs font-display font-black uppercase border border-[#0D1117] text-[#0D1117] hover:bg-[#E3447C] hover:text-[#FFFFFF]"
            >
              Open Full Executive Report →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
