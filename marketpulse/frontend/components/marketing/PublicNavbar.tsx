"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Menu,
  X,
  Zap,
  ArrowRight,
  ShieldCheck,
  Cpu,
  Layers,
  Compass,
} from "lucide-react";

export function PublicNavbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { label: "Product", href: "/product" },
    { label: "How It Works", href: "/how-it-works" },
    { label: "Use Cases", href: "/use-cases" },
    { label: "About", href: "/about" },
    { label: "Contact", href: "/contact" },
  ];

  return (
    <header
      className={`sticky top-0 z-40 w-full transition-all duration-200 ${
        scrolled
          ? "bg-[#FFFFFF]/95 backdrop-blur-md border-b-2 border-[#0D1117] shadow-market-sm"
          : "bg-[#FFFFFF] border-b-2 border-[#0D1117]"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
        {/* Brand Logo */}
        <Link
          href="/"
          className="flex items-center gap-2 group text-decoration-none select-none"
        >
          <div className="w-10 h-10 rounded-lg bg-[#08B0D5] border-2 border-[#0D1117] flex items-center justify-center font-display font-black text-xl text-[#0D1117] shadow-market-sm group-hover:translate-x-0.5 group-hover:translate-y-0.5 transition-transform">
            M
          </div>
          <div className="flex flex-col leading-none">
            <span className="font-display font-extrabold text-2xl tracking-tight text-[#0D1117]">
              MARKET<span className="text-[#08B0D5]">PULSE</span>
            </span>
            <span className="text-[10px] font-bold tracking-widest text-[#64748B] uppercase">
              Autonomous Intelligence
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-1 lg:gap-2">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3.5 py-2 text-sm font-display font-bold uppercase tracking-wide rounded-md transition-colors ${
                  isActive
                    ? "text-[#0D1117] bg-[#08B0D5]/20 border border-[#08B0D5]"
                    : "text-[#0D1117] hover:bg-[#F4F8FA] hover:text-[#08B0D5]"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Right CTA Actions */}
        <div className="hidden md:flex items-center gap-3">
          <Link
            href="/app"
            className="px-4 py-2 text-sm font-display font-bold uppercase tracking-wider text-[#0D1117] hover:text-[#08B0D5] transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/app"
            className="btn-market inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-[#08B0D5] text-[#0D1117] font-display font-extrabold uppercase text-sm shadow-market hover:bg-[#068AA8]"
          >
            <Zap className="w-4 h-4 fill-current text-[#0D1117]" />
            <span>Open Workspace</span>
            <ArrowRight className="w-4 h-4 stroke-[3]" />
          </Link>
        </div>

        {/* Mobile menu button */}
        <div className="flex md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 border-2 border-[#0D1117] rounded-lg bg-[#FFFFFF] shadow-market-sm text-[#0D1117] focus:outline-none"
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6 stroke-[2.5]" />
            ) : (
              <Menu className="w-6 h-6 stroke-[2.5]" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b-2 border-[#0D1117] bg-[#FFFFFF] px-4 pt-3 pb-6 space-y-3">
          <div className="flex flex-col space-y-2">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="px-3 py-2 text-base font-display font-bold uppercase text-[#0D1117] hover:bg-[#F4F8FA] rounded-md"
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="pt-4 border-t border-[#E2E8F0] flex flex-col gap-2">
            <Link
              href="/app"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full text-center py-2.5 text-sm font-display font-bold uppercase text-[#0D1117] border border-[#0D1117] rounded-lg bg-[#F4F8FA]"
            >
              Sign In
            </Link>
            <Link
              href="/app"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full text-center py-3 text-sm font-display font-black uppercase text-[#0D1117] bg-[#08B0D5] border-2 border-[#0D1117] rounded-lg shadow-market"
            >
              Open Workspace →
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
