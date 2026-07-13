import { sourceDownloadUrl, type LegalSource } from "./api";

function formatBytes(bytes?: number | null): string {
  if (!bytes) return "";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function LegalSourcesSidebar({ sources }: { sources: LegalSource[] }) {
  const primary = sources.filter((s) => s.type === "primary");
  const secondary = sources.filter((s) => s.type === "secondary");

  return (
    <aside className="sidebar">
      <div className="sidebar-inner">
        <h2>Legal sources</h2>
        <p className="sidebar-desc">
          Grounded in official DPDP Act &amp; Rules. Download to verify any citation.
        </p>

        <SourceGroup label="Primary" items={primary} />
        <SourceGroup label="Secondary" items={secondary} />
      </div>
    </aside>
  );
}

function SourceGroup({ label, items }: { label: string; items: LegalSource[] }) {
  if (!items.length) return null;
  return (
    <div className="sidebar-group">
      <h3>{label}</h3>
      {items.map((s) => (
        <div key={s.id} className="sidebar-source">
          <p className="sidebar-source-title">{s.title}</p>
          <p className="sidebar-source-meta">{s.gazette_reference || s.publisher}</p>
          <div className="sidebar-actions">
            {s.file_available && (
              <a className="sidebar-btn primary" href={sourceDownloadUrl(s.id)} download={s.filename}>
                PDF {formatBytes(s.file_size_bytes)}
              </a>
            )}
            <a className="sidebar-btn" href={s.official_url} target="_blank" rel="noopener noreferrer">
              Official ↗
            </a>
          </div>
        </div>
      ))}
    </div>
  );
}
