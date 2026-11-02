"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  ArrowRight,
  Mail,
  Building,
  CheckCircle2,
  Clock,
  ShieldCheck,
  Zap,
} from "lucide-react";

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);
  const [formState, setFormState] = useState({
    name: "",
    email: "",
    company: "",
    role: "",
    industry: "E-Commerce",
    message: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formState.email || !formState.name) return;
    setSubmitted(true);
  };

  return (
    <div className="w-full bg-[#FFFFFF] text-[#0D1117]">
      {/* Header */}
      <section className="w-full bg-[#0D1117] text-[#FFFFFF] py-20 px-4 sm:px-6 lg:px-8 border-b-3 border-[#0D1117]">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#08B0D5] text-[#0D1117] font-display font-extrabold text-xs uppercase tracking-wider">
            <Mail className="w-4 h-4" />
            <span>ENTERPRISE & GENERAL INQUIRIES</span>
          </div>

          <h1 className="font-display font-black uppercase text-5xl sm:text-7xl lg:text-8xl tracking-tight leading-[0.92]">
            LET&apos;S TALK
            <br />
            <span className="text-[#08B0D5]">INTELLIGENCE.</span>
          </h1>

          <p className="text-lg sm:text-xl text-[#F4F8FA] max-w-3xl leading-relaxed font-medium">
            Interested in deploying MARKETPULSE for your venture fund, corporate strategy team, or research department? Reach out to our engineering and advisory team.
          </p>
        </div>
      </section>

      {/* Main Content & Form */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          {/* Left Column: Direct Info */}
          <div className="lg:col-span-5 space-y-8">
            <div className="space-y-4">
              <span className="text-xs font-display font-black text-[#E3447C] uppercase tracking-wider">
                GET IN TOUCH
              </span>
              <h2 className="font-display font-black text-3xl sm:text-4xl uppercase text-[#0D1117]">
                Deploy MarketPulse for Your Organization
              </h2>
              <p className="text-sm text-[#64748B] font-medium leading-relaxed">
                Whether you need dedicated private Tavily search proxies, custom LangGraph agent configurations, or on-premises deployment support, we&apos;re ready to assist.
              </p>
            </div>

            <div className="space-y-4">
              <div className="p-5 rounded-xl border-2 border-[#0D1117] bg-[#F4F8FA] space-y-2">
                <span className="text-xs font-display font-black text-[#0D1117] uppercase flex items-center gap-2">
                  <Clock className="w-4 h-4 text-[#08B0D5]" />
                  Response SLA
                </span>
                <p className="text-xs text-[#64748B] font-medium">
                  Our strategic engineering team typically responds within 4 business hours.
                </p>
              </div>

              <div className="p-5 rounded-xl border-2 border-[#0D1117] bg-[#FFFFFF] shadow-market-sm space-y-2">
                <span className="text-xs font-display font-black text-[#0D1117] uppercase flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-[#08B0D5]" />
                  Enterprise Data Privacy
                </span>
                <p className="text-xs text-[#64748B] font-medium">
                  We never train on user research questions or proprietary data. Your research runs remain completely isolated.
                </p>
              </div>
            </div>

            <div className="p-6 rounded-2xl bg-[#08B0D5] border-2 border-[#0D1117] text-[#0D1117] space-y-3">
              <span className="font-display font-black text-sm uppercase">
                Ready to explore right now?
              </span>
              <p className="text-xs font-medium leading-relaxed">
                You can immediately access the live application workspace and test all 8 agents on public datasets.
              </p>
              <Link
                href="/app"
                className="btn-market inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-[#0D1117] text-[#FFFFFF] font-display font-extrabold text-xs uppercase shadow-market-sm hover:bg-[#E3447C]"
              >
                <span>Open Instant Workspace</span>
                <ArrowRight className="w-4 h-4 stroke-[3]" />
              </Link>
            </div>
          </div>

          {/* Right Column: Contact Form */}
          <div className="lg:col-span-7">
            <div className="card-market p-8 sm:p-10 rounded-2xl bg-[#FFFFFF] border-3 border-[#0D1117] shadow-market-xl">
              {submitted ? (
                <div className="py-12 text-center space-y-6">
                  <div className="w-16 h-16 rounded-full bg-[#08B0D5]/20 border-2 border-[#08B0D5] text-[#08B0D5] flex items-center justify-center mx-auto">
                    <CheckCircle2 className="w-8 h-8" />
                  </div>
                  <h3 className="font-display font-black text-3xl uppercase text-[#0D1117]">
                    Inquiry Received!
                  </h3>
                  <p className="text-sm text-[#64748B] font-medium max-w-md mx-auto leading-relaxed">
                    Thank you, <span className="font-bold text-[#0D1117]">{formState.name}</span>. A principal solutions architect will contact you at <span className="font-bold text-[#0D1117]">{formState.email}</span> within 4 hours.
                  </p>
                  <button
                    onClick={() => setSubmitted(false)}
                    className="btn-market px-6 py-2.5 rounded-lg bg-[#08B0D5] text-[#0D1117] text-xs font-display font-black uppercase shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
                  >
                    Submit Another Inquiry
                  </button>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="border-b-2 border-[#0D1117] pb-4">
                    <h3 className="font-display font-black text-2xl uppercase text-[#0D1117]">
                      Request a Strategic Consultation
                    </h3>
                    <p className="text-xs text-[#64748B] font-semibold mt-1">
                      Fill out the form below to connect with our team.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                        Full Name *
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Sarah Jenkins"
                        value={formState.name}
                        onChange={(e) =>
                          setFormState({ ...formState, name: e.target.value })
                        }
                        className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                        Work Email *
                      </label>
                      <input
                        type="email"
                        required
                        placeholder="s.jenkins@enterprise.com"
                        value={formState.email}
                        onChange={(e) =>
                          setFormState({ ...formState, email: e.target.value })
                        }
                        className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                        Company / Organization
                      </label>
                      <input
                        type="text"
                        placeholder="e.g. Apex Global Ventures"
                        value={formState.company}
                        onChange={(e) =>
                          setFormState({ ...formState, company: e.target.value })
                        }
                        className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                        Industry Focus
                      </label>
                      <select
                        value={formState.industry}
                        onChange={(e) =>
                          setFormState({ ...formState, industry: e.target.value })
                        }
                        className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-bold focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
                      >
                        <option value="E-Commerce">E-Commerce & Retail</option>
                        <option value="Telecommunications">Telecommunications</option>
                        <option value="Food Delivery">Food Delivery & Logistics</option>
                        <option value="Financial Services">Financial Services & Fintech</option>
                        <option value="Manufacturing">Manufacturing & Supply Chain</option>
                        <option value="Technology">Technology & SaaS</option>
                        <option value="Healthcare">Healthcare & Life Sciences</option>
                        <option value="Other">Other Sector</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-display font-black uppercase text-[#0D1117]">
                      What research challenges are you looking to solve?
                    </label>
                    <textarea
                      rows={4}
                      placeholder="Tell us about the market decisions, competitor gaps, or scenario modeling you need to execute..."
                      value={formState.message}
                      onChange={(e) =>
                        setFormState({ ...formState, message: e.target.value })
                      }
                      className="w-full px-4 py-3 rounded-lg border-2 border-[#0D1117] bg-[#F4F8FA] text-sm text-[#0D1117] font-medium focus:outline-none focus:bg-[#FFFFFF] focus:ring-2 focus:ring-[#08B0D5]"
                    />
                  </div>

                  <button
                    type="submit"
                    className="btn-market w-full py-4 rounded-xl bg-[#08B0D5] text-[#0D1117] font-display font-black text-base uppercase tracking-wider shadow-market-sm hover:bg-[#E3447C] hover:text-[#FFFFFF]"
                  >
                    Send Strategic Inquiry →
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
