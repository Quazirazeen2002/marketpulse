"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  History,
  Search,
  RefreshCw,
  Scale,
  CheckCircle2,
  Clock,
  ArrowRight,
  Sparkles,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { ResearchRunSummary } from "@/lib/types";

export default function ResearchHistoryPage() {
  const [runs, setRuns] = useState<ResearchRunSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  // Compare tool state
  const [selectedRunA, setSelectedRunA] = useState<string>("");
  const [selectedRunB, setSelectedRunB] = useState<string>("");
  const [comparing, setComparing] = useState(false);
  const [compareResult, setCompareResult] = useState<any | null>(null);

  const loadHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getResearchHistory(50);
      setRuns(data || []);
      if (data && data.length >= 2) {
        setSelectedRunA(data[0].id);
        setSelectedRunB(data[1].id);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load research audit history.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleCompare = async () => {
    if (!selectedRunA || !selectedRunB || selectedRunA === selectedRunB) return;
    try {
      setComparing(true);
      const res = await api.compareResearchRuns(selectedRunA, selectedRunB);
      setCompareResult(res);
    } catch (err: any) {
      alert(`Comparison failed: ${err.message}`);
    } finally {
      setComparing(false);
    }
  };

  const filteredRuns = runs.filter(
    (r) =>
      r.objective?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.industry?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.geography?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.id?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
            <History className="w-3.5 h-3.5" />
            <span>SQLITE AUDIT ARCHIVE</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Research History & Run Comparison
          </h1>
          <p className="text-sm text-[#64748B] font-medium leading-relaxed">
            Immutable log of all autonomous investigations. Compare historical findings, verify source deltas, and cross-reference claim verification rates.
          </p>
        </div>

        <button
          onClick={loadHistory}
          disabled={loading}
          className="p-3 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] hover:bg-[#FFFFFF] text-[#0D1117] shadow-market-sm shrink-0"
          title="Refresh History"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {/* Compare Tool Card */}
      {runs.length >= 2 && (
        <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-lg space-y-4">
          <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
            <span className="text-xs font-display font-black text-[#08B0D5] uppercase flex items-center gap-1.5">
              <Scale className="w-4 h-4" />
              Side-by-Side Run Comparator
            </span>
            <span className="text-[10px] font-bold text-[#64748B] uppercase">
              POST /api/research/compare
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-12 gap-4 items-end">
            <div className="sm:col-span-5 space-y-1">
              <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                Investigation A:
              </label>
              <select
                value={selectedRunA}
                onChange={(e) => setSelectedRunA(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold uppercase text-[#0D1117]"
              >
                {runs.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.objective.slice(0, 34)}... ({r.id.slice(0, 8)})
                  </option>
                ))}
              </select>
            </div>

            <div className="sm:col-span-5 space-y-1">
              <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                Investigation B:
              </label>
              <select
                value={selectedRunB}
                onChange={(e) => setSelectedRunB(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold uppercase text-[#0D1117]"
              >
                {runs.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.objective.slice(0, 34)}... ({r.id.slice(0, 8)})
                  </option>
                ))}
              </select>
            </div>

            <div className="sm:col-span-2">
              <button
                onClick={handleCompare}
                disabled={comparing || selectedRunA === selectedRunB}
                className="btn-market w-full py-2.5 rounded-lg bg-[#08B0D5] text-xs font-display font-black uppercase text-[#0D1117] shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF] disabled:opacity-50"
              >
                {comparing ? "Comparing..." : "Compare"}
              </button>
            </div>
          </div>

          {/* Comparison Output */}
          {compareResult && (
            <div className="p-4 rounded-xl bg-[#F4F8FA] border-2 border-[#0D1117] space-y-3 mt-4 text-xs">
              <div className="flex items-center justify-between font-display font-black uppercase text-[#0D1117] border-b border-[#0D1117] pb-2">
                <span>Comparison Summary</span>
                <span>Delta Analysis</span>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="font-bold text-[#0D1117]">Run A: {selectedRunA.slice(0, 8)}</p>
                  <p className="text-[#64748B]">Sources: {compareResult.run_a?.source_count || 0}</p>
                  <p className="text-[#64748B]">Verified Claims: {compareResult.run_a?.verified_claims_count || 0}</p>
                </div>
                <div>
                  <p className="font-bold text-[#0D1117]">Run B: {selectedRunB.slice(0, 8)}</p>
                  <p className="text-[#64748B]">Sources: {compareResult.run_b?.source_count || 0}</p>
                  <p className="text-[#64748B]">Verified Claims: {compareResult.run_b?.verified_claims_count || 0}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Audit Table Card */}
      <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b-2 border-[#0D1117] pb-4">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 absolute left-3 top-3 text-[#64748B]" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by objective, ID, industry..."
              className="w-full pl-9 pr-4 py-2 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-xs font-medium text-[#0D1117] focus:outline-none focus:bg-[#FFFFFF]"
            />
          </div>

          <span className="text-xs font-display font-bold uppercase text-[#64748B]">
            {filteredRuns.length} Total Runs Archived
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="border-b-2 border-[#0D1117] font-display font-black uppercase text-[#64748B]">
              <tr>
                <th className="py-3 px-4">Run ID & Objective</th>
                <th className="py-3 px-4">Market Focus</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Sources</th>
                <th className="py-3 px-4">Claims</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E2E8F0] font-medium text-[#0D1117]">
              {filteredRuns.map((r) => (
                <tr key={r.id} className="hover:bg-[#F4F8FA] transition-colors">
                  <td className="py-4 px-4 max-w-sm truncate">
                    <p className="font-display font-bold text-[#0D1117] truncate">
                      {r.objective}
                    </p>
                    <p className="text-[10px] text-[#64748B] font-mono mt-0.5">
                      {r.id}
                    </p>
                  </td>
                  <td className="py-4 px-4">
                    <span className="font-bold">{r.industry}</span>
                    <span className="text-[#64748B] block text-[10px]">{r.geography}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded text-[10px] font-display font-black uppercase border ${
                        r.status === "completed"
                          ? "bg-[#08B0D5]/20 text-[#08B0D5] border-[#08B0D5]"
                          : r.status === "running"
                          ? "bg-[#E3447C]/20 text-[#E3447C] border-[#E3447C] animate-pulse"
                          : "bg-[#64748B]/20 text-[#0D1117] border-[#64748B]"
                      }`}
                    >
                      {r.status}
                    </span>
                  </td>
                  <td className="py-4 px-4 font-bold">
                    {r.total_sources || 0}
                  </td>
                  <td className="py-4 px-4 font-bold text-[#08B0D5]">
                    {r.verified_claims || 0}
                  </td>
                  <td className="py-4 px-4 text-right space-x-2">
                    <Link
                      href={`/app/research/${r.id}`}
                      className="btn-market inline-block px-3 py-1.5 rounded bg-[#F4F8FA] hover:bg-[#FFFFFF] text-[10px] font-display font-black uppercase shadow-market-sm border border-[#0D1117]"
                    >
                      Progress
                    </Link>
                    {r.status === "completed" && (
                      <Link
                        href={`/app/reports/${r.id}`}
                        className="btn-market inline-block px-3 py-1.5 rounded bg-[#08B0D5] text-[10px] font-display font-black uppercase shadow-market-sm text-[#0D1117] hover:bg-[#E3447C] hover:text-[#FFFFFF]"
                      >
                        Report →
                      </Link>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
