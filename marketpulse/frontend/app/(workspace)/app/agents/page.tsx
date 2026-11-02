"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Cpu,
  CheckCircle2,
  Zap,
  ChevronRight,
  X,
} from "lucide-react";
import { AGENTS } from "@/lib/constants/agents";

export default function AgentObservatoryPage() {
  const [agents] = useState(AGENTS);
  const [selectedAgent, setSelectedAgent] = useState<any | null>(null);
  const [loading] = useState(false);
  const [error] = useState<string | null>(null);

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
            <Cpu className="w-3.5 h-3.5" />
            <span>AI AGENT OBSERVATORY</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Autonomous Multi-Agent Fleet
          </h1>
          <p className="text-sm text-[#64748B] font-medium max-w-2xl">
            Live telemetry and execution boundaries for the Chief Research Director (Meta Muse Wonder) and seven specialist agents (Meta Spark 1.3).
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <span className="px-3.5 py-2 rounded-xl border-2 border-[#0D1117] bg-[#08B0D5] text-xs font-display font-black text-[#0D1117] shadow-market-sm">
            8 AGENTS ACTIVE
          </span>
          <Link
            href="/app/research/new"
            className="btn-market inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#0D1117] text-[#FFFFFF] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C]"
          >
            <span>Deploy Fleet</span>
            <Zap className="w-3.5 h-3.5 fill-current" />
          </Link>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase">
          {error}
        </div>
      )}

      {/* Agents Grid (8 Agent Cards) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {loading ? (
          Array.from({ length: 8 }).map((_, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl border-2 border-[#0D1117] bg-[#FFFFFF] animate-pulse h-64"
            />
          ))
        ) : (
          agents.map((agent) => {
            const isDirector = agent.id === "director";
            return (
              <div
                key={agent.id}
                className={`card-market p-6 rounded-2xl flex flex-col justify-between space-y-4 border-3 border-[#0D1117] ${
                  isDirector
                    ? "bg-[#0D1117] text-[#FFFFFF]"
                    : "bg-[#FFFFFF] text-[#0D1117]"
                }`}
              >
                <div className="space-y-3">
                  {/* Top Bar: Model pill & Status */}
                  <div className="flex items-center justify-between">
                    <span
                      className={`px-2.5 py-0.5 rounded text-[10px] font-display font-black uppercase ${
                        isDirector
                          ? "bg-[#08B0D5] text-[#0D1117]"
                          : "bg-[#0D1117] text-[#FFFFFF]"
                      }`}
                    >
                      {agent.model}
                    </span>
                    <span className="flex items-center gap-1 text-[11px] font-bold">
                      <span className="w-2 h-2 rounded-full bg-[#08B0D5] animate-pulse"></span>
                      <span className={isDirector ? "text-[#08B0D5]" : "text-[#08B0D5]"}>
                        READY
                      </span>
                    </span>
                  </div>

                  {/* Title & Role */}
                  <div>
                    <h3 className="font-display font-black text-xl uppercase leading-tight">
                      {agent.name}
                    </h3>
                    <p
                      className={`text-xs font-bold uppercase mt-0.5 ${
                        isDirector ? "text-[#E3447C]" : "text-[#08B0D5]"
                      }`}
                    >
                      {agent.role}
                    </p>
                  </div>

                  {/* Responsibilities list preview */}
                  <ul className="space-y-1 text-xs opacity-90 line-clamp-3">
                    {agent.responsibilities.slice(0, 2).map((r, idx) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="font-bold">•</span>
                        <span>{r}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Bottom Inspection Action */}
                <div
                  className={`pt-3 border-t flex items-center justify-between ${
                    isDirector ? "border-[#FFFFFF]/20" : "border-[#E2E8F0]"
                  }`}
                >
                  <span className="text-[11px] font-mono opacity-70">
                    ID: {agent.id}
                  </span>
                  <button
                    onClick={() => setSelectedAgent(agent)}
                    className={`text-xs font-display font-black uppercase flex items-center gap-1 hover:underline ${
                      isDirector ? "text-[#08B0D5]" : "text-[#08B0D5]"
                    }`}
                  >
                    <span>Inspect Details</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Agent Detail Inspection Drawer / Modal */}
      {selectedAgent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="card-market w-full max-w-2xl rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl p-6 sm:p-8 space-y-6">
            <div className="flex items-start justify-between border-b-2 border-[#0D1117] pb-4">
              <div>
                <span className="px-2.5 py-0.5 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
                  {selectedAgent.model}
                </span>
                <h2 className="font-display font-black text-2xl uppercase text-[#0D1117] mt-2">
                  {selectedAgent.name}
                </h2>
                <p className="text-xs font-display font-bold text-[#E3447C] uppercase">
                  {selectedAgent.role}
                </p>
              </div>
              <button
                onClick={() => setSelectedAgent(null)}
                className="p-2 rounded-lg border-2 border-[#0D1117] hover:bg-[#F4F8FA] text-[#0D1117]"
              >
                <X className="w-5 h-5 stroke-[2.5]" />
              </button>
            </div>

            {/* Responsibilities */}
            <div className="space-y-3">
              <h4 className="font-display font-black text-xs uppercase text-[#0D1117] tracking-wider">
                Full Agent Responsibilities
              </h4>
              <div className="p-4 rounded-xl bg-[#F4F8FA] border-2 border-[#0D1117] space-y-2 text-xs">
                {selectedAgent.responsibilities.map((r: string, i: number) => (
                  <div key={i} className="flex items-start gap-2 text-[#0D1117]">
                    <CheckCircle2 className="w-4 h-4 text-[#08B0D5] shrink-0 mt-0.5" />
                    <span>{r}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Tool Activity & Structured Output Protocol */}
            <div className="space-y-2">
              <h4 className="font-display font-black text-xs uppercase text-[#0D1117] tracking-wider">
                Tool Integrations & Structured Schema
              </h4>
              <div className="p-4 rounded-xl bg-[#0D1117] text-[#FFFFFF] text-xs space-y-2 font-mono">
                <p className="text-[#08B0D5] font-bold">
                  // Pydantic Schema: {selectedAgent.id}_output_v1
                </p>
                <p className="text-[#F4F8FA]">
                  Tools: TavilySearchEngine, HTMLToEvidenceConverter, ClaimDeduplicator, CitationVerifier
                </p>
                <p className="text-[#94A3B8]">
                  Privacy Guard: Raw chain-of-thought strictly sequestered; only verified atomic claims published to SQLite.
                </p>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedAgent(null)}
                className="btn-market px-6 py-2.5 rounded-lg bg-[#08B0D5] text-xs font-display font-black uppercase text-[#0D1117] shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
              >
                Close Dossier
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
