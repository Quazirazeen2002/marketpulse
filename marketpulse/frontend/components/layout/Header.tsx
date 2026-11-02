"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Search,
  Plus,
  MessageSquare,
  Sparkles,
  Zap,
  Info,
  Home,
  CheckCircle2,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { ServiceHealth } from "@/lib/types";

export function Header() {
  const pathname = usePathname();
  const [health, setHealth] = useState<ServiceHealth | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function checkHealth() {
      try {
        const res = await api.getServiceHealth();
        if (isMounted) setHealth(res);
      } catch (err) {
        if (isMounted) setHealth(null);
      }
    }
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  // Format breadcrumb segments
  const segments = pathname.split("/").filter(Boolean);
  const breadcrumbs = segments.map((seg, idx) => {
    const href = "/" + segments.slice(0, idx + 1).join("/");
    const formatted = seg.charAt(0).toUpperCase() + seg.slice(1).replace(/-/g, " ");
    return { name: formatted, href };
  });

  return (
    <div className="sticky top-0 z-40 flex flex-col w-full">
      {/* Feastables MrBeast Top Running Marquee Announcement Bar */}
      <div className="w-full bg-[#67318F] text-[#FFEA00] border-b-2 border-black overflow-hidden py-1.5 select-none text-xs font-display font-black italic tracking-wider">
        <div className="animate-marquee whitespace-nowrap flex items-center gap-8">
          <span className="flex items-center gap-2">
            🚨 <span>100% EVIDENCE-PROVEN DEEP RESEARCH</span> ⚡
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2 text-white">
            <span>8 MULTI-AGENT SPECIALISTS</span> 🤖
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2 text-[#15CCFF]">
            <span>DETERMINISTIC FINANCIAL SIMULATION</span> 📊
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2 text-[#FF5DB5]">
            <span>0% LLM HALLUCINATION RISK</span> 🎯
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2">
            <span>META MUSE WONDER + SPARK 1.3 ORCHESTRATION</span> 💡
          </span>
          <span className="text-white">•</span>
          {/* Duplicate for infinite loop */}
          <span className="flex items-center gap-2">
            🚨 <span>100% EVIDENCE-PROVEN DEEP RESEARCH</span> ⚡
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2 text-white">
            <span>8 MULTI-AGENT SPECIALISTS</span> 🤖
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2 text-[#15CCFF]">
            <span>DETERMINISTIC FINANCIAL SIMULATION</span> 📊
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2 text-[#FF5DB5]">
            <span>0% LLM HALLUCINATION RISK</span> 🎯
          </span>
          <span className="text-white">•</span>
          <span className="flex items-center gap-2">
            <span>META MUSE WONDER + SPARK 1.3 ORCHESTRATION</span> 💡
          </span>
          <span className="text-white">•</span>
        </div>
      </div>

      {/* Main Header Bar */}
      <header className="flex h-16 w-full items-center justify-between border-b-2 border-black bg-white px-4 md:px-6 shadow-feast-sm">
        {/* Left: Breadcrumbs & Quick Navigation Links */}
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="flex items-center gap-1.5 font-display font-black italic text-lg tracking-tight text-black hover:text-[#15CCFF] transition-colors"
          >
            <span>MARKETPULSE</span>
            <span className="inline-block -rotate-6 rounded bg-[#FF3BB1] px-1.5 py-0.2 text-[10px] font-black uppercase text-white shadow-[1px_1px_0px_#000]">
              PRO
            </span>
          </Link>

          <span className="text-slate-300 font-bold hidden sm:inline">|</span>

          {/* Quick Page Links */}
          <div className="hidden lg:flex items-center gap-2 text-xs font-display font-bold italic uppercase">
            <Link
              href="/landing"
              className={`px-2.5 py-1 rounded-md border border-black transition-all ${
                pathname === "/landing"
                  ? "bg-[#15CCFF] text-black shadow-[2px_2px_0px_#000]"
                  : "bg-slate-100 text-slate-700 hover:bg-[#15CCFF] hover:text-black"
              }`}
            >
              🚀 Landing Page
            </Link>
            <Link
              href="/about"
              className={`px-2.5 py-1 rounded-md border border-black transition-all ${
                pathname === "/about"
                  ? "bg-[#FFEA00] text-black shadow-[2px_2px_0px_#000]"
                  : "bg-slate-100 text-slate-700 hover:bg-[#FFEA00] hover:text-black"
              }`}
            >
              ⚡ About Us
            </Link>
            <Link
              href="/research/chat"
              className={`px-2.5 py-1 rounded-md border border-black transition-all ${
                pathname === "/research/chat"
                  ? "bg-[#FF3BB1] text-white shadow-[2px_2px_0px_#000]"
                  : "bg-slate-100 text-slate-700 hover:bg-[#FF3BB1] hover:text-white"
              }`}
            >
              💬 AI Research Chat
            </Link>
          </div>

          {/* Standard Breadcrumb Trail */}
          <div className="hidden xl:flex items-center gap-1.5 text-xs text-slate-500 font-medium">
            {breadcrumbs.map((crumb, idx) => (
              <React.Fragment key={crumb.href}>
                <span className="text-slate-300">/</span>
                {idx === breadcrumbs.length - 1 ? (
                  <span className="font-bold text-black">{crumb.name}</span>
                ) : (
                  <Link href={crumb.href} className="hover:text-black transition-colors">
                    {crumb.name}
                  </Link>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Right Controls */}
        <div className="flex items-center gap-3">
          {/* Backend Health Badge with Feastables Border */}
          <div className="hidden sm:flex items-center gap-2 rounded-full border-2 border-black bg-[#F8F6F0] px-3 py-1 text-xs shadow-[2px_2px_0px_#000]">
            {health ? (
              <>
                <span className="relative flex h-2.5 w-2.5">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#15CCFF] opacity-75"></span>
                  <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-[#15CCFF]"></span>
                </span>
                <span className="font-display font-bold italic uppercase tracking-wider text-black text-[11px]">
                  FastAPI Online
                </span>
                {health.active_background_tasks > 0 && (
                  <span className="rounded bg-[#FF3BB1] px-1.5 py-0.2 text-[10px] font-black uppercase text-white">
                    {health.active_background_tasks} Active
                  </span>
                )}
              </>
            ) : (
              <>
                <span className="h-2.5 w-2.5 rounded-full bg-[#FF9125]"></span>
                <span className="font-display font-bold italic uppercase text-slate-600 text-[11px]">
                  Connecting...
                </span>
              </>
            )}
          </div>

          {/* Chatbot CTA Shortcut */}
          <Link
            href="/research/chat"
            className="flex h-9 items-center gap-1.5 rounded-lg border-2 border-black bg-[#15CCFF] px-3 text-xs font-display font-black italic uppercase text-black shadow-feast-sm hover:shadow-feast hover:-translate-y-0.5 transition-all"
            title="Chatbot style research interface"
          >
            <MessageSquare className="h-4 w-4" />
            <span className="hidden md:inline">Research Chat</span>
          </Link>

          {/* New Research Primary CTA */}
          <Link
            href="/research/new"
            className="flex h-9 items-center gap-1.5 rounded-lg border-2 border-black bg-[#FFEA00] px-3.5 text-xs font-display font-black italic uppercase text-black shadow-feast-sm hover:shadow-feast hover:-translate-y-0.5 transition-all"
          >
            <Plus className="h-4 w-4 stroke-[3]" />
            <span>New Research</span>
          </Link>
        </div>
      </header>
    </div>
  );
}
