"use client";

import React, { useState } from "react";
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
  ShieldCheck,
  GitBranch,
  Repeat,
  FileCheck,
} from "lucide-react";

export default function HowItWorksPage() {
  const [selectedPhase, setSelectedPhase] = useState<"stage1" | "stage2">("stage1");

  const stage1Steps = [
    {
      num: "01",
      title: "Research Objective Formulation & Decomposition",
      model: "Meta Muse Wonder (Director)",
      desc: "The Research Director receives the high-level business objective and target industry/geography. It decomposes the problem into orthogonal investigative questions tailored to macro structure, competitor behavior, and consumer demand.",
    },
    {
      num: "02",
      title: "Live Web Spidering & Document Acquisition",
      model: "Tavily Search API",
      desc: "Targeted queries crawl high-credibility industry publications, government statistics, competitor pricing pages, customer review boards, and financial disclosures. Content is cached and fingerprint-hashed.",
    },
    {
      num: "03",
      title: "Atomic Evidence Extraction",
      model: "Meta Spark 1.3 (Specialists)",
      desc: "Specialists parse raw HTML and PDFs into discrete evidence records. Each fact is tagged with an excerpt, source URL, publisher, timestamp, relevance score, and reliability rating.",
    },
    {
      num: "04",
      title: "Claim Verification & Contradiction Detection",
      model: "Meta Muse Wonder & Spark 1.3",
      desc: "Claims are matched against evidence. Supporting and contradicting evidence is cross-examined. If two sources dispute a metric (e.g., market growth rate), the system flags the contradiction with arbitration rationale.",
    },
    {
      num: "05",
      title: "Stage 1 Executive Intelligence Synthesis",
      model: "Meta Muse Wonder (Director)",
      desc: "The Director weaves verified claims into a cohesive, structured report with traceable evidence citations and comprehensive quality dimension scoring.",
    },
  ];

  const stage2Steps = [
    {
      num: "01",
      title: "Autonomous Opportunity Hypothesis Generation",
      model: "Opportunity Discovery Analyst (Spark 1.3)",
      desc: "Analyzes cross-domain signals (e.g. competitor pricing tiers vs customer friction points) to generate high-probability business hypotheses for underserved segments.",
    },
    {
      num: "02",
      title: "Autonomous Follow-Up Web Investigations",
      model: "LangGraph Dynamic Feedback Loop",
      desc: "Unlike standard static workflows, the system dynamically generates new Tavily search tasks to validate or reject its own hypotheses, running up to 3 iterative research loops.",
    },
    {
      num: "03",
      title: "Deterministic Opportunity Scoring",
      model: "MarketPulse Scoring Engine",
      desc: "Computes raw scores across Demand Urgency, Competitive White Space, Feasibility, and Monetization. Discloses dimension weights and raw calculations separately from risk assessments.",
    },
    {
      num: "04",
      title: "5x5 Risk & Vulnerability Matrix",
      model: "Risk & Industry Analyst (Spark 1.3)",
      desc: "Systematically assesses regulatory, supply chain, and competitive retaliation risks. Maps likelihood vs impact to compute residual risk scores and mitigation playbooks.",
    },
    {
      num: "05",
      title: "Deterministic Financial Scenario Modeling",
      model: "Python Simulation Engine",
      desc: "Runs Base, Best, and Worst case outcomes with 5D sensitivity analysis (price, orders, return rate, marketing, delivery) backed purely by Python unit-economics formulas.",
    },
    {
      num: "06",
      title: "Final 10-Section Strategic Executive Report",
      model: "Meta Muse Wonder (Director)",
      desc: "Synthesizes the complete strategic picture into an editorial report with executive summary, methodology, market analysis, competitor positioning, opportunity discovery, and scenario tables.",
    },
  ];

  return (
    <div className="w-full bg-[#FFFFFF] text-[#0D1117]">
      {/* Header Banner */}
      <section className="w-full bg-[#08B0D5] text-[#0D1117] py-20 px-4 sm:px-6 lg:px-8 border-b-2 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#0D1117] text-[#FFFFFF] font-display font-extrabold text-xs uppercase tracking-wider shadow-market-sm">
            <Cpu className="w-4 h-4 text-[#08B0D5]" />
            <span>AUTHORITATIVE ARCHITECTURE</span>
          </div>

          <h1 className="font-display font-black uppercase text-5xl sm:text-7xl lg:text-8xl tracking-tight leading-[0.92]">
            HOW MARKETPULSE
            <br />
            <span className="text-[#FFFFFF]">ACTUALLY WORKS.</span>
          </h1>

          <p className="text-lg sm:text-xl text-[#0D1117] max-w-3xl leading-relaxed font-bold">
            No magic black boxes. No hidden fallback models. See the exact multi-agent graph, data contracts, and deterministic execution pipeline behind every research run.
          </p>
        </div>
      </section>

      {/* Interactive Architecture Flow Diagram */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
            LANGGRAPH ORCHESTRATION GRAPH
          </span>
          <h2 className="font-display font-black text-4xl sm:text-5xl uppercase text-[#0D1117]">
            Two-Stage Autonomous Intelligence Engine
          </h2>
          <p className="text-base text-[#64748B] font-medium">
            Stage 1 establishes grounded factual evidence. Stage 2 executes autonomous strategic intelligence, opportunity discovery, and deterministic scenario simulation.
          </p>
        </div>

        {/* Phase Toggle Buttons */}
        <div className="flex justify-center gap-4">
          <button
            onClick={() => setSelectedPhase("stage1")}
            className={`btn-market px-6 py-3.5 rounded-xl font-display font-black text-sm uppercase transition-all ${
              selectedPhase === "stage1"
                ? "bg-[#0D1117] text-[#08B0D5] shadow-market"
                : "bg-[#FFFFFF] text-[#0D1117] border-2 border-[#0D1117]"
            }`}
          >
            Stage 1: Evidence-Driven Research
          </button>
          <button
            onClick={() => setSelectedPhase("stage2")}
            className={`btn-market px-6 py-3.5 rounded-xl font-display font-black text-sm uppercase transition-all ${
              selectedPhase === "stage2"
                ? "bg-[#E3447C] text-[#FFFFFF] shadow-market"
                : "bg-[#FFFFFF] text-[#0D1117] border-2 border-[#0D1117]"
            }`}
          >
            Stage 2: Strategic Intelligence & Discovery
          </button>
        </div>

        {/* Visual Graph Nodes */}
        <div className="p-8 rounded-2xl border-3 border-[#0D1117] bg-[#F4F8FA] shadow-market-lg space-y-6">
          <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-4">
            <span className="font-display font-black text-sm uppercase text-[#0D1117]">
              {selectedPhase === "stage1"
                ? "STAGE 1 EXECUTION GRAPH (EVIDENCE PROVENANCE)"
                : "STAGE 2 EXECUTION GRAPH (OPPORTUNITIES & SIMULATION)"}
            </span>
            <span className="px-3 py-1 rounded bg-[#08B0D5] border border-[#0D1117] font-display font-black text-xs uppercase text-[#0D1117]">
              LANGGRAPH STATEFUL GRAPH
            </span>
          </div>

          <div className="space-y-4">
            {(selectedPhase === "stage1" ? stage1Steps : stage2Steps).map((step) => (
              <div
                key={step.num}
                className="p-5 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
              >
                <div className="flex items-start gap-4">
                  <span className="w-10 h-10 rounded-lg bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] font-display font-black text-base flex items-center justify-center shrink-0">
                    {step.num}
                  </span>
                  <div className="space-y-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-display font-black text-lg text-[#0D1117] uppercase">
                        {step.title}
                      </h3>
                      <span className="px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] text-[11px] font-bold uppercase">
                        {step.model}
                      </span>
                    </div>
                    <p className="text-xs text-[#64748B] font-medium leading-relaxed max-w-3xl">
                      {step.desc}
                    </p>
                  </div>
                </div>

                <span className="px-3 py-1 rounded bg-[#F4F8FA] border border-[#0D1117] text-[11px] font-display font-bold uppercase text-[#08B0D5] shrink-0">
                  Deterministic Step
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Model Allocation Governance Callout */}
      <section className="w-full bg-[#0D1117] text-[#FFFFFF] py-20 px-4 sm:px-6 lg:px-8 border-t-2 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="space-y-3">
            <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
              MANDATORY GOVERNANCE
            </span>
            <h2 className="font-display font-black text-4xl sm:text-5xl uppercase tracking-tight">
              Strict AI Model Allocation
            </h2>
            <p className="text-sm sm:text-base text-[#E2E8F0] max-w-3xl font-medium leading-relaxed">
              To guarantee repeatable depth and high-integrity reasoning, MARKETPULSE enforces an explicit architectural separation between synthesizing and specialist roles:
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="p-6 rounded-2xl border-2 border-[#1E293B] bg-[#161B22] space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-display font-black text-xl text-[#08B0D5] uppercase">
                  Meta Muse Wonder
                </span>
                <span className="px-2.5 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-black uppercase">
                  Director Model
                </span>
              </div>
              <p className="text-xs text-[#E2E8F0] leading-relaxed">
                Allocated exclusively to the Research Director. Handles multi-hypothesis cross-examination, arbitration of conflicting sources, executive narrative synthesis, and research depth evaluation.
              </p>
            </div>

            <div className="p-6 rounded-2xl border-2 border-[#1E293B] bg-[#161B22] space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-display font-black text-xl text-[#E3447C] uppercase">
                  Meta Spark 1.3
                </span>
                <span className="px-2.5 py-1 rounded bg-[#E3447C] text-[#FFFFFF] text-xs font-black uppercase">
                  Specialist Model
                </span>
              </div>
              <p className="text-xs text-[#E2E8F0] leading-relaxed">
                Allocated to all 7 specialist agents: Market, Competitor, Customer, Marketing, Commercial, Opportunity Discovery, and Risk & Industry analysts. Provides structured extraction without drift.
              </p>
            </div>
          </div>

          <div className="pt-4 flex items-center justify-center">
            <Link
              href="/app/research/new"
              className="btn-market inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-base uppercase shadow-market hover:bg-[#068AA8]"
            >
              <span>Test The Pipeline Yourself</span>
              <ArrowRight className="w-5 h-5 stroke-[3]" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
