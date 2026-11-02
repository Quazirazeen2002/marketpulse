import React from "react";
import Link from "next/link";
import { FolderSearch, ArrowRight } from "lucide-react";

interface EmptyStateProps {
  title: string;
  description: string;
  actionLabel?: string;
  actionHref?: string;
  icon?: React.ReactNode;
}

export function EmptyState({
  title,
  description,
  actionLabel,
  actionHref,
  icon,
}: EmptyStateProps) {
  return (
    <div className="p-12 text-center border-2 border-dashed border-[#0D1117] rounded-2xl bg-[#FFFFFF] space-y-4 max-w-lg mx-auto select-none">
      <div className="w-12 h-12 rounded-xl bg-[#F4F8FA] border-2 border-[#0D1117] flex items-center justify-center mx-auto text-[#0D1117]">
        {icon || <FolderSearch className="w-6 h-6 text-[#64748B]" />}
      </div>
      <div className="space-y-1">
        <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
          {title}
        </h3>
        <p className="text-xs text-[#64748B] font-medium leading-relaxed max-w-sm mx-auto">
          {description}
        </p>
      </div>

      {actionLabel && actionHref && (
        <Link
          href={actionHref}
          className="btn-market inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#068AA8]"
        >
          <span>{actionLabel}</span>
          <ArrowRight className="w-3.5 h-3.5 stroke-[3]" />
        </Link>
      )}
    </div>
  );
}
