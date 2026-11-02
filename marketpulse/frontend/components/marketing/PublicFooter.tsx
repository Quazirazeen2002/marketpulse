"use client";

import React from "react";
import Link from "next/link";
import {
  ShieldCheck,
  Cpu,
  Layers,
  ArrowRight,
  Database,
  Lock,
  ExternalLink,
} from "lucide-react";

export function PublicFooter() {
  return (
    <footer className="w-full bg-[#0D1117] text-[#FFFFFF] border-t-2 border-[#0D1117]">
      {/* Upper Bold Banner */}
      <div className="border-b border-[#1E293B] py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-[#08B0D5] border-2 border-[#FFFFFF] flex items-center justify-center font-display font-black text-xl text-[#0D1117]">
                M
              </div>
              <span className="font-display font-black text-3xl tracking-tight text-[#FFFFFF]">
                MARKET<span className="text-[#08B0D5]">PULSE</span>
              </span>
            </div>
            <p className="mt-3 max-w-md text-sm text-[#E2E8F0] leading-relaxed">
              Autonomous business intelligence, evidence-driven research, and deterministic financial scenario simulation. Powered by Meta Muse Wonder, Meta Spark 1.3, and Tavily.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <Link
              href="/app/research/new"
              className="btn-market inline-flex items-center gap-2 px-6 py-3.5 rounded-lg bg-[#08B0D5] text-[#0D1117] font-display font-black text-sm uppercase shadow-market-sm hover:bg-[#068AA8]"
            >
              <span>Start Investigation</span>
              <ArrowRight className="w-4 h-4 stroke-[3]" />
            </Link>
            <Link
              href="/app"
              className="btn-market inline-flex items-center gap-2 px-6 py-3.5 rounded-lg bg-[#FFFFFF] text-[#0D1117] font-display font-bold text-sm uppercase shadow-market-sm hover:bg-[#E2E8F0]"
            >
              <span>Explore Workspace</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Navigation Links */}
      <div className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 gap-8">
        {/* Col 1: Platform */}
        <div>
          <h4 className="text-xs font-display font-black uppercase tracking-wider text-[#08B0D5] mb-4">
            Platform
          </h4>
          <ul className="space-y-2.5 text-sm font-medium">
            <li>
              <Link href="/product" className="text-[#E9E9E9] hover:text-[#08B0D5] transition-colors">
                Product Architecture
              </Link>
            </li>
            <li>
              <Link href="/how-it-works" className="text-[#E9E9E9] hover:text-[#08B0D5] transition-colors">
                How It Works
              </Link>
            </li>
            <li>
              <Link href="/app/agents" className="text-[#E9E9E9] hover:text-[#08B0D5] transition-colors">
                Agent Observatory
              </Link>
            </li>
            <li>
              <Link href="/app/simulator" className="text-[#E9E9E9] hover:text-[#08B0D5] transition-colors">
                Financial Simulator
              </Link>
            </li>
            <li>
              <Link href="/app/opportunities" className="text-[#E9E9E9] hover:text-[#08B0D5] transition-colors">
                Opportunity Discovery
              </Link>
            </li>
          </ul>
        </div>

        {/* Col 2: Solutions */}
        <div>
          <h4 className="text-xs font-display font-black uppercase tracking-wider text-[#08B0D5] mb-4">
            Solutions & Industries
          </h4>
          <ul className="space-y-2.5 text-sm font-medium">
            <li>
              <Link href="/use-cases" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                E-Commerce Intelligence
              </Link>
            </li>
            <li>
              <Link href="/use-cases" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                Telecommunications
              </Link>
            </li>
            <li>
              <Link href="/use-cases" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                Food Delivery & Logistics
              </Link>
            </li>
            <li>
              <Link href="/use-cases" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                Financial Services
              </Link>
            </li>
            <li>
              <Link href="/use-cases" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                Manufacturing & Supply Chain
              </Link>
            </li>
          </ul>
        </div>

        {/* Col 3: Research Tech */}
        <div>
          <h4 className="text-xs font-display font-black uppercase tracking-wider text-[#08B0D5] mb-4">
            Technology
          </h4>
          <ul className="space-y-2.5 text-sm font-medium">
            <li className="flex items-center gap-2 text-[#E2E8F0]">
              <span className="w-2 h-2 rounded-full bg-[#08B0D5]"></span>
              <span>Meta Muse Wonder (Director)</span>
            </li>
            <li className="flex items-center gap-2 text-[#E2E8F0]">
              <span className="w-2 h-2 rounded-full bg-[#08B0D5]"></span>
              <span>Meta Spark 1.3 (Specialists)</span>
            </li>
            <li className="flex items-center gap-2 text-[#E2E8F0]">
              <span className="w-2 h-2 rounded-full bg-[#E3447C]"></span>
              <span>Tavily Search API</span>
            </li>
            <li className="flex items-center gap-2 text-[#E2E8F0]">
              <span className="w-2 h-2 rounded-full bg-[#08B0D5]"></span>
              <span>LangGraph Multi-Agent</span>
            </li>
            <li className="flex items-center gap-2 text-[#E2E8F0]">
              <span className="w-2 h-2 rounded-full bg-[#E2E8F0]"></span>
              <span>Deterministic Financial Math</span>
            </li>
          </ul>
        </div>

        {/* Col 4: Company & Legal */}
        <div>
          <h4 className="text-xs font-display font-black uppercase tracking-wider text-[#08B0D5] mb-4">
            Company & Contact
          </h4>
          <ul className="space-y-2.5 text-sm font-medium">
            <li>
              <Link href="/about" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                About MARKETPULSE
              </Link>
            </li>
            <li>
              <Link href="/contact" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                Contact & Demo
              </Link>
            </li>
            <li>
              <Link href="/contact" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                Privacy Policy
              </Link>
            </li>
            <li>
              <Link href="/contact" className="text-[#E2E8F0] hover:text-[#08B0D5] transition-colors">
                Terms of Service
              </Link>
            </li>
            <li>
              <span className="inline-block px-2.5 py-1 text-xs rounded border border-[#334155] bg-[#1E293B] text-[#E2E8F0] mt-2">
                FastAPI + Next.js App Router
              </span>
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom Legal / Copyright Bar */}
      <div className="border-t border-[#262626] py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[#777777]">
        <p>© {new Date().getFullYear()} MARKETPULSE Intelligence. All rights reserved.</p>
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5 text-[#E9E9E9]">
            <span className="w-2 h-2 rounded-full bg-[#22c55e]"></span>
            <span>FastAPI Authoritative Backend Online</span>
          </span>
          <span>•</span>
          <Link href="/app/settings" className="hover:text-[#FFFFFF] transition-colors">
            System Telemetry
          </Link>
        </div>
      </div>
    </footer>
  );
}
