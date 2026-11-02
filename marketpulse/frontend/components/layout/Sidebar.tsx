"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Search,
  Activity,
  Bot,
  TrendingUp,
  Users,
  Compass,
  Megaphone,
  Briefcase,
  Lightbulb,
  GitBranch,
  ShieldAlert,
  Calculator,
  FileCheck,
  FileText,
  History,
  Settings,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  MessageSquare,
  Rocket,
  Info,
} from "lucide-react";

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
  badgeColor?: string;
  category?: string;
}

const navItems: NavItem[] = [
  // Showcase Pages
  { name: "Landing Page", href: "/landing", icon: Rocket, category: "Welcome", badge: "EXPLORE", badgeColor: "bg-[#FFEA00] text-black" },
  { name: "About MarketPulse", href: "/about", icon: Info, category: "Welcome" },

  // Core Operations
  { name: "Overview Dashboard", href: "/", icon: LayoutDashboard, category: "Command Center" },
  { name: "AI Research Chat", href: "/research/chat", icon: MessageSquare, category: "Command Center", badge: "CHAT", badgeColor: "bg-[#FF3BB1] text-white" },
  { name: "New Research Form", href: "/research/new", icon: Search, category: "Command Center" },
  { name: "Active Pipeline", href: "/research/active", icon: Activity, category: "Command Center" },
  { name: "Agent Observatory", href: "/agents", icon: Bot, category: "Command Center" },

  // Domain Intelligence
  { name: "Market Intelligence", href: "/intelligence/market", icon: TrendingUp, category: "Specialist Intel" },
  { name: "Competitor Intelligence", href: "/intelligence/competitors", icon: Compass, category: "Specialist Intel" },
  { name: "Customer Intelligence", href: "/intelligence/customers", icon: Users, category: "Specialist Intel" },
  { name: "Marketing Intelligence", href: "/intelligence/marketing", icon: Megaphone, category: "Specialist Intel" },
  { name: "Commercial Intelligence", href: "/intelligence/commercial", icon: Briefcase, category: "Specialist Intel" },

  // Strategy & Execution
  { name: "Opportunity Discovery", href: "/opportunities", icon: Lightbulb, category: "Strategy & Simulation" },
  { name: "Research Hypotheses", href: "/hypotheses", icon: GitBranch, category: "Strategy & Simulation" },
  { name: "Risk Observatory", href: "/risks", icon: ShieldAlert, category: "Strategy & Simulation" },
  { name: "Scenario Simulator", href: "/simulator", icon: Calculator, category: "Strategy & Simulation" },

  // Evidence & Historical
  { name: "Evidence Explorer", href: "/evidence", icon: FileCheck, category: "Output & Governance" },
  { name: "Executive Reports", href: "/reports", icon: FileText, category: "Output & Governance" },
  { name: "Research History", href: "/research/history", icon: History, category: "Output & Governance" },
  { name: "Settings & System", href: "/settings", icon: Settings, category: "Output & Governance" },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  // Group items by category
  const categories = Array.from(new Set(navItems.map((item) => item.category || "General")));

  return (
    <aside
      className={`relative flex flex-col border-r-2 border-black bg-[#0B0E14] text-slate-100 transition-all duration-300 select-none z-30 ${
        collapsed ? "w-20" : "w-72"
      } min-h-screen`}
    >
      {/* Brand Header */}
      <div className="flex h-16 items-center justify-between border-b-2 border-black bg-[#0B0E14] px-4">
        {!collapsed ? (
          <Link href="/" className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg border-2 border-black bg-[#15CCFF] text-black shadow-[2px_2px_0px_#FFEA00]">
              <Sparkles className="h-5 w-5 fill-current" />
            </div>
            <div className="flex flex-col">
              <div className="flex items-center gap-1.5">
                <span className="font-display font-black italic tracking-tight text-white text-lg leading-none">
                  MARKETPULSE
                </span>
                <span className="rounded bg-[#FF3BB1] px-1 py-0.2 text-[9px] font-black italic uppercase text-white shadow-[1px_1px_0px_#000]">
                  AI
                </span>
              </div>
              <span className="text-[10px] font-display font-bold uppercase tracking-wider text-[#15CCFF]">
                Multi-Agent Intel
              </span>
            </div>
          </Link>
        ) : (
          <div className="mx-auto flex h-9 w-9 items-center justify-center rounded-lg border-2 border-black bg-[#15CCFF] text-black shadow-[2px_2px_0px_#FFEA00]">
            <Sparkles className="h-5 w-5 fill-current" />
          </div>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hidden md:flex h-7 w-7 items-center justify-center rounded-md border border-black bg-slate-800 text-slate-300 hover:bg-[#15CCFF] hover:text-black transition-colors"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
        {categories.map((category) => {
          const items = navItems.filter((item) => item.category === category);
          return (
            <div key={category} className="space-y-1">
              {!collapsed && (
                <div className="px-3 pb-1 text-[11px] font-display font-black italic uppercase tracking-wider text-[#FFEA00]">
                  {category}
                </div>
              )}
              {items.map((item) => {
                const isActive =
                  item.href === "/"
                    ? pathname === "/"
                    : pathname.startsWith(item.href);
                const Icon = item.icon;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    title={collapsed ? item.name : undefined}
                    className={`flex items-center gap-3 rounded-lg px-3 py-2 text-xs font-display font-bold italic tracking-wide transition-all ${
                      isActive
                        ? "border-2 border-black bg-[#15CCFF] text-black shadow-feast-sm -translate-x-0.5"
                        : "text-slate-300 hover:bg-[#1F2937] hover:text-white"
                    } ${collapsed ? "justify-center px-2" : ""}`}
                  >
                    <Icon className={`h-4.5 w-4.5 shrink-0 ${isActive ? "text-black stroke-[2.5]" : "text-slate-400"}`} />
                    {!collapsed && <span className="truncate uppercase">{item.name}</span>}
                    {!collapsed && item.badge && (
                      <span className={`ml-auto rounded px-1.5 py-0.2 text-[9px] font-black italic uppercase border border-black shadow-[1px_1px_0px_#000] ${item.badgeColor || "bg-[#FFEA00] text-black"}`}>
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>
          );
        })}
      </div>

      {/* Footer Model Allocation Badge */}
      {!collapsed && (
        <div className="p-3 border-t-2 border-black bg-[#111827]">
          <div className="rounded-lg border-2 border-black bg-[#67318F] p-3 text-white shadow-feast-sm">
            <div className="flex items-center justify-between pb-1.5 border-b border-purple-400/30">
              <span className="text-[10px] font-display font-black uppercase text-[#FFEA00]">
                Model Governance
              </span>
              <span className="h-2 w-2 rounded-full bg-[#15CCFF] animate-pulse"></span>
            </div>
            <div className="mt-2 space-y-1 text-[11px] font-sans">
              <div className="flex items-center justify-between">
                <span className="text-purple-200">Director:</span>
                <span className="font-bold text-[#FFEA00]">Muse Wonder</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-purple-200">7 Specialists:</span>
                <span className="font-bold text-[#15CCFF]">Spark 1.3</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-purple-200">Web Search:</span>
                <span className="font-bold text-[#FF5DB5]">Tavily API</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
