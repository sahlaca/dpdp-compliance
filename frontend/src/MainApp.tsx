import { useEffect, useState } from "react";
import {
  downloadReport,
  downloadTechnicalReport,
  fetchQuestionnaire,
  fetchSources,
  fetchTechnicalQuestionnaire,
  generateReport,
  generateTechnicalReport,
} from "./api";
import type { AuthUser } from "./auth";
import { clearAuth, welcomeDisplayName } from "./auth";
import { AssessmentHub, type AssessmentTrack } from "./AssessmentHub";
import { LegalSourcesPanel } from "./LegalSourcesPanel";
import { type Answers } from "./QuestionnaireForm";
import { ReportHistory } from "./ReportHistory";
import { ReportView } from "./ReportView";
import { TechnicalReportView } from "./TechnicalReportView";
import { APP_DISCLAIMER, APP_FEATURES, APP_TAGLINE, APP_BRAND_TITLE, AROHA_LOGO_URL, DPDP_FULL_NAME, OVERVIEW_SUBTITLE, OVERVIEW_TITLE } from "./appContent";
import type { TechnicalAnswers } from "./TechnicalQuestionnaireForm";
import type {
  GapReport,
  LegalSource,
  QuestionnaireResponse,
  SavedReport,
  TechnicalQuestionnaireResponse,
  TechnicalReport,
} from "./types";
import { isTechnicalReport } from "./types";

type Tab = "overview" | "assessment" | "sources" | "report" | "history";

export function MainApp({ user, onLogout }: { user: AuthUser; onLogout: () => void }) {
  const [tab, setTab] = useState<Tab>("overview");
  const [assessmentTrack, setAssessmentTrack] = useState<AssessmentTrack>("legal");
  const [questionnaire, setQuestionnaire] = useState<QuestionnaireResponse | null>(null);
  const [technicalQuestionnaire, setTechnicalQuestionnaire] = useState<TechnicalQuestionnaireResponse | null>(
    null,
  );
  const [legalSources, setLegalSources] = useState<LegalSource[]>([]);
  const [companyName, setCompanyName] = useState(user.company_name ?? "");
  const [sector, setSector] = useState("hospitality");
  const [legalAnswers, setLegalAnswers] = useState<Answers>({});
  const [technicalAnswers, setTechnicalAnswers] = useState<TechnicalAnswers>({});
  const [legalReport, setLegalReport] = useState<GapReport | null>(null);
  const [technicalReport, setTechnicalReport] = useState<TechnicalReport | null>(null);
  const [activeReportType, setActiveReportType] = useState<AssessmentTrack | null>(null);
  const [legalFormKey, setLegalFormKey] = useState(0);
  const [technicalFormKey, setTechnicalFormKey] = useState(0);
  const [legalLoading, setLegalLoading] = useState(false);
  const [technicalLoading, setTechnicalLoading] = useState(false);
  const [legalDownloading, setLegalDownloading] = useState(false);
  const [technicalDownloading, setTechnicalDownloading] = useState(false);
  const [legalError, setLegalError] = useState<string | null>(null);
  const [technicalError, setTechnicalError] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([fetchQuestionnaire(), fetchSources(), fetchTechnicalQuestionnaire()])
      .then(([q, catalog, technicalQ]) => {
        setQuestionnaire(q);
        setTechnicalQuestionnaire(technicalQ);
        setLegalSources(catalog.sources);
        setSector(q.sectors[0]?.value ?? "hospitality");
      })
      .catch((err) => setError(err.message));
  }, []);

  function updateLegalAnswer(questionId: string, val: unknown) {
    setLegalAnswers((prev) => {
      if (val === undefined) {
        const { [questionId]: _removed, ...rest } = prev;
        return rest;
      }
      return { ...prev, [questionId]: val };
    });
  }

  function updateTechnicalAnswer(questionId: string, val: TechnicalAnswers[string]) {
    setTechnicalAnswers((prev) => {
      if (val === undefined) {
        const { [questionId]: _removed, ...rest } = prev;
        return rest;
      }
      return { ...prev, [questionId]: val };
    });
  }

  function handleStartOver() {
    if (activeReportType === "technical") {
      setTechnicalReport(null);
      setTechnicalAnswers({});
      setTechnicalError(null);
      setTechnicalFormKey((k) => k + 1);
      setAssessmentTrack("technical");
    } else {
      setLegalReport(null);
      setLegalAnswers({});
      setLegalError(null);
      setLegalFormKey((k) => k + 1);
      setAssessmentTrack("legal");
    }
    setActiveReportType(null);
    setCompanyName(user.company_name ?? "");
    setSector(questionnaire?.sectors[0]?.value ?? "hospitality");
    setTab("assessment");
  }

  function handleGoToAssessment(track: AssessmentTrack) {
    setAssessmentTrack(track);
    setTab("assessment");
  }

  const legalPayload = () => ({ company_name: companyName, sector, answers: legalAnswers });

  const technicalPayload = () => ({
    company_name: companyName,
    sector,
    answers: Object.fromEntries(
      Object.entries(technicalAnswers).filter(([, v]) => v !== undefined),
    ) as Record<string, string>,
  });

  async function handleLegalSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLegalLoading(true);
    setLegalError(null);
    try {
      const result = await generateReport(legalPayload());
      setLegalReport(result);
      setActiveReportType("legal");
      setTab("report");
    } catch (err) {
      setLegalError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLegalLoading(false);
    }
  }

  async function handleTechnicalSubmit(e: React.FormEvent) {
    e.preventDefault();
    setTechnicalLoading(true);
    setTechnicalError(null);
    try {
      const result = await generateTechnicalReport(technicalPayload());
      setTechnicalReport(result);
      setActiveReportType("technical");
      setTab("report");
    } catch (err) {
      setTechnicalError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setTechnicalLoading(false);
    }
  }

  async function handleLegalDownload() {
    setLegalDownloading(true);
    try {
      const blob = await downloadReport(legalPayload());
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `DPDP_Legal_Gap_Report_${companyName.replace(/\s+/g, "_")}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setLegalError(err instanceof Error ? err.message : "Download failed");
    } finally {
      setLegalDownloading(false);
    }
  }

  async function handleTechnicalDownload() {
    setTechnicalDownloading(true);
    try {
      const blob = await downloadTechnicalReport(technicalPayload());
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `DPDP_Technical_Gap_Report_${companyName.replace(/\s+/g, "_")}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setTechnicalError(err instanceof Error ? err.message : "Download failed");
    } finally {
      setTechnicalDownloading(false);
    }
  }

  function handleOpenSavedReport(report: SavedReport) {
    if (isTechnicalReport(report)) {
      setTechnicalReport(report);
      setActiveReportType("technical");
    } else {
      setLegalReport(report);
      setActiveReportType("legal");
    }
    setTab("report");
  }

  function handleLogout() {
    clearAuth();
    onLogout();
  }

  const hasReport = Boolean(legalReport || technicalReport);

  const tabs: { id: Tab; label: string; disabled?: boolean }[] = [
    { id: "overview", label: "Overview" },
    { id: "assessment", label: "Assessment" },
    { id: "sources", label: "Legal sources" },
    { id: "report", label: "Gap report", disabled: !hasReport },
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
                  <li>Choose legal or technical assessment (or complete both)</li>
                  <li>Answer the structured questionnaire for your chosen track</li>
                  <li>Receive a personalized gap report and download a professional PDF</li>
                </ol>
              </section>
              <section className="card">
                <h2>What you get</h2>
                <ul className="steps-list">
                  <li>Legal: 39 DPDP obligations assessed with regulatory citations</li>
                  <li>Technical: 7-domain infrastructure scorecard with remediation pathway</li>
                  <li>Both reports saved separately to your account history</li>
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
          <AssessmentHub
            track={assessmentTrack}
            onTrackChange={setAssessmentTrack}
            legalQuestionnaire={questionnaire}
            technicalQuestionnaire={technicalQuestionnaire}
            companyName={companyName}
            sector={sector}
            legalAnswers={legalAnswers}
            technicalAnswers={technicalAnswers}
            legalFormKey={legalFormKey}
            technicalFormKey={technicalFormKey}
            legalLoading={legalLoading}
            technicalLoading={technicalLoading}
            legalError={legalError}
            technicalError={technicalError}
            onCompanyNameChange={setCompanyName}
            onSectorChange={setSector}
            onLegalAnswerChange={updateLegalAnswer}
            onTechnicalAnswerChange={updateTechnicalAnswer}
            onLegalSubmit={handleLegalSubmit}
            onTechnicalSubmit={handleTechnicalSubmit}
          />
        )}

        {tab === "sources" && <LegalSourcesPanel sources={legalSources} />}

        {tab === "report" && activeReportType === "legal" && legalReport && (
          <>
            <div className="report-toolbar">
              <button className="btn ghost small" type="button" onClick={handleStartOver}>
                New Legal Assessment
              </button>
              <button
                className="btn ghost small"
                type="button"
                onClick={() => handleGoToAssessment("technical")}
              >
                Go to Technical Assessment
              </button>
            </div>
            <ReportView
              report={legalReport}
              onDownload={handleLegalDownload}
              downloading={legalDownloading}
            />
          </>
        )}

        {tab === "report" && activeReportType === "technical" && technicalReport && (
          <>
            <div className="report-toolbar">
              <button className="btn ghost small" type="button" onClick={handleStartOver}>
                New Technical Assessment
              </button>
              <button
                className="btn ghost small"
                type="button"
                onClick={() => handleGoToAssessment("legal")}
              >
                Go to Legal Assessment
              </button>
            </div>
            <TechnicalReportView
              report={technicalReport}
              onDownload={handleTechnicalDownload}
              downloading={technicalDownloading}
            />
          </>
        )}

        {tab === "history" && <ReportHistory onOpenReport={handleOpenSavedReport} />}
      </main>
    </div>
  );
}
