import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export function ErrorState({
  title = "Something went wrong",
  message,
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="p-8 rounded-2xl border-2 border-[#E3447C] bg-[#FFFFFF] shadow-market-sm space-y-4 max-w-lg mx-auto text-center">
      <div className="w-12 h-12 rounded-xl bg-[#E3447C]/15 border-2 border-[#E3447C] flex items-center justify-center mx-auto text-[#E3447C]">
        <AlertTriangle className="w-6 h-6" />
      </div>
      <div className="space-y-1">
        <h3 className="font-display font-black text-xl uppercase text-[#0D1117]">
          {title}
        </h3>
        <p className="text-xs text-[#64748B] font-medium leading-relaxed">
          {message}
        </p>
      </div>

      {onRetry && (
        <button
          onClick={onRetry}
          className="btn-market inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#0D1117] text-[#FFFFFF] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#08B0D5] hover:text-[#0D1117]"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Operation</span>
        </button>
      )}
    </div>
  );
}
