"use client";

import React from "react";
import Link from "next/link";
import {
  Sparkles,
  ArrowRight,
  Zap,
  Search,
  CheckCircle2,
  TrendingUp,
  BarChart3,
  Lightbulb,
  FileText,
  Layers,
  Cpu,
  DollarSign,
  AlertTriangle,
  Database,
  Check,
  X,
  ShieldCheck,
  ArrowUpRight,
} from "lucide-react";

export default function ProductPage() {
  const features = [
    {
      title: "Autonomous Deep Web Spidering",
      desc: "Live multi-query search powered by Tavily. Dispatches dozens of targeted queries, downloads raw HTML, parses tables, extracts PDF documents, and generates sha256 content hashes.",
      tag: "STAGE 1",
    },
    {
      title: "7 Domain Specialist Analysts",
      desc: "Dedicated agents operating under Meta Spark 1.3 analyze macro market structure, competitor pricing tiers, customer complaint patterns, brand positioning, commercial gaps, and risk exposure.",
      tag: "MULTI-AGENT",
    },
    {
      title: "Autonomous Opportunity Discovery",
      desc: "Correlates customer friction points with competitor blind spots to generate testable business opportunities. Automatically triggers iterative follow-up investigations.",
      tag: "STAGE 2",
    },
    {
      title: "Atomic Evidence Extraction & Provenance",
      desc: "Breaks raw sources into atomic facts with exact excerpts, source URLs, publisher attribution, and date stamps. Zero ungrounded summaries.",
      tag: "VERIFICATION",
    },
    {
      title: "Deterministic Financial Simulation",
      desc: "Pure Python financial modeling with zero LLM arithmetic hallucinations. Computes revenue, gross margin, contribution margin, break-even orders, and 5D sensitivity analysis.",
      tag: "FINANCIAL MATH",
    },
    {
      title: "Editorial Executive Reports",
      desc: "Compiled by the Research Director (Meta Muse Wonder) into 10 structured sections with clickable citations, evidence drawers, and exports in Markdown, JSON, and PDF.",
      tag: "EXECUTIVE REPORTING",
    },
  ];

  const comparisonRows = [
    {
      capability: "Primary Source Acquisition",
      traditionalConsulting: "Weeks of manual analyst searching",
      genericChatbots: "Stale training data (no live web)",
      marketpulse: "Autonomous multi-query Tavily spidering",
    },
    {
      capability: "Evidence Provenance",
      traditionalConsulting: "Vague slide-deck footnotes",
      genericChatbots: "Frequent hallucinations without source URLs",
      marketpulse: "Atomic evidence cards with sha256 content hashes",
    },
    {
      capability: "Contradiction Detection",
      traditionalConsulting: "Filtered out to present tidy narrative",
      genericChatbots: "Ignores conflicting sources",
      marketpulse: "Explicit cross-examination & arbitration",
    },
    {
      capability: "Opportunity White-Space Discovery",
      traditionalConsulting: "Expensive custom engagement",
      genericChatbots: "Passive replies to prompt only",
      marketpulse: "Autonomous hypothesis generation & follow-up",
    },
    {
      capability: "Financial Scenario Modeling",
      traditionalConsulting: "Static Excel sheet with hidden formulas",
      genericChatbots: "Unreliable LLM math hallucinations",
      marketpulse: "Deterministic Python unit economics & sensitivity",
    },
    {
      capability: "Time to First Comprehensive Report",
      traditionalConsulting: "4 to 8 weeks",
      genericChatbots: "Instant but shallow paragraph",
      marketpulse: "3 to 8 minutes of exhaustive multi-agent research",
    },
  ];

  return (
    <div className="w-full bg-[#FFFFFF] text-[#0D1117]">
      {/* Product Hero */}
      <section className="w-full bg-[#0D1117] text-[#FFFFFF] py-20 px-4 sm:px-6 lg:px-8 border-b-2 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] font-display font-extrabold text-xs uppercase tracking-wider">
            <Sparkles className="w-4 h-4 fill-current" />
            <span>PRODUCT OVERVIEW</span>
          </div>

          <h1 className="font-display font-black uppercase text-5xl sm:text-7xl lg:text-8xl tracking-tight leading-[0.92]">
            ENGINEERED FOR
            <br />
            <span className="text-[#08B0D5]">STRATEGIC RIGOR.</span>
          </h1>

          <p className="text-lg sm:text-xl text-[#E2E8F0] max-w-3xl leading-relaxed font-medium">
            MARKETPULSE replaces slow, subjective human consulting and unreliable LLM chatbots with an inspectable, evidence-grounded multi-agent business intelligence platform.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-4">
            <Link
              href="/app/research/new"
              className="btn-market inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-sm uppercase shadow-market-sm hover:bg-[#068AA8]"
            >
              <span>Launch Research Run</span>
              <ArrowRight className="w-4 h-4 stroke-[3]" />
            </Link>
            <Link
              href="/how-it-works"
              className="btn-market inline-flex items-center gap-2 px-7 py-4 rounded-xl bg-[#FFFFFF] text-[#0D1117] font-display font-bold text-sm uppercase shadow-market-sm hover:bg-[#F4F8FA]"
            >
              <span>View Architecture</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Core Capabilities Grid */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="space-y-3">
          <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
            DEEP ARCHITECTURAL STRENGTHS
          </span>
          <h2 className="font-display font-black text-4xl sm:text-5xl uppercase tracking-tight text-[#0D1117]">
            Six Pillars of MarketPulse Intelligence
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feat) => (
            <div
              key={feat.title}
              className="card-market p-7 rounded-2xl flex flex-col justify-between space-y-4 bg-[#FFFFFF]"
            >
              <div className="space-y-3">
                <span className="inline-block px-2.5 py-0.5 rounded bg-[#08B0D5] text-[#0D1117] font-display font-black text-[11px] uppercase border border-[#0D1117]">
                  {feat.tag}
                </span>
                <h3 className="font-display font-black text-2xl uppercase text-[#0D1117] leading-tight">
                  {feat.title}
                </h3>
                <p className="text-sm text-[#64748B] leading-relaxed font-medium">
                  {feat.desc}
                </p>
              </div>

              <div className="pt-3 border-t border-[#E2E8F0]">
                <span className="text-xs font-display font-bold text-[#08B0D5] uppercase flex items-center gap-1">
                  Active in Platform <Check className="w-3.5 h-3.5 text-[#08B0D5]" />
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Comparative Matrix Section */}
      <section className="w-full bg-[#F4F8FA] py-20 px-4 sm:px-6 lg:px-8 border-y-2 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-10">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <span className="inline-block px-3 py-1 rounded bg-[#0D1117] text-[#FFFFFF] font-display font-black text-xs uppercase tracking-wider">
              HEAD-TO-HEAD COMPARISON
            </span>
            <h2 className="font-display font-black text-4xl sm:text-5xl uppercase text-[#0D1117]">
              Why Teams Choose MarketPulse
            </h2>
            <p className="text-base text-[#64748B] font-medium">
              See how our evidence-grounded autonomous system compares against traditional boutique consultancies and generic LLM tools.
            </p>
          </div>

          {/* Comparison Table */}
          <div className="overflow-x-auto rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg">
            <table className="w-full text-left text-sm">
              <thead className="bg-[#0D1117] text-[#FFFFFF] font-display font-black text-xs uppercase tracking-wider border-b-2 border-[#0D1117]">
                <tr>
                  <th className="py-4 px-6">Capability</th>
                  <th className="py-4 px-6 text-[#E2E8F0]">Traditional Consulting</th>
                  <th className="py-4 px-6 text-[#E2E8F0]">Generic AI Wrappers</th>
                  <th className="py-4 px-6 text-[#08B0D5] bg-[#161B22]">MARKETPULSE</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E8F0] font-medium">
                {comparisonRows.map((row, i) => (
                  <tr key={i} className="hover:bg-[#F4F8FA]/50 transition-colors">
                    <td className="py-4 px-6 font-display font-black text-[#0D1117]">
                      {row.capability}
                    </td>
                    <td className="py-4 px-6 text-[#64748B]">
                      {row.traditionalConsulting}
                    </td>
                    <td className="py-4 px-6 text-[#64748B]">
                      {row.genericChatbots}
                    </td>
                    <td className="py-4 px-6 font-bold text-[#0D1117] bg-[#08B0D5]/15 border-l-2 border-[#0D1117]">
                      {row.marketpulse}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* CTA Strip */}
      <section className="w-full bg-[#08B0D5] text-[#0D1117] py-16 px-4 sm:px-6 lg:px-8 text-center border-b-2 border-[#0D1117]">
        <div className="max-w-4xl mx-auto space-y-6">
          <h2 className="font-display font-black uppercase text-4xl sm:text-6xl text-[#0D1117] tracking-tight">
            Ready to experience autonomous intelligence?
          </h2>
          <p className="text-base sm:text-lg text-[#0D1117]/90 font-medium max-w-xl mx-auto">
            Run your first research investigation now. Completely inspectable, traceable, and backed by deterministic calculations.
          </p>
          <div className="pt-2">
            <Link
              href="/app/research/new"
              className="btn-market inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-[#0D1117] text-[#FFFFFF] font-display font-black text-base uppercase shadow-market-sm hover:bg-[#E3447C]"
            >
              <span>Launch Research Workspace</span>
              <ArrowRight className="w-5 h-5 stroke-[3]" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
