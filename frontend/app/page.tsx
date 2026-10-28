"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { apiRequest } from "@/lib/api";


// ============================================================
// TYPES
// ============================================================

interface Source {
  id: number;
  url: string;
  title: string | null;
  report_id: number;
}

interface CompanyOverview {
  company: string;
  ticker: string;
  sector: string;
  industry: string;
  headquarters: string;
  core_business: string;
}

interface RecentDevelopment {
  development: string;
  date: string;
  source: string;
  business_relevance: string;
}

interface BusinessSignal {
  signal: string;
  category: string;
  evidence: string;
}

interface PainPoint {
  pain_point: string;
  evidence: string;
  reasoning: string;
}

interface Opportunity {
  opportunity: string;
  evidence: string;
  why_it_matters: string;
  suggested_action: string;
}

interface Risk {
  risk: string;
  evidence: string;
}

interface NextAction {
  action: string;
  reason: string;
}

interface StructuredReport {
  executive_summary: string[];

  company_overview: CompanyOverview;

  recent_developments: RecentDevelopment[];

  business_signals: BusinessSignal[];

  potential_pain_points: PainPoint[];

  potential_opportunities: Opportunity[];

  risks_and_unknowns: Risk[];

  recommended_next_actions: NextAction[];
}

interface ResearchResponse {
  id: number;
  company_name: string;
  report_content: string;
  user_id: number;
  created_at: string;
  sources: Source[];
}


// ============================================================
// MAIN PAGE
// ============================================================

export default function Home() {

  const router = useRouter();

  const [company, setCompany] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [result, setResult] =
    useState<ResearchResponse | null>(
      null
    );

  const [authenticated, setAuthenticated] =
    useState(false);


  // ==========================================================
  // AUTH CHECK
  // ==========================================================

  useEffect(() => {

    const token =
      localStorage.getItem(
        "access_token"
      );

    if (!token) {

      router.push("/login");

      return;
    }

    setAuthenticated(true);

  }, [router]);


  // ==========================================================
  // LOGOUT
  // ==========================================================

  function logout() {

    localStorage.removeItem(
      "access_token"
    );

    router.push("/login");
  }


  // ==========================================================
  // GENERATE RESEARCH
  // ==========================================================

  async function generateResearch() {

    if (!company.trim()) {

      setError(
        "Please enter a company name."
      );

      return;
    }


    try {

      setLoading(true);

      setError("");

      setResult(null);


      const data =
        await apiRequest<ResearchResponse>(
          "/research",
          {
            method: "POST",

            body: JSON.stringify({
              company_name:
                company.trim(),
            }),
          }
        );


      setResult(data);

    } catch (err) {

      const message =
        err instanceof Error
          ? err.message
          : "Research generation failed.";


      if (
        message.includes("token") ||
        message.includes("authentication") ||
        message.includes("credentials")
      ) {

        localStorage.removeItem(
          "access_token"
        );

        router.push("/login");

        return;
      }


      setError(message);

    } finally {

      setLoading(false);
    }
  }


  // ==========================================================
  // PARSE STRUCTURED REPORT
  // ==========================================================

  function parseReport():

    StructuredReport | null {

    if (!result) {
      return null;
    }


    try {

      return JSON.parse(
        result.report_content
      );

    } catch {

      return null;
    }
  }


  const report =
    parseReport();


  // ==========================================================
  // AUTH LOADING
  // ==========================================================

  if (!authenticated) {

    return (

      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-white">

        <div className="text-center">

          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-blue-500" />

          <p className="mt-4 text-sm text-slate-400">
            Checking authentication...
          </p>

        </div>

      </main>
    );
  }


  // ==========================================================
  // DASHBOARD
  // ==========================================================

  return (

    <main className="min-h-screen bg-slate-950 text-white">


      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="border-b border-slate-800 bg-slate-950">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>

            <h1 className="text-xl font-semibold">
              AI Enterprise Research
            </h1>

            <p className="text-sm text-slate-500">
              Research & Action Agent
            </p>

          </div>


          <div className="flex items-center gap-4">

            <div className="hidden items-center gap-2 rounded-full bg-green-500/10 px-3 py-1 text-xs text-green-400 md:flex">

              <span className="h-2 w-2 rounded-full bg-green-400" />

              Agent Online

            </div>


            <button
              onClick={logout}
              className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:border-slate-500 hover:text-white"
            >

              Logout

            </button>

          </div>

        </div>

      </header>


      {/* ======================================================
          CONTENT
      ====================================================== */}

      <section className="mx-auto max-w-7xl px-6 py-12">


        {/* HERO */}

        <div className="max-w-4xl">

          <p className="text-sm font-medium tracking-widest text-blue-400">
            AI-POWERED ENTERPRISE RESEARCH
          </p>


          <h2 className="mt-4 text-4xl font-bold leading-tight md:text-5xl">

            Research any company
            <br />

            <span className="text-slate-500">
              with an AI agent.
            </span>

          </h2>


          <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-400">

            Generate an evidence-backed company
            intelligence brief using company data,
            recent news, and web research.

          </p>

        </div>


        {/* ==================================================
            SEARCH
        ================================================== */}

        <div className="mt-10 max-w-4xl rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <label
            htmlFor="company"
            className="mb-2 block text-sm font-medium"
          >

            Company Name

          </label>


          <div className="flex flex-col gap-3 md:flex-row">

            <input
              id="company"
              type="text"
              value={company}
              disabled={loading}
              onChange={(event) =>
                setCompany(
                  event.target.value
                )
              }
              onKeyDown={(event) => {

                if (
                  event.key === "Enter"
                ) {

                  generateResearch();

                }

              }}
              placeholder="e.g. NVIDIA"
              className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 outline-none placeholder:text-slate-600 focus:border-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            />


            <button
              onClick={generateResearch}
              disabled={loading}
              className="rounded-lg bg-blue-600 px-7 py-3 font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-slate-700"
            >

              {loading
                ? "Researching..."
                : "Generate Brief"}

            </button>

          </div>


          {error && (

            <div className="mt-4 rounded-lg border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">

              {error}

            </div>

          )}

        </div>


        {/* ==================================================
            LOADING
        ================================================== */}

        {loading && (

          <div className="mt-8 max-w-4xl rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <div className="flex items-center gap-4">

              <div className="h-6 w-6 animate-spin rounded-full border-2 border-slate-700 border-t-blue-500" />

              <div>

                <p className="font-medium">
                  AI agent is researching...
                </p>

                <p className="mt-1 text-sm text-slate-400">

                  Collecting company data,
                  recent news and web evidence.

                </p>

              </div>

            </div>

          </div>

        )}


        {/* ==================================================
            REPORT
        ================================================== */}

        {result && report && (

          <div className="mt-10 max-w-6xl space-y-6">


            {/* REPORT HEADER */}

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

              <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">

                <div>

                  <p className="text-xs font-medium tracking-widest text-blue-400">
                    RESEARCH REPORT
                  </p>

                  <h2 className="mt-2 text-3xl font-bold">
                    {result.company_name}
                  </h2>

                </div>


                <div className="text-sm text-slate-500">

                  Report #{result.id}

                </div>

              </div>

            </div>


            {/* =================================================
                EXECUTIVE SUMMARY
            ================================================= */}

            <ReportSection
              title="Executive Summary"
            >

              <div className="space-y-3">

                {report.executive_summary?.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="flex gap-3"
                    >

                      <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-blue-500" />

                      <p className="leading-7 text-slate-300">
                        {item}
                      </p>

                    </div>

                  )
                )}

              </div>

            </ReportSection>


            {/* =================================================
                COMPANY OVERVIEW
            ================================================= */}

            <ReportSection
              title="Company Overview"
            >

              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">

                <InfoCard
                  label="Company"
                  value={
                    report.company_overview?.company
                  }
                />

                <InfoCard
                  label="Ticker"
                  value={
                    report.company_overview?.ticker
                  }
                />

                <InfoCard
                  label="Sector"
                  value={
                    report.company_overview?.sector
                  }
                />

                <InfoCard
                  label="Industry"
                  value={
                    report.company_overview?.industry
                  }
                />

                <InfoCard
                  label="Headquarters"
                  value={
                    report.company_overview?.headquarters
                  }
                />

                <InfoCard
                  label="Core Business"
                  value={
                    report.company_overview?.core_business
                  }
                />

              </div>

            </ReportSection>


            {/* =================================================
                RECENT DEVELOPMENTS
            ================================================= */}

            <ReportSection
              title="Recent Developments"
            >

              {report.recent_developments?.length ? (

                <div className="space-y-4">

                  {report.recent_developments.map(
                    (item, index) => (

                      <div
                        key={index}
                        className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                      >

                        <div className="flex flex-col justify-between gap-2 md:flex-row">

                          <h4 className="font-semibold">
                            {item.development}
                          </h4>

                          <span className="text-sm text-slate-500">
                            {item.date}
                          </span>

                        </div>

                        <p className="mt-3 text-sm leading-6 text-slate-400">
                          {item.business_relevance}
                        </p>

                        <p className="mt-3 text-xs text-blue-400">
                          Source: {item.source}
                        </p>

                      </div>

                    )
                  )}

                </div>

              ) : (

                <EmptyState />

              )}

            </ReportSection>


            {/* =================================================
                BUSINESS SIGNALS
            ================================================= */}

            <ReportSection
              title="Business Signals"
            >

              <div className="grid gap-4 md:grid-cols-2">

                {report.business_signals?.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                    >

                      <div className="flex items-center justify-between gap-3">

                        <h4 className="font-semibold">
                          {item.signal}
                        </h4>

                        <span className="rounded-full bg-blue-500/10 px-2 py-1 text-xs text-blue-400">
                          {item.category}
                        </span>

                      </div>

                      <p className="mt-3 text-sm leading-6 text-slate-400">
                        {item.evidence}
                      </p>

                    </div>

                  )
                )}

              </div>

            </ReportSection>


            {/* =================================================
                PAIN POINTS
            ================================================= */}

            <ReportSection
              title="Potential Customer Pain Points"
            >

              <div className="space-y-4">

                {report.potential_pain_points?.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                    >

                      <h4 className="font-semibold">
                        {item.pain_point}
                      </h4>

                      <p className="mt-3 text-sm leading-6 text-slate-400">

                        <span className="font-medium text-slate-300">
                          Evidence:
                        </span>{" "}

                        {item.evidence}

                      </p>

                      <p className="mt-3 text-sm leading-6 text-slate-500">

                        {item.reasoning}

                      </p>

                    </div>

                  )
                )}

              </div>

            </ReportSection>


            {/* =================================================
                OPPORTUNITIES
            ================================================= */}

            <ReportSection
              title="Potential Opportunities"
            >

              <div className="grid gap-4 md:grid-cols-2">

                {report.potential_opportunities?.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                    >

                      <h4 className="text-lg font-semibold">
                        {item.opportunity}
                      </h4>


                      <div className="mt-4 space-y-3">

                        <p className="text-sm leading-6 text-slate-400">

                          <span className="font-medium text-slate-300">
                            Evidence:
                          </span>{" "}

                          {item.evidence}

                        </p>


                        <p className="text-sm leading-6 text-slate-400">

                          <span className="font-medium text-slate-300">
                            Why it matters:
                          </span>{" "}

                          {item.why_it_matters}

                        </p>


                        <div className="rounded-lg bg-blue-500/5 p-4">

                          <p className="text-xs font-medium uppercase tracking-wide text-blue-400">
                            Suggested Action
                          </p>

                          <p className="mt-2 text-sm leading-6 text-slate-300">

                            {item.suggested_action}

                          </p>

                        </div>

                      </div>

                    </div>

                  )
                )}

              </div>

            </ReportSection>


            {/* =================================================
                RISKS
            ================================================= */}

            <ReportSection
              title="Risks & Unknowns"
            >

              <div className="space-y-3">

                {report.risks_and_unknowns?.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                    >

                      <h4 className="font-semibold">
                        {item.risk}
                      </h4>

                      <p className="mt-2 text-sm leading-6 text-slate-400">
                        {item.evidence}
                      </p>

                    </div>

                  )
                )}

              </div>

            </ReportSection>


            {/* =================================================
                NEXT ACTIONS
            ================================================= */}

            <ReportSection
              title="Recommended Next Actions"
            >

              <div className="space-y-3">

                {report.recommended_next_actions?.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="flex gap-4 rounded-xl border border-slate-800 bg-slate-950 p-5"
                    >

                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-500/10 text-sm font-semibold text-blue-400">

                        {index + 1}

                      </div>


                      <div>

                        <h4 className="font-semibold">
                          {item.action}
                        </h4>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                          {item.reason}
                        </p>

                      </div>

                    </div>

                  )
                )}

              </div>

            </ReportSection>


            {/* =================================================
                SOURCES
            ================================================= */}

            <ReportSection
              title="Sources"
            >

              {result.sources?.length ? (

                <div className="space-y-3">

                  {result.sources.map(
                    (source) => (

                      <a
                        key={source.id}
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block rounded-xl border border-slate-800 bg-slate-950 p-4 transition hover:border-blue-500"
                      >

                        <p className="font-medium text-blue-400">

                          {source.title ||
                            "Source"}

                        </p>

                        <p className="mt-2 break-all text-xs text-slate-500">

                          {source.url}

                        </p>

                      </a>

                    )
                  )}

                </div>

              ) : (

                <EmptyState />

              )}

            </ReportSection>


            {/* =================================================
                METADATA
            ================================================= */}

            <div className="pb-10 text-xs text-slate-600">

              Generated:
              {" "}
              {new Date(
                result.created_at
              ).toLocaleString()}

              {" • "}

              User ID:
              {" "}
              {result.user_id}

            </div>

          </div>

        )}


        {/* ==================================================
            CAPABILITY CARDS
        ================================================== */}

        {!result && (

          <div className="mt-16 grid gap-4 md:grid-cols-4">

            <Feature
              title="Company Data"
              description="Company fundamentals and business information."
            />

            <Feature
              title="News"
              description="Recent developments and announcements."
            />

            <Feature
              title="Web Research"
              description="Broader industry and competitive signals."
            />

            <Feature
              title="AI Analysis"
              description="Evidence-backed research brief generated by Groq."
            />

          </div>

        )}

      </section>

    </main>
  );
}


// ============================================================
// REPORT SECTION
// ============================================================

function ReportSection({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {

  return (

    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

      <h3 className="mb-6 text-xl font-semibold">
        {title}
      </h3>

      {children}

    </section>

  );
}


// ============================================================
// INFO CARD
// ============================================================

function InfoCard({
  label,
  value,
}: {
  label: string;
  value?: string;
}) {

  return (

    <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">

      <p className="text-xs uppercase tracking-wide text-slate-500">
        {label}
      </p>

      <p className="mt-2 font-medium text-slate-200">
        {value || "Unknown"}
      </p>

    </div>

  );
}


// ============================================================
// FEATURE
// ============================================================

function Feature({
  title,
  description,
}: {
  title: string;
  description: string;
}) {

  return (

    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">

      <h3 className="font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-400">
        {description}
      </p>

    </div>

  );
}


// ============================================================
// EMPTY STATE
// ============================================================

function EmptyState() {

  return (

    <p className="text-sm text-slate-500">
      No information available from the collected evidence.
    </p>

  );
}