import React from "react";

interface LoadingSkeletonProps {
  count?: number;
  heightClass?: string;
}

export function LoadingSkeleton({
  count = 3,
  heightClass = "h-36",
}: LoadingSkeletonProps) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={`w-full rounded-2xl border-2 border-[#171717] bg-[#FFFFFF] animate-pulse ${heightClass}`}
        />
      ))}
    </div>
  );
}
