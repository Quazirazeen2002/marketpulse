"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  FileQuestion,
  GitBranch,
  RefreshCw,
  Search,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { HypothesisRecord } from "@/lib/types";

export default function HypothesesObservatoryPage() {
  const [hypotheses, setHypotheses] = useState<HypothesisRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<string>("all");

  const loadHypotheses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getHypotheses();
      setHypotheses(data || []);
    } catch (err: any) {
      setError(err.message || "Failed to load hypotheses.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHypotheses();
  }, []);

  const lifecycleStages = [
    { num: "01", name: "Observation", desc: "Atomic finding extracted from live web via Tavily" },
    { num: "02", name: "Hypothesis", desc: "Autonomous formulation of testable premise" },
    { num: "03", name: "Research Task", desc: "Dynamic generation of targeted search queries" },
    { num: "04", name: "Evidence", desc: "Tavily web spidering & atomic extraction" },
    { num: "05", name: "Verification", desc: "Director cross-examines claim & contradictions" },
    { num: "06", name: "Assessment", desc: "Scored business opportunity or rejection" },
  ];

  const getStatusBadge = (status: string) => {
    const s = status.toLowerCase();
    if (s.includes("supported") && !s.includes("partially")) {
      return "bg-[#08B0D5]/20 text-[#08B0D5] border-[#08B0D5]";
    } else if (s.includes("partially")) {
      return "bg-[#08B0D5]/15 text-[#0D1117] border-[#08B0D5]";
    } else if (s.includes("investigating")) {
      return "bg-[#08B0D5]/20 text-[#08B0D5] border-[#08B0D5] animate-pulse";
    } else if (s.includes("rejected")) {
      return "bg-[#E3447C]/20 text-[#E3447C] border-[#E3447C]";
    } else {
      return "bg-[#64748B]/20 text-[#64748B] border-[#64748B]";
    }
  };

  const filteredHypotheses = hypotheses.filter((h) => {
    if (selectedStatus === "all") return true;
    return h.validation_status?.toLowerCase().includes(selectedStatus.toLowerCase());
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
            <GitBranch className="w-3.5 h-3.5" />
            <span>AUTONOMOUS FEEDBACK LOOPS</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Research Hypotheses & Loop Inspection
          </h1>
          <p className="text-sm text-[#64748B] font-medium leading-relaxed">
            Track how raw market findings evolve into testable hypotheses, trigger iterative web investigations, and achieve validated disposition.
          </p>
        </div>

        <button
          onClick={loadHypotheses}
          disabled={loading}
          className="p-3 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] hover:bg-[#FFFFFF] text-[#0D1117] shadow-market-sm shrink-0"
          title="Refresh Hypotheses"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {/* Interactive Lifecycle Timeline Strip */}
      <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-6">
        <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
          <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
            LIFECYCLE PIPELINE ARCHITECTURE
          </span>
          <span className="px-2.5 py-0.5 rounded bg-[#08B0D5] text-[10px] font-display font-black uppercase text-[#0D1117]">
            UP TO 3 AUTONOMOUS ITERATIONS
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {lifecycleStages.map((stage) => (
            <div
              key={stage.num}
              className="p-3.5 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] space-y-1 shadow-market-sm"
            >
              <span className="text-[10px] font-display font-black text-[#08B0D5] uppercase">
                {stage.num} / STEP
              </span>
              <h4 className="font-display font-black text-sm uppercase text-[#0D1117]">
                {stage.name}
              </h4>
              <p className="text-[10px] text-[#64748B] font-medium leading-tight">
                {stage.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2">
        {["all", "supported", "partially supported", "investigating", "rejected", "inconclusive"].map(
          (st) => (
            <button
              key={st}
              onClick={() => setSelectedStatus(st)}
              className={`px-3.5 py-1.5 rounded-lg border-2 text-xs font-display font-bold uppercase transition-all ${
                selectedStatus === st
                  ? "bg-[#08B0D5] text-[#0D1117] border-[#0D1117] shadow-market-sm font-black"
                  : "bg-[#FFFFFF] text-[#0D1117] border-[#0D1117] hover:bg-[#F4F8FA]"
              }`}
            >
              {st}
            </button>
          )
        )}
      </div>

      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase">
          {error}
        </div>
      )}

      {/* Hypotheses List */}
      {loading ? (
        <div className="space-y-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl border-2 border-[#0D1117] bg-[#FFFFFF] animate-pulse h-36"
            />
          ))}
        </div>
      ) : filteredHypotheses.length === 0 ? (
        <div className="p-12 text-center border-2 border-dashed border-[#0D1117] rounded-2xl bg-[#FFFFFF] space-y-4">
          <FileQuestion className="w-10 h-10 text-[#64748B] mx-auto" />
          <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
            No Hypotheses Found
          </h3>
          <p className="text-xs text-[#64748B] max-w-sm mx-auto">
            Hypotheses are spawned during Stage 2 Strategic Intelligence workflows.
          </p>
          <Link
            href="/app/research/new"
            className="inline-block px-5 py-2.5 rounded-xl bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
          >
            Start New Research Run
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredHypotheses.map((h) => {
            const statusClass = getStatusBadge(h.validation_status || "proposed");
            return (
              <div
                key={h.hypothesis_id || h.id}
                className="card-market p-6 rounded-2xl bg-[#FFFFFF] border-2 border-[#0D1117] shadow-market space-y-4"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#E2E8F0] pb-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] font-mono text-[11px] font-bold">
                      {h.hypothesis_id || `HYP-${h.id}`}
                    </span>
                    <span className="text-xs font-display font-bold text-[#64748B] uppercase">
                      Iteration {h.research_iteration || 1}
                    </span>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-md border text-xs font-display font-black uppercase ${statusClass}`}
                  >
                    {h.validation_status || "Proposed"}
                  </span>
                </div>

                <div className="space-y-2">
                  <h3 className="font-display font-black text-lg text-[#0D1117] uppercase leading-snug">
                    {h.hypothesis_statement}
                  </h3>

                  {h.originating_findings && h.originating_findings.length > 0 && (
                    <div className="p-3 rounded-lg bg-[#F4F8FA] border border-[#0D1117] text-xs space-y-1">
                      <span className="font-display font-bold uppercase text-[10px] text-[#08B0D5]">
                        Originating Findings:
                      </span>
                      <ul className="space-y-0.5 text-xs text-[#0D1117] font-medium">
                        {h.originating_findings.map((f, idx) => (
                          <li key={idx}>• {f}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Follow-up tasks & Final disposition */}
                {h.followup_tasks && h.followup_tasks.length > 0 && (
                  <div className="pt-2 text-xs flex flex-wrap items-center gap-2">
                    <span className="font-display font-bold text-[#64748B] uppercase text-[11px]">
                      Follow-up Tasks Dispatched:
                    </span>
                    {h.followup_tasks.map((task, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 rounded bg-[#FFFFFF] border border-[#0D1117] font-mono text-[10px] text-[#0D1117]"
                      >
                        {task}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
