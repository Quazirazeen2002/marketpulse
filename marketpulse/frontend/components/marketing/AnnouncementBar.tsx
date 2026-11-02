"use client";

import React from "react";
import Link from "next/link";
import { Sparkles, ArrowRight } from "lucide-react";

interface AnnouncementBarProps {
  text?: string;
  badge?: string;
  ctaText?: string;
  ctaHref?: string;
}

export function AnnouncementBar({
  text = "INTRODUCING THE NEXT GENERATION OF BUSINESS INTELLIGENCE",
  badge = "STAGE 3 LIVE",
  ctaText = "START DISCOVERING",
  ctaHref = "/app/research/new",
}: AnnouncementBarProps) {
  return (
    <div className="relative z-50 w-full overflow-hidden border-b-2 border-[#0D1117] bg-[#08B0D5] text-[#0D1117] py-2 px-4 select-none">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4 text-xs sm:text-sm font-display font-bold">
        {/* Ticker / Main text */}
        <div className="flex items-center gap-2 overflow-hidden truncate">
          <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#0D1117] text-[#08B0D5] text-[11px] font-black uppercase tracking-wider shrink-0">
            <Sparkles className="w-3 h-3 fill-current" />
            {badge}
          </span>
          <span className="truncate uppercase tracking-tight">{text}</span>
        </div>

        {/* Action Link */}
        <Link
          href={ctaHref}
          className="inline-flex items-center gap-1.5 px-3 py-1 bg-[#E3447C] text-[#FFFFFF] hover:bg-[#C93268] rounded transition-colors text-xs uppercase font-black shrink-0 border border-[#0D1117] shadow-market-sm"
        >
          <span>{ctaText}</span>
          <ArrowRight className="w-3 h-3 stroke-[3]" />
        </Link>
      </div>
    </div>
  );
}
