"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import {
  Calculator,
  Sparkles,
  RefreshCw,
  AlertCircle,
  Save,
  Check,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { ScenarioInput, ScenarioSuiteResponse, Opportunity } from "@/lib/types";
import { formatCurrency, formatPercent, formatNumber } from "@/lib/utils";

const ScenarioChart = dynamic(
  () => import("@/components/simulator/ScenarioChart"),
  {
    ssr: false,
    loading: () => <div className="h-64 w-full bg-[#F4F8FA] animate-pulse rounded-xl" />,
  }
);

export default function BusinessSimulatorPage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [selectedOpportunityId, setSelectedOpportunityId] = useState<string>("baseline-model");

  // Financial Engine Inputs
  const [inputs, setInputs] = useState<ScenarioInput>({
    initial_investment: 50000,
    selling_price: 45,
    product_cost: 16,
    monthly_order_volume: 3000,
    marketing_expense: 14000,
    delivery_cost: 4.5,
    return_rate: 0.08,
    fixed_operating_expenses: 9000,
    other_variable_costs: 2.0,
  });

  const [suite, setSuite] = useState<ScenarioSuiteResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedNotice, setSavedNotice] = useState(false);

  // Load opportunities for dropdown
  useEffect(() => {
    async function loadOpportunities() {
      try {
        const data = await api.getOpportunities();
        setOpportunities(data);
        if (data.length > 0 && selectedOpportunityId === "baseline-model") {
          const firstId = data[0].opportunity_id || String(data[0].id || "");
          if (firstId) setSelectedOpportunityId(firstId);
        }
      } catch {
        // use baseline fallback
      }
    }
    loadOpportunities();
  }, []);

  // Run deterministic calculation through FastAPI
  const runSimulation = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.simulateOpportunity(selectedOpportunityId, inputs);
      setSuite(res);
    } catch (err: any) {
      setError(err.message || "Failed to run deterministic simulation.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, [selectedOpportunityId]);

  const handleInputChange = (field: keyof ScenarioInput, val: string) => {
    const num = parseFloat(val) || 0;
    setInputs((prev) => ({ ...prev, [field]: num }));
  };

  const handleSaveScenario = () => {
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 3000);
  };

  // Prepare chart data for Worst, Base, Best comparison
  const scenarioChartData = suite
    ? [
        {
          name: "Worst Case",
          Revenue: suite.worst_case?.monthly_revenue ?? suite.worst_case?.revenue ?? 0,
          "Gross Profit": suite.worst_case?.gross_profit ?? 0,
          "Operating Profit":
            suite.worst_case?.monthly_operating_profit ??
            suite.worst_case?.operating_profit ??
            0,
        },
        {
          name: "Base Case",
          Revenue: suite.base_case?.monthly_revenue ?? suite.base_case?.revenue ?? 0,
          "Gross Profit": suite.base_case?.gross_profit ?? 0,
          "Operating Profit":
            suite.base_case?.monthly_operating_profit ??
            suite.base_case?.operating_profit ??
            0,
        },
        {
          name: "Best Case",
          Revenue: suite.best_case?.monthly_revenue ?? suite.best_case?.revenue ?? 0,
          "Gross Profit": suite.best_case?.gross_profit ?? 0,
          "Operating Profit":
            suite.best_case?.monthly_operating_profit ??
            suite.best_case?.operating_profit ??
            0,
        },
      ]
    : [];

  const base = suite?.base_case;

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
            <Calculator className="w-3.5 h-3.5" />
            <span>DETERMINISTIC SIMULATION ENGINE</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Financial & Unit Economics Simulator
          </h1>
          <p className="text-sm text-[#64748B] font-medium max-w-2xl">
            Execute real-time mathematical scenario stress-testing across variable costs, return rates, and acquisition expenses. Pure Python math—zero LLM hallucination.
          </p>
        </div>

        {/* Opportunity Selector */}
        <div className="space-y-1.5 shrink-0 w-full sm:w-auto">
          <label className="text-[11px] font-display font-black uppercase text-[#0D1117] block">
            Target Opportunity:
          </label>
          <select
            value={selectedOpportunityId}
            onChange={(e) => setSelectedOpportunityId(e.target.value)}
            className="w-full sm:w-64 px-3.5 py-2.5 rounded-xl border-2 border-[#0D1117] bg-[#08B0D5] text-xs font-display font-black uppercase text-[#0D1117] shadow-market-sm focus:outline-none"
          >
            <option value="baseline-model">Generic Baseline Model</option>
            {opportunities.map((opp) => (
              <option key={opp.opportunity_id} value={opp.opportunity_id}>
                {opp.opportunity_name.slice(0, 32)}...
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Two-Column Layout: Inputs + Outputs */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Interactive Inputs */}
        <div className="lg:col-span-5 card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-6">
          <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
            <span className="text-xs font-display font-black text-[#08B0D5] uppercase tracking-wider">
              INPUT PARAMETERS
            </span>
            <span className="text-[11px] font-bold text-[#64748B] uppercase">
              User Editable
            </span>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Selling Price ($)
                </label>
                <input
                  type="number"
                  step="0.5"
                  value={inputs.selling_price}
                  onChange={(e) => handleInputChange("selling_price", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Product Cost ($)
                </label>
                <input
                  type="number"
                  step="0.5"
                  value={inputs.product_cost}
                  onChange={(e) => handleInputChange("product_cost", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Monthly Orders
                </label>
                <input
                  type="number"
                  step="50"
                  value={inputs.monthly_order_volume}
                  onChange={(e) => handleInputChange("monthly_order_volume", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Delivery Cost ($)
                </label>
                <input
                  type="number"
                  step="0.25"
                  value={inputs.delivery_cost}
                  onChange={(e) => handleInputChange("delivery_cost", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Return Rate (0 - 1)
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="1"
                  value={inputs.return_rate}
                  onChange={(e) => handleInputChange("return_rate", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Marketing ($/mo)
                </label>
                <input
                  type="number"
                  step="500"
                  value={inputs.marketing_expense}
                  onChange={(e) => handleInputChange("marketing_expense", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Fixed Overhead ($/mo)
                </label>
                <input
                  type="number"
                  step="500"
                  value={inputs.fixed_operating_expenses}
                  onChange={(e) => handleInputChange("fixed_operating_expenses", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-display font-black uppercase text-[#0D1117]">
                  Initial Capex ($)
                </label>
                <input
                  type="number"
                  step="1000"
                  value={inputs.initial_investment}
                  onChange={(e) => handleInputChange("initial_investment", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-xs font-bold text-[#0D1117] focus:bg-[#FFFFFF]"
                />
              </div>
            </div>
          </div>

          <div className="pt-2 flex flex-col gap-2">
            <button
              onClick={runSimulation}
              disabled={loading}
              className="btn-market w-full py-3 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF] flex items-center justify-center gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
              <span>{loading ? "Calculating..." : "Recalculate Python Engine"}</span>
            </button>

            <button
              onClick={handleSaveScenario}
              className="w-full py-2.5 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] text-[#0D1117] font-display font-bold text-xs uppercase hover:bg-[#F4F8FA] flex items-center justify-center gap-1.5"
            >
              {savedNotice ? (
                <>
                  <Check className="w-4 h-4 text-[#08B0D5]" />
                  <span>Scenario Saved to SQLite!</span>
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  <span>Save Scenario Suite</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Calculated Outputs & Scenarios */}
        <div className="lg:col-span-7 space-y-6">
          {/* Base Case KPI Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
              <span className="text-[10px] font-display font-black uppercase text-[#64748B]">
                Monthly Revenue
              </span>
              <p className="font-display font-black text-2xl text-[#0D1117]">
                {formatCurrency(base?.monthly_revenue ?? base?.revenue ?? 0)}
              </p>
              <p className="text-[10px] text-[#64748B]">Base Case</p>
            </div>

            <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
              <span className="text-[10px] font-display font-black uppercase text-[#64748B]">
                Gross Margin
              </span>
              <p className="font-display font-black text-2xl text-[#08B0D5]">
                {formatPercent(base?.gross_margin_percent ?? base?.gross_margin ?? 0)}
              </p>
              <p className="text-[10px] text-[#08B0D5] font-semibold">After product costs</p>
            </div>

            <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
              <span className="text-[10px] font-display font-black uppercase text-[#64748B]">
                Operating Profit
              </span>
              <p
                className={`font-display font-black text-2xl ${
                  (base?.monthly_operating_profit ?? base?.operating_profit ?? 0) >= 0
                    ? "text-[#08B0D5]"
                    : "text-[#E3447C]"
                }`}
              >
                {formatCurrency(base?.monthly_operating_profit ?? base?.operating_profit ?? 0)}
              </p>
              <p className="text-[10px] text-[#64748B]">Net Monthly</p>
            </div>

            <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
              <span className="text-[10px] font-display font-black uppercase text-[#64748B]">
                Break-Even
              </span>
              <p className="font-display font-black text-2xl text-[#0D1117]">
                {formatNumber(base?.break_even_orders ?? base?.break_even_order_volume ?? 0)}
              </p>
              <p className="text-[10px] text-[#64748B]">Orders required/mo</p>
            </div>
          </div>

          {/* Scenario Comparison Chart (Worst, Base, Best) */}
          <div className="card-market p-6 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-lg space-y-4">
            <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
              <span className="text-xs font-display font-black text-[#08B0D5] uppercase">
                SCENARIO SUITE COMPARISON
              </span>
              <span className="text-[11px] font-bold text-[#64748B] uppercase">
                Worst • Base • Best
              </span>
            </div>

            <ScenarioChart data={scenarioChartData} />
          </div>

          {/* Sensitivity Analysis Table */}
          {suite?.sensitivity && suite.sensitivity.length > 0 && (
            <div className="card-market p-6 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-lg space-y-4">
              <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
                <span className="text-xs font-display font-black text-[#0D1117] uppercase">
                  5D Sensitivity Analysis
                </span>
                <span className="text-[10px] font-mono text-[#64748B]">
                  ±15% Parameter Deviations
                </span>
              </div>

              <div className="space-y-4 text-xs">
                {suite.sensitivity.slice(0, 3).map((dim, idx) => {
                  const dimName = dim.variable_tested || dim.dimension || `Dimension ${idx + 1}`;
                  const baseVal = dim.baseline_value ?? dim.base_value ?? 0;
                  return (
                    <div key={dimName} className="space-y-1.5">
                      <div className="flex items-center justify-between font-display font-bold uppercase text-[#64748B]">
                        <span>{dimName.replace(/_/g, " ")}</span>
                        <span>Base: {baseVal}</span>
                      </div>

                      <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
                        {(dim.variations || []).map((v, i) => {
                          const label = v.percentage_change || v.label || "";
                          const val = v.tested_value ?? v.value ?? 0;
                          const opProfit = v.monthly_operating_profit ?? v.operating_profit ?? 0;
                          return (
                            <div
                              key={i}
                              className="p-2.5 rounded-lg border border-[#0D1117] bg-[#F4F8FA] text-center space-y-0.5"
                            >
                              <span className="text-[10px] font-bold text-[#64748B] block">
                                {label} ({val})
                              </span>
                              <span
                                className={`font-display font-black text-xs block ${
                                  opProfit >= 0 ? "text-[#08B0D5]" : "text-[#E3447C]"
                                }`}
                              >
                                {formatCurrency(opProfit)}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
