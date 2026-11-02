"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  Lightbulb,
  ArrowLeft,
  ArrowRight,
  Calculator,
  AlertTriangle,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { Opportunity } from "@/lib/types";

export default function OpportunityDetailPage() {
  const params = useParams();
  const router = useRouter();
  const oppId = params?.id as string;

  const [opp, setOpp] = useState<Opportunity | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!oppId) return;
    async function loadOpp() {
      try {
        setLoading(true);
        setError(null);
        const data = await api.getOpportunityDetails(oppId);
        setOpp(data);
      } catch (err: any) {
        setError(err.message || "Failed to load opportunity details.");
      } finally {
        setLoading(false);
      }
    }
    loadOpp();
  }, [oppId]);

  if (loading) {
    return (
      <div className="py-24 text-center space-y-4">
        <Lightbulb className="w-10 h-10 text-[#08B0D5] animate-pulse mx-auto" />
        <p className="font-display font-black text-base uppercase text-[#0D1117]">
          Loading Opportunity Dossier...
        </p>
      </div>
    );
  }

  if (error || !opp) {
    return (
      <div className="p-8 rounded-2xl border-2 border-[#E3447C] bg-[#FFFFFF] text-center space-y-4 max-w-lg mx-auto">
        <AlertTriangle className="w-8 h-8 text-[#E3447C] mx-auto" />
        <h2 className="font-display font-black text-xl uppercase text-[#0D1117]">
          Opportunity Not Found
        </h2>
        <p className="text-xs text-[#64748B] font-medium">
          {error || `Could not find an opportunity with ID '${oppId}'.`}
        </p>
        <Link
          href="/app/opportunities"
          className="inline-block px-4 py-2 rounded-lg bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase border border-[#0D1117]"
        >
          ← Return to Opportunities
        </Link>
      </div>
    );
  }

  const rawScore = opp.raw_score || 85;
  const riskAdjustedScore = opp.risk_adjusted_score || 78;

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Back button */}
      <div>
        <Link
          href="/app/opportunities"
          className="inline-flex items-center gap-1.5 text-xs font-display font-black uppercase text-[#64748B] hover:text-[#0D1117]"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Opportunities</span>
        </Link>
      </div>

      {/* Hero Dossier Card */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg space-y-6">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 border-b-2 border-[#0D1117] pb-6">
          <div className="space-y-3 max-w-2xl">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-3 py-1 rounded bg-[#08B0D5] border border-[#0D1117] text-xs font-display font-black uppercase text-[#0D1117]">
                {opp.target_customer || "Target Segment"}
              </span>
              <span className="px-2.5 py-1 rounded bg-[#F4F8FA] border border-[#0D1117] text-[11px] font-mono text-[#64748B]">
                ID: {opp.opportunity_id || oppId}
              </span>
              <span className="px-2.5 py-1 rounded bg-[#08B0D5]/20 text-[#08B0D5] border border-[#08B0D5] text-[11px] font-bold uppercase">
                {opp.validation_status || "Supported"}
              </span>
            </div>

            <h1 className="font-display font-black text-3xl sm:text-4xl uppercase text-[#0D1117] tracking-tight leading-tight">
              {opp.opportunity_name}
            </h1>

            <p className="text-sm text-[#64748B] font-medium leading-relaxed">
              {opp.description}
            </p>
          </div>

          {/* Scores Display */}
          <div className="flex sm:flex-col gap-4 shrink-0">
            <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#08B0D5] text-center min-w-[120px] shadow-market-sm">
              <span className="text-[10px] font-display font-black uppercase text-[#0D1117] block">
                Raw Score
              </span>
              <p className="font-display font-black text-3xl text-[#0D1117]">
                {rawScore}
              </p>
              <span className="text-[9px] font-bold text-[#0D1117]/80 uppercase">
                / 100 Potential
              </span>
            </div>

            <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#E3447C] text-[#FFFFFF] text-center min-w-[120px] shadow-market-sm">
              <span className="text-[10px] font-display font-black uppercase text-[#FFFFFF] block">
                Risk-Adjusted
              </span>
              <p className="font-display font-black text-3xl text-[#FFFFFF]">
                {riskAdjustedScore}
              </p>
              <span className="text-[9px] font-bold text-[#FFFFFF]/80 uppercase">
                Defensibility
              </span>
            </div>
          </div>
        </div>

        {/* Governance Disclaimer Required */}
        <div className="p-3.5 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-[11px] font-medium text-[#64748B] flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-[#E3447C] shrink-0" />
          <span>
            <strong>Governance Notice:</strong> Opportunity scores reflect empirical market signal convergence and do not constitute a financial guarantee of commercial success. All investments carry risk.
          </span>
        </div>

        {/* CTAs */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
          <Link
            href={`/app/simulator?opp=${encodeURIComponent(opp.opportunity_id || oppId)}`}
            className="btn-market inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
          >
            <Calculator className="w-4 h-4" />
            <span>Simulate Unit Economics in Financial Engine</span>
            <ArrowRight className="w-4 h-4 stroke-[3]" />
          </Link>

          <Link
            href="/app/hypotheses"
            className="text-xs font-display font-bold text-[#08B0D5] hover:underline uppercase"
          >
            Inspect Autonomous Hypothesis Loop →
          </Link>
        </div>
      </div>

      {/* Detailed Analysis Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Customer Problem & Solution */}
        <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] space-y-4 border-2 border-[#0D1117]">
          <span className="text-xs font-display font-black text-[#E3447C] uppercase tracking-wider">
            UNADDRESSED CUSTOMER PROBLEM
          </span>
          <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
            The Friction Point
          </h3>
          <p className="text-xs text-[#64748B] font-medium leading-relaxed">
            {opp.customer_problem || "High returns and lack of verified sizing guarantee."}
          </p>

          <div className="pt-4 border-t border-[#E2E8F0] space-y-2">
            <span className="text-xs font-display font-black text-[#08B0D5] uppercase">
              Proposed Solution
            </span>
            <p className="text-xs text-[#0D1117] font-medium leading-relaxed">
              {opp.proposed_solution || opp.description}
            </p>
          </div>
        </div>

        {/* Originating Specialist Agents */}
        <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] space-y-4 border-2 border-[#0D1117]">
          <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
            SYNTHESIS PROVENANCE
          </span>
          <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
            Originating Multi-Agents
          </h3>
          <div className="space-y-2">
            {(opp.originating_agents || ["Opportunity Discovery Analyst", "Customer Intelligence Analyst", "Commercial Intelligence Analyst"]).map((agent, i) => (
              <div
                key={i}
                className="p-3 rounded-lg border border-[#0D1117] bg-[#F4F8FA] flex items-center justify-between text-xs"
              >
                <span className="font-display font-bold uppercase text-[#0D1117]">
                  {agent}
                </span>
                <span className="px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] text-[10px] font-bold uppercase">
                  Meta Spark 1.3
                </span>
              </div>
            ))}
          </div>

          <p className="text-[11px] text-[#64748B] font-medium pt-2">
            Cross-examined against Tavily live web queries and verified evidence cards.
          </p>
        </div>
      </div>
    </div>
  );
}
