import React from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

interface CTAButtonProps {
  children: React.ReactNode;
  href?: string;
  onClick?: () => void;
  variant?: "primary" | "secondary" | "dark" | "outline";
  size?: "sm" | "md" | "lg";
  icon?: React.ReactNode;
  showArrow?: boolean;
  className?: string;
  disabled?: boolean;
}

export function CTAButton({
  children,
  href,
  onClick,
  variant = "primary",
  size = "md",
  icon,
  showArrow = false,
  className = "",
  disabled = false,
}: CTAButtonProps) {
  const variantStyles = {
    primary:
      "bg-[#08B0D5] text-[#0D1117] hover:bg-[#068AA8] border-2 border-[#0D1117] shadow-market",
    secondary:
      "bg-[#E3447C] text-[#FFFFFF] hover:bg-[#C93268] border-2 border-[#0D1117] shadow-market",
    dark:
      "bg-[#0D1117] text-[#FFFFFF] hover:bg-[#08B0D5] hover:text-[#0D1117] border-2 border-[#0D1117] shadow-market",
    outline:
      "bg-[#FFFFFF] text-[#0D1117] hover:bg-[#F4F8FA] border-2 border-[#0D1117] shadow-market-sm",
  };

  const sizeStyles = {
    sm: "px-3.5 py-1.5 text-xs",
    md: "px-5 py-2.5 text-sm",
    lg: "px-8 py-4 text-base",
  };

  const baseClasses = `btn-market inline-flex items-center justify-center gap-2 rounded-xl font-display font-black uppercase tracking-wider transition-all select-none disabled:opacity-50 disabled:pointer-events-none ${variantStyles[variant]} ${sizeStyles[size]} ${className}`;

  if (href) {
    return (
      <Link href={href} className={baseClasses}>
        {icon}
        <span>{children}</span>
        {showArrow && <ArrowRight className="w-4 h-4 stroke-[3]" />}
      </Link>
    );
  }

  return (
    <button onClick={onClick} disabled={disabled} className={baseClasses}>
      {icon}
      <span>{children}</span>
      {showArrow && <ArrowRight className="w-4 h-4 stroke-[3]" />}
    </button>
  );
}
