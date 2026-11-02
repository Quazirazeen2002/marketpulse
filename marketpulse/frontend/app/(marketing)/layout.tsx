import React from "react";
import { AnnouncementBar } from "@/components/marketing/AnnouncementBar";
import { PublicNavbar } from "@/components/marketing/PublicNavbar";
import { PublicFooter } from "@/components/marketing/PublicFooter";

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col bg-[#F4F8FA] text-[#0D1117]">
      <AnnouncementBar />
      <PublicNavbar />
      <main className="flex-1">{children}</main>
      <PublicFooter />
    </div>
  );
}
