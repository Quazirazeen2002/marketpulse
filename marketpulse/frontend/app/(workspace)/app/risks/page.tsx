"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  AlertTriangle,
  RefreshCw,
  ShieldCheck,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { RiskAssessment } from "@/lib/types";

export default function RiskObservatoryPage() {
  const [risks, setRisks] = useState<RiskAssessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [severityFilter, setSeverityFilter] = useState("all");

  const loadRisks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getRisks();
      setRisks(data);
    } catch (err: any) {
      setError(err.message || "Failed to load risk assessments.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRisks();
  }, []);

  const filteredRisks = risks.filter((r) => {
    const matchesCat =
      categoryFilter === "all" ||
      r.category?.toLowerCase() === categoryFilter.toLowerCase();
    const matchesSev =
      severityFilter === "all" ||
      (severityFilter === "high" && (r.risk_score || 0) >= 15) ||
      (severityFilter === "medium" &&
        (r.risk_score || 0) >= 8 &&
        (r.risk_score || 0) < 15) ||
      (severityFilter === "low" && (r.risk_score || 0) < 8);
    return matchesCat && matchesSev;
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#E3447C] text-[#FFFFFF] text-xs font-display font-black uppercase">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>RISK & INDUSTRY ANALYST (META SPARK 1.3)</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Systemic Risk Observatory
          </h1>
          <p className="text-sm text-[#64748B] font-medium leading-relaxed">
            Multi-dimensional vulnerability evaluations mapping likelihood, business impact, evidence provenance, actionable mitigation strategies, and residual risk.
          </p>
        </div>

        <button
          onClick={loadRisks}
          disabled={loading}
          className="p-3 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] hover:bg-[#FFFFFF] text-[#0D1117] shadow-market-sm shrink-0"
          title="Refresh Risks"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {/* 5x5 / Severity Risk Matrix Grid */}
      <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-6">
        <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
          <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
            LIKELIHOOD VS. IMPACT SEVERITY MATRIX
          </span>
          <span className="text-xs font-bold text-[#64748B] uppercase">
            {risks.length} Total Risks Evaluated
          </span>
        </div>

        {/* Matrix Visualization */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-5 rounded-xl border-2 border-[#0D1117] bg-[#E3447C]/15 space-y-2">
            <span className="text-xs font-display font-black uppercase text-[#E3447C]">
              High Severity / Critical
            </span>
            <p className="font-display font-black text-3xl text-[#0D1117]">
              {risks.filter((r) => (r.risk_score || 0) >= 15).length}
            </p>
            <p className="text-[11px] text-[#64748B] font-medium">
              High Likelihood & High Impact • Immediate mitigation required
            </p>
          </div>

          <div className="p-5 rounded-xl border-2 border-[#0D1117] bg-[#08B0D5]/20 space-y-2">
            <span className="text-xs font-display font-black uppercase text-[#0D1117]">
              Moderate Severity
            </span>
            <p className="font-display font-black text-3xl text-[#0D1117]">
              {
                risks.filter(
                  (r) => (r.risk_score || 0) >= 8 && (r.risk_score || 0) < 15
                ).length
              }
            </p>
            <p className="text-[11px] text-[#64748B] font-medium">
              Medium probability or contained impact • Operational monitoring
            </p>
          </div>

          <div className="p-5 rounded-xl border-2 border-[#0D1117] bg-[#08B0D5]/10 space-y-2">
            <span className="text-xs font-display font-black uppercase text-[#08B0D5]">
              Low Severity / Defensible
            </span>
            <p className="font-display font-black text-3xl text-[#0D1117]">
              {risks.filter((r) => (r.risk_score || 0) < 8).length}
            </p>
            <p className="text-[11px] text-[#64748B] font-medium">
              Low probability or minor impact • Routine governance
            </p>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-[11px] font-display font-black uppercase text-[#64748B]">
            Category:
          </span>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-3 py-1.5 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-xs font-bold uppercase text-[#0D1117]"
          >
            <option value="all">All Categories</option>
            <option value="regulatory">Regulatory</option>
            <option value="competitive">Competitive</option>
            <option value="market">Market & Demand</option>
            <option value="financial">Financial / Unit Economics</option>
            <option value="operational">Operational</option>
          </select>

          <span className="text-[11px] font-display font-black uppercase text-[#64748B] ml-2">
            Severity:
          </span>
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="px-3 py-1.5 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-xs font-bold uppercase text-[#0D1117]"
          >
            <option value="all">All Severities</option>
            <option value="high">High (Score &gt;= 15)</option>
            <option value="medium">Medium (8-14)</option>
            <option value="low">Low (&lt; 8)</option>
          </select>
        </div>

        <span className="text-xs font-display font-bold uppercase text-[#64748B]">
          Showing {filteredRisks.length} Assessments
        </span>
      </div>

      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase">
          {error}
        </div>
      )}

      {/* Risk Cards List */}
      {loading ? (
        <div className="space-y-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl border-2 border-[#0D1117] bg-[#FFFFFF] animate-pulse h-48"
            />
          ))}
        </div>
      ) : filteredRisks.length === 0 ? (
        <div className="p-12 text-center border-2 border-dashed border-[#0D1117] rounded-2xl bg-[#FFFFFF] space-y-4">
          <ShieldAlert className="w-10 h-10 text-[#64748B] mx-auto" />
          <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
            No Risk Assessments Found
          </h3>
          <p className="text-xs text-[#64748B] max-w-sm mx-auto">
            Risk assessments are synthesized during Stage 2 Strategic Intelligence investigations.
          </p>
          <Link
            href="/app/research/new"
            className="inline-block px-5 py-2.5 rounded-xl bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
          >
            Run Research Run
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredRisks.map((risk) => {
            const score = risk.risk_score || 10;
            const isHigh = score >= 15;
            return (
              <div
                key={risk.risk_id || risk.id}
                className="card-market p-6 rounded-2xl bg-[#FFFFFF] border-2 border-[#0D1117] shadow-market space-y-4"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#E2E8F0] pb-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded bg-[#F4F8FA] border border-[#0D1117] text-[10px] font-display font-black uppercase text-[#0D1117]">
                      {risk.category || "General Risk"}
                    </span>
                    <span className="text-xs font-mono font-bold text-[#64748B]">
                      {risk.risk_id || `RISK-${risk.id}`}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-[#F4F8FA] text-[11px] font-bold uppercase">
                      Likelihood: <strong>{risk.likelihood || "Moderate"}</strong>
                    </span>
                    <span className="px-2 py-0.5 rounded bg-[#F4F8FA] text-[11px] font-bold uppercase">
                      Impact: <strong>{risk.impact || "Moderate"}</strong>
                    </span>
                    <span
                      className={`px-3 py-1 rounded text-xs font-display font-black uppercase border ${
                        isHigh
                          ? "bg-[#E3447C] text-[#FFFFFF] border-[#0D1117]"
                          : "bg-[#08B0D5] text-[#0D1117] border-[#0D1117]"
                      }`}
                    >
                      Severity: {score}/25
                    </span>
                  </div>
                </div>

                {/* Description & Assessment */}
                <div className="space-y-2">
                  <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
                    {risk.risk_name}
                  </h3>
                  <p className="text-xs text-[#64748B] font-medium leading-relaxed">
                    {risk.assessment}
                  </p>
                </div>

                {/* Mitigation & Residual Risk */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  <div className="p-3.5 rounded-xl bg-[#F4F8FA] border border-[#0D1117] text-xs space-y-1">
                    <span className="font-display font-black uppercase text-[10px] text-[#08B0D5]">
                      Actionable Mitigation Strategy:
                    </span>
                    <p className="text-[#0D1117] font-medium leading-relaxed">
                      {risk.mitigation_strategy || "Continuous monitoring of competitor pricing adjustments."}
                    </p>
                  </div>

                  <div className="p-3.5 rounded-xl bg-[#FFFFFF] border border-[#0D1117] text-xs space-y-1">
                    <span className="font-display font-black uppercase text-[10px] text-[#64748B]">
                      Residual Risk Post-Mitigation:
                    </span>
                    <p className="text-[#0D1117] font-medium leading-relaxed">
                      {risk.residual_risk || "Low to moderate residual variance after implementing SLAs."}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
