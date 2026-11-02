"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Search,
  Compass,
  Cpu,
  Lightbulb,
  FileQuestion,
  ShieldAlert,
  Database,
  FileText,
  Calculator,
  History,
  Settings,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  ChevronDown,
} from "lucide-react";

interface AppSidebarProps {
  collapsed?: boolean;
  onToggleCollapse?: () => void;
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export function AppSidebar({
  collapsed = false,
  onToggleCollapse,
  mobileOpen = false,
  onCloseMobile,
}: AppSidebarProps) {
  const pathname = usePathname();
  const [intelligenceOpen, setIntelligenceOpen] = useState(
    pathname.startsWith("/app/intelligence")
  );

  const mainNavigation = [
    {
      label: "Command Center",
      href: "/app",
      icon: LayoutDashboard,
      exact: true,
    },
    {
      label: "New Research",
      href: "/app/research/new",
      icon: Search,
    },
    {
      label: "Agent Observatory",
      href: "/app/agents",
      icon: Cpu,
      badge: "8 AGENTS",
    },
    {
      label: "Opportunities",
      href: "/app/opportunities",
      icon: Lightbulb,
      badge: "SCORED",
      badgeColor: "bg-[#E3447C] text-[#FFFFFF]",
    },
    {
      label: "Hypotheses",
      href: "/app/hypotheses",
      icon: FileQuestion,
    },
    {
      label: "Risk Observatory",
      href: "/app/risks",
      icon: ShieldAlert,
    },
    {
      label: "Evidence Explorer",
      href: "/app/evidence",
      icon: Database,
    },
    {
      label: "Executive Reports",
      href: "/app/reports",
      icon: FileText,
    },
    {
      label: "Business Simulator",
      href: "/app/simulator",
      icon: Calculator,
      badge: "MATH",
      badgeColor: "bg-[#08B0D5] text-[#0D1117]",
    },
    {
      label: "Research History",
      href: "/app/history",
      icon: History,
    },
    {
      label: "System Settings",
      href: "/app/settings",
      icon: Settings,
    },
  ];

  const intelligenceSubLinks = [
    { label: "Overview Hub", href: "/app/intelligence" },
    { label: "Market Intelligence", href: "/app/intelligence/market" },
    { label: "Competitor Intelligence", href: "/app/intelligence/competitors" },
    { label: "Customer Intelligence", href: "/app/intelligence/customers" },
    { label: "Marketing Intelligence", href: "/app/intelligence/marketing" },
    { label: "Commercial Intelligence", href: "/app/intelligence/commercial" },
  ];

  const sidebarContent = (
    <div className="flex flex-col h-full bg-[#FFFFFF] border-r-2 border-[#0D1117] text-[#0D1117] select-none">
      {/* Brand Header */}
      <div className="h-18 px-4 border-b-2 border-[#0D1117] flex items-center justify-between">
        <Link
          href="/"
          className="flex items-center gap-2 group text-decoration-none"
        >
          <div className="w-9 h-9 rounded-lg bg-[#08B0D5] border-2 border-[#0D1117] flex items-center justify-center font-display font-black text-lg text-[#0D1117] shadow-market-sm group-hover:translate-x-0.5 group-hover:translate-y-0.5 transition-transform shrink-0">
            M
          </div>
          {!collapsed && (
            <div className="flex flex-col leading-none">
              <span className="font-display font-extrabold text-xl tracking-tight text-[#0D1117]">
                MARKET<span className="text-[#08B0D5]">PULSE</span>
              </span>
              <span className="text-[9px] font-bold tracking-widest text-[#64748B] uppercase">
                Workspace Shell
              </span>
            </div>
          )}
        </Link>

        {/* Desktop Collapse Button */}
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="hidden md:flex p-1.5 rounded-md hover:bg-[#E2E8F0] text-[#64748B] hover:text-[#0D1117]"
            title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? (
              <ChevronRight className="w-4 h-4" />
            ) : (
              <ChevronLeft className="w-4 h-4" />
            )}
          </button>
        )}
      </div>

      {/* Main Navigation Items */}
      <div className="flex-1 overflow-y-auto p-3 space-y-1">
        {mainNavigation.map((item) => {
          const Icon = item.icon;
          const isActive = item.exact
            ? pathname === item.href
            : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onCloseMobile}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-display font-bold uppercase tracking-wider transition-all ${
                isActive
                  ? "bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117] shadow-market-sm"
                  : "text-[#0D1117] hover:bg-[#E2E8F0]"
              }`}
              title={collapsed ? item.label : undefined}
            >
              <Icon className="w-4 h-4 shrink-0 stroke-[2.2]" />
              {!collapsed && (
                <div className="flex items-center justify-between flex-1 truncate">
                  <span className="truncate">{item.label}</span>
                  {item.badge && (
                    <span
                      className={`text-[9px] px-1.5 py-0.5 rounded font-black tracking-widest ${
                        item.badgeColor || "bg-[#0D1117] text-[#FFFFFF]"
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </div>
              )}
            </Link>
          );
        })}

        {/* Intelligence Accordion Group */}
        <div className="pt-2">
          {!collapsed && (
            <button
              onClick={() => setIntelligenceOpen(!intelligenceOpen)}
              className="w-full flex items-center justify-between px-3 py-2 text-[11px] font-display font-black text-[#64748B] uppercase tracking-wider hover:text-[#0D1117]"
            >
              <div className="flex items-center gap-2">
                <Compass className="w-3.5 h-3.5 text-[#08B0D5]" />
                <span>Intelligence Domains</span>
              </div>
              <ChevronDown
                className={`w-3.5 h-3.5 transition-transform ${
                  intelligenceOpen ? "rotate-180" : ""
                }`}
              />
            </button>
          )}

          {!collapsed && intelligenceOpen && (
            <div className="pl-4 pr-1 py-1 space-y-1 border-l-2 border-[#E2E8F0] ml-4 mt-1">
              {intelligenceSubLinks.map((sub) => {
                const isSubActive = pathname === sub.href;
                return (
                  <Link
                    key={sub.href}
                    href={sub.href}
                    onClick={onCloseMobile}
                    className={`block px-2.5 py-1.5 rounded text-[11px] font-display font-bold uppercase transition-colors ${
                      isSubActive
                        ? "text-[#08B0D5] bg-[#08B0D5]/15 font-black"
                        : "text-[#64748B] hover:text-[#0D1117] hover:bg-[#E2E8F0]"
                    }`}
                  >
                    {sub.label}
                  </Link>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Footer Info / Marketing Link */}
      <div className="p-3 border-t-2 border-[#0D1117] bg-[#F4F8FA]">
        {!collapsed ? (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-[11px] font-bold text-[#64748B]">
              <span>FastAPI Backend</span>
              <span className="flex items-center gap-1 text-[#08B0D5]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#08B0D5]"></span>
                Connected
              </span>
            </div>
            <Link
              href="/"
              className="flex items-center justify-between px-2.5 py-1.5 rounded bg-[#FFFFFF] border border-[#0D1117] text-[11px] font-display font-bold text-[#0D1117] hover:bg-[#08B0D5] transition-colors"
            >
              <span>View Marketing Site</span>
              <ExternalLink className="w-3 h-3" />
            </Link>
          </div>
        ) : (
          <div className="flex justify-center">
            <span
              className="w-2.5 h-2.5 rounded-full bg-[#08B0D5]"
              title="FastAPI Backend Online"
            />
          </div>
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside
        className={`hidden md:block transition-all duration-200 shrink-0 ${
          collapsed ? "w-20" : "w-64"
        }`}
      >
        <div className="h-screen sticky top-0">{sidebarContent}</div>
      </aside>

      {/* Mobile Drawer Overlay */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex">
          <div
            className="fixed inset-0 bg-black/50 backdrop-blur-xs"
            onClick={onCloseMobile}
          />
          <div className="relative w-72 max-w-[80vw] h-full z-10">
            {sidebarContent}
          </div>
        </div>
      )}
    </>
  );
}
