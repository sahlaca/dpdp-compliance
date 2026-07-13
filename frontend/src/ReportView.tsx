import { useEffect, useState } from "react";
import { renderLegalReportHtml } from "./api";
import type { GapReport } from "./types";

export function ReportView({
  report,
  onDownload,
  downloading,
}: {
  report: GapReport;
  onDownload: () => void;
  downloading: boolean;
}) {
  const [html, setHtml] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setHtml(null);
    setError(null);
    renderLegalReportHtml(report)
      .then(setHtml)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to render report"));
  }, [report]);

  return (
    <div className="legal-report-shell">
      <div className="report-toolbar legal-report-toolbar">
        <button className="btn secondary" onClick={onDownload} disabled={downloading}>
          {downloading ? "Preparing PDF…" : "Download PDF report"}
        </button>
      </div>

      {error && <p className="error-banner">{error}</p>}
      {!html && !error && <p className="section-note">Loading report…</p>}
      {html && (
        <div className="legal-report-embed" dangerouslySetInnerHTML={{ __html: html }} />
      )}
    </div>
  );
}
