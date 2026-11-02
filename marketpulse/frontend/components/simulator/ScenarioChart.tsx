"use client";

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { formatCurrency } from "@/lib/utils";

interface ScenarioChartProps {
  data: Array<{
    name: string;
    Revenue: number;
    "Gross Profit": number;
    "Operating Profit": number;
  }>;
}

export default function ScenarioChart({ data }: ScenarioChartProps) {
  if (!data || data.length === 0) return null;

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 11, fontFamily: "var(--font-space)", fontWeight: 700 }}
            stroke="#0D1117"
          />
          <YAxis
            tick={{ fontSize: 11, fontFamily: "var(--font-space)" }}
            tickFormatter={(val) => `$${val / 1000}k`}
            stroke="#0D1117"
          />
          <Tooltip
            formatter={(val: any) => [formatCurrency(Number(val)), ""]}
            contentStyle={{
              backgroundColor: "#0D1117",
              border: "2px solid #08B0D5",
              borderRadius: "8px",
              fontSize: "12px",
              color: "#FFFFFF",
              fontFamily: "var(--font-space)",
              fontWeight: 700,
            }}
          />
          <Legend
            wrapperStyle={{
              fontSize: "11px",
              fontFamily: "var(--font-space)",
              fontWeight: 700,
              textTransform: "uppercase",
            }}
          />
          <Bar dataKey="Revenue" fill="#08B0D5" radius={[4, 4, 0, 0]} stroke="#0D1117" strokeWidth={1.5} />
          <Bar dataKey="Gross Profit" fill="#E3447C" radius={[4, 4, 0, 0]} stroke="#0D1117" strokeWidth={1.5} />
          <Bar dataKey="Operating Profit" fill="#0D1117" radius={[4, 4, 0, 0]} stroke="#0D1117" strokeWidth={1.5} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
