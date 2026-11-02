"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  FileText,
  Search,
  RefreshCw,
  ArrowRight,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { ResearchRunSummary } from "@/lib/types";

export default function ReportsIndexPage() {
  const [runs, setRuns] = useState<ResearchRunSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const loadReports = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getResearchHistory(50);
      setRuns(data || []);
    } catch (err: any) {
      setError(err.message || "Failed to load reports archive.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  const completedRuns = runs.filter((r) => r.status === "completed");
  const filteredRuns = completedRuns.filter(
    (r) =>
      r.objective?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.industry?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.geography?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
            <FileText className="w-3.5 h-3.5" />
            <span>EXECUTIVE DOSSIER ARCHIVE</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Synthesized Executive Reports
          </h1>
          <p className="text-sm text-[#64748B] font-medium leading-relaxed">
            Traceable, 10-section strategic reports compiled by Chief Research Director (Meta Muse Wonder) with complete evidence citations, methodology notes, and export formats.
          </p>
        </div>

        <button
          onClick={loadReports}
          disabled={loading}
          className="p-3 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] hover:bg-[#FFFFFF] text-[#0D1117] shadow-market-sm shrink-0"
          title="Refresh Reports"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {/* Search Bar */}
      <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm flex items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-[#64748B]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search reports by objective, industry, market..."
            className="w-full pl-9 pr-4 py-2 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-xs font-medium text-[#0D1117] focus:outline-none focus:bg-[#FFFFFF]"
          />
        </div>

        <span className="text-xs font-display font-bold uppercase text-[#64748B] hidden sm:block">
          {completedRuns.length} Reports Ready for Inspection
        </span>
      </div>

      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase">
          {error}
        </div>
      )}

      {/* Reports Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl border-2 border-[#0D1117] bg-[#FFFFFF] animate-pulse h-64"
            />
          ))}
        </div>
      ) : filteredRuns.length === 0 ? (
        <div className="p-12 text-center border-2 border-dashed border-[#0D1117] rounded-2xl bg-[#FFFFFF] space-y-4">
          <FileText className="w-10 h-10 text-[#64748B] mx-auto" />
          <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
            No completed executive reports yet
          </h3>
          <p className="text-xs text-[#64748B] max-w-sm mx-auto">
            Completed research runs are compiled into 10-section executive reports.
          </p>
          <Link
            href="/app/research/new"
            className="inline-block px-5 py-2.5 rounded-xl bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
          >
            Launch Investigation
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredRuns.map((run) => (
            <div
              key={run.id}
              className="card-market p-6 rounded-2xl flex flex-col justify-between space-y-5 bg-[#FFFFFF] border-3 border-[#0D1117]"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded bg-[#F4F8FA] border border-[#0D1117] text-[10px] font-display font-black uppercase text-[#0D1117]">
                    {run.industry}
                  </span>
                  <span className="px-2.5 py-0.5 rounded bg-[#08B0D5]/20 text-[#08B0D5] border border-[#08B0D5] text-[10px] font-bold uppercase">
                    COMPLETED
                  </span>
                </div>

                <h3 className="font-display font-black text-lg uppercase text-[#0D1117] leading-tight line-clamp-2">
                  {run.objective}
                </h3>

                <div className="space-y-1 text-xs text-[#64748B]">
                  <p>Geography: <strong className="text-[#0D1117]">{run.geography}</strong></p>
                  <p>Quality Tier: <strong className="text-[#08B0D5]">{run.research_quality || "Verified High"}</strong></p>
                </div>
              </div>

              <div className="pt-3 border-t-2 border-[#0D1117] space-y-3">
                <div className="flex items-center justify-between text-[11px] font-bold text-[#64748B]">
                  <span>{run.total_sources || 0} Sources</span>
                  <span className="text-[#08B0D5]">{run.verified_claims || 0} Claims Verified</span>
                </div>

                <div className="flex items-center justify-between gap-2">
                  <Link
                    href={`/app/reports/${run.id}`}
                    className="btn-market w-full py-2 rounded-lg bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm text-center flex items-center justify-center gap-1.5 hover:bg-[#E3447C] hover:text-[#FFFFFF]"
                  >
                    <span>Read Report</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
