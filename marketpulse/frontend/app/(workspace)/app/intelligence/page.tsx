"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Compass,
  TrendingUp,
  Users,
  Target,
  Megaphone,
  DollarSign,
  ArrowRight,
  Zap,
} from "lucide-react";
import { api } from "@/lib/api/client";

export default function IntelligenceHubPage() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    api.getOverviewStats().then(setStats).catch(() => null);
  }, []);

  const domains = [
    {
      title: "Market Intelligence",
      slug: "market",
      icon: TrendingUp,
      agent: "Market Intelligence Analyst",
      model: "Meta Spark 1.3",
      tag: "MACRO & INDUSTRY",
      desc: "Investigate market structure, segmentation, growth indicators, regulatory shifts, and emerging business dynamics.",
      color: "bg-[#08B0D5] text-[#0D1117]",
    },
    {
      title: "Competitor Intelligence",
      slug: "competitors",
      icon: Target,
      agent: "Competitor Intelligence Analyst",
      model: "Meta Spark 1.3",
      tag: "STRATEGY & POSITIONING",
      desc: "Benchmark competitor profiles, pricing tiers, product feature matrices, distribution models, strengths, and blind spots.",
      color: "bg-[#0D1117] text-[#FFFFFF]",
    },
    {
      title: "Customer Intelligence",
      slug: "customers",
      icon: Users,
      agent: "Customer Intelligence Analyst",
      model: "Meta Spark 1.3",
      tag: "DEMAND & FRICTION",
      desc: "Extract customer personas, purchase drivers, unaddressed complaints, friction points, and unmet consumer needs.",
      color: "bg-[#E3447C] text-[#FFFFFF]",
    },
    {
      title: "Marketing Intelligence",
      slug: "marketing",
      icon: Megaphone,
      agent: "Marketing Intelligence Analyst",
      model: "Meta Spark 1.3",
      tag: "CAMPAIGNS & CHANNELS",
      desc: "Analyze brand messaging, campaign rhythms, high-ROI acquisition channels, and messaging differentiation white spaces.",
      color: "bg-[#FFFFFF] text-[#0D1117]",
    },
    {
      title: "Commercial Intelligence",
      slug: "commercial",
      icon: DollarSign,
      agent: "Commercial Intelligence Analyst",
      model: "Meta Spark 1.3",
      tag: "PRICING & UNIT ECONOMICS",
      desc: "Benchmark fee structures, delivery costs, revenue streams, monetization options, and commercial margin risks.",
      color: "bg-[#08B0D5] text-[#0D1117]",
    },
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
            <Compass className="w-3.5 h-3.5" />
            <span>SPECIALIST DOMAIN INTELLIGENCE</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Intelligence Domain Hub
          </h1>
          <p className="text-sm text-[#64748B] font-medium max-w-2xl">
            Deep-dive into specialized vertical research streams authored by Meta Spark 1.3 specialists and arbitrated by Meta Muse Wonder.
          </p>
        </div>

        <Link
          href="/app/research/new"
          className="btn-market inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF] shrink-0"
        >
          <Zap className="w-4 h-4 fill-current" />
          <span>Launch Investigation</span>
        </Link>
      </div>

      {/* 5 Domain Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {domains.map((dom) => {
          const Icon = dom.icon;
          return (
            <div
              key={dom.slug}
              className="card-market p-6 sm:p-8 rounded-2xl flex flex-col justify-between space-y-6 bg-[#FFFFFF] border-3 border-[#0D1117]"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded bg-[#F4F8FA] border border-[#0D1117] text-[10px] font-display font-black uppercase text-[#0D1117]">
                    {dom.tag}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] text-[10px] font-bold uppercase">
                    {dom.model}
                  </span>
                </div>

                <div className="w-12 h-12 rounded-xl bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] flex items-center justify-center font-display font-black text-xl shadow-market-sm">
                  <Icon className="w-6 h-6" />
                </div>

                <div className="space-y-1">
                  <h3 className="font-display font-black text-2xl uppercase text-[#0D1117]">
                    {dom.title}
                  </h3>
                  <p className="text-xs font-bold text-[#E3447C] uppercase">
                    {dom.agent}
                  </p>
                </div>

                <p className="text-xs text-[#64748B] font-medium leading-relaxed">
                  {dom.desc}
                </p>
              </div>

              <div className="pt-4 border-t border-[#E2E8F0]">
                <Link
                  href={`/app/intelligence/${dom.slug}`}
                  className="btn-market w-full py-2.5 rounded-lg bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase shadow-market-sm flex items-center justify-center gap-1.5 hover:bg-[#E3447C] hover:text-[#FFFFFF]"
                >
                  <span>Open {dom.title}</span>
                  <ArrowRight className="w-3.5 h-3.5 stroke-[3]" />
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
