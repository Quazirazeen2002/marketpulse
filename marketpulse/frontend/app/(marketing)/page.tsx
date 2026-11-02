"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  ArrowRight,
  Zap,
  ShieldCheck,
  Search,
  CheckCircle2,
  TrendingUp,
  BarChart3,
  Lightbulb,
  FileText,
  Layers,
  Cpu,
  Compass,
  DollarSign,
  AlertTriangle,
  ArrowUpRight,
  Database,
  ExternalLink,
  ChevronRight,
  Check,
} from "lucide-react";

export default function MarketingLandingPage() {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      num: "01",
      title: "Define your business question",
      desc: "Specify your objective, industry vertical, target geography, and investigation depth. The Research Director decomposes the problem into structured investigative angles.",
      tag: "ORCHESTRATION",
    },
    {
      num: "02",
      title: "Investigate the market",
      desc: "Tavily spidering crawls high-credibility primary sources, filings, industry reports, and publications. Raw HTML is normalized and content-fingerprinted.",
      tag: "SOURCE ACQUISITION",
    },
    {
      num: "03",
      title: "Analyze customers & competitors",
      desc: "Specialists extract pricing tiers, feature matrices, customer complaints, friction points, and market dynamics into atomic evidence cards.",
      tag: "EVIDENCE EXTRACTION",
    },
    {
      num: "04",
      title: "Discover opportunities",
      desc: "Autonomous cross-domain correlation detects unexploited market white spaces, underserved customer cohorts, and pricing anomalies.",
      tag: "WHITE-SPACE DISCOVERY",
    },
    {
      num: "05",
      title: "Validate hypotheses",
      desc: "When a potential opportunity surfaces, the engine autonomously spawns follow-up search queries to verify or contradict the hypothesis.",
      tag: "AUTONOMOUS LOOP",
    },
    {
      num: "06",
      title: "Evaluate business risks",
      desc: "Systemic risk analysts model a 5x5 severity matrix spanning regulatory hurdles, competitor retaliation, unit economics, and operational traps.",
      tag: "RISK MATRIX",
    },
    {
      num: "07",
      title: "Simulate strategic scenarios",
      desc: "Deterministic Python financial engine runs Base, Best, and Worst case outcomes with 5D sensitivity analysis on orders, prices, and return rates.",
      tag: "FINANCIAL SIMULATION",
    },
    {
      num: "08",
      title: "Generate intelligence reports",
      desc: "Synthesize an executive-ready 10-section report complete with traceable citations, evidence IDs, and downloadable Markdown, JSON, and PDF formats.",
      tag: "EXECUTIVE SYNTHESIS",
    },
  ];

  const specialists = [
    {
      name: "Market Intelligence Analyst",
      role: "Macro & Industry Dynamics",
      model: "Meta Spark 1.3",
      desc: "Evaluates market size, segment CAGR, macroeconomic tailwinds, and structural shifts.",
      color: "bg-[#08B0D5]",
      textColor: "text-[#0D1117]",
    },
    {
      name: "Competitor Intelligence Analyst",
      role: "Competitive Strategy & Positioning",
      model: "Meta Spark 1.3",
      desc: "Maps direct/indirect players, analyzes pricing tiers, distribution channels, and capability gaps.",
      color: "bg-[#0D1117]",
      textColor: "text-[#FFFFFF]",
    },
    {
      name: "Customer Intelligence Analyst",
      role: "Demand & Friction Mapping",
      model: "Meta Spark 1.3",
      desc: "Extracts persona motivations, unaddressed complaint patterns, and willingness-to-pay signals.",
      color: "bg-[#08B0D5]",
      textColor: "text-[#0D1117]",
    },
    {
      name: "Marketing Intelligence Analyst",
      role: "Go-to-Market & Acquisition Channels",
      model: "Meta Spark 1.3",
      desc: "Dissects competitor campaign messaging, organic search gaps, and high-leverage marketing angles.",
      color: "bg-[#FFFFFF]",
      textColor: "text-[#0D1117]",
    },
    {
      name: "Commercial Intelligence Analyst",
      role: "Monetization & Unit Economics",
      model: "Meta Spark 1.3",
      desc: "Benchmarks fee structures, margin thresholds, hidden charges, and commercial friction.",
      color: "bg-[#08B0D5]",
      textColor: "text-[#0D1117]",
    },
    {
      name: "Opportunity Discovery Analyst",
      role: "Autonomous Hypothesis Generator",
      model: "Meta Spark 1.3",
      desc: "Surfaces unaddressed market niches and triggers targeted autonomous follow-up investigations.",
      color: "bg-[#E3447C]",
      textColor: "text-[#FFFFFF]",
    },
    {
      name: "Risk & Industry Analyst",
      role: "Threat & Vulnerability Assessment",
      model: "Meta Spark 1.3",
      desc: "Models 5x5 severity matrix, regulatory risks, competitor response risks, and mitigations.",
      color: "bg-[#E3447C]",
      textColor: "text-[#FFFFFF]",
    },
  ];

  const useCases = [
    {
      industry: "E-Commerce & Retail",
      headline: "Fashion E-commerce in Emerging Markets",
      problem: "High return rates and cash-on-delivery friction eroding operating margins.",
      solution: "Uncovered underserved premium modest-fashion segment with prepaid digital checkout incentives.",
      score: 87,
    },
    {
      industry: "Telecommunications",
      headline: "Customer Experience & Fiber Monetization",
      problem: "Subscriber churn driven by opaque throttling and complex billing structures.",
      solution: "Identified low-latency gamer bundle with guaranteed SLA and transparent pricing.",
      score: 84,
    },
    {
      industry: "Food Delivery",
      headline: "Dark Kitchens & Merchant Logistics",
      problem: "Merchant commission fatigue and delivery driver retention deficits.",
      solution: "Modeled hybrid subscription + batch delivery model improving contribution margin by 14%.",
      score: 91,
    },
    {
      industry: "Financial Services",
      headline: "SME Micro-Lending & Cash Flow",
      problem: "Traditional collateral requirements blocking high-volume small merchant loans.",
      solution: "Designed invoice-backed automated underwriting tied to POS inventory turns.",
      score: 89,
    },
    {
      industry: "Manufacturing",
      headline: "Supply-Chain Decoupling & Sourcing",
      problem: "Single-source vulnerability in raw material supply chain causing assembly delays.",
      solution: "Validated dual-sourcing network with regional suppliers, lowering stockout risks by 35%.",
      score: 82,
    },
    {
      industry: "Technology & SaaS",
      headline: "Enterprise AI Workflow Tooling",
      problem: "Generic LLM wrappers facing extreme customer churn and low willingness-to-pay.",
      solution: "Targeted deterministic compliance audit automation with traceable evidence provenance.",
      score: 93,
    },
    {
      industry: "Healthcare Operations",
      headline: "Specialty Clinic Scheduling & Utilization",
      problem: "No-show rates of 22% resulting in severe physician downtime and lost clinic revenue.",
      solution: "Built predictive multi-channel reminder cadence with digital pre-intake verification.",
      score: 86,
    },
    {
      industry: "Logistics & Fleet",
      headline: "Last-Mile Cold Chain Monitoring",
      problem: "Perishable spoilage disputes between 3PL carriers and pharmaceutical vendors.",
      solution: "Autonomous IoT sensor verification with real-time exception alerting and proof of delivery.",
      score: 88,
    },
  ];

  return (
    <div className="w-full overflow-hidden">
      {/* =========================================================================
          SECTION 3: HERO SECTION
          MrBeast-inspired oversized typography, high contrast, vibrant electric cyan focal point
          ========================================================================= */}
      <section className="relative w-full bg-[#08B0D5] text-[#0D1117] border-b-2 border-[#0D1117] pt-12 sm:pt-20 pb-16 sm:pb-24 px-4 sm:px-6 lg:px-8">
        {/* Decorative Floating Badges */}
        <div className="absolute top-6 right-6 lg:right-16 hidden sm:block rotate-3 z-10">
          <span className="inline-block px-4 py-2 rounded-lg bg-[#0D1117] text-[#FFFFFF] font-display font-black text-xs uppercase tracking-wider shadow-market-sm border border-[#FFFFFF]">
            ⚡ 8 MULTI-AGENTS • EMPIRICAL EVIDENCE
          </span>
        </div>
        <div className="absolute bottom-8 left-6 hidden lg:block -rotate-3 z-10">
          <span className="inline-block px-4 py-2 rounded-lg bg-[#E3447C] text-[#FFFFFF] font-display font-black text-xs uppercase tracking-wider shadow-market-sm border border-[#0D1117]">
            🔬 TRACEABLE CITATIONS & EVIDENCE
          </span>
        </div>

        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Column: Headlines & CTAs */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-[#0D1117] text-[#FFFFFF] border-2 border-[#0D1117] text-xs font-display font-extrabold uppercase tracking-wide shadow-market-sm">
                <Sparkles className="w-4 h-4 text-[#08B0D5] fill-current" />
                <span>Next-Generation Autonomous Market Intelligence</span>
              </div>

              {/* Main Headline */}
              <h1 className="font-display font-black uppercase text-5xl sm:text-7xl lg:text-8xl tracking-tight leading-[0.92] text-[#0D1117]">
                STOP GUESSING.
                <br />
                <span className="text-[#FFFFFF] underline decoration-[#0D1117] decoration-4">
                  START DISCOVERING.
                </span>
              </h1>

              {/* Sub-Headline */}
              <p className="font-display font-extrabold text-xl sm:text-2xl text-[#0D1117] uppercase tracking-tight">
                Your market is moving. Your intelligence should move faster.
              </p>

              {/* Supporting Description */}
              <p className="text-base sm:text-lg text-[#0D1117] font-medium leading-relaxed max-w-2xl">
                MARKETPULSE investigates markets, understands competitors, discovers business opportunities, and turns raw web evidence into validated, strategic decisions backed by deterministic financial modeling.
              </p>

              {/* Primary & Secondary CTAs */}
              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Link
                  href="/app/research/new"
                  className="btn-market inline-flex items-center gap-3 px-8 py-4 rounded-xl bg-[#0D1117] text-[#FFFFFF] hover:bg-[#E3447C] font-display font-black text-base uppercase tracking-wider shadow-market-lg"
                >
                  <Zap className="w-5 h-5 text-[#08B0D5] fill-current" />
                  <span>START YOUR RESEARCH</span>
                  <ArrowRight className="w-5 h-5 stroke-[3]" />
                </Link>

                <Link
                  href="/product"
                  className="btn-market inline-flex items-center gap-2 px-7 py-4 rounded-xl bg-[#FFFFFF] text-[#0D1117] hover:bg-[#F4F8FA] font-display font-extrabold text-base uppercase tracking-wider shadow-market"
                >
                  <span>EXPLORE THE PLATFORM</span>
                </Link>
              </div>

              {/* Trust/Evidence Proof Pills */}
              <div className="pt-4 flex flex-wrap items-center gap-6 text-xs font-display font-bold text-[#0D1117] uppercase">
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-[#0D1117]" />
                  Meta Muse Wonder Director
                </span>
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-[#0D1117]" />
                  Meta Spark 1.3 Specialists
                </span>
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-[#0D1117]" />
                  Tavily Live Web Spidering
                </span>
              </div>
            </div>

            {/* Right Column: Visual Composition of the MARKETPULSE Intelligence Engine */}
            <div className="lg:col-span-5">
              <div className="relative rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] p-6 shadow-market-xl space-y-4">
                {/* Header of Simulated Engine Monitor */}
                <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
                  <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full bg-[#E3447C] border border-[#0D1117]"></span>
                    <span className="w-3.5 h-3.5 rounded-full bg-[#08B0D5] border border-[#0D1117]"></span>
                    <span className="w-3.5 h-3.5 rounded-full bg-[#22c55e] border border-[#0D1117]"></span>
                  </div>
                  <span className="font-display font-black text-xs uppercase tracking-wider text-[#0D1117]">
                    INTELLIGENCE ENGINE • ACTIVE
                  </span>
                </div>

                {/* Director Node */}
                <div className="p-3.5 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-[#08B0D5] text-[#0D1117] flex items-center justify-center font-display font-black text-sm">
                      RD
                    </div>
                    <div>
                      <p className="font-display font-extrabold text-sm text-[#0D1117]">
                        Research Director
                      </p>
                      <p className="text-xs text-[#64748B] font-semibold">
                        Meta Muse Wonder • Synthesizer
                      </p>
                    </div>
                  </div>
                  <span className="px-2.5 py-1 rounded-md bg-[#22c55e]/20 border border-[#22c55e] text-[#15803d] text-[11px] font-bold uppercase">
                    ORCHESTRATING
                  </span>
                </div>

                {/* Live Signal Stream Cards */}
                <div className="space-y-2.5">
                  <div className="p-3 rounded-lg border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm flex items-start gap-3">
                    <div className="w-7 h-7 rounded bg-[#08B0D5] text-[#0D1117] flex items-center justify-center shrink-0 mt-0.5">
                      <Search className="w-4 h-4" />
                    </div>
                    <div className="text-xs space-y-0.5 min-w-0">
                      <p className="font-display font-bold text-[#0D1117] truncate">
                        Tavily Search: 18 primary sources retrieved
                      </p>
                      <p className="text-[#64748B] truncate">
                        Extracted 42 atomic evidence statements with URL hashes
                      </p>
                    </div>
                  </div>

                  <div className="p-3 rounded-lg border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm flex items-start gap-3">
                    <div className="w-7 h-7 rounded bg-[#E3447C] text-[#FFFFFF] flex items-center justify-center shrink-0 mt-0.5">
                      <Lightbulb className="w-4 h-4" />
                    </div>
                    <div className="text-xs space-y-0.5 min-w-0">
                      <p className="font-display font-bold text-[#0D1117] truncate">
                        Opportunity Discovered: COD Mitigation Bundle
                      </p>
                      <p className="text-[#64748B]">
                        Score: <span className="font-black text-[#08B0D5]">89/100</span> • Risk-Adjusted: <span className="font-bold text-[#0D1117]">Low Risk</span>
                      </p>
                    </div>
                  </div>

                  <div className="p-3 rounded-lg border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm flex items-start gap-3">
                    <div className="w-7 h-7 rounded bg-[#08B0D5] text-[#0D1117] flex items-center justify-center shrink-0 mt-0.5">
                      <DollarSign className="w-4 h-4" />
                    </div>
                    <div className="text-xs space-y-0.5 min-w-0">
                      <p className="font-display font-bold text-[#0D1117] truncate">
                        Python Simulation: +$14,200 Monthly Profit
                      </p>
                      <p className="text-[#64748B]">
                        Deterministic Math • Break-even: 642 orders/month
                      </p>
                    </div>
                  </div>
                </div>

                {/* Footer Status Pill */}
                <div className="pt-2 flex items-center justify-between text-xs font-display font-extrabold text-[#64748B]">
                  <span className="flex items-center gap-1.5 text-[#0D1117]">
                    <span className="w-2.5 h-2.5 rounded-full bg-[#22c55e] animate-ping"></span>
                    Continuous LangGraph Stream
                  </span>
                  <Link
                    href="/app"
                    className="text-[#08B0D5] hover:underline flex items-center gap-1"
                  >
                    View Observatory <ArrowUpRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 4: INTELLIGENCE IN ACTION
          "MORE THAN SEARCH. MORE THAN SUMMARIES."
          3 bold feature panels: Discover what is happening / Find what competitors are missing / Decide what to do next
          ========================================================================= */}
      <section className="w-full bg-[#FFFFFF] text-[#0D1117] border-b-2 border-[#0D1117] py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto space-y-4">
            <span className="inline-block px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] font-display font-extrabold text-xs uppercase tracking-wider shadow-market-sm">
              THE MARKETPULSE ADVANTAGE
            </span>
            <h2 className="font-display font-black uppercase text-4xl sm:text-6xl text-[#0D1117] tracking-tight leading-none">
              MORE THAN SEARCH.
              <br />
              <span className="text-[#08B0D5]">MORE THAN SUMMARIES.</span>
            </h2>
            <p className="text-base sm:text-lg text-[#64748B] font-medium">
              Ordinary tools regurgitate hallucinated generic paragraphs. MARKETPULSE verifies claims against acquired evidence, identifies hidden market white spaces, and calculates actual unit economics.
            </p>
          </div>

          {/* 3 Bold Panels */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Panel 1 */}
            <div className="card-market p-8 rounded-2xl flex flex-col justify-between space-y-6 bg-[#F4F8FA]">
              <div className="space-y-4">
                <div className="w-14 h-14 rounded-xl bg-[#08B0D5] text-[#FFFFFF] border-2 border-[#0D1117] flex items-center justify-center shadow-market-sm">
                  <Search className="w-7 h-7" />
                </div>
                <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
                  01 / SIGNAL ACQUISITION
                </span>
                <h3 className="font-display font-extrabold text-2xl uppercase tracking-tight text-[#0D1117]">
                  Discover what is happening.
                </h3>
                <p className="text-sm text-[#0D1117]/80 leading-relaxed font-medium">
                  We don’t rely on stale training data. Autonomous spiders acquire fresh industry filings, user reviews, pricing pages, and news through Tavily, extracting atomized evidence cards with complete provenance.
                </p>
              </div>

              <div className="border-t-2 border-[#0D1117] pt-4">
                <span className="text-xs font-display font-bold uppercase text-[#0D1117] flex items-center gap-1.5">
                  <Check className="w-4 h-4 text-[#08B0D5] stroke-[3]" />
                  Evidence-Grounded Factual Audit Standard
                </span>
              </div>
            </div>

            {/* Panel 2 */}
            <div className="card-market p-8 rounded-2xl flex flex-col justify-between space-y-6 bg-[#08B0D5] text-[#0D1117]">
              <div className="space-y-4">
                <div className="w-14 h-14 rounded-xl bg-[#0D1117] text-[#08B0D5] border-2 border-[#0D1117] flex items-center justify-center shadow-market-sm">
                  <Lightbulb className="w-7 h-7" />
                </div>
                <span className="text-xs font-display font-black text-[#0D1117] uppercase tracking-wider">
                  02 / WHITE-SPACE ANALYSIS
                </span>
                <h3 className="font-display font-extrabold text-2xl uppercase tracking-tight text-[#0D1117]">
                  Find what competitors are missing.
                </h3>
                <p className="text-sm text-[#0D1117]/90 leading-relaxed font-medium">
                  Autonomous hypothesis synthesis correlates customer complaints with competitor pricing gaps to unearth hidden business opportunities your rivals have overlooked.
                </p>
              </div>

              <div className="border-t-2 border-[#0D1117] pt-4">
                <span className="text-xs font-display font-bold uppercase text-[#0D1117] flex items-center gap-1.5">
                  <Check className="w-4 h-4 text-[#0D1117] stroke-[3]" />
                  Autonomous Follow-up Investigation
                </span>
              </div>
            </div>

            {/* Panel 3 */}
            <div className="card-market p-8 rounded-2xl flex flex-col justify-between space-y-6 bg-[#FFFFFF]">
              <div className="space-y-4">
                <div className="w-14 h-14 rounded-xl bg-[#E3447C] text-[#FFFFFF] border-2 border-[#0D1117] flex items-center justify-center shadow-market-sm">
                  <TrendingUp className="w-7 h-7" />
                </div>
                <span className="text-xs font-display font-black text-[#E3447C] uppercase tracking-wider">
                  03 / DECISION ENGINEERING
                </span>
                <h3 className="font-display font-extrabold text-2xl uppercase tracking-tight text-[#0D1117]">
                  Decide what to do next.
                </h3>
                <p className="text-sm text-[#0D1117]/80 leading-relaxed font-medium">
                  Every opportunity is backed by deterministic financial modeling. Simulate pricing, return rates, CAC, and order volume to calculate exact break-even requirements before deploying capital.
                </p>
              </div>

              <div className="border-t-2 border-[#0D1117] pt-4">
                <span className="text-xs font-display font-bold uppercase text-[#0D1117] flex items-center gap-1.5">
                  <Check className="w-4 h-4 text-[#E3447C] stroke-[3]" />
                  Deterministic Python Math
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 5: THE INTELLIGENCE ENGINE
          "EIGHT MINDS. ONE INTELLIGENCE ENGINE."
          Show Research Director (Muse Wonder) + Seven Specialist Agents (Spark 1.3)
          ========================================================================= */}
      <section className="w-full bg-[#0D1117] text-[#FFFFFF] border-b-2 border-[#0D1117] py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Section Header */}
          <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 border-b border-[#1E293B] pb-8">
            <div className="space-y-3">
              <span className="inline-block px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase tracking-wider">
                MULTI-AGENT REASONING ARCHITECTURE
              </span>
              <h2 className="font-display font-black uppercase text-4xl sm:text-6xl text-[#FFFFFF] tracking-tight leading-none">
                EIGHT MINDS.
                <br />
                <span className="text-[#08B0D5]">ONE INTELLIGENCE ENGINE.</span>
              </h2>
            </div>
            <p className="max-w-md text-sm text-[#E2E8F0] leading-relaxed">
              Every investigation is orchestrated by a Chief Intelligence Director and executed by seven domain specialists, each assigned precise model allocations without fallback or degradation.
            </p>
          </div>

          {/* Director Banner Card */}
          <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#FFFFFF] bg-[#08B0D5] text-[#0D1117] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-xl bg-[#0D1117] text-[#08B0D5] border-2 border-[#0D1117] flex items-center justify-center font-display font-black text-2xl shadow-market-sm">
                RD
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-display font-black text-2xl uppercase">
                    Research Director
                  </h3>
                  <span className="px-2.5 py-0.5 rounded-full bg-[#0D1117] text-[#08B0D5] text-xs font-display font-extrabold uppercase">
                    Meta Muse Wonder
                  </span>
                </div>
                <p className="text-sm text-[#0D1117]/90 font-medium mt-1">
                  Chief Synthesizer • Hypothesis Formulation • Contradiction Arbitration • Executive Report Synthesis
                </p>
              </div>
            </div>

            <Link
              href="/app/agents"
              className="btn-market inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-[#0D1117] text-[#FFFFFF] font-display font-extrabold text-sm uppercase shadow-market-sm hover:bg-[#E3447C] shrink-0"
            >
              <span>Inspect in Observatory</span>
              <ArrowRight className="w-4 h-4 stroke-[3]" />
            </Link>
          </div>

          {/* 7 Specialist Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {specialists.map((agent, idx) => (
              <div
                key={agent.name}
                className="p-5 rounded-xl border-2 border-[#1E293B] bg-[#161B22] hover:border-[#08B0D5] transition-all space-y-3 flex flex-col justify-between"
              >
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between">
                    <span className="w-7 h-7 rounded-md bg-[#0D1117] text-[#08B0D5] font-display font-bold text-xs flex items-center justify-center border border-[#1E293B]">
                      0{idx + 1}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-[#0D1117] border border-[#1E293B] text-[#E2E8F0] text-[10px] font-bold uppercase">
                      {agent.model}
                    </span>
                  </div>
                  <h4 className="font-display font-black text-lg text-[#FFFFFF] leading-snug">
                    {agent.name}
                  </h4>
                  <p className="text-xs font-bold text-[#08B0D5] uppercase">
                    {agent.role}
                  </p>
                  <p className="text-xs text-[#E2E8F0] leading-relaxed">
                    {agent.desc}
                  </p>
                </div>

                <div className="pt-2 border-t border-[#1E293B] flex items-center justify-between text-[11px] text-[#64748B]">
                  <span>LangGraph Node</span>
                  <span className="text-[#22c55e] font-bold">READY</span>
                </div>
              </div>
            ))}

            {/* Final Info Card */}
            <div className="p-5 rounded-xl border-2 border-[#E3447C] bg-[#E3447C] text-[#FFFFFF] flex flex-col justify-between space-y-4 shadow-market-sm">
              <div className="space-y-2">
                <span className="inline-block px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] text-[10px] font-black uppercase">
                  ZERO FALLBACK
                </span>
                <h4 className="font-display font-black text-xl uppercase leading-tight">
                  Deterministic Model Allocation
                </h4>
                <p className="text-xs text-[#FFFFFF]/90 font-medium leading-relaxed">
                  No hidden model swaps. All 7 specialists strictly execute on Meta Spark 1.3, while the Director reasons on Meta Muse Wonder.
                </p>
              </div>

              <Link
                href="/how-it-works"
                className="inline-flex items-center gap-1.5 text-xs font-display font-black uppercase text-[#FFFFFF] hover:underline"
              >
                Learn Architecture →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 6: HOW IT WORKS
          8-Step Process with engaging storytelling layout
          ========================================================================= */}
      <section className="w-full bg-[#F4F8FA] text-[#0D1117] border-b-2 border-[#0D1117] py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto space-y-4">
            <span className="inline-block px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] font-display font-black text-xs uppercase tracking-wider shadow-market-sm">
              EVIDENCE-DRIVEN PIPELINE
            </span>
            <h2 className="font-display font-black uppercase text-4xl sm:text-6xl text-[#0D1117] tracking-tight leading-none">
              FROM QUESTION TO STRATEGY
              <br />
              <span className="text-[#E3447C]">IN EIGHT PRECISION STEPS</span>
            </h2>
            <p className="text-base sm:text-lg text-[#64748B] font-medium">
              Click through the execution stages to see how MARKETPULSE transforms unstructured web noise into validated business decisions.
            </p>
          </div>

          {/* Interactive Steps Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left Column: Step Navigation List */}
            <div className="lg:col-span-5 space-y-2">
              {steps.map((step, idx) => (
                <button
                  key={step.num}
                  onClick={() => setActiveStep(idx)}
                  className={`w-full text-left p-4 rounded-xl border-2 transition-all flex items-center justify-between ${
                    activeStep === idx
                      ? "border-[#0D1117] bg-[#08B0D5] shadow-market text-[#0D1117]"
                      : "border-transparent bg-[#FFFFFF] hover:border-[#0D1117] text-[#0D1117]"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="font-display font-black text-base opacity-75">
                      {step.num}
                    </span>
                    <span className="font-display font-extrabold text-sm uppercase">
                      {step.title}
                    </span>
                  </div>
                  <ChevronRight
                    className={`w-4 h-4 transition-transform ${
                      activeStep === idx ? "rotate-90 stroke-[3]" : ""
                    }`}
                  />
                </button>
              ))}
            </div>

            {/* Right Column: Step Detail Display */}
            <div className="lg:col-span-7">
              <div className="card-market p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-6">
                <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-4">
                  <span className="px-3 py-1 rounded bg-[#0D1117] text-[#08B0D5] font-display font-black text-xs uppercase tracking-wider">
                    {steps[activeStep].tag}
                  </span>
                  <span className="font-display font-black text-3xl text-[#08B0D5]">
                    STEP {steps[activeStep].num} / 08
                  </span>
                </div>

                <div className="space-y-4">
                  <h3 className="font-display font-black text-3xl uppercase text-[#0D1117] tracking-tight">
                    {steps[activeStep].title}
                  </h3>
                  <p className="text-base text-[#0D1117]/80 leading-relaxed font-medium">
                    {steps[activeStep].desc}
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-[#F4F8FA] border-2 border-[#0D1117] space-y-2 text-xs">
                  <p className="font-display font-extrabold uppercase text-[#0D1117]">
                    Execution Guarantees:
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[#64748B] font-semibold">
                    <span className="flex items-center gap-1.5 text-[#0D1117]">
                      <Check className="w-3.5 h-3.5 text-[#22c55e]" />
                      Persistent SQLite State
                    </span>
                    <span className="flex items-center gap-1.5 text-[#0D1117]">
                      <Check className="w-3.5 h-3.5 text-[#22c55e]" />
                      Real-time SSE Event Stream
                    </span>
                    <span className="flex items-center gap-1.5 text-[#0D1117]">
                      <Check className="w-3.5 h-3.5 text-[#22c55e]" />
                      Claim Verification Verification
                    </span>
                    <span className="flex items-center gap-1.5 text-[#0D1117]">
                      <Check className="w-3.5 h-3.5 text-[#22c55e]" />
                      Zero Silent Fallbacks
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2">
                  <button
                    disabled={activeStep === 0}
                    onClick={() => setActiveStep((prev) => Math.max(0, prev - 1))}
                    className="px-4 py-2 rounded-lg border border-[#0D1117] text-xs font-display font-bold uppercase disabled:opacity-30"
                  >
                    ← Previous
                  </button>
                  <button
                    disabled={activeStep === steps.length - 1}
                    onClick={() =>
                      setActiveStep((prev) => Math.min(steps.length - 1, prev + 1))
                    }
                    className="btn-market px-5 py-2 rounded-lg bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase disabled:opacity-30 shadow-market-sm hover:bg-[#068AA8]"
                  >
                    Next Step →
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 7: OPPORTUNITY DISCOVERY SHOWCASE
          "THE BEST OPPORTUNITIES ARE THE ONES YOU HAVEN'T ASKED ABOUT YET."
          Illustrative Example: Pain point -> Hypothesis -> Follow-up -> Evidence -> Business Opportunity
          ========================================================================= */}
      <section className="w-full bg-[#FFFFFF] text-[#0D1117] border-b-2 border-[#0D1117] py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Header */}
          <div className="max-w-3xl space-y-4">
            <span className="inline-block px-3 py-1 rounded bg-[#E3447C] text-[#FFFFFF] border-2 border-[#0D1117] font-display font-black text-xs uppercase tracking-wider shadow-market-sm">
              AUTONOMOUS DISCOVERY LOOP
            </span>
            <h2 className="font-display font-black uppercase text-4xl sm:text-6xl text-[#0D1117] tracking-tight leading-none">
              THE BEST OPPORTUNITIES
              <br />
              <span className="text-[#08B0D5]">ARE THE ONES YOU HAVEN&apos;T ASKED ABOUT YET.</span>
            </h2>
            <p className="text-base sm:text-lg text-[#64748B] font-medium leading-relaxed">
              Traditional research only answers what you query. MARKETPULSE generates autonomous hypotheses from raw findings, triggers its own follow-up web investigations, and delivers scored business opportunities.
            </p>
          </div>

          {/* Illustrative Pipeline Walkthrough */}
          <div className="relative rounded-2xl border-3 border-[#0D1117] bg-[#08B0D5] p-6 sm:p-10 shadow-market-xl space-y-8">
            <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-4">
              <span className="font-display font-black text-sm uppercase text-[#0D1117] tracking-wider">
                ILLUSTRATIVE LIFECYCLE: E-COMMERCE RETURN RATE MITIGATION
              </span>
              <span className="px-3 py-1 rounded bg-[#0D1117] text-[#FFFFFF] text-xs font-display font-extrabold uppercase">
                DEMONSTRATION TEMPLATE
              </span>
            </div>

            {/* 5-Step Flow Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              {/* Card 1 */}
              <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm space-y-2">
                <span className="w-6 h-6 rounded bg-[#08B0D5] text-[#0D1117] font-display font-bold text-xs flex items-center justify-center">
                  1
                </span>
                <p className="font-display font-black text-xs text-[#08B0D5] uppercase">
                  Customer Pain Point
                </p>
                <p className="text-xs text-[#0D1117] font-medium">
                  34% of fashion apparel orders returned due to sizing ambiguity and rigid cash-on-delivery returns.
                </p>
              </div>

              {/* Card 2 */}
              <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm space-y-2">
                <span className="w-6 h-6 rounded bg-[#0D1117] text-[#FFFFFF] font-display font-bold text-xs flex items-center justify-center">
                  2
                </span>
                <p className="font-display font-black text-xs text-[#0D1117] uppercase">
                  Opportunity Hypothesis
                </p>
                <p className="text-xs text-[#0D1117] font-medium">
                  Customers will adopt prepaid digital checkout if paired with instant home try-on and 100% size guarantee.
                </p>
              </div>

              {/* Card 3 */}
              <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm space-y-2">
                <span className="w-6 h-6 rounded bg-[#E3447C] text-[#FFFFFF] font-display font-bold text-xs flex items-center justify-center">
                  3
                </span>
                <p className="font-display font-black text-xs text-[#E3447C] uppercase">
                  Autonomous Web Search
                </p>
                <p className="text-xs text-[#0D1117] font-medium">
                  Engine executes 4 Tavily queries targeting regional logistics SLAs, 3PL returns cost, and checkout conversion rates.
                </p>
              </div>

              {/* Card 4 */}
              <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm space-y-2">
                <span className="w-6 h-6 rounded bg-[#22c55e] text-[#0D1117] font-display font-bold text-xs flex items-center justify-center">
                  4
                </span>
                <p className="font-display font-black text-xs text-[#15803d] uppercase">
                  Verified Evidence
                </p>
                <p className="text-xs text-[#0D1117] font-medium">
                  7 primary sources verify prepaid checkout reduces return frequency by 41% while cutting reverse logistics expense.
                </p>
              </div>

              {/* Card 5 */}
              <div className="p-4 rounded-xl border-2 border-[#0D1117] bg-[#0D1117] text-[#FFFFFF] shadow-market-sm space-y-2">
                <span className="w-6 h-6 rounded bg-[#08B0D5] text-[#0D1117] font-display font-bold text-xs flex items-center justify-center">
                  5
                </span>
                <p className="font-display font-black text-xs text-[#08B0D5] uppercase">
                  Business Opportunity
                </p>
                <p className="text-xs text-[#E2E8F0] font-medium">
                  Score: <span className="text-[#08B0D5] font-bold">89/100</span>. Deterministic modeling projects +$18,400 monthly profit uplift.
                </p>
              </div>
            </div>

            <div className="pt-2 flex flex-wrap items-center justify-between gap-4">
              <span className="text-xs font-display font-bold text-[#0D1117] uppercase">
                Ready to run this on your industry?
              </span>
              <Link
                href="/app/opportunities"
                className="btn-market inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-[#0D1117] text-[#FFFFFF] font-display font-extrabold text-xs uppercase shadow-market-sm hover:bg-[#E3447C]"
              >
                <span>Explore Opportunity Dashboard</span>
                <ArrowRight className="w-4 h-4 stroke-[3]" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 8: BUSINESS INTELLIGENCE USE CASES
          Industry Cards (Illustrative): E-commerce, Telecom, Food delivery, Financial services, Retail, Manufacturing, Technology, Healthcare
          ========================================================================= */}
      <section className="w-full bg-[#F4F8FA] text-[#0D1117] border-b-2 border-[#0D1117] py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b-2 border-[#0D1117] pb-6">
            <div className="space-y-3">
              <span className="inline-block px-3 py-1 rounded bg-[#08B0D5] border-2 border-[#0D1117] font-display font-black text-xs uppercase tracking-wider shadow-market-sm text-[#0D1117]">
                CROSS-INDUSTRY APPLICABILITY
              </span>
              <h2 className="font-display font-black uppercase text-4xl sm:text-6xl text-[#0D1117] tracking-tight leading-none">
                PROVEN IN REAL MARKETS
              </h2>
            </div>
            <p className="max-w-md text-sm text-[#64748B] font-medium">
              Explore how MARKETPULSE investigates competitive gaps, pricing structures, and consumer friction across diverse sectors.
            </p>
          </div>

          {/* 8 Industry Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {useCases.map((uc) => (
              <div
                key={uc.headline}
                className="card-market p-6 rounded-2xl flex flex-col justify-between space-y-4 bg-[#FFFFFF]"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="px-2.5 py-0.5 rounded bg-[#F4F8FA] border border-[#0D1117] text-[11px] font-display font-black uppercase text-[#0D1117]">
                      {uc.industry}
                    </span>
                    <span className="font-display font-black text-xs text-[#08B0D5]">
                      {uc.score}/100 SCORE
                    </span>
                  </div>

                  <h3 className="font-display font-black text-lg uppercase text-[#0D1117] leading-tight">
                    {uc.headline}
                  </h3>

                  <div className="space-y-1 text-xs">
                    <p className="text-[#64748B]">
                      <span className="font-bold text-[#E3447C]">Problem:</span> {uc.problem}
                    </p>
                    <p className="text-[#0D1117] font-medium">
                      <span className="font-bold text-[#08B0D5]">Opportunity:</span> {uc.solution}
                    </p>
                  </div>
                </div>

                <div className="pt-3 border-t border-[#E2E8F0] flex items-center justify-between text-xs">
                  <span className="text-[11px] font-bold text-[#64748B] uppercase">
                    Illustrative Scenario
                  </span>
                  <Link
                    href="/use-cases"
                    className="text-[#08B0D5] font-display font-bold hover:underline flex items-center gap-1"
                  >
                    View Details →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 9: RESEARCH EXPERIENCE
          Original product preview composition: Timeline, Agent Observatory, Evidence, Opportunity, Report
          ========================================================================= */}
      <section className="w-full bg-[#0D1117] text-[#FFFFFF] border-b-2 border-[#0D1117] py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto space-y-4">
            <span className="inline-block px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase tracking-wider">
              INSPECTABLE RESEARCH WORKSPACE
            </span>
            <h2 className="font-display font-black uppercase text-4xl sm:text-6xl text-[#FFFFFF] tracking-tight leading-none">
              THE WORKSPACE YOU WISHED
              <br />
              <span className="text-[#08B0D5]">YOUR CONSULTANTS USED</span>
            </h2>
            <p className="text-base sm:text-lg text-[#E2E8F0] font-medium">
              Every step is open to inspection. Trace any sentence in the final report back to the exact URL, author, timestamp, and verification status.
            </p>
          </div>

          {/* Product Canvas Mockup */}
          <div className="rounded-2xl border-3 border-[#FFFFFF] bg-[#161B22] p-4 sm:p-8 shadow-market-xl space-y-6">
            {/* Top Command Bar */}
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-4">
              <div className="flex items-center gap-3">
                <span className="w-3.5 h-3.5 rounded-full bg-[#22c55e] animate-pulse"></span>
                <span className="font-display font-black text-sm uppercase text-[#FFFFFF] tracking-wide">
                  RESEARCH RUN #RUN-8F2B9C • ACTIVE
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs font-display font-bold">
                <span className="px-3 py-1 rounded bg-[#0D1117] border border-[#1E293B] text-[#E2E8F0]">
                  34 SOURCES
                </span>
                <span className="px-3 py-1 rounded bg-[#0D1117] border border-[#1E293B] text-[#08B0D5]">
                  89 EVIDENCE CARDS
                </span>
                <span className="px-3 py-1 rounded bg-[#0D1117] border border-[#1E293B] text-[#22c55e]">
                  42 VERIFIED CLAIMS
                </span>
              </div>
            </div>

            {/* Split Preview Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Column: Real-time Timeline & Agent Events */}
              <div className="lg:col-span-5 p-5 rounded-xl border-2 border-[#1E293B] bg-[#0D1117] space-y-4">
                <div className="flex items-center justify-between border-b border-[#1E293B] pb-2">
                  <span className="font-display font-black text-xs uppercase text-[#08B0D5]">
                    AGENT EXECUTION STREAM
                  </span>
                  <span className="text-[10px] text-[#64748B]">SSE STREAM</span>
                </div>

                <div className="space-y-3 text-xs">
                  <div className="p-2.5 rounded bg-[#161B22] border-l-3 border-[#08B0D5]">
                    <p className="font-bold text-[#FFFFFF]">Director Decomposed Objectives</p>
                    <p className="text-[#E2E8F0] text-[11px]">Spawned 4 investigative sub-threads</p>
                  </div>
                  <div className="p-2.5 rounded bg-[#161B22] border-l-3 border-[#08B0D5]">
                    <p className="font-bold text-[#FFFFFF]">Tavily Search Dispatched</p>
                    <p className="text-[#E2E8F0] text-[11px]">Acquired 18 primary sources (PDF & HTML)</p>
                  </div>
                  <div className="p-2.5 rounded bg-[#161B22] border-l-3 border-[#22c55e]">
                    <p className="font-bold text-[#FFFFFF]">Claim Verification Completed</p>
                    <p className="text-[#E2E8F0] text-[11px]">42 verified, 0 ungrounded claims accepted</p>
                  </div>
                  <div className="p-2.5 rounded bg-[#161B22] border-l-3 border-[#E3447C]">
                    <p className="font-bold text-[#FFFFFF]">Contradiction Arbitrated</p>
                    <p className="text-[#E2E8F0] text-[11px]">Pricing discrepancy flagged in 2 filings</p>
                  </div>
                </div>
              </div>

              {/* Right Column: Executive Report White Canvas */}
              <div className="lg:col-span-7 p-6 rounded-xl border-2 border-[#1E293B] bg-[#FFFFFF] text-[#0D1117] space-y-4">
                <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-2">
                  <span className="font-display font-black text-xs uppercase text-[#08B0D5]">
                    EXECUTIVE REPORT PREVIEW
                  </span>
                  <span className="text-xs font-bold text-[#64748B]">10 SECTIONS READY</span>
                </div>

                <div className="space-y-2">
                  <h4 className="font-display font-black text-xl uppercase tracking-tight">
                    Strategic Market Analysis: Modest Fashion Digital Sourcing
                  </h4>
                  <p className="text-xs text-[#64748B] font-semibold">
                    Compiled by Research Director (Meta Muse Wonder) • Citations Traceable to 34 URLs
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-[#F4F8FA] border border-[#0D1117] text-xs leading-relaxed space-y-2">
                  <p className="font-medium text-[#0D1117]">
                    &quot;Primary consumer research confirms a 62% preference shift toward verified sizing guarantees. Competitors current average return rates stand at 31%, creating an immediate margin expansion opportunity for first-movers adopting automated returns mitigation.&quot;
                  </p>
                  <p className="text-[11px] text-[#08B0D5] font-bold">
                    [Citation #EV-014: Commerce Ministry Annual Filing 2025]
                  </p>
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <Link
                    href="/app/reports"
                    className="btn-market px-4 py-2 rounded-lg bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#068AA8]"
                  >
                    Open Live Reports →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 10: FINAL CALL TO ACTION
          "YOUR NEXT BUSINESS OPPORTUNITY STARTS WITH A QUESTION."
          CTA: "START INVESTIGATING"
          ========================================================================= */}
      <section className="w-full bg-[#08B0D5] text-[#0D1117] border-b-2 border-[#0D1117] py-20 px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <span className="inline-block px-4 py-1.5 rounded-full bg-[#0D1117] text-[#FFFFFF] font-display font-black text-xs uppercase tracking-wider shadow-market-sm">
            DISCOVER THE UNKNOWN
          </span>

          <h2 className="font-display font-black uppercase text-5xl sm:text-7xl lg:text-8xl tracking-tight leading-[0.92] text-[#0D1117]">
            YOUR NEXT BUSINESS OPPORTUNITY
            <br />
            <span className="text-[#FFFFFF]">STARTS WITH A QUESTION.</span>
          </h2>

          <p className="text-base sm:text-xl text-[#0D1117] font-bold max-w-2xl mx-auto leading-relaxed">
            Stop waiting weeks for consultant decks full of guesses. Deploy 8 autonomous AI minds to scrape evidence, discover white spaces, and simulate outcomes in minutes.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <Link
              href="/app/research/new"
              className="btn-market inline-flex items-center gap-3 px-10 py-5 rounded-xl bg-[#0D1117] text-[#FFFFFF] hover:bg-[#E3447C] font-display font-black text-lg uppercase tracking-wider shadow-market-xl"
            >
              <Zap className="w-6 h-6 text-[#08B0D5] fill-current" />
              <span>START INVESTIGATING</span>
              <ArrowRight className="w-6 h-6 stroke-[3]" />
            </Link>

            <Link
              href="/app"
              className="btn-market inline-flex items-center gap-2 px-8 py-5 rounded-xl bg-[#FFFFFF] text-[#0D1117] hover:bg-[#F4F8FA] font-display font-black text-lg uppercase tracking-wider shadow-market-lg"
            >
              <span>EXPLORE WORKSPACE</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
