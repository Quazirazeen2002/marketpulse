"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  ArrowRight,
  Database,
  CheckCircle2,
  Lightbulb,
  ShieldAlert,
  Search,
  Activity,
  FileCheck,
  TrendingUp,
  AlertTriangle,
  Zap,
  RefreshCw,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { api } from "@/lib/api/client";
import { OverviewStats, ResearchRunSummary, Opportunity } from "@/lib/types";
import { formatNumber } from "@/lib/utils";

export default function WorkspaceDashboard() {
  const [stats, setStats] = useState<OverviewStats | null>(null);
  const [recentRuns, setRecentRuns] = useState<ResearchRunSummary[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [statsData, oppsData] = await Promise.all([
        api.getOverviewStats().catch(() => null),
        api.getOpportunities(undefined, 4).catch(() => []),
      ]);

      if (statsData) {
        setStats(statsData);
        setRecentRuns(statsData.recent_runs || []);
      }
      setOpportunities(oppsData || []);
    } catch (err: any) {
      setError(err.message || "Failed to load platform statistics.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Prepare chart data from real backend metrics
  const activityData = [
    { name: "Runs", count: stats?.total_research_runs || 0 },
    { name: "Sources", count: stats?.total_sources || 0 },
    { name: "Evidence", count: stats?.evidence_records || 0 },
    { name: "Claims", count: stats?.verified_claims || 0 },
    { name: "Opps", count: stats?.discovered_opportunities || 0 },
    { name: "Risks", count: stats?.total_risks || 0 },
  ];

  const claimRatioData = [
    {
      name: "Verified",
      value: stats?.verified_claims || 0,
      color: "#08B0D5",
    },
    {
      name: "Unverified",
      value: Math.max(0, (stats?.total_claims || 0) - (stats?.verified_claims || 0)),
      color: "#E2E8F0",
    },
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Top Banner / Hero */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] border border-[#0D1117] text-xs font-display font-black uppercase text-[#0D1117]">
            <Sparkles className="w-3.5 h-3.5 fill-current" />
            <span>OPERATIONAL TELEMETRY</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            YOUR INTELLIGENCE COMMAND CENTER.
          </h1>
          <p className="text-sm text-[#64748B] font-medium max-w-2xl">
            Live multi-agent research telemetry, atomic evidence metrics, scored white-space opportunities, and deterministic scenario models.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3 shrink-0">
          <button
            onClick={loadData}
            disabled={loading}
            className="p-3 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] hover:bg-[#FFFFFF] text-[#0D1117] transition-colors"
            title="Refresh Metrics"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
          <Link
            href="/app/research/new"
            className="btn-market inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-sm uppercase shadow-market hover:bg-[#E3447C] hover:text-[#FFFFFF]"
          >
            <Zap className="w-4 h-4 fill-current" />
            <span>Start New Research</span>
            <ArrowRight className="w-4 h-4 stroke-[3]" />
          </Link>
        </div>
      </div>

      {/* Error state alert */}
      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-display font-bold uppercase">
            <AlertTriangle className="w-4 h-4" />
            <span>{error}</span>
          </div>
          <button
            onClick={loadData}
            className="text-xs font-black underline uppercase"
          >
            Retry
          </button>
        </div>
      )}

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        {/* Total Investigations */}
        <div className="card-market p-5 rounded-2xl bg-[#FFFFFF] space-y-2">
          <div className="flex items-center justify-between text-[#64748B]">
            <span className="text-xs font-display font-black uppercase">
              Total Runs
            </span>
            <Search className="w-4 h-4 text-[#0D1117]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#0D1117]">
            {loading ? "..." : formatNumber(stats?.total_research_runs || 0)}
          </p>
          <p className="text-[11px] font-bold text-[#64748B] uppercase">
            {stats?.active_investigations || 0} currently executing
          </p>
        </div>

        {/* Completed Reports */}
        <div className="card-market p-5 rounded-2xl bg-[#FFFFFF] space-y-2">
          <div className="flex items-center justify-between text-[#64748B]">
            <span className="text-xs font-display font-black uppercase">
              Completed Reports
            </span>
            <FileCheck className="w-4 h-4 text-[#08B0D5]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#08B0D5]">
            {loading ? "..." : formatNumber(stats?.completed_investigations || 0)}
          </p>
          <p className="text-[11px] font-bold text-[#64748B] uppercase">
            {stats?.high_quality_runs || 0} high-quality verified
          </p>
        </div>

        {/* Sources Retrieved */}
        <div className="card-market p-5 rounded-2xl bg-[#FFFFFF] space-y-2">
          <div className="flex items-center justify-between text-[#64748B]">
            <span className="text-xs font-display font-black uppercase">
              Sources Retrieved
            </span>
            <Database className="w-4 h-4 text-[#0D1117]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#0D1117]">
            {loading ? "..." : formatNumber(stats?.total_sources || 0)}
          </p>
          <p className="text-[11px] font-bold text-[#64748B] uppercase">
            Primary URLs & PDFs
          </p>
        </div>

        {/* Evidence Records */}
        <div className="card-market p-5 rounded-2xl bg-[#FFFFFF] space-y-2">
          <div className="flex items-center justify-between text-[#64748B]">
            <span className="text-xs font-display font-black uppercase">
              Atomic Evidence
            </span>
            <CheckCircle2 className="w-4 h-4 text-[#08B0D5]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#0D1117]">
            {loading ? "..." : formatNumber(stats?.evidence_records || 0)}
          </p>
          <p className="text-[11px] font-bold text-[#64748B] uppercase">
            Fingerprinted Excerpts
          </p>
        </div>

        {/* Verified Claims */}
        <div className="card-market p-5 rounded-2xl bg-[#FFFFFF] space-y-2">
          <div className="flex items-center justify-between text-[#64748B]">
            <span className="text-xs font-display font-black uppercase">
              Verified Claims
            </span>
            <ShieldAlert className="w-4 h-4 text-[#08B0D5]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#08B0D5]">
            {loading ? "..." : formatNumber(stats?.verified_claims || 0)}
          </p>
          <p className="text-[11px] font-bold text-[#64748B] uppercase">
            Cross-examined facts
          </p>
        </div>

        {/* Opportunities Discovered - Hot Pink highlight */}
        <div className="card-market p-5 rounded-2xl bg-[#E3447C] space-y-2 text-[#FFFFFF]">
          <div className="flex items-center justify-between text-[#FFFFFF]">
            <span className="text-xs font-display font-black uppercase">
              Opportunities
            </span>
            <Lightbulb className="w-4 h-4 fill-current text-[#FFFFFF]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#FFFFFF]">
            {loading ? "..." : formatNumber(stats?.discovered_opportunities || 0)}
          </p>
          <p className="text-[11px] font-bold uppercase opacity-90 text-[#FFFFFF]">
            Autonomous white-spaces
          </p>
        </div>

        {/* Total Hypotheses */}
        <div className="card-market p-5 rounded-2xl bg-[#FFFFFF] space-y-2">
          <div className="flex items-center justify-between text-[#64748B]">
            <span className="text-xs font-display font-black uppercase">
              Hypotheses
            </span>
            <TrendingUp className="w-4 h-4 text-[#0D1117]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#0D1117]">
            {loading ? "..." : formatNumber(stats?.total_hypotheses || 0)}
          </p>
          <p className="text-[11px] font-bold text-[#64748B] uppercase">
            Follow-up research loops
          </p>
        </div>

        {/* Risk Assessments */}
        <div className="card-market p-5 rounded-2xl bg-[#FFFFFF] space-y-2">
          <div className="flex items-center justify-between text-[#64748B]">
            <span className="text-xs font-display font-black uppercase">
              Risk Assessments
            </span>
            <AlertTriangle className="w-4 h-4 text-[#E3447C]" />
          </div>
          <p className="font-display font-black text-3xl sm:text-4xl text-[#E3447C]">
            {loading ? "..." : formatNumber(stats?.total_risks || 0)}
          </p>
          <p className="text-[11px] font-bold text-[#64748B] uppercase">
            5x5 matrix evaluations
          </p>
        </div>
      </div>

      {/* Visual Analytics Row: Bar Chart of Metrics + Claim Verification Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Research Activity Bar Chart */}
        <div className="lg:col-span-8 card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] space-y-6">
          <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-4">
            <div>
              <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
                PLATFORM SCALE
              </span>
              <h2 className="font-display font-black text-2xl uppercase text-[#0D1117]">
                Research Entity Distribution
              </h2>
            </div>
            <span className="px-3 py-1 rounded bg-[#F4F8FA] border border-[#0D1117] text-xs font-display font-bold uppercase">
              SQLite Ground Truth
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={activityData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 11, fontFamily: "var(--font-space)", fontWeight: 700 }}
                  stroke="#0D1117"
                />
                <YAxis
                  tick={{ fontSize: 11, fontFamily: "var(--font-space)" }}
                  stroke="#0D1117"
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0D1117",
                    border: "2px solid #08B0D5",
                    borderRadius: "8px",
                    color: "#FFFFFF",
                    fontFamily: "var(--font-space)",
                    fontWeight: 700,
                  }}
                />
                <Bar dataKey="count" fill="#08B0D5" stroke="#0D1117" strokeWidth={2} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Claim Verification Ratio & System Health */}
        <div className="lg:col-span-4 card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] space-y-6 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="border-b-2 border-[#0D1117] pb-4">
              <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
                CLAIM AUDITING
              </span>
              <h2 className="font-display font-black text-2xl uppercase text-[#0D1117]">
                Verification Ratio
              </h2>
            </div>

            <div className="flex items-center justify-center py-2">
              <div className="w-36 h-36">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={claimRatioData}
                      dataKey="value"
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={65}
                      stroke="#0D1117"
                      strokeWidth={2}
                    >
                      {claimRatioData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="space-y-2 text-xs font-display font-bold uppercase">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-[#08B0D5]"></span>
                  Verified Claims
                </span>
                <span className="font-black text-[#0D1117]">
                  {stats?.verified_claims || 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-[#E2E8F0] border border-[#0D1117]"></span>
                  Unverified / Filtered
                </span>
                <span className="font-black text-[#64748B]">
                  {Math.max(0, (stats?.total_claims || 0) - (stats?.verified_claims || 0))}
                </span>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t-2 border-[#0D1117]">
            <Link
              href="/app/evidence"
              className="btn-market w-full py-2.5 rounded-lg bg-[#F4F8FA] hover:bg-[#FFFFFF] text-xs font-display font-black uppercase text-center block"
            >
              Inspect Evidence Explorer →
            </Link>
          </div>
        </div>
      </div>

      {/* Top Discovered Opportunities Highlight */}
      <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b-2 border-[#0D1117] pb-4">
          <div>
            <span className="text-xs font-display font-black text-[#E3447C] uppercase tracking-wider">
              HIGH-IMPACT DISCOVERIES
            </span>
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117]">
              Top Autonomous Opportunities
            </h2>
          </div>
          <Link
            href="/app/opportunities"
            className="text-xs font-display font-black text-[#08B0D5] hover:underline uppercase flex items-center gap-1"
          >
            <span>View All Opportunities</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {opportunities.length === 0 ? (
          <div className="py-8 text-center space-y-3">
            <Lightbulb className="w-8 h-8 text-[#64748B] mx-auto" />
            <p className="text-xs font-display font-bold uppercase text-[#64748B]">
              No strategic opportunities recorded yet.
            </p>
            <Link
              href="/app/research/new"
              className="inline-block px-4 py-2 rounded-lg bg-[#08B0D5] border-2 border-[#0D1117] text-xs font-display font-black uppercase text-[#0D1117]"
            >
              Run an investigation to discover opportunities
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {opportunities.map((opp) => (
              <div
                key={opp.opportunity_id || opp.id}
                className="p-5 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] flex flex-col justify-between space-y-4 hover:border-[#08B0D5] transition-colors"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] text-[10px] font-display font-black uppercase">
                      {opp.target_customer || "Strategic Segment"}
                    </span>
                    <span className="px-2.5 py-1 rounded bg-[#E3447C] text-[#FFFFFF] border border-[#0D1117] text-xs font-display font-black">
                      {opp.risk_adjusted_score || opp.raw_score || 85}/100 SCORE
                    </span>
                  </div>
                  <h3 className="font-display font-black text-lg text-[#0D1117] uppercase leading-tight">
                    {opp.opportunity_name}
                  </h3>
                  <p className="text-xs text-[#64748B] font-medium leading-relaxed line-clamp-2">
                    {opp.description || opp.proposed_solution}
                  </p>
                </div>

                <div className="pt-2 border-t border-[#0D1117]/20 flex items-center justify-between text-xs">
                  <Link
                    href={`/app/simulator?opp=${encodeURIComponent(opp.opportunity_id || "")}`}
                    className="font-display font-bold text-[#08B0D5] hover:underline"
                  >
                    Simulate Unit Economics →
                  </Link>
                  <Link
                    href={`/app/opportunities/${opp.opportunity_id || opp.id}`}
                    className="font-display font-black text-[#0D1117] hover:underline"
                  >
                    Full Dossier →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent Investigations Table */}
      <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b-2 border-[#0D1117] pb-4">
          <div>
            <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
              AUDIT RECORD
            </span>
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117]">
              Recent Research Investigations
            </h2>
          </div>
          <Link
            href="/app/history"
            className="text-xs font-display font-black text-[#08B0D5] hover:underline uppercase flex items-center gap-1"
          >
            <span>View Full History</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {recentRuns.length === 0 ? (
          <div className="py-8 text-center space-y-3">
            <Search className="w-8 h-8 text-[#64748B] mx-auto" />
            <p className="text-xs font-display font-bold uppercase text-[#64748B]">
              No research runs recorded yet.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b-2 border-[#0D1117] font-display font-black uppercase text-[#64748B]">
                <tr>
                  <th className="py-3 px-4">Run ID / Objective</th>
                  <th className="py-3 px-4">Industry / Geography</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Evidence</th>
                  <th className="py-3 px-4">Claims</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E8F0] font-medium text-[#0D1117]">
                {recentRuns.map((run) => (
                  <tr key={run.id} className="hover:bg-[#F4F8FA] transition-colors">
                    <td className="py-3 px-4 max-w-xs truncate">
                      <p className="font-display font-bold text-[#0D1117] truncate">
                        {run.objective}
                      </p>
                      <p className="text-[10px] text-[#64748B] font-mono">
                        {run.id}
                      </p>
                    </td>
                    <td className="py-3 px-4">
                      <span>{run.industry}</span>
                      <span className="text-[#64748B] block text-[10px]">{run.geography}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`inline-block px-2 py-0.5 rounded text-[10px] font-display font-black uppercase ${
                          run.status === "completed"
                            ? "bg-[#08B0D5]/20 text-[#08B0D5] border border-[#08B0D5]"
                            : run.status === "running"
                            ? "bg-[#E3447C]/20 text-[#E3447C] border border-[#E3447C] animate-pulse"
                            : "bg-[#64748B]/20 text-[#0D1117]"
                        }`}
                      >
                        {run.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-bold">
                      {run.total_sources || 0} sources
                    </td>
                    <td className="py-3 px-4 font-bold text-[#08B0D5]">
                      {run.verified_claims || 0} verified
                    </td>
                    <td className="py-3 px-4 text-right">
                      <Link
                        href={`/app/research/${run.id}`}
                        className="btn-market inline-block px-3 py-1.5 rounded bg-[#08B0D5] text-[#0D1117] text-[10px] font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
                      >
                        Workspace →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
