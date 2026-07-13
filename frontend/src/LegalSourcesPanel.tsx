import { sourceDownloadUrl, type LegalSource } from "./api";

function formatBytes(bytes?: number | null): string {
  if (!bytes) return "";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function LegalSourcesPanel({ sources }: { sources: LegalSource[] }) {
  const primary = sources.filter((s) => s.type === "primary");
  const secondary = sources.filter((s) => s.type === "secondary");

  return (
    <div className="sources-panel">
      <p className="section-note">
        Grounded in official DPDP Act and Rules documents. Download any source to verify
        citations in your report.
      </p>
      <SourceGroup label="Primary sources" items={primary} />
      <SourceGroup label="Secondary references" items={secondary} />
    </div>
  );
}

function SourceGroup({ label, items }: { label: string; items: LegalSource[] }) {
  if (!items.length) return null;
  return (
    <div className="sources-group">
      <h3>{label}</h3>
      <div className="sources-grid">
        {items.map((s) => (
          <article key={s.id} className="source-card">
            <h4>{s.title}</h4>
            <p className="source-meta">{s.gazette_reference || s.publisher}</p>
            <p className="source-desc">{s.description}</p>
            <div className="source-actions">
              {s.file_available && (
                <a className="btn secondary small" href={sourceDownloadUrl(s.id)} download={s.filename}>
                  Download PDF {formatBytes(s.file_size_bytes)}
                </a>
              )}
              <a className="btn ghost small" href={s.official_url} target="_blank" rel="noopener noreferrer">
                Official source ↗
              </a>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
