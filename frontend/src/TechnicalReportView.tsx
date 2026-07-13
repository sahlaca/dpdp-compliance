import { useEffect, useState } from "react";
import { renderTechnicalReportHtml } from "./api";
import type { TechnicalReport } from "./types";

export function TechnicalReportView({
  report,
  onDownload,
  downloading,
}: {
  report: TechnicalReport;
  onDownload: () => void;
  downloading: boolean;
}) {
  const [html, setHtml] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setHtml(null);
    setError(null);
    renderTechnicalReportHtml(report)
      .then(setHtml)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to render report"));
  }, [report]);

  return (
    <div className="technical-report-shell">
      <div className="report-toolbar technical-report-toolbar">
        <button className="btn secondary" onClick={onDownload} disabled={downloading}>
          {downloading ? "Preparing PDF…" : "Download PDF report"}
        </button>
      </div>

      {error && <p className="error-banner">{error}</p>}
      {!html && !error && <p className="section-note">Loading report…</p>}
      {html && (
        <div
          className="technical-report-embed"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      )}
    </div>
  );
}
