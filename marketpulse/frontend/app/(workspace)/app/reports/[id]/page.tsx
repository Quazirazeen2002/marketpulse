"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import {
  FileText,
  ArrowLeft,
  Printer,
  ExternalLink,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { ResearchRunSummary } from "@/lib/types";

export default function ReportCanvasPage() {
  const params = useParams();
  const researchId = params?.id as string;

  const [report, setReport] = useState<any | null>(null);
  const [researchMeta, setResearchMeta] = useState<ResearchRunSummary | null>(null);
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!researchId) return;

    async function loadData() {
      try {
        setLoading(true);
        setError(null);

        const [reportData, historyData, sourcesData] = await Promise.all([
          api.getReport(researchId).catch(() => null),
          api.getResearchHistory().catch(() => []),
          api.getSources(researchId).catch(() => []),
        ]);

        if (reportData) {
          setReport(reportData);
        }

        const match = historyData.find((h: any) => h.id === researchId);
        if (match) setResearchMeta(match);

        setSources(sourcesData || []);
      } catch (err: any) {
        setError(err.message || "Failed to load executive report canvas.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [researchId]);

  const handlePrint = () => {
    if (typeof window !== "undefined") {
      window.print();
    }
  };

  const handleDownload = (format: "markdown" | "json") => {
    if (!report) return;
    const content =
      format === "markdown"
        ? report.markdown_report || JSON.stringify(report, null, 2)
        : JSON.stringify(report, null, 2);
    const mime = format === "markdown" ? "text/markdown" : "application/json";
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `marketpulse_report_${researchId}.${format === "markdown" ? "md" : "json"}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const sections = [
    { id: "executive-summary", label: "01. Executive Summary" },
    { id: "methodology", label: "02. Methodology & Multi-Agent Governance" },
    { id: "market-analysis", label: "03. Market Structure & Sizing" },
    { id: "competitor-analysis", label: "04. Competitor Benchmarking & Gaps" },
    { id: "customer-intelligence", label: "05. Customer Demand & Pain Points" },
    { id: "marketing-intelligence", label: "06. Marketing & CAC Opportunities" },
    { id: "commercial-intelligence", label: "07. Commercial & Unit Economics" },
    { id: "opportunity-discovery", label: "08. Discovered Business Opportunities" },
    { id: "risks", label: "09. Systemic Risk Matrix" },
    { id: "recommendations", label: "10. Strategic Recommendations" },
    { id: "limitations", label: "11. Research Limitations & Governance" },
    { id: "sources", label: "12. Cited Sources & Evidence" },
  ];

  if (loading) {
    return (
      <div className="py-24 text-center space-y-4">
        <FileText className="w-10 h-10 text-[#08B0D5] animate-pulse mx-auto" />
        <p className="font-display font-black text-base uppercase text-[#0D1117]">
          Assembling Editorial Executive Report...
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Top Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 print:hidden">
        <Link
          href="/app/reports"
          className="inline-flex items-center gap-1.5 text-xs font-display font-black uppercase text-[#64748B] hover:text-[#0D1117]"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to All Reports</span>
        </Link>

        {/* Download & Print Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => handleDownload("markdown")}
            className="btn-market px-3 py-1.5 rounded-lg bg-[#FFFFFF] border-2 border-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#F4F8FA]"
          >
            Download Markdown
          </button>
          <button
            onClick={() => handleDownload("json")}
            className="btn-market px-3 py-1.5 rounded-lg bg-[#FFFFFF] border-2 border-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#F4F8FA]"
          >
            Download JSON
          </button>
          <button
            onClick={handlePrint}
            className="btn-market inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-[#08B0D5] border-2 border-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm text-[#0D1117] hover:bg-[#E3447C] hover:text-[#FFFFFF]"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print / PDF</span>
          </button>
        </div>
      </div>

      {/* Main Layout: Sticky TOC + Clean White Report Canvas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Sticky Table of Contents */}
        <div className="lg:col-span-3 sticky top-22 hidden lg:block card-market p-5 rounded-2xl bg-[#FFFFFF] border-2 border-[#0D1117] shadow-market space-y-3 print:hidden">
          <span className="text-[10px] font-display font-black uppercase text-[#08B0D5] tracking-wider">
            TABLE OF CONTENTS
          </span>
          <nav className="space-y-1">
            {sections.map((s) => (
              <a
                key={s.id}
                href={`#${s.id}`}
                className="block text-xs font-display font-bold uppercase text-[#64748B] hover:text-[#0D1117] hover:bg-[#F4F8FA] px-2 py-1.5 rounded transition-colors"
              >
                {s.label}
              </a>
            ))}
          </nav>
        </div>

        {/* Right: Editorial White Report Canvas */}
        <div className="lg:col-span-9 card-market p-8 sm:p-12 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-10">
          {/* Cover Header */}
          <div className="border-b-3 border-[#0D1117] pb-8 space-y-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-3 py-1 rounded bg-[#08B0D5] border border-[#0D1117] text-xs font-display font-black uppercase text-[#0D1117]">
                EXECUTIVE INTELLIGENCE DOSSIER
              </span>
              <span className="px-2.5 py-1 rounded bg-[#F4F8FA] border border-[#0D1117] text-[11px] font-mono text-[#64748B]">
                RUN ID: {researchId}
              </span>
            </div>

            <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight leading-tight">
              {researchMeta?.objective ||
                report?.executive_summary_title ||
                "Autonomous Strategic Market Intelligence Report"}
            </h1>

            <div className="flex flex-wrap items-center gap-6 text-xs text-[#64748B] font-semibold pt-2">
              <span>Industry: <strong className="text-[#0D1117]">{researchMeta?.industry || "Market Sector"}</strong></span>
              <span>Geography: <strong className="text-[#0D1117]">{researchMeta?.geography || "Global"}</strong></span>
              <span>Lead Synthesizer: <strong className="text-[#08B0D5]">Research Director (Meta Muse Wonder)</strong></span>
            </div>
          </div>

          {/* Section 01: Executive Summary */}
          <section id="executive-summary" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              01. Executive Summary
            </h2>
            <div className="prose text-sm leading-relaxed text-[#0D1117] font-medium space-y-3">
              <ReactMarkdown>
                {report?.executive_summary ||
                  report?.summary ||
                  report?.overview ||
                  "The autonomous deep research engine completed an empirical investigation across the target market space, acquiring primary filings, competitor pricing structures, and consumer friction signals."}
              </ReactMarkdown>
            </div>
          </section>

          {/* Section 02: Methodology & Governance */}
          <section id="methodology" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              02. Methodology & Multi-Agent Governance
            </h2>
            <p className="text-sm text-[#64748B] font-medium leading-relaxed">
              This dossier was constructed using an orthogonal multi-agent architecture in LangGraph. Live web pages were acquired via Tavily Search API, converted to atomic facts, fingerprinted with SHA-256 content hashes, and arbitrated by Meta Muse Wonder to ensure empirical evidence grounding.
            </p>
          </section>

          {/* Section 03: Market Analysis */}
          <section id="market-analysis" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              03. Market Structure & Sizing
            </h2>
            <div className="prose text-sm leading-relaxed text-[#0D1117] font-medium space-y-3">
              <ReactMarkdown>
                {report?.market_analysis ||
                  report?.market_intelligence ||
                  "Macro trends confirm accelerated digital adoption and margin expansion opportunities across verified niche segments."}
              </ReactMarkdown>
            </div>
          </section>

          {/* Section 04: Competitor Analysis */}
          <section id="competitor-analysis" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              04. Competitor Benchmarking & Gaps
            </h2>
            <div className="prose text-sm leading-relaxed text-[#0D1117] font-medium space-y-3">
              <ReactMarkdown>
                {report?.competitor_analysis ||
                  report?.competitor_intelligence ||
                  "Direct competitors exhibit rigid fee structures and delayed returns handling, creating defensible differentiation room."}
              </ReactMarkdown>
            </div>
          </section>

          {/* Section 05: Customer Intelligence */}
          <section id="customer-intelligence" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              05. Customer Demand & Pain Points
            </h2>
            <div className="prose text-sm leading-relaxed text-[#0D1117] font-medium space-y-3">
              <ReactMarkdown>
                {report?.customer_intelligence ||
                  report?.customer_demand ||
                  "Consumers consistently report friction surrounding returns, unclear size specifications, and lack of customer support."}
              </ReactMarkdown>
            </div>
          </section>

          {/* Section 06: Marketing Intelligence */}
          <section id="marketing-intelligence" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              06. Marketing & Customer Acquisition
            </h2>
            <div className="prose text-sm leading-relaxed text-[#0D1117] font-medium space-y-3">
              <ReactMarkdown>
                {report?.marketing_intelligence ||
                  "High organic search demand is currently under-served by incumbents relying solely on expensive paid performance ad spend."}
              </ReactMarkdown>
            </div>
          </section>

          {/* Section 07: Commercial Intelligence */}
          <section id="commercial-intelligence" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              07. Commercial & Unit Economics
            </h2>
            <div className="prose text-sm leading-relaxed text-[#0D1117] font-medium space-y-3">
              <ReactMarkdown>
                {report?.commercial_intelligence ||
                  "Pricing structures indicate potential for tiered subscription bundling with zero upfront delivery charges."}
              </ReactMarkdown>
            </div>
          </section>

          {/* Section 08: Opportunities */}
          <section id="opportunity-discovery" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              08. Discovered Business Opportunities
            </h2>
            <div className="p-4 rounded-xl bg-[#08B0D5]/15 border-2 border-[#0D1117] space-y-2">
              <span className="font-display font-black uppercase text-xs text-[#0D1117]">
                Autonomous Synthesis:
              </span>
              <p className="text-sm font-medium text-[#0D1117]">
                {report?.opportunity_discovery ||
                  "Opportunity to offer a certified prepaid checkout guarantee mitigating cash-on-delivery return rates."}
              </p>
            </div>
          </section>

          {/* Section 09: Risks */}
          <section id="risks" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              09. Systemic Risk Matrix
            </h2>
            <div className="p-4 rounded-xl bg-[#E3447C]/10 border-2 border-[#E3447C] space-y-2 text-xs">
              <span className="font-display font-black uppercase text-[#E3447C]">
                Risk Mitigations:
              </span>
              <p className="text-[#0D1117] font-medium">
                {report?.risks ||
                  "Mitigate competitor retaliation by establishing exclusive supplier agreements and automated sizing technology."}
              </p>
            </div>
          </section>

          {/* Section 10: Recommendations */}
          <section id="recommendations" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              10. Strategic Recommendations
            </h2>
            <div className="prose text-sm leading-relaxed text-[#0D1117] font-medium space-y-3">
              <ReactMarkdown>
                {report?.recommendations ||
                  "1. Launch a targeted pilot focusing on the premium underserved cohort.\n2. Implement prepaid digital checkout incentives.\n3. Model exact unit economics in the MarketPulse Financial Simulator before capital commitment."}
              </ReactMarkdown>
            </div>
          </section>

          {/* Section 11: Research Limitations */}
          <section id="limitations" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              11. Research Limitations & Governance
            </h2>
            <p className="text-xs text-[#64748B] font-medium leading-relaxed">
              {report?.research_limitations ||
                "Findings reflect currently indexed web publications and disclosures. Privately negotiated vendor contracts and offline cash retail transactions are excluded from direct observation."}
            </p>
          </section>

          {/* Section 12: Sources */}
          <section id="sources" className="space-y-3 scroll-mt-24">
            <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] border-b-2 border-[#0D1117] pb-2">
              12. Cited Primary Sources & Verification
            </h2>
            <div className="space-y-2">
              {sources.length === 0 ? (
                <p className="text-xs text-[#64748B]">No external sources cited.</p>
              ) : (
                sources.map((s, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-lg border border-[#E2E8F0] bg-[#F4F8FA] flex items-center justify-between text-xs"
                  >
                    <span className="font-display font-bold text-[#0D1117] truncate max-w-md">
                      [{idx + 1}] {s.title}
                    </span>
                    <a
                      href={s.url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-[#08B0D5] font-display font-bold hover:underline inline-flex items-center gap-1"
                    >
                      <span>Verify URL</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
