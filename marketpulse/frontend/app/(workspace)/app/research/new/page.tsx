"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Sparkles,
  Search,
  ArrowRight,
  Zap,
  CheckCircle2,
  AlertCircle,
  Clock,
  Layers,
  Sliders,
  Globe,
} from "lucide-react";
import { api } from "@/lib/api/client";

export default function NewResearchPage() {
  const router = useRouter();

  const [objective, setObjective] = useState("");
  const [industry, setIndustry] = useState("Fashion E-Commerce");
  const [geography, setGeography] = useState("Bangladesh");
  const [timeHorizon, setTimeHorizon] = useState("Current (Real-time)");
  const [researchDepth, setResearchDepth] = useState("standard");
  const [additionalInstructions, setAdditionalInstructions] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const promptTemplates = [
    {
      title: "Fashion E-Commerce in Emerging Markets",
      objective:
        "Investigate consumer return rates, sizing ambiguity, and COD payment bottlenecks in Bangladesh modest fashion e-commerce.",
      industry: "Fashion E-Commerce",
      geography: "Bangladesh",
    },
    {
      title: "Telecommunications & Gaming SLAs",
      objective:
        "Examine peak-hour broadband latency complaints and willingness to pay for dedicated gamer fiber plans in South Asia.",
      industry: "Telecommunications",
      geography: "South Asia",
    },
    {
      title: "Food Delivery Dark Kitchen Economics",
      objective:
        "Analyze restaurant commission dissatisfaction and consumer demand for pooled batch delivery subscription models.",
      industry: "Food & Logistics",
      geography: "Emerging Markets",
    },
    {
      title: "SME POS-Linked Revenue Financing",
      objective:
        "Assess unbanked small merchant cash-flow friction and adoption potential of automated daily micro-sweep credit.",
      industry: "Financial Services",
      geography: "Southeast Asia",
    },
  ];

  const applyTemplate = (t: typeof promptTemplates[0]) => {
    setObjective(t.objective);
    setIndustry(t.industry);
    setGeography(t.geography);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!objective.trim()) {
      setError("Please provide a research objective.");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const res = await api.createResearchRun({
        objective: objective.trim(),
        industry: industry.trim(),
        geography: geography.trim(),
        time_horizon: timeHorizon,
        research_depth: researchDepth,
        additional_instructions: additionalInstructions.trim(),
      });

      if (res && res.research_id) {
        router.push(`/app/research/${res.research_id}`);
      } else {
        throw new Error("Did not receive a valid research ID from backend.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to dispatch research task.");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] border border-[#0D1117] text-xs font-display font-black uppercase text-[#0D1117]">
          <Zap className="w-3.5 h-3.5 fill-current" />
          <span>RESEARCH DISPATCH</span>
        </div>
        <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
          New Research Investigation
        </h1>
        <p className="text-sm text-[#64748B] font-medium leading-relaxed">
          Formulate your market inquiry. The Research Director (Meta Muse Wonder) will break down the objective and deploy seven specialists (Meta Spark 1.3) with Tavily web spidering.
        </p>
      </div>

      {/* Quick Template Chips */}
      <div className="space-y-3">
        <span className="text-xs font-display font-black text-[#0D1117] uppercase tracking-wider">
          Quick Start Templates:
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {promptTemplates.map((t) => (
            <button
              key={t.title}
              type="button"
              onClick={() => applyTemplate(t)}
              className="p-3.5 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] hover:bg-[#08B0D5] transition-all text-left space-y-1 shadow-market-sm group"
            >
              <p className="font-display font-black text-xs uppercase text-[#0D1117] group-hover:text-[#0D1117]">
                {t.title}
              </p>
              <p className="text-[11px] text-[#64748B] group-hover:text-[#0D1117]/80 font-medium line-clamp-1">
                {t.objective}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Main Form Card */}
      <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Objective Textarea */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label
                htmlFor="objective"
                className="text-xs font-display font-black uppercase text-[#0D1117] tracking-wider"
              >
                Primary Research Objective *
              </label>
              <span className="text-[11px] text-[#64748B] font-semibold">
                Required • Minimum 5 characters
              </span>
            </div>
            <textarea
              id="objective"
              rows={4}
              required
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              placeholder="e.g. Investigate customer demand shifts, pricing friction, and unaddressed market niches in Bangladesh fashion e-commerce..."
              className="w-full px-4 py-3.5 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
            />
          </div>

          {/* Grid Parameters: Industry, Geography, Time Horizon, Depth */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {/* Industry */}
            <div className="space-y-2">
              <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                Target Industry
              </label>
              <input
                type="text"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                placeholder="e.g. Fashion E-commerce, FinTech, Logistics"
                className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
              />
            </div>

            {/* Geography */}
            <div className="space-y-2">
              <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                Target Geography
              </label>
              <input
                type="text"
                value={geography}
                onChange={(e) => setGeography(e.target.value)}
                placeholder="e.g. Bangladesh, South Asia, Global"
                className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
              />
            </div>

            {/* Time Horizon */}
            <div className="space-y-2">
              <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                Time Horizon
              </label>
              <select
                value={timeHorizon}
                onChange={(e) => setTimeHorizon(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm font-bold text-[#0D1117] focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
              >
                <option value="Current (Real-time)">Current (Real-time)</option>
                <option value="Near-term (1-2 Years)">Near-term (1-2 Years)</option>
                <option value="Historical & Emerging">Historical & Emerging</option>
              </select>
            </div>

            {/* Research Depth */}
            <div className="space-y-2">
              <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                Investigation Depth
              </label>
              <select
                value={researchDepth}
                onChange={(e) => setResearchDepth(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm font-bold text-[#0D1117] focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
              >
                <option value="standard">Standard (Rapid Scan • 10-15 Sources)</option>
                <option value="deep">Deep (Comprehensive Multi-Agent • 25-40 Sources)</option>
                <option value="comprehensive">Comprehensive (Exhaustive • 50+ Sources)</option>
              </select>
            </div>
          </div>

          {/* Additional Instructions */}
          <div className="space-y-2">
            <label className="text-xs font-display font-black uppercase text-[#0D1117]">
              Custom Constraints or Additional Instructions (Optional)
            </label>
            <input
              type="text"
              value={additionalInstructions}
              onChange={(e) => setAdditionalInstructions(e.target.value)}
              placeholder="e.g. Focus specifically on return rates, COD payment friction, and pricing tiers below $30."
              className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
            />
          </div>

          {/* Submit Action */}
          <div className="pt-4 border-t-2 border-[#0D1117] flex flex-col sm:flex-row items-center justify-between gap-4">
            <span className="text-xs font-display font-bold text-[#64748B] uppercase flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#08B0D5]" />
              Runs in background thread • Reconnectable
            </span>

            <button
              type="submit"
              disabled={loading}
              className="btn-market w-full sm:w-auto inline-flex items-center justify-center gap-3 px-8 py-4 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-sm uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF] disabled:opacity-50"
            >
              <Zap className="w-4 h-4 fill-current" />
              <span>{loading ? "Dispatching Investigation..." : "Generate Research Intelligence"}</span>
              <ArrowRight className="w-4 h-4 stroke-[3]" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
