"use client";

import React from "react";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";

interface ShellProps {
  children: React.ReactNode;
}

export function Shell({ children }: ShellProps) {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900 font-sans antialiased">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden min-w-0">
        <Header />
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
