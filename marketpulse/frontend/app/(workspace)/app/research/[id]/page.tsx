"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import {
  Activity,
  CheckCircle2,
  AlertCircle,
  Clock,
  Database,
  FileCheck,
  Sparkles,
  Bot,
  ExternalLink,
  ChevronDown,
  ChevronRight,
  RefreshCw,
  FileText,
  Lightbulb,
  ShieldCheck,
  Search,
  Zap,
  ArrowRight,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { ResearchProgress } from "@/lib/types";

export default function ActiveResearchWorkspace() {
  const params = useParams();
  const router = useRouter();
  const researchId = params?.id as string;

  const [progress, setProgress] = useState<ResearchProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [connectionType, setConnectionType] = useState<"sse" | "polling">("sse");
  const [showEventLog, setShowEventLog] = useState(true);
  const [strategicDispatching, setStrategicDispatching] = useState(false);

  const eventSourceRef = useRef<EventSource | null>(null);
  const pollTimerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!researchId) return;

    let isMounted = true;
    const API_BASE_URL =
      process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
    const sseUrl = `${API_BASE_URL}/api/research/${researchId}/events/stream`;

    function startPolling() {
      setConnectionType("polling");
      async function poll() {
        try {
          const data = await api.getResearchProgress(researchId);
          if (isMounted) {
            setProgress(data);
            setLoading(false);
            if (
              data.execution_status === "completed" ||
              data.execution_status === "failed"
            ) {
              if (pollTimerRef.current) clearInterval(pollTimerRef.current);
            }
          }
        } catch (err: any) {
          if (isMounted) {
            setError(err.message || "Failed to poll research progress.");
            setLoading(false);
          }
        }
      }

      poll();
      pollTimerRef.current = setInterval(poll, 2500);
    }

    try {
      const es = new EventSource(sseUrl);
      eventSourceRef.current = es;

      es.onopen = () => {
        if (isMounted) {
          setConnectionType("sse");
          setLoading(false);
        }
      };

      es.onmessage = (event) => {
        if (!isMounted) return;
        try {
          const data = JSON.parse(event.data);
          if (data.type === "event" || data.type === "status") {
            setProgress((prev) => {
              const currentEvents = prev?.progress_events || [];
              const newEvent = data.event;
              const updatedEvents = newEvent
                ? currentEvents.some((e) => e.event_id === newEvent.event_id)
                  ? currentEvents
                  : [...currentEvents, newEvent]
                : currentEvents;

              return {
                research_id: researchId,
                objective: prev?.objective || data.objective,
                execution_status: data.execution_status || prev?.execution_status || "running",
                current_stage: data.current_stage || prev?.current_stage || "executing",
                elapsed_seconds: data.elapsed_seconds || prev?.elapsed_seconds || 0,
                source_count: data.source_count !== undefined ? data.source_count : prev?.source_count || 0,
                evidence_count: data.evidence_count !== undefined ? data.evidence_count : prev?.evidence_count || 0,
                verified_claims_count:
                  data.verified_claims_count !== undefined
                    ? data.verified_claims_count
                    : prev?.verified_claims_count || 0,
                contradictions_count:
                  data.contradictions_count !== undefined
                    ? data.contradictions_count
                    : prev?.contradictions_count || 0,
                agent_status: data.agent_status || prev?.agent_status || {},
                progress_events: updatedEvents,
                final_report: data.final_report || prev?.final_report,
                error: data.error || prev?.error,
              };
            });
            setLoading(false);
          }
        } catch {
          // ignore parsing error
        }
      };

      es.onerror = () => {
        if (eventSourceRef.current) {
          eventSourceRef.current.close();
          eventSourceRef.current = null;
        }
        if (isMounted) {
          startPolling();
        }
      };
    } catch {
      startPolling();
    }

    return () => {
      isMounted = false;
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      if (pollTimerRef.current) {
        clearInterval(pollTimerRef.current);
      }
    };
  }, [researchId]);

  const handleLaunchStrategicDiscovery = async () => {
    try {
      setStrategicDispatching(true);
      const res = await api.submitStrategicAnalysis({
        research_id: researchId,
        strategic_objective: progress?.objective || "",
      });
      if (res && res.analysis_id) {
        router.push(`/app/opportunities`);
      }
    } catch (err: any) {
      alert(`Strategic dispatch failed: ${err.message}`);
    } finally {
      setStrategicDispatching(false);
    }
  };

  const status = progress?.execution_status || "pending";

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header Bar */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-3xl">
          <div className="flex flex-wrap items-center gap-2">
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-display font-black uppercase border border-[#0D1117] ${
                status === "completed"
                  ? "bg-[#08B0D5] text-[#0D1117]"
                  : status === "failed"
                  ? "bg-[#E3447C] text-[#FFFFFF]"
                  : "bg-[#08B0D5] text-[#0D1117] animate-pulse"
              }`}
            >
              <Activity className="w-3.5 h-3.5" />
              <span>Status: {status}</span>
            </span>

            <span className="px-2.5 py-1 rounded bg-[#F4F8FA] border border-[#0D1117] text-[11px] font-mono text-[#64748B]">
              {researchId}
            </span>

            <span className="px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] text-[10px] font-display font-bold uppercase">
              {connectionType === "sse" ? "⚡ Live SSE Stream" : "🔄 Polling (2.5s)"}
            </span>
          </div>

          <h1 className="font-display font-black text-2xl sm:text-4xl uppercase text-[#0D1117] tracking-tight">
            {progress?.objective || "Active Multi-Agent Investigation"}
          </h1>
        </div>

        {/* Action buttons */}
        <div className="flex flex-wrap items-center gap-3 shrink-0">
          {status === "completed" && (
            <>
              <Link
                href={`/app/reports/${researchId}`}
                className="btn-market inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#0799ba]"
              >
                <FileText className="w-4 h-4" />
                <span>Read Executive Report</span>
              </Link>

              <button
                onClick={handleLaunchStrategicDiscovery}
                disabled={strategicDispatching}
                className="btn-market inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#E3447C] text-[#FFFFFF] font-display font-black text-xs uppercase shadow-market-sm hover:bg-[#c93267] disabled:opacity-50"
              >
                <Lightbulb className="w-4 h-4 fill-current" />
                <span>
                  {strategicDispatching ? "Spawning Loop..." : "Discover Opportunities (Stage 2)"}
                </span>
                <ArrowRight className="w-4 h-4 stroke-[3]" />
              </button>
            </>
          )}

          <Link
            href="/app/research/new"
            className="btn-market inline-flex items-center gap-1.5 px-4 py-3 rounded-xl bg-[#FFFFFF] text-[#0D1117] font-display font-bold text-xs uppercase shadow-market-sm border-2 border-[#0D1117] hover:bg-[#F4F8FA]"
          >
            <span>New Run</span>
          </Link>
        </div>
      </div>

      {/* Real-time Status Metric Counters */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
          <span className="text-[11px] font-display font-black text-[#64748B] uppercase">
            Sources Retrieved
          </span>
          <p className="font-display font-black text-2xl text-[#0D1117]">
            {progress?.source_count || 0}
          </p>
          <p className="text-[10px] text-[#64748B]">Tavily Web Spidering</p>
        </div>

        <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
          <span className="text-[11px] font-display font-black text-[#64748B] uppercase">
            Atomic Evidence
          </span>
          <p className="font-display font-black text-2xl text-[#0D1117]">
            {progress?.evidence_count || 0}
          </p>
          <p className="text-[10px] text-[#64748B]">Extracted & Fingerprinted</p>
        </div>

        <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
          <span className="text-[11px] font-display font-black text-[#64748B] uppercase">
            Verified Claims
          </span>
          <p className="font-display font-black text-2xl text-[#08B0D5]">
            {progress?.verified_claims_count || 0}
          </p>
          <p className="text-[10px] text-[#08B0D5] font-semibold">Cross-examined</p>
        </div>

        <div className="card-market p-4 rounded-xl bg-[#FFFFFF] space-y-1 border-2 border-[#0D1117]">
          <span className="text-[11px] font-display font-black text-[#64748B] uppercase">
            Contradictions
          </span>
          <p className="font-display font-black text-2xl text-[#E3447C]">
            {progress?.contradictions_count || 0}
          </p>
          <p className="text-[10px] text-[#E3447C] font-semibold">Arbitrated by Director</p>
        </div>
      </div>

      {/* Two Column Execution Layout: Timeline / Events + Report Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Real-time Event Stream */}
        <div className="lg:col-span-6 card-market p-6 rounded-2xl bg-[#FFFFFF] space-y-6 border-3 border-[#0D1117]">
          <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
            <div>
              <span className="text-[11px] font-display font-black text-[#08B0D5] uppercase">
                EXECUTION AUDIT LOG
              </span>
              <h2 className="font-display font-black text-xl uppercase text-[#0D1117]">
                Live Agent Events
              </h2>
            </div>
            <span className="px-2.5 py-1 rounded bg-[#F4F8FA] border border-[#0D1117] text-[11px] font-bold text-[#0D1117]">
              {progress?.progress_events?.length || 0} Events
            </span>
          </div>

          {/* Event Stream List */}
          <div className="space-y-3 max-h-[550px] overflow-y-auto pr-2">
            {!progress?.progress_events || progress.progress_events.length === 0 ? (
              <div className="py-12 text-center space-y-2">
                <Activity className="w-6 h-6 text-[#64748B] animate-spin mx-auto" />
                <p className="text-xs font-display font-bold uppercase text-[#64748B]">
                  Waiting for initial agent events...
                </p>
              </div>
            ) : (
              progress.progress_events.map((evt, idx) => (
                <div
                  key={evt.event_id || idx}
                  className="p-3.5 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] text-xs space-y-1 shadow-market-sm"
                >
                  <div className="flex items-center justify-between text-[10px] text-[#64748B] font-bold">
                    <span className="px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] uppercase">
                      {evt.agent_name || "Research Director"}
                    </span>
                    <span>{evt.timestamp ? new Date(evt.timestamp).toLocaleTimeString() : ""}</span>
                  </div>
                  <p className="font-display font-bold text-[#0D1117] text-xs">
                    {evt.message}
                  </p>
                  {evt.node_name && (
                    <span className="inline-block text-[10px] font-mono text-[#64748B]">
                      Node: {evt.node_name}
                    </span>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Column: Active Agent States & Final Report Canvas */}
        <div className="lg:col-span-6 space-y-6">
          {/* Agent Status Grid */}
          <div className="card-market p-6 rounded-2xl bg-[#FFFFFF] space-y-4 border-3 border-[#0D1117]">
            <div className="border-b-2 border-[#0D1117] pb-3 flex items-center justify-between">
              <h3 className="font-display font-black text-lg uppercase text-[#0D1117]">
                Specialist Allocations
              </h3>
              <span className="text-xs font-display font-bold text-[#64748B] uppercase">
                LangGraph State
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-lg border border-[#0D1117] bg-[#08B0D5]/15">
                <p className="font-display font-black text-[#0D1117]">Research Director</p>
                <p className="text-[10px] text-[#64748B] font-semibold">Meta Muse Wonder</p>
                <span className="text-[10px] text-[#08B0D5] font-bold uppercase mt-1 block">
                  {progress?.agent_status?.["Research Director"] || "Active"}
                </span>
              </div>

              <div className="p-3 rounded-lg border border-[#0D1117] bg-[#FFFFFF]">
                <p className="font-display font-black text-[#0D1117]">Market Analyst</p>
                <p className="text-[10px] text-[#64748B] font-semibold">Meta Spark 1.3</p>
                <span className="text-[10px] text-[#08B0D5] font-bold uppercase mt-1 block">
                  {progress?.agent_status?.["Market Intelligence Analyst"] || "Active"}
                </span>
              </div>

              <div className="p-3 rounded-lg border border-[#0D1117] bg-[#FFFFFF]">
                <p className="font-display font-black text-[#0D1117]">Competitor Analyst</p>
                <p className="text-[10px] text-[#64748B] font-semibold">Meta Spark 1.3</p>
                <span className="text-[10px] text-[#08B0D5] font-bold uppercase mt-1 block">
                  {progress?.agent_status?.["Competitor Intelligence Analyst"] || "Active"}
                </span>
              </div>

              <div className="p-3 rounded-lg border border-[#0D1117] bg-[#FFFFFF]">
                <p className="font-display font-black text-[#0D1117]">Customer Analyst</p>
                <p className="text-[10px] text-[#64748B] font-semibold">Meta Spark 1.3</p>
                <span className="text-[10px] text-[#08B0D5] font-bold uppercase mt-1 block">
                  {progress?.agent_status?.["Customer Intelligence Analyst"] || "Active"}
                </span>
              </div>
            </div>
          </div>

          {/* Report Preview if completed */}
          {progress?.final_report ? (
            <div className="card-market p-6 rounded-2xl bg-[#FFFFFF] space-y-4 border-3 border-[#0D1117]">
              <div className="flex items-center justify-between border-b-2 border-[#0D1117] pb-3">
                <span className="text-xs font-display font-black text-[#08B0D5] uppercase">
                  EXECUTIVE SYNTHESIS READY
                </span>
                <Link
                  href={`/app/reports/${researchId}`}
                  className="text-xs font-display font-bold text-[#08B0D5] hover:underline"
                >
                  Open Full Canvas →
                </Link>
              </div>

              <div className="p-4 rounded-xl bg-[#F4F8FA] border border-[#0D1117] max-h-60 overflow-y-auto text-xs prose leading-relaxed">
                <ReactMarkdown>
                  {typeof progress.final_report === "string"
                    ? progress.final_report
                    : progress.final_report?.executive_summary ||
                      progress.final_report?.markdown_report ||
                      JSON.stringify(progress.final_report, null, 2)}
                </ReactMarkdown>
              </div>
            </div>
          ) : (
            <div className="p-8 rounded-2xl border-2 border-dashed border-[#0D1117] text-center space-y-3">
              <Clock className="w-8 h-8 text-[#64748B] animate-pulse mx-auto" />
              <h4 className="font-display font-black text-sm uppercase text-[#0D1117]">
                Synthesis In Progress
              </h4>
              <p className="text-xs text-[#64748B] max-w-sm mx-auto">
                Once specialist agents extract all evidence and cross-examine claims, the Director will author the executive report here.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
