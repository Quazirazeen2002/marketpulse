"use client";

import React from "react";
import Link from "next/link";
import {
  Sparkles,
  ShieldCheck,
  Zap,
  CheckCircle2,
  Lock,
  Search,
  Scale,
  Award,
  ArrowRight,
  Database,
  Cpu,
  Target,
  Compass,
} from "lucide-react";

export default function AboutPage() {
  const principles = [
    {
      num: "01",
      title: "Evidence Before Assertion",
      desc: "Ungrounded summaries in executive strategy are dangerous. Every single claim in MARKETPULSE must be explicitly anchored to a retrieved web source, raw text excerpt, and cryptographic content hash.",
    },
    {
      num: "02",
      title: "Inspectable Multi-Agent Routing",
      desc: "Our agents aren't mysterious black boxes. You can inspect every search query, Tavily payload, contradiction arbitration, and LangGraph reasoning node in real time as research executes.",
    },
    {
      num: "03",
      title: "Deterministic Math Over Hallucinated Arithmetic",
      desc: "LLMs consistently produce arithmetic drift on multi-variable financial statements. MARKETPULSE combines Meta AI semantic reasoning with a 100% deterministic Python financial simulation engine.",
    },
    {
      num: "04",
      title: "Empirical Rigor in Minutes",
      desc: "What takes traditional consulting teams 6 weeks and tens of thousands of dollars is delivered in minutes with verifiable provenance, democratizing top-tier business intelligence for modern operators.",
    },
  ];

  return (
    <div className="w-full bg-[#FFFFFF] text-[#0D1117]">
      {/* Hero */}
      <section className="w-full bg-[#08B0D5] text-[#0D1117] py-20 px-4 sm:px-6 lg:px-8 border-b-3 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#0D1117] text-[#FFFFFF] font-display font-extrabold text-xs uppercase tracking-wider shadow-market-sm">
            <Compass className="w-4 h-4 text-[#08B0D5]" />
            <span>OUR MISSION & VALUES</span>
          </div>

          <h1 className="font-display font-black uppercase text-5xl sm:text-7xl lg:text-8xl tracking-tight leading-[0.92]">
            DEMOCRATIZING
            <br />
            <span className="text-[#0D1117]">STRATEGIC TRUTH.</span>
          </h1>

          <p className="text-lg sm:text-xl text-[#0D1117] max-w-3xl leading-relaxed font-bold">
            We built MARKETPULSE to eliminate guesswork from business decisions. We combine multi-agent cognitive orchestration with empirical evidence and deterministic mathematical modeling.
          </p>
        </div>
      </section>

      {/* Origin Story / Manifesto */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 space-y-6">
            <span className="text-xs font-display font-black text-[#E3447C] uppercase tracking-wider">
              THE PROBLEM WE SET OUT TO SOLVE
            </span>
            <h2 className="font-display font-black text-4xl sm:text-5xl uppercase text-[#0D1117] leading-tight">
              Why Traditional Business Intelligence Is Broken
            </h2>
            <div className="space-y-4 text-base text-[#64748B] font-medium leading-relaxed">
              <p>
                For decades, companies had two flawed choices for strategic market research: pay traditional strategy consultancies tens of thousands of dollars for generic slide decks based on junior analyst web browsing, or rely on consumer LLM chatbots that fabricate citations and hallucinate financial numbers.
              </p>
              <p>
                Neither approach offers verifiable truth. When capital allocation, product launches, or market entries are at stake, you cannot afford guesswork.
              </p>
              <p>
                MARKETPULSE bridges this gap. By deploying eight coordinated AI agents governed by strict model allocations (Chief Research Director powered by Meta Muse Wonder, and seven Specialist Analysts powered by Meta Spark 1.3), we scrape the live web via Tavily, extract atomic evidence, detect contradictions, discover white-space opportunities, and model deterministic unit economics without arithmetic drift.
              </p>
            </div>
          </div>

          <div className="lg:col-span-5">
            <div className="p-8 rounded-2xl border-3 border-[#0D1117] bg-[#F4F8FA] shadow-market-xl space-y-6">
              <div className="flex items-center gap-3 border-b-2 border-[#0D1117] pb-4">
                <div className="w-10 h-10 rounded-lg bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] flex items-center justify-center font-display font-black text-lg">
                  MP
                </div>
                <div>
                  <h3 className="font-display font-black text-lg uppercase text-[#0D1117]">
                    The MarketPulse Standard
                  </h3>
                  <p className="text-xs text-[#E3447C] font-bold">
                    Evidence-Grounded Factual Audit Standard
                  </p>
                </div>
              </div>

              <div className="space-y-4 text-xs font-medium text-[#0D1117]">
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[#08B0D5] shrink-0 mt-0.5" />
                  <p>Every claim backed by an exact live URL, extracted excerpt, and content hash.</p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[#08B0D5] shrink-0 mt-0.5" />
                  <p>Conflicting metrics flagged with explicit contradiction arbitration.</p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[#08B0D5] shrink-0 mt-0.5" />
                  <p>Financial margins computed in Python with zero arithmetic drift.</p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[#08B0D5] shrink-0 mt-0.5" />
                  <p>Autonomous opportunity hypotheses tested in iterative search loops.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Four Guiding Principles */}
      <section className="w-full bg-[#0D1117] text-[#FFFFFF] py-20 px-4 sm:px-6 lg:px-8 border-y-3 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-12">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
              OUR CORE PHILOSOPHY
            </span>
            <h2 className="font-display font-black text-4xl sm:text-5xl uppercase tracking-tight text-[#FFFFFF]">
              Four Guiding Principles
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {principles.map((p) => (
              <div
                key={p.num}
                className="p-8 rounded-2xl border-2 border-[#1E293B] bg-[#161B22] space-y-4 hover:border-[#08B0D5] transition-all"
              >
                <div className="flex items-center justify-between">
                  <span className="font-display font-black text-3xl text-[#08B0D5]">
                    {p.num}
                  </span>
                  <span className="w-3 h-3 rounded-full bg-[#E3447C]"></span>
                </div>
                <h3 className="font-display font-black text-2xl uppercase text-[#FFFFFF]">
                  {p.title}
                </h3>
                <p className="text-sm text-[#94A3B8] leading-relaxed font-medium">
                  {p.desc}
                </p>
              </div>
            ))}
          </div>

          <div className="pt-4 flex items-center justify-center">
            <Link
              href="/app/research/new"
              className="btn-market inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-base uppercase shadow-market hover:bg-[#E3447C] hover:text-[#FFFFFF]"
            >
              <span>Start Your First Investigation</span>
              <ArrowRight className="w-5 h-5 stroke-[3]" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
