import React from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  variant?: "white" | "yellow" | "dark" | "blue";
}

export function MetricCard({
  label,
  value,
  subtitle,
  icon,
  variant = "white",
}: MetricCardProps) {
  const variantStyles = {
    white: "bg-[#FFFFFF] text-[#0D1117] border-2 border-[#0D1117]",
    yellow: "bg-[#08B0D5] text-[#0D1117] border-2 border-[#0D1117]",
    dark: "bg-[#0D1117] text-[#FFFFFF] border-2 border-[#0D1117]",
    blue: "bg-[#E3447C] text-[#FFFFFF] border-2 border-[#0D1117]",
  };

  return (
    <div
      className={`card-market p-5 rounded-2xl flex flex-col justify-between space-y-2 ${variantStyles[variant]}`}
    >
      <div className="flex items-center justify-between text-xs font-display font-black uppercase opacity-75">
        <span>{label}</span>
        {icon}
      </div>
      <p className="font-display font-black text-3xl sm:text-4xl tracking-tight">
        {value}
      </p>
      {subtitle && (
        <p className="text-[11px] font-bold uppercase opacity-80">{subtitle}</p>
      )}
    </div>
  );
}
