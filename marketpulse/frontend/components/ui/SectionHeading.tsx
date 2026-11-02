import React from "react";

interface SectionHeadingProps {
  badge?: string;
  title: string;
  highlight?: string;
  subtitle?: string;
  align?: "left" | "center";
  theme?: "light" | "dark";
}

export function SectionHeading({
  badge,
  title,
  highlight,
  subtitle,
  align = "left",
  theme = "light",
}: SectionHeadingProps) {
  const isCenter = align === "center";
  const isDark = theme === "dark";

  return (
    <div className={`space-y-3 ${isCenter ? "text-center max-w-3xl mx-auto" : "max-w-3xl"}`}>
      {badge && (
        <span
          className={`inline-block px-3 py-1 rounded text-xs font-display font-black uppercase tracking-wider border-2 border-[#0D1117] shadow-market-sm ${
            isDark ? "bg-[#08B0D5] text-[#0D1117]" : "bg-[#E3447C] text-[#FFFFFF]"
          }`}
        >
          {badge}
        </span>
      )}
      <h2
        className={`font-display font-black uppercase text-3xl sm:text-5xl tracking-tight leading-tight ${
          isDark ? "text-[#FFFFFF]" : "text-[#0D1117]"
        }`}
      >
        {title} {highlight && <span className="text-[#08B0D5]">{highlight}</span>}
      </h2>
      {subtitle && (
        <p className={`text-sm sm:text-base font-medium leading-relaxed ${isDark ? "text-[#E2E8F0]" : "text-[#64748B]"}`}>
          {subtitle}
        </p>
      )}
    </div>
  );
}
