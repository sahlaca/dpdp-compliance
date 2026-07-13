import { useEffect, useState } from "react";
import {
  downloadReport,
  fetchQuestionnaire,
  fetchSources,
  generateReport,
} from "./api";
import type { AuthUser } from "./auth";
import { clearAuth, welcomeDisplayName } from "./auth";
import { LegalSourcesPanel } from "./LegalSourcesPanel";
import { QuestionnaireForm, type Answers } from "./QuestionnaireForm";
import { ReportHistory } from "./ReportHistory";
import { ReportView } from "./ReportView";
import {
  APP_DISCLAIMER,
  APP_FEATURES,
  APP_TAGLINE,
  APP_BRAND_TITLE,
  AROHA_LOGO_URL,
  DPDP_FULL_NAME,
  OVERVIEW_SUBTITLE,
  OVERVIEW_TITLE,
} from "./appContent";
import type { GapReport, LegalSource, QuestionnaireResponse } from "./types";

type Tab = "overview" | "assessment" | "sources" | "report" | "history";

export function MainApp({ user, onLogout }: { user: AuthUser; onLogout: () => void }) {
  const [tab, setTab] = useState<Tab>("overview");
  const [questionnaire, setQuestionnaire] = useState<QuestionnaireResponse | null>(null);
  const [legalSources, setLegalSources] = useState<LegalSource[]>([]);
  const [companyName, setCompanyName] = useState(user.company_name ?? "");
  const [sector, setSector] = useState("hospitality");
  const [answers, setAnswers] = useState<Answers>({});
  const [report, setReport] = useState<GapReport | null>(null);
  const [formKey, setFormKey] = useState(0);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([fetchQuestionnaire(), fetchSources()])
      .then(([q, catalog]) => {
        setQuestionnaire(q);
        setLegalSources(catalog.sources);
        setSector(q.sectors[0]?.value ?? "hospitality");
      })
      .catch((err) => setError(err.message));
  }, []);

  function updateAnswer(questionId: string, val: unknown) {
    setAnswers((prev) => {
      if (val === undefined) {
        const { [questionId]: _removed, ...rest } = prev;
        return rest;
      }
      return { ...prev, [questionId]: val };
    });
  }

  function handleStartOver() {
    setReport(null);
    setAnswers({});
    setFormError(null);
    setFormKey((k) => k + 1);
    setCompanyName(user.company_name ?? "");
    setSector(questionnaire?.sectors[0]?.value ?? "hospitality");
    setTab("assessment");
  }

  const payload = () => ({ company_name: companyName, sector, answers });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setFormError(null);
    try {
      const result = await generateReport(payload());
      setReport(result);
      setTab("report");
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  async function handleDownload() {
    setDownloading(true);
    try {
      const blob = await downloadReport(payload());
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `DPDP_Compliance_Gap_Report_${companyName.replace(/\s+/g, "_")}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Download failed");
    } finally {
      setDownloading(false);
    }
  }

  function handleOpenSavedReport(saved: GapReport) {
    setReport(saved);
    setTab("report");
  }

  function handleLogout() {
    clearAuth();
    onLogout();
  }

  const tabs: { id: Tab; label: string; disabled?: boolean }[] = [
    { id: "overview", label: "Overview" },
    { id: "assessment", label: "Assessment" },
    { id: "sources", label: "Legal sources" },
    { id: "report", label: "Gap report", disabled: !report },
    { id: "history", label: "Report history" },
  ];

  const welcomeName = welcomeDisplayName(user);

  return (
    <div className="app-layout">
      <header className="topbar">
        <div className="topbar-brand">
          <div className="logo-badge">
            <img src={AROHA_LOGO_URL} alt="Aroha" />
          </div>
          <div className="brand-copy">
            <span className="brand-text">{APP_BRAND_TITLE}</span>
            <span className="brand-subtitle">{DPDP_FULL_NAME}</span>
          </div>
        </div>
        <nav className="tab-nav">
          {tabs.map((t) => (
            <button
              key={t.id}
              type="button"
              className={`tab-btn ${tab === t.id ? "active" : ""}`}
              disabled={t.disabled}
              onClick={() => setTab(t.id)}
            >
              {t.label}
            </button>
          ))}
        </nav>
        <div className="topbar-user">
          <span className="user-name">{user.full_name}</span>
          <button type="button" className="btn ghost small" onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </header>

      <main className="main-content wide">
        {error && tab === "overview" && <p className="error-banner">{error}</p>}

        {tab === "overview" && (
          <div className="overview-panel">
            <header className="page-header compact">
              <div>
                <p className="eyebrow">{welcomeName ? `Welcome, ${welcomeName}` : "Welcome"}</p>
                <h1>{OVERVIEW_TITLE}</h1>
                <p className="subtitle">{OVERVIEW_SUBTITLE}</p>
              </div>
              <div className="header-actions">
                <button className="btn" type="button" onClick={() => setTab("assessment")}>
                  Start Assessment →
                </button>
              </div>
            </header>

            <div className="overview-grid">
              <section className="card">
                <h2>How it works</h2>
                <ol className="steps-list">
                  <li>Answer the structured questionnaire about your data practices</li>
                  <li>Receive a personalized DPDP compliance gap report</li>
                  <li>Download a professional PDF for internal sharing</li>
                </ol>
              </section>
              <section className="card">
                <h2>What you get</h2>
                <ul className="steps-list">
                  <li>39 DPDP obligations assessed with regulatory citations</li>
                  <li>Prioritized action plan aligned to Nov 2026 / May 2027 deadlines</li>
                  <li>Reports saved automatically to your account history</li>
                </ul>
              </section>
            </div>

            <section className="overview-about">
              <p className="overview-about-eyebrow">About this tool</p>
              <h2>{DPDP_FULL_NAME}</h2>
              <p className="overview-about-lead">{APP_TAGLINE}</p>
              <ul className="overview-about-features">
                {APP_FEATURES.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              <p className="overview-about-note">{APP_DISCLAIMER}</p>
            </section>
          </div>
        )}

        {tab === "assessment" && questionnaire && (
          <div className="assessment-hub">
            <header className="page-header compact">
              <div>
                <p className="eyebrow">Assessment</p>
                <h1>{OVERVIEW_TITLE}</h1>
                <p className="subtitle">
                  Answer questions about your data practices to receive a compliance gap report with
                  regulatory citations.
                </p>
              </div>
            </header>
            <QuestionnaireForm
              questionnaire={questionnaire}
              companyName={companyName}
              sector={sector}
              answers={answers}
              formKey={formKey}
              loading={loading}
              error={formError}
              onCompanyNameChange={setCompanyName}
              onSectorChange={setSector}
              onAnswerChange={updateAnswer}
              onSubmit={handleSubmit}
            />
          </div>
        )}

        {tab === "sources" && <LegalSourcesPanel sources={legalSources} />}

        {tab === "report" && report && (
          <>
            <div className="report-toolbar">
              <button className="btn ghost small" type="button" onClick={handleStartOver}>
                New Assessment
              </button>
            </div>
            <ReportView report={report} onDownload={handleDownload} downloading={downloading} />
          </>
        )}

        {tab === "history" && <ReportHistory onOpenReport={handleOpenSavedReport} />}
      </main>
    </div>
  );
}
