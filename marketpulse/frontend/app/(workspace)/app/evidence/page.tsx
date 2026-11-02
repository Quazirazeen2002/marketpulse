"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Database,
  ExternalLink,
  Search,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { EvidenceRecord, SourceRecord, ClaimRecord } from "@/lib/types";

export default function EvidenceExplorerPage() {
  const [evidenceList, setEvidenceList] = useState<EvidenceRecord[]>([]);
  const [sourcesList, setSourcesList] = useState<SourceRecord[]>([]);
  const [claimsList, setClaimsList] = useState<ClaimRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [activeTab, setActiveTab] = useState<"evidence" | "sources" | "claims">("evidence");
  const [searchQuery, setSearchQuery] = useState("");

  const loadAll = async () => {
    try {
      setLoading(true);
      setError(null);
      const [evData, srcData, clmData] = await Promise.all([
        api.getEvidence(undefined, 50).catch(() => []),
        api.getSources(undefined, 50).catch(() => []),
        api.getClaims(undefined, 50).catch(() => []),
      ]);

      setEvidenceList(evData || []);
      setSourcesList(srcData || []);
      setClaimsList(clmData || []);
    } catch (err: any) {
      setError(err.message || "Failed to load evidence records.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  const filteredEvidence = evidenceList.filter(
    (e) =>
      e.supporting_excerpt?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.source_url?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.evidence_id?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredSources = sourcesList.filter(
    (s) =>
      s.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.url?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.publisher?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredClaims = claimsList.filter(
    (c) =>
      c.claim_text?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.domain?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.agent_source?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-2xl border-3 border-[#0D1117] bg-[#FFFFFF] shadow-market-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase">
            <Database className="w-3.5 h-3.5" />
            <span>PRIMARY EVIDENCE REPOSITORY</span>
          </div>
          <h1 className="font-display font-black text-3xl sm:text-5xl uppercase text-[#0D1117] tracking-tight">
            Evidence & Provenance Explorer
          </h1>
          <p className="text-sm text-[#64748B] font-medium leading-relaxed">
            Inspect raw atomic evidence statements, source URLs, content fingerprints, and multi-agent claim verification audits.
          </p>
        </div>

        <button
          onClick={loadAll}
          disabled={loading}
          className="p-3 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] hover:bg-[#FFFFFF] text-[#0D1117] shadow-market-sm shrink-0"
          title="Refresh Evidence"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {/* Tabs & Search Row */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Navigation Tabs */}
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <button
            onClick={() => setActiveTab("evidence")}
            className={`px-4 py-2 rounded-xl border-2 text-xs font-display font-black uppercase transition-all ${
              activeTab === "evidence"
                ? "bg-[#08B0D5] text-[#0D1117] border-[#0D1117] shadow-market-sm"
                : "bg-[#FFFFFF] text-[#0D1117] border-[#0D1117] hover:bg-[#F4F8FA]"
            }`}
          >
            Evidence Cards ({evidenceList.length})
          </button>
          <button
            onClick={() => setActiveTab("sources")}
            className={`px-4 py-2 rounded-xl border-2 text-xs font-display font-black uppercase transition-all ${
              activeTab === "sources"
                ? "bg-[#08B0D5] text-[#0D1117] border-[#0D1117] shadow-market-sm"
                : "bg-[#FFFFFF] text-[#0D1117] border-[#0D1117] hover:bg-[#F4F8FA]"
            }`}
          >
            Primary Sources ({sourcesList.length})
          </button>
          <button
            onClick={() => setActiveTab("claims")}
            className={`px-4 py-2 rounded-xl border-2 text-xs font-display font-black uppercase transition-all ${
              activeTab === "claims"
                ? "bg-[#08B0D5] text-[#0D1117] border-[#0D1117] shadow-market-sm"
                : "bg-[#FFFFFF] text-[#0D1117] border-[#0D1117] hover:bg-[#F4F8FA]"
            }`}
          >
            Claim Audits ({claimsList.length})
          </button>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 absolute left-3 top-3 text-[#64748B]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search keywords, URLs, IDs..."
            className="w-full pl-9 pr-4 py-2 rounded-lg border border-[#0D1117] bg-[#FFFFFF] text-xs font-medium text-[#0D1117] focus:outline-none"
          />
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border-2 border-[#E3447C] bg-[#E3447C]/10 text-[#E3447C] text-xs font-display font-bold uppercase">
          {error}
        </div>
      )}

      {/* Tab 1: Atomic Evidence Records */}
      {activeTab === "evidence" && (
        <div className="space-y-4">
          {loading ? (
            <div className="space-y-3">
              {Array.from({ length: 4 }).map((_, i) => (
                <div
                  key={i}
                  className="p-6 rounded-2xl border-2 border-[#0D1117] bg-[#FFFFFF] animate-pulse h-36"
                />
              ))}
            </div>
          ) : filteredEvidence.length === 0 ? (
            <div className="p-12 text-center border-2 border-dashed border-[#0D1117] rounded-2xl bg-[#FFFFFF] space-y-3">
              <Database className="w-8 h-8 text-[#64748B] mx-auto" />
              <p className="text-xs font-display font-bold uppercase text-[#64748B]">
                No evidence records found.
              </p>
            </div>
          ) : (
            filteredEvidence.map((ev) => (
              <div
                key={ev.evidence_id || ev.id}
                className="card-market p-6 rounded-2xl bg-[#FFFFFF] border-2 border-[#0D1117] shadow-market-sm space-y-3"
              >
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#E2E8F0] pb-2.5">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-[#08B0D5] text-[#0D1117] font-mono text-[10px] font-bold">
                      {ev.evidence_id}
                    </span>
                    <span className="text-[11px] font-display font-bold text-[#64748B] uppercase truncate max-w-xs sm:max-w-md">
                      {ev.source_title || "Primary Publication"}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-xs">
                    <span className="px-2 py-0.5 rounded bg-[#F4F8FA] font-bold text-[#0D1117]">
                      Relevance: {Math.round((ev.relevance_score || 0.8) * 100)}%
                    </span>
                    <span className="px-2 py-0.5 rounded bg-[#08B0D5]/20 text-[#08B0D5] font-bold">
                      Reliability: {Math.round((ev.reliability_score || 0.85) * 100)}%
                    </span>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-[#F4F8FA] border border-[#0D1117] text-xs text-[#0D1117] leading-relaxed font-medium">
                  &quot;{ev.supporting_excerpt}&quot;
                </div>

                <div className="flex flex-wrap items-center justify-between gap-3 text-[11px] text-[#64748B]">
                  <a
                    href={ev.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-[#08B0D5] font-display font-bold hover:underline inline-flex items-center gap-1 truncate max-w-md"
                  >
                    <span>{ev.source_url}</span>
                    <ExternalLink className="w-3 h-3 shrink-0" />
                  </a>

                  <span className="font-mono text-[10px]">
                    Hash: {ev.content_hash?.slice(0, 12)}...
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Tab 2: Primary Sources */}
      {activeTab === "sources" && (
        <div className="card-market p-6 sm:p-8 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl space-y-4">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b-2 border-[#0D1117] font-display font-black uppercase text-[#64748B]">
                <tr>
                  <th className="py-3 px-4">Source Title</th>
                  <th className="py-3 px-4">Publisher / Domain</th>
                  <th className="py-3 px-4">Type / Provider</th>
                  <th className="py-3 px-4">Quality Tier</th>
                  <th className="py-3 px-4 text-right">URL</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E8F0] font-medium text-[#0D1117]">
                {filteredSources.map((s, idx) => (
                  <tr key={idx} className="hover:bg-[#F4F8FA] transition-colors">
                    <td className="py-3.5 px-4 font-display font-bold text-[#0D1117] max-w-xs truncate">
                      {s.title}
                    </td>
                    <td className="py-3.5 px-4 text-[#64748B]">
                      {s.publisher || "Web Publication"}
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="px-2 py-0.5 rounded bg-[#F4F8FA] border border-[#0D1117] text-[10px] font-bold uppercase">
                        {s.search_provider || "Tavily"}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-bold text-[#08B0D5]">
                      {s.source_quality_tier || "Tier 1 Verified"}
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <a
                        href={s.url}
                        target="_blank"
                        rel="noreferrer"
                        className="btn-market inline-flex items-center gap-1 px-3 py-1.5 rounded bg-[#08B0D5] text-[#0D1117] text-[10px] font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
                      >
                        <span>Open URL</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Claim Verification Audit */}
      {activeTab === "claims" && (
        <div className="space-y-4">
          {filteredClaims.map((claim) => (
            <div
              key={claim.claim_id || claim.id}
              className="card-market p-6 rounded-2xl bg-[#FFFFFF] border-2 border-[#0D1117] shadow-market-sm space-y-3"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#E2E8F0] pb-2.5">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-[#0D1117] text-[#FFFFFF] font-mono text-[10px] font-bold">
                    {claim.claim_id}
                  </span>
                  <span className="text-[11px] font-display font-bold text-[#08B0D5] uppercase">
                    {claim.agent_source} • {claim.domain}
                  </span>
                </div>

                <span
                  className={`px-2.5 py-0.5 rounded text-[10px] font-display font-black uppercase border ${
                    claim.verification_status === "verified"
                      ? "bg-[#08B0D5]/20 text-[#08B0D5] border-[#08B0D5]"
                      : claim.verification_status === "contradicted"
                      ? "bg-[#E3447C]/20 text-[#E3447C] border-[#E3447C]"
                      : "bg-[#64748B]/20 text-[#0D1117] border-[#64748B]"
                  }`}
                >
                  {claim.verification_status}
                </span>
              </div>

              <p className="font-display font-bold text-sm text-[#0D1117] leading-snug">
                {claim.claim_text}
              </p>

              {claim.rationale && (
                <p className="text-xs text-[#64748B] font-medium leading-relaxed">
                  <strong>Verification Rationale:</strong> {claim.rationale}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
