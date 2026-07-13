"""PDF/HTML export for technical gap assessment reports."""

from __future__ import annotations

from html import escape
from typing import Any

from app.reports.export import _fmt_date, _sector_label
from app.branding import render_report_cover, report_cover_styles


def _bar(pct: int) -> str:
    filled = max(0, min(40, round(pct * 0.4)))
    return "█" * filled + "░" * (40 - filled)


def _status_class(status: str) -> str:
    return {
        "Critical": "status-critical",
        "Warning": "status-warning",
        "Healthy": "status-healthy",
    }.get(status, "")


def _status_display(status: str) -> str:
    icons = {"Critical": "🚨 Critical", "Warning": "⚠️ Warning", "Healthy": "✅ Healthy"}
    return icons.get(status, status)


def _paragraphs(text: str) -> str:
    return "".join(f"<p>{escape(p.strip())}</p>" for p in text.split("\n\n") if p.strip())


def technical_report_styles(for_pdf: bool) -> str:
    page_rules = """
    @page {
      size: A4;
      margin: 1.6cm 1.4cm 2.2cm 1.4cm;
      @bottom-center {
        content: "DPDP Technical Gap Assessment  ·  Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #94a3b8;
      }
    }
    @page :first {
      margin-top: 1.2cm;
    }
    """ if for_pdf else ""
    pdf_only = """
    .page-break { page-break-before: always; }
    .phase-block { page-break-inside: avoid; }
    .response-block { page-break-inside: avoid; }
    """ if for_pdf else ""
    return f"""
    {page_rules}
    {pdf_only}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      color: #0f172a;
      line-height: 1.5;
      font-size: 10pt;
      margin: 0;
      padding: 0;
    }}
    {report_cover_styles()}
    .technical-report-body {{
      font-family: inherit;
      color: inherit;
      font-size: inherit;
      line-height: inherit;
    }}
    h2.section-title {{
      font-size: 12pt;
      color: #1e40af;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 0.35rem;
      margin: 1.35rem 0 0.75rem;
    }}
    .prose {{ font-size: 9.5pt; color: #334155; margin-bottom: 0.75rem; }}
    .prose p {{ margin: 0 0 0.65rem; }}
    .score-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 1.1rem 1.25rem;
      margin-bottom: 1rem;
    }}
    .score-value {{ font-size: 30pt; font-weight: 700; color: #0f172a; line-height: 1; }}
    .score-meta {{ margin: 0.5rem 0 0.15rem; color: #475569; font-size: 9.5pt; }}
    .score-note {{ margin: 0.35rem 0 0.75rem; color: #64748b; font-size: 9pt; }}
    .score-bar {{
      font-family: "Courier New", Courier, monospace;
      font-size: 9pt;
      color: #64748b;
      letter-spacing: 0.5px;
      word-break: break-all;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 0.75rem;
      font-size: 9pt;
    }}
    th, td {{
      border: 1px solid #e2e8f0;
      padding: 0.5rem 0.6rem;
      text-align: left;
      vertical-align: top;
    }}
    th {{ background: #f1f5f9; font-weight: 600; }}
    .status-critical {{ color: #dc2626; font-weight: 600; }}
    .status-warning {{ color: #d97706; font-weight: 600; }}
    .status-healthy {{ color: #16a34a; font-weight: 600; }}
    .gap-item {{
      border: 1px solid #fecaca;
      border-left: 4px solid #dc2626;
      padding: 0.85rem 1rem;
      margin: 0.65rem 0;
      background: #fef2f2;
      border-radius: 6px;
      font-size: 9.5pt;
    }}
    .gap-item h3 {{ margin: 0 0 0.5rem; font-size: 10.5pt; color: #991b1b; }}
    .gap-label {{ font-weight: 700; color: #0f172a; }}
    .gap-text {{ margin: 0.35rem 0 0.65rem; color: #334155; }}
    .phase-block {{
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 0.9rem 1rem;
      margin-bottom: 0.75rem;
      background: #fff;
    }}
    .phase-block h3 {{ margin: 0 0 0.25rem; font-size: 10.5pt; color: #1e3a8a; }}
    .phase-timeline {{ margin: 0 0 0.5rem; font-size: 8.5pt; color: #64748b; font-weight: 600; }}
    .phase-summary {{ margin: 0 0 0.5rem; font-size: 9.5pt; color: #334155; }}
    .phase-block ul {{ margin: 0.35rem 0 0; padding-left: 1.15rem; font-size: 9pt; color: #334155; }}
    .phase-block li {{ margin-bottom: 0.3rem; }}
    .response-block {{
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 0.85rem 1rem;
      margin-bottom: 0.75rem;
    }}
    .response-block h3 {{ margin: 0 0 0.65rem; font-size: 10pt; color: #1e40af; }}
    .response-intro {{
      font-size: 9pt;
      color: #64748b;
      margin: 0 0 0.75rem;
    }}
    .response-accordion summary {{
      cursor: pointer;
      font-size: 10pt;
      font-weight: 600;
      color: #1e40af;
      list-style: none;
      padding: 0.15rem 0;
    }}
    .response-accordion summary::-webkit-details-marker {{ display: none; }}
    .response-accordion summary::before {{
      content: "▸ ";
      color: #64748b;
      font-weight: 700;
    }}
    .response-accordion[open] summary::before {{ content: "▾ "; }}
    .response-accordion .response-body {{ margin-top: 0.65rem; }}
    .response-row {{
      padding: 0.55rem 0;
      border-bottom: 1px solid #f1f5f9;
      font-size: 9pt;
    }}
    .response-row:last-child {{ border-bottom: none; }}
    .response-code {{ font-weight: 700; color: #1e40af; }}
    .response-answer {{ color: #64748b; margin: 0.2rem 0 0; }}
    .disclaimer {{
      font-size: 8.5pt;
      color: #64748b;
      font-style: italic;
      margin-top: 1.25rem;
      border-top: 1px solid #e2e8f0;
      padding-top: 0.75rem;
    }}
    """


def render_technical_report_body(report: dict[str, Any], for_pdf: bool = False) -> str:
    """Shared report body used by web preview and PDF export."""
    company = escape(report.get("company_name", ""))
    sector = escape(_sector_label(report.get("sector", "")))
    generated = escape(_fmt_date(report.get("generated_at", "")))
    summary = report.get("summary", {})
    pct = summary.get("overall_compliance_pct", 0)

    domain_rows = ""
    for d in report.get("domains", []):
        status = d.get("status", "")
        domain_rows += f"""
        <tr>
          <td>{d.get('number', '')}. {escape(d.get('name', ''))}</td>
          <td>{d.get('max_points', 0)}</td>
          <td>{d.get('score', 0)}</td>
          <td>{d.get('compliance_pct', 0)}%</td>
          <td class="{_status_class(status)}">{escape(_status_display(status))}</td>
        </tr>"""

    gaps_html = ""
    for i, g in enumerate(report.get("critical_gaps", []), 1):
        gaps_html += f"""
        <div class="gap-item">
          <h3>{i}. {escape(g.get('title', g.get('code', '')))} ({escape(g.get('domain', ''))})</h3>
          <p class="gap-text"><span class="gap-label">The Gap:</span> {escape(g.get('gap', g.get('prompt', '')))}</p>
          <p class="gap-text"><span class="gap-label">The Legal Risk:</span> {escape(g.get('legal_risk', ''))}</p>
          <p class="gap-text"><span class="gap-label">Recommended Service:</span> {escape(g.get('recommended_service') or g.get('service_opportunity', ''))}</p>
        </div>"""

    plan_html = ""
    for phase in report.get("remediation_pathway", []):
        deliverables = phase.get("deliverables") or phase.get("items") or []
        items = "".join(f"<li>{escape(i)}</li>" for i in deliverables)
        timeline = phase.get("timeline", phase.get("deadline", ""))
        timeline_html = f'<p class="phase-timeline">Timeline: {escape(timeline)}</p>' if timeline else ""
        summary_text = phase.get("summary", "")
        summary_html = f'<p class="phase-summary">{escape(summary_text)}</p>' if summary_text else ""
        list_label = "" if phase.get("phase", "").startswith("Conclusion") else "<p class='gap-label'>Key deliverables:</p>"
        plan_html += f"""
        <div class="phase-block">
          <h3>{escape(phase.get('phase', ''))}</h3>
          {timeline_html}
          {summary_html}
          {list_label}
          <ul>{items}</ul>
        </div>"""

    responses_html = ""
    for d in report.get("domains", []):
        questions = d.get("questions", [])
        answered = sum(1 for q in questions if q.get("answered"))
        rows = ""
        for q in questions:
            rows += f"""
            <div class="response-row">
              <div><span class="response-code">{escape(q.get('code', ''))}</span> {escape(q.get('prompt', ''))}</div>
              <div class="response-answer">{escape(q.get('answer_label', 'Not answered'))}</div>
            </div>"""
        domain_label = f"Domain {d.get('number', '')}: {escape(d.get('name', ''))}"
        meta = f"{len(questions)} questions · {answered} answered"
        if for_pdf:
            responses_html += f"""
        <div class="response-block">
          <h3>{domain_label}</h3>
          {rows}
        </div>"""
        else:
            responses_html += f"""
        <details class="response-block response-accordion">
          <summary>{domain_label} <span style="font-weight:400;color:#64748b">({meta})</span></summary>
          <div class="response-body">{rows}</div>
        </details>"""

    overview = report.get("executive_overview", "")
    remediation_break = '<div class="page-break"></div>' if for_pdf else ""
    questionnaire_break = '<div class="page-break"></div>' if for_pdf else ""
    response_intro = (
        ""
        if for_pdf
        else '<p class="response-intro">Expand each domain below to review individual questionnaire responses.</p>'
    )

    return f"""
  <div class="technical-report-body">
    {render_report_cover(company, sector, generated, "Technical Assessment", include_logo=for_pdf)}

    <h2 class="section-title">1. Executive Overview</h2>
    <div class="prose">{_paragraphs(overview)}</div>

    <h2 class="section-title">2. Compliance Scorecard</h2>
    <div class="score-box">
      <div class="score-value">{pct}%</div>
      <p class="score-meta">
        <strong>Current Compliance Rating:</strong> {pct}% ({escape(summary.get('risk_level', ''))})<br/>
        <strong>Total Score:</strong> {summary.get('total_score', 0)} / {summary.get('max_points', 0)} points collected
        (adjusted based on applicable questions)
      </p>
      <p class="score-note">{escape(summary.get('scorecard_note', ''))}</p>
      <div class="score-bar">[{_bar(pct)}] {pct}%</div>
    </div>

    <h2 class="section-title">Domain Breakdown</h2>
    <table>
      <thead>
        <tr>
          <th>Assessment Domain</th>
          <th>Maximum Points</th>
          <th>Score Achieved</th>
          <th>Compliance %</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>{domain_rows}</tbody>
    </table>

    <h2 class="section-title">3. Critical Risk Exposures</h2>
    {gaps_html or '<p class="score-note">No critical gaps (No responses) identified.</p>'}

    {remediation_break}
    <h2 class="section-title">4. Technical Remediation Pathway</h2>
    <p class="prose"><p>To transition {company} from {escape(summary.get('risk_level', 'current risk'))} toward full compliance, we recommend a phased technical rollout over the next 8 weeks.</p></p>
    {plan_html}

    {questionnaire_break}
    <h2 class="section-title">5. Questionnaire Responses</h2>
    {response_intro}
    {responses_html}

    <p class="disclaimer">{escape(report.get("disclaimer", ""))}</p>
  </div>"""


def render_technical_html_report(report: dict[str, Any], for_pdf: bool = False) -> str:
    body = render_technical_report_body(report, for_pdf=for_pdf)
    styles = technical_report_styles(for_pdf)
    company = escape(report.get("company_name", ""))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"/>
<title>DPDP Compliance Gap Report — {company}</title>
<style>{styles}</style></head><body>{body}</body></html>"""


def render_technical_pdf_report(report: dict[str, Any]) -> bytes:
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise RuntimeError(
            "PDF generation requires weasyprint. Use Docker or: pip install weasyprint"
        ) from exc

    html = render_technical_html_report(report, for_pdf=True)
    return HTML(string=html).write_pdf()
