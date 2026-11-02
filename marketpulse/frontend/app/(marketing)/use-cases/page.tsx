"use client";

import React from "react";
import Link from "next/link";
import {
  Sparkles,
  ArrowRight,
  ShoppingBag,
  Smartphone,
  Truck,
  Building2,
  Factory,
  CreditCard,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
} from "lucide-react";

export default function UseCasesPage() {
  const industries = [
    {
      id: "ecommerce",
      title: "Fashion E-Commerce in Emerging Markets",
      subtitle: "Return Rate Reduction & Sizing Assurance",
      icon: ShoppingBag,
      tag: "RETAIL & E-COMMERCE",
      problem:
        "High 32% return rates on cash-on-delivery orders degrade unit economics and tie up warehouse working capital.",
      findings: [
        "42% of customer returns are driven by sizing ambiguity across varying local sizing standards.",
        "Competitor apparel brands offer generous return windows without verifying genuine sizing mismatch.",
        "Consumers express 68% willingness to prepay via digital wallet if given an instant fit guarantee.",
      ],
      opportunity:
        "Prepaid Modest-Fashion Sizing Bundle with Automated Digital Measurement",
      score: 87,
      financialImpact: "+$14,200 monthly operating profit from reduced reverse-logistics friction.",
    },
    {
      id: "telecom",
      title: "Telecommunications & Broadband Monetization",
      subtitle: "Customer Experience & Gaming SLAs",
      icon: Smartphone,
      tag: "TELECOMMUNICATIONS",
      problem:
        "Severe subscriber churn driven by hidden throttling, opaque bill shock, and peak-hour latency spikes.",
      findings: [
        "Over 55% of negative customer reviews cite gaming and video call degradation during 8-11 PM.",
        "Incumbent operators only offer generic speed upgrades without latency guarantees.",
        "A 14% power-user segment is willing to pay a 30% premium for guaranteed sub-20ms ping.",
      ],
      opportunity:
        "Dedicated Gamer Fiber Add-On with Guaranteed Peak-Hour Latency SLA",
      score: 84,
      financialImpact: "Reduces annual subscriber churn by 3.8%, protecting $1.2M in annual recurring revenue.",
    },
    {
      id: "food-delivery",
      title: "Food Delivery & Merchant Logistics",
      subtitle: "Dark Kitchen Economics & Delivery Batching",
      icon: Truck,
      tag: "FOOD & LOGISTICS",
      problem:
        "Merchant commission fatigue (30-35%) leading top restaurants to exit aggregate delivery platforms.",
      findings: [
        "Average basket sizes under $15 result in negative contribution margins per order after driver payout.",
        "Customer willingness to wait an extra 15 minutes for pooled delivery reaches 71% when delivery fee is waived.",
        "Merchants prioritize predictable kitchen prep pacing over hyper-fast 15-minute dispatch.",
      ],
      opportunity:
        "Hybrid Subscription Batch Delivery Model with Low Merchant Take-Rates",
      score: 91,
      financialImpact: "+18% contribution margin improvement per routed batch cluster.",
    },
    {
      id: "retail",
      title: "Omnichannel Consumer Retail",
      subtitle: "Private Label Positioning & Shelf Optimization",
      icon: Building2,
      tag: "RETAIL",
      problem:
        "Erosion of branded FMCG margins against aggressive retailer private-label discounting.",
      findings: [
        "Consumers actively trade down on staple pantry goods but trade up on premium organic condiments.",
        "Competitors are slow to reformulate clean-label alternatives with transparent ingredient origins.",
        "Store-level scanner data shows 2.4x higher velocity on sustainably packaged SKUs.",
      ],
      opportunity:
        "Clean-Label Regional Functional Food Line with Direct-to-Consumer Subscription",
      score: 85,
      financialImpact: "Captures 7.2% niche market share within 9 months of launch.",
    },
    {
      id: "manufacturing",
      title: "Industrial Manufacturing & Sourcing",
      subtitle: "Supply Chain Decoupling & Component Resilience",
      icon: Factory,
      tag: "MANUFACTURING",
      problem:
        "Critical supply-chain disruptions caused by single-source overseas micro-component reliance.",
      findings: [
        "Port congestion and tariffs added 41 days of average lead time over the prior two quarters.",
        "Regional nearshoring alternatives exist with 12% higher unit cost but 70% shorter transit cycles.",
        "Tier-1 competitors experienced 3 assembly line shutdowns due to inventory stockouts.",
      ],
      opportunity:
        "Dual-Sourced Regional Buffer Supply Network with Dynamic Inventory Triggering",
      score: 89,
      financialImpact: "Averts estimated $850K in downtime penalties per quarter.",
    },
    {
      id: "fintech",
      title: "Fintech & SME Cash-Flow Financing",
      subtitle: "POS Micro-Lending with Real-Time Underwriting",
      icon: CreditCard,
      tag: "FINANCIAL SERVICES",
      problem:
        "Small retailers unable to secure working capital credit due to lack of audited financial statements.",
      findings: [
        "Small merchants generate consistent daily POS terminal volume with predictable seasonal peaks.",
        "Traditional banks take 21 days for loan approval with a 65% rejection rate.",
        "Merchants eagerly adopt automatic daily micro-deductions tied directly to card processing receipts.",
      ],
      opportunity:
        "Automated POS-Linked Merchant Revenue-Based Financing with Daily Sweep Repayment",
      score: 92,
      financialImpact: "Achieves 98.4% repayment compliance rate with 4.2% net interest margin.",
    },
  ];

  return (
    <div className="w-full bg-[#FFFFFF] text-[#0D1117]">
      {/* Header */}
      <section className="w-full bg-[#0D1117] text-[#FFFFFF] py-20 px-4 sm:px-6 lg:px-8 border-b-3 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] font-display font-extrabold text-xs uppercase tracking-wider">
            <Sparkles className="w-4 h-4 fill-current" />
            <span>ILLUSTRATIVE DEMONSTRATION SCENARIOS</span>
          </div>

          <h1 className="font-display font-black uppercase text-5xl sm:text-7xl lg:text-8xl tracking-tight leading-[0.92]">
            INTELLIGENCE FOR
            <br />
            <span className="text-[#08B0D5]">EVERY INDUSTRY.</span>
          </h1>

          <p className="text-lg sm:text-xl text-[#F4F8FA] max-w-3xl leading-relaxed font-medium">
            Explore how MARKETPULSE investigates competitive positioning, customer complaints, and commercial viability across distinct market sectors using multi-agent web verification.
          </p>

          <p className="text-xs text-[#94A3B8] font-semibold italic">
            * Note: The scenarios below are empirical demonstration workflows generated by MARKETPULSE to illustrate multi-agent reasoning capabilities, Tavily web-query synthesis, and deterministic financial calculations—not confidential client data.
          </p>
        </div>
      </section>

      {/* Use Cases Cards Grid */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
        {industries.map((industry) => {
          const Icon = industry.icon;
          return (
            <div
              key={industry.id}
              className="card-market p-8 sm:p-10 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-lg space-y-8"
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b-2 border-[#0D1117] pb-6">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-xl bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] flex items-center justify-center font-display font-black text-xl shadow-market-sm shrink-0">
                    <Icon className="w-7 h-7" />
                  </div>
                  <div>
                    <span className="text-xs font-display font-black text-[#E3447C] uppercase tracking-wider">
                      {industry.tag}
                    </span>
                    <h2 className="font-display font-black text-2xl sm:text-3xl uppercase text-[#0D1117] tracking-tight">
                      {industry.title}
                    </h2>
                    <p className="text-sm text-[#64748B] font-medium">
                      {industry.subtitle}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="px-3.5 py-1.5 rounded-lg bg-[#E3447C] text-[#FFFFFF] font-display font-black text-sm uppercase shadow-market-sm">
                    {industry.score}/100 OPPORTUNITY SCORE
                  </span>
                </div>
              </div>

              {/* 3 Columns: Problem, Evidence Findings, Discovered Opportunity */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Col 1: Problem */}
                <div className="p-6 rounded-xl bg-[#F4F8FA] border-2 border-[#0D1117] space-y-3">
                  <span className="text-xs font-display font-black text-[#E3447C] uppercase flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4" />
                    Market Friction & Pain Point
                  </span>
                  <p className="text-sm text-[#0D1117] leading-relaxed font-medium">
                    {industry.problem}
                  </p>
                </div>

                {/* Col 2: Evidence Findings */}
                <div className="p-6 rounded-xl bg-[#FFFFFF] border-2 border-[#0D1117] space-y-3">
                  <span className="text-xs font-display font-black text-[#08B0D5] uppercase flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" />
                    Key Web Findings (Tavily)
                  </span>
                  <ul className="space-y-2 text-xs text-[#64748B] font-medium">
                    {industry.findings.map((finding, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-[#08B0D5] font-black">•</span>
                        <span>{finding}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Col 3: Discovered Opportunity & Financials */}
                <div className="p-6 rounded-xl bg-[#08B0D5]/15 border-2 border-[#0D1117] space-y-3 text-[#0D1117]">
                  <span className="text-xs font-display font-black uppercase flex items-center gap-1.5 text-[#0D1117]">
                    <Lightbulb className="w-4 h-4 fill-current text-[#E3447C]" />
                    Autonomous Opportunity
                  </span>
                  <p className="font-display font-extrabold text-base leading-snug">
                    {industry.opportunity}
                  </p>
                  <p className="text-xs font-bold text-[#0D1117]/90 pt-2 border-t border-[#0D1117]/30">
                    Financial Projection: {industry.financialImpact}
                  </p>
                </div>
              </div>

              {/* Action */}
              <div className="flex items-center justify-end pt-2">
                <Link
                  href="/app/research/new"
                  className="btn-market inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-[#0D1117] text-[#FFFFFF] font-display font-extrabold text-xs uppercase shadow-market-sm hover:bg-[#08B0D5] hover:text-[#0D1117]"
                >
                  <span>Investigate This Sector</span>
                  <ArrowRight className="w-4 h-4 stroke-[3]" />
                </Link>
              </div>
            </div>
          );
        })}
      </section>
    </div>
  );
}
