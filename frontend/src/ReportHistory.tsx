import { useEffect, useState } from "react";
import { fetchReportHistory, fetchSavedReport, type ReportHistoryItem } from "./api";
import type { SavedReport } from "./types";

function historyStats(item: ReportHistoryItem): string {
  if (item.assessment_type === "technical") {
    const s = item.summary as {
      overall_compliance_pct?: number;
      risk_level?: string;
      questions_answered?: number;
      questions_total?: number;
    };
    return `${s.overall_compliance_pct ?? 0}% compliance · ${s.risk_level ?? "—"} · ${s.questions_answered ?? 0}/${s.questions_total ?? 0} answered`;
  }
  const s = item.summary as {
    gaps_found?: number;
    critical_gaps?: number;
    questions_answered?: number;
    questions_total?: number;
  };
  return `${s.gaps_found ?? 0} gaps · ${s.critical_gaps ?? 0} critical · ${s.questions_answered ?? 0}/${s.questions_total ?? 0} responses recorded`;
}

export function ReportHistory({
  onOpenReport,
}: {
  onOpenReport: (report: SavedReport) => void;
}) {
  const [items, setItems] = useState<ReportHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchReportHistory()
      .then(setItems)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load history"))
      .finally(() => setLoading(false));
  }, []);

  async function openReport(id: number) {
    try {
      const report = await fetchSavedReport(id);
      onOpenReport(report);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load report");
    }
  }

  if (loading) return <p className="section-note">Loading report history…</p>;
  if (error) return <p className="error-banner">{error}</p>;
  if (!items.length) {
    return (
      <div className="empty-state card">
        <h2>No saved reports yet</h2>
        <p className="section-note">
          Complete a legal or technical assessment and generate a gap report. Each report is saved to
          your account automatically.
        </p>
      </div>
    );
  }

  return (
    <div className="history-list">
      {items.map((item) => (
        <article key={item.id} className="card history-item">
          <div>
            <div className="history-item-head">
              <h3>{item.company_name}</h3>
              <span
                className={`assessment-badge ${item.assessment_type === "technical" ? "technical" : "legal"}`}
              >
                {item.assessment_type === "technical" ? "Technical" : "Legal"}
              </span>
            </div>
            <p className="section-note">
              {item.sector.replace(/_/g, " ")} ·{" "}
              {new Date(item.generated_at).toLocaleString("en-IN", {
                timeZone: "Asia/Kolkata",
                dateStyle: "medium",
                timeStyle: "short",
              })}{" "}
              IST
            </p>
            <p className="history-stats">{historyStats(item)}</p>
          </div>
          <button className="btn secondary small" type="button" onClick={() => openReport(item.id)}>
            View report
          </button>
        </article>
      ))}
    </div>
  );
}
