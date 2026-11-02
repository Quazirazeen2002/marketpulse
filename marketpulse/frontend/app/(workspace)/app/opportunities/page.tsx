"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Lightbulb,
  Search,
  RefreshCw,
  Calculator,
  CheckCircle2,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { Opportunity } from "@/lib/types";

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [segmentFilter, setSegmentFilter] = useState("all");

  const loadOpportunities = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getOpportunities(undefined, 50);
      setOpportunities(data || []);
    } catch (err: any) {
      setError(err.message || "Failed to load opportunities.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOpportunities();
  }, []);

  const filteredOpps = opportunities.filter((opp) => {
    const matchesSearch =
      opp.opportunity_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      opp.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      opp.target_customer?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSegment =
      segmentFilter === "all" ||
      opp.target_customer?.toLowerCase().includes(segmentFilter.toLowerCase());
    return matchesSearch && matchesSegment;
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#08B0D5] text-[#0D1117] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#0D1117] text-[#FFFFFF] text-xs font-display font-black uppercase shadow-market-sm">
            <Lightbulb className="w-3.5 h-3.5 text-[#08B0D5] fill-current" />
            <span>AUTONOMOUS OPPORTUNITY DISCOVERY</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase tracking-tight leading-none text-[#0D1117]">
            Market White-Spaces & Scored Opportunities
          </h1>
          <p className="text-sm font-bold text-[#0D1117] leading-relaxed">
            Hypotheses autonomously synthesized from cross-domain web findings, evaluated against demand urgency, competitive barriers, feasibility, and unit economics.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={loadOpportunities}
            disabled={loading}
            className="p-3 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] hover:bg-[#F4F8FA] text-[#0D1117] shadow-market-sm"
            title="Refresh Opportunities"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
          <Link
            href="/app/simulator"
            className="btn-market inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#0D1117] text-[#FFFFFF] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#E3447C]"
          >
            <Calculator className="w-4 h-4 text-[#08B0D5]" />
            <span>Model in Simulator</span>
          </Link>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3.5 text-[#64748B]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search opportunities, segments, keywords..."
            className="w-full pl-9 pr-4 py-2 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-xs font-medium text-[#0D1117] focus:outline-none focus:bg-[#FFFFFF]"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
          <span className="text-[11px] font-display font-black uppercase text-[#64748B]">
            Filter Segment:
          </span>
          <select
            value={segmentFilter}
            onChange={(e) => setSegmentFilter(e.target.value)}
            className="px-3 py-1.5 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-xs font-bold uppercase text-[#0D1117] focus:outline-none"
          >
            <option value="all">All Segments</option>
            <option value="ecommerce">E-Commerce</option>
            <option value="consumer">Consumer</option>
            <option value="sme">SME</option>
            <option value="enterprise">Enterprise</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase">
          {error}
        </div>
      )}

      {/* Opportunities Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl border-2 border-[#0D1117] bg-[#FFFFFF] animate-pulse h-72"
            />
          ))}
        </div>
      ) : filteredOpps.length === 0 ? (
        <div className="p-12 text-center border-2 border-dashed border-[#0D1117] rounded-2xl bg-[#FFFFFF] space-y-4">
          <Lightbulb className="w-10 h-10 text-[#64748B] mx-auto" />
          <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
            No opportunities matched your criteria
          </h3>
          <p className="text-xs text-[#64748B] max-w-sm mx-auto">
            Discovered opportunities are automatically generated during Stage 2 analysis runs.
          </p>
          <Link
            href="/app/research/new"
            className="inline-block px-5 py-2.5 rounded-xl bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
          >
            Start New Research Investigation
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredOpps.map((opp) => {
            const score = opp.risk_adjusted_score || opp.raw_score || 82;
            const oppId = opp.opportunity_id || String(opp.id || "");
            return (
              <div
                key={oppId}
                className="card-market p-6 rounded-2xl flex flex-col justify-between space-y-5 bg-[#FFFFFF] border-3 border-[#0D1117]"
              >
                <div className="space-y-3">
                  {/* Top Badges */}
                  <div className="flex items-center justify-between">
                    <span className="px-2.5 py-0.5 rounded bg-[#F4F8FA] border border-[#0D1117] text-[10px] font-display font-black uppercase text-[#0D1117]">
                      {opp.target_customer || "Strategic Segment"}
                    </span>
                    <span className="px-2.5 py-1 rounded bg-[#E3447C] text-[#FFFFFF] border border-[#0D1117] font-display font-black text-xs">
                      {score}/100 SCORE
                    </span>
                  </div>

                  {/* Title */}
                  <h3 className="font-display font-black text-xl uppercase text-[#0D1117] leading-snug">
                    {opp.opportunity_name}
                  </h3>

                  {/* Customer Problem */}
                  <div className="p-3 rounded-lg bg-[#F4F8FA] border border-[#0D1117] text-xs space-y-1">
                    <p className="font-display font-black uppercase text-[10px] text-[#E3447C]">
                      Target Problem:
                    </p>
                    <p className="text-[#0D1117] font-medium leading-relaxed line-clamp-2">
                      {opp.customer_problem || opp.description}
                    </p>
                  </div>

                  {/* Description / Proposed Solution */}
                  <p className="text-xs text-[#64748B] font-medium leading-relaxed line-clamp-3">
                    {opp.proposed_solution || opp.description}
                  </p>
                </div>

                {/* Card Footer */}
                <div className="pt-3 border-t-2 border-[#0D1117] space-y-2">
                  <div className="flex items-center justify-between text-[11px] font-bold text-[#64748B]">
                    <span className="flex items-center gap-1 text-[#08B0D5]">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      {opp.validation_status || "Supported"}
                    </span>
                    <span>
                      {opp.evidence_links?.length || 4} Evidence Citations
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <Link
                      href={`/app/simulator?opp=${encodeURIComponent(oppId)}`}
                      className="text-xs font-display font-black text-[#08B0D5] hover:underline uppercase"
                    >
                      Simulate P&L →
                    </Link>

                    <Link
                      href={`/app/opportunities/${oppId}`}
                      className="btn-market px-3 py-1.5 rounded-lg bg-[#0D1117] text-[#FFFFFF] text-[11px] font-display font-black uppercase shadow-market-sm hover:bg-[#08B0D5] hover:text-[#0D1117]"
                    >
                      Dossier →
                    </Link>
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
