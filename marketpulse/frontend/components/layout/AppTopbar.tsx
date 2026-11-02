"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Menu,
  Activity,
  Zap,
  ChevronRight,
} from "lucide-react";
import { api } from "@/lib/api/client";

interface AppTopbarProps {
  onOpenMobile?: () => void;
}

export function AppTopbar({ onOpenMobile }: AppTopbarProps) {
  const pathname = usePathname();
  const [activeTasks, setActiveTasks] = useState<number>(0);
  const [backendOnline, setBackendOnline] = useState<boolean>(true);

  useEffect(() => {
    let mounted = true;
    async function checkHealth() {
      try {
        const health = await api.getServiceHealth();
        if (mounted) {
          setActiveTasks(health.active_background_tasks || 0);
          setBackendOnline(true);
        }
      } catch {
        if (mounted) {
          setBackendOnline(false);
        }
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  // Format breadcrumbs from pathname
  const pathParts = pathname.split("/").filter(Boolean);
  const breadcrumbItems = pathParts.map((part, index) => {
    const href = "/" + pathParts.slice(0, index + 1).join("/");
    const label = part.charAt(0).toUpperCase() + part.slice(1).replace(/-/g, " ");
    return { href, label };
  });

  return (
    <header className="h-18 px-4 sm:px-6 bg-[#FFFFFF] border-b-2 border-[#0D1117] flex items-center justify-between gap-4 sticky top-0 z-30 select-none">
      {/* Left: Mobile hamburger & Breadcrumbs */}
      <div className="flex items-center gap-3">
        {onOpenMobile && (
          <button
            onClick={onOpenMobile}
            className="md:hidden p-2 rounded-lg border-2 border-[#0D1117] bg-[#08B0D5] text-[#0D1117] shadow-market-sm"
            aria-label="Open Navigation Menu"
          >
            <Menu className="w-5 h-5 stroke-[2.5]" />
          </button>
        )}

        {/* Breadcrumb Trail */}
        <nav className="flex items-center gap-1.5 text-xs font-display font-bold uppercase tracking-wider text-[#64748B]">
          <Link href="/app" className="hover:text-[#08B0D5] transition-colors">
            Workspace
          </Link>
          {breadcrumbItems.slice(1).map((crumb, idx) => (
            <React.Fragment key={crumb.href}>
              <ChevronRight className="w-3.5 h-3.5 text-[#0D1117]" />
              <Link
                href={crumb.href}
                className={`transition-colors truncate max-w-[140px] sm:max-w-none ${
                  idx === breadcrumbItems.length - 2
                    ? "text-[#0D1117] font-black"
                    : "hover:text-[#08B0D5]"
                }`}
              >
                {crumb.label}
              </Link>
            </React.Fragment>
          ))}
        </nav>
      </div>

      {/* Right Actions & Status Badges */}
      <div className="flex items-center gap-3">
        {/* Backend Status Badge */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-[11px] font-display font-black uppercase shadow-market-sm">
          <span
            className={`w-2 h-2 rounded-full ${
              backendOnline ? "bg-[#08B0D5] animate-pulse" : "bg-[#E3447C]"
            }`}
          />
          <span className="text-[#0D1117]">
            {backendOnline ? "API Online" : "API Offline"}
          </span>
        </div>

        {/* Active Research Runs Badge */}
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border-2 border-[#0D1117] bg-[#FFFFFF] text-[11px] font-display font-black uppercase shadow-market-sm">
          <Activity
            className={`w-3.5 h-3.5 ${
              activeTasks > 0 ? "text-[#E3447C] animate-spin" : "text-[#64748B]"
            }`}
          />
          <span className="text-[#0D1117]">
            {activeTasks} Active Run{activeTasks === 1 ? "" : "s"}
          </span>
        </div>

        {/* Quick New Research CTA */}
        <Link
          href="/app/research/new"
          className="btn-market hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
        >
          <Zap className="w-3.5 h-3.5 fill-current" />
          <span>New Run</span>
        </Link>
      </div>
    </header>
  );
}
