import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  weight: ["500", "600", "700"],
  variable: "--font-space",
  display: "swap",
});

export const metadata: Metadata = {
  title: "MARKETPULSE — Autonomous Business Intelligence & Opportunity Discovery",
  description:
    "Next-generation AI market research engine powered by Meta Muse Wonder, Meta Spark 1.3, and Tavily. Turn web evidence into verified strategic intelligence.",
  keywords: [
    "Market Research",
    "Competitive Intelligence",
    "Autonomous Agents",
    "Business Intelligence",
    "LangGraph",
    "Meta AI",
    "Tavily",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${spaceGrotesk.variable} h-full antialiased scroll-smooth`}
    >
      <body className="min-h-full flex flex-col bg-[#F4F8FA] text-[#0D1117] font-sans selection:bg-[#08B0D5] selection:text-[#0D1117]">
        {children}
      </body>
    </html>
  );
}
