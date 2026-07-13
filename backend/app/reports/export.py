"""Generate downloadable HTML and PDF compliance reports."""

from __future__ import annotations

from datetime import datetime
from html import escape
from typing import Any
from zoneinfo import ZoneInfo

from app.branding import render_report_cover, report_cover_styles

_STATUS_LABELS = {
    "met": "Met",
    "partial": "Partially Met",
    "not_met": "Not Met",
    "not_answered": "Not Answered",
    "not_applicable": "Not Applicable",
}

_STATUS_COLORS = {
    "met": "#16a34a",
    "partial": "#d97706",
    "not_met": "#dc2626",
    "not_answered": "#64748b",
    "not_applicable": "#64748b",
}

_SECTOR_LABELS = {
    "hospitality": "Hospitality",
    "retail": "Retail & E-commerce",
    "healthcare": "Healthcare",
    "d2c": "D2C / Consumer Brand",
    "food_beverage": "Food & Beverage",
    "travel_tourism": "Travel & Tourism",
    "fintech": "Fintech & Financial Services",
    "insurance": "Insurance",
    "education": "Education & Edtech",
    "real_estate": "Real Estate",
    "logistics": "Logistics & Transport",
    "manufacturing": "Manufacturing",
    "it_saas": "IT, Software & SaaS",
    "professional_services": "Professional Services",
    "media_entertainment": "Media & Entertainment",
    "automotive": "Automotive",
    "telecom": "Telecom",
    "agriculture": "Agriculture & Agritech",
    "nonprofit": "Non-profit / NGO",
    "staffing": "Staffing & HR",
    "beauty_wellness": "Beauty & Wellness",
    "fitness": "Fitness & Sports",
    "other": "Other",
}


def _fmt_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        ist = dt.astimezone(ZoneInfo("Asia/Kolkata"))
        return ist.strftime("%d %B %Y, %I:%M %p IST")
    except (ValueError, TypeError):
        return iso


def _sector_label(sector: str) -> str:
    return _SECTOR_LABELS.get(sector, sector.replace("_", " ").title())


def _paragraphs(text: str) -> str:
    return "".join(f"<p>{escape(p.strip())}</p>" for p in text.split("\n\n") if p.strip())


def _legal_executive_overview(report: dict[str, Any]) -> str:
    overview = report.get("executive_overview", "")
    if overview:
        return overview

    from app.reports.generator import build_legal_executive_overview

    summary = report.get("summary", {})
    return build_legal_executive_overview(
        report.get("company_name", "Your organization"),
        obligations_in_scope=summary.get("obligations_in_scope", summary.get("total_obligations", 0)),
        obligations_assessed=summary.get("obligations_assessed", summary.get("total_obligations", 0)),
        gaps_found=summary.get("gaps_found", 0),
        critical_gaps=summary.get("critical_gaps", 0),
        obligations_pending=summary.get("obligations_not_answered", 0),
    )


def _report_styles(for_pdf: bool) -> str:
    page_rules = """
    @page {
      size: A4;
      margin: 1.6cm 1.4cm 2cm 1.4cm;
      @bottom-center {
        content: "DPDP Compliance Gap Report  ·  Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #94a3b8;
      }
    }
    @page :first {
      margin-top: 1.2cm;
    }
    """ if for_pdf else ""

    web_summary = """
    .summary-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 0.75rem;
    }
    .summary-row .stat {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: auto;
      height: auto;
      min-height: 5.5rem;
      padding: 1rem 0.75rem;
      border: 1px solid #e2e8f0;
    }
    .summary-row .stat-value {
      font-size: 1.75rem;
    }
    .summary-row .stat-label {
      font-size: 0.7rem;
      min-height: auto;
    }
    """ if not for_pdf else ""

    return f"""
    {page_rules}
    {web_summary}
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
    h2.section-title {{
      font-size: 12pt;
      color: #1e40af;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 0.35rem;
      margin: 1.5rem 0 0.75rem;
    }}
    h2.category {{
      font-size: 11pt;
      color: #1e3a8a;
      background: #eff6ff;
      padding: 0.4rem 0.65rem;
      border-radius: 4px;
      margin: 1.25rem 0 0.5rem;
      border: none;
    }}
    .summary-intro {{
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 8px;
      padding: 0.75rem 1rem;
      margin: 0 0 0.75rem;
      font-size: 9pt;
      color: #334155;
      line-height: 1.5;
    }}
    .summary-intro strong {{
      color: #1e40af;
    }}
    .prose {{
      font-size: 9.5pt;
      color: #334155;
      margin: 0 0 0.85rem;
      line-height: 1.55;
    }}
    .prose p {{
      margin: 0 0 0.65rem;
    }}
    .prose p:last-child {{
      margin-bottom: 0;
    }}
    .summary-card {{
      width: 100%;
      margin: 0 0 0.75rem;
      padding: 0;
    }}
    .summary-row {{
      display: table;
      width: 100%;
      table-layout: fixed;
      border-collapse: collapse;
    }}
    .summary-row .stat {{
      display: table-cell;
      background: #f8fafc;
      border: 4px solid #fff;
      border-radius: 8px;
      padding: 0.85rem 0.5rem;
      text-align: center;
      vertical-align: middle;
      width: 33.33%;
      height: 4.25rem;
      box-sizing: border-box;
    }}
    .stat-value {{
      font-size: 20pt;
      font-weight: 700;
      display: block;
      color: #0f172a;
      line-height: 1.15;
      margin-bottom: 0.35rem;
    }}
    .stat-value.critical {{ color: #dc2626; }}
    .stat-label {{
      font-size: 7.5pt;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      display: block;
      line-height: 1.35;
      min-height: 2.1em;
    }}
    .timeline-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 0.5rem;
    }}
    .timeline-table th, .timeline-table td {{
      border: 1px solid #e2e8f0;
      padding: 0.5rem 0.65rem;
      text-align: left;
      font-size: 9pt;
    }}
    .timeline-table th {{
      background: #f1f5f9;
      color: #475569;
      font-weight: 600;
    }}
    .phase-block {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 0.75rem 1rem;
      margin-bottom: 0.75rem;
    }}
    .phase-block h3 {{
      margin: 0 0 0.4rem;
      font-size: 10pt;
      color: #1e40af;
    }}
    .phase-block ul {{
      margin: 0;
      padding-left: 1.1rem;
      font-size: 9.5pt;
    }}
    .phase-block li {{ margin-bottom: 0.25rem; }}
    .question-row {{
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 0.65rem 0.85rem;
      margin-bottom: 0.5rem;
      page-break-inside: avoid;
    }}
    .question-prompt {{
      margin: 0 0 0.35rem;
      font-size: 9.5pt;
      color: #0f172a;
    }}
    .question-answer {{
      margin: 0;
      font-size: 9pt;
    }}
    .obligation {{
      border-left: 4px solid #cbd5e1;
      padding: 0.65rem 0 0.65rem 0.85rem;
      margin: 0.65rem 0;
      page-break-inside: avoid;
    }}
    .ob-row {{
      display: table;
      width: 100%;
      margin-bottom: 0.35rem;
    }}
    .ob-title {{
      display: table-cell;
      font-weight: 600;
      font-size: 10pt;
      vertical-align: top;
      width: 75%;
    }}
    .badge {{
      display: table-cell;
      text-align: right;
      vertical-align: top;
      color: #fff;
      font-size: 7.5pt;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 0.2rem 0.45rem;
      border-radius: 4px;
      white-space: nowrap;
    }}
    .refs {{
      font-size: 8.5pt;
      color: #64748b;
      margin: 0 0 0.35rem;
    }}
    .ob-field {{
      margin: 0.3rem 0;
      font-size: 9.5pt;
      color: #0f172a;
      line-height: 1.45;
    }}
    .ob-field.requirement {{
      color: #64748b;
      font-size: 9pt;
    }}
    .field-legend {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      margin: 0 0 0.85rem;
      font-size: 9pt;
      color: #334155;
      line-height: 1.5;
    }}
    .legend-title {{
      font-weight: 600;
      color: #0f172a;
      margin: 0 0 0.35rem;
    }}
    .legend-list {{
      margin: 0;
      padding-left: 1.15rem;
    }}
    .legend-list li {{
      margin-bottom: 0.2rem;
    }}
    .response-intro {{
      font-size: 9pt;
      color: #64748b;
      margin: 0 0 0.75rem;
    }}
    .question-accordion summary {{
      cursor: pointer;
      font-size: 10pt;
      font-weight: 600;
      color: #1e40af;
      list-style: none;
      padding: 0.15rem 0;
    }}
    .question-accordion summary::-webkit-details-marker {{ display: none; }}
    .question-accordion summary::before {{
      content: "▸ ";
      color: #64748b;
      font-weight: 700;
    }}
    .question-accordion[open] summary::before {{ content: "▾ "; }}
    .question-accordion .question-body {{ margin-top: 0.5rem; }}
    .field-legend p {{
      margin: 0.15rem 0;
    }}
    .field-legend p:first-child {{
      font-weight: 600;
      color: #0f172a;
      margin-bottom: 0.35rem;
    }}
    .obligation p {{ margin: 0.25rem 0; font-size: 9.5pt; }}
    blockquote {{
      margin: 0.4rem 0 0;
      padding: 0.45rem 0.65rem;
      background: #f1f5f9;
      border-left: 3px solid #3b82f6;
      font-size: 8.5pt;
    }}
    blockquote p {{ margin: 0; font-style: italic; color: #334155; }}
    blockquote small {{ color: #64748b; }}
    .sources-list {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .sources-list li {{
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 0.6rem 0.75rem;
      margin-bottom: 0.5rem;
      font-size: 9pt;
      page-break-inside: avoid;
    }}
    .disclaimer {{
      font-size: 8.5pt;
      color: #64748b;
      font-style: italic;
      margin-top: 1.5rem;
      padding-top: 0.75rem;
      border-top: 1px solid #e2e8f0;
    }}
    .page-break {{ page-break-before: always; }}
    a {{ color: #1d4ed8; text-decoration: none; }}
    .no-print {{ display: none; }}
    """


def _render_obligation_field_legend(report: dict[str, Any]) -> str:
    legend = report.get("obligation_field_legend")
    if isinstance(legend, dict) and legend.get("items"):
        items_html = "".join(
            f'<li><strong>{escape(item.get("label", ""))}</strong> — {escape(item.get("description", ""))}</li>'
            for item in legend["items"]
        )
        title = escape(legend.get("title", "For each obligation below:"))
        return f'<div class="field-legend"><p class="legend-title">{title}</p><ul class="legend-list">{items_html}</ul></div>'

    lines = legend if isinstance(legend, list) else [
        "For each obligation below:",
        "Requirement — What does the law say?",
        "Assessment — Where do we stand?",
        "Recommended Action — What should we do now?",
    ]
    return '<div class="field-legend">' + "".join(f"<p>{escape(line)}</p>" for line in lines) + "</div>"


def render_legal_report_body(
    report: dict[str, Any],
    base_url: str = "",
    for_pdf: bool = False,
) -> str:
    company = escape(report.get("company_name", ""))
    sector = escape(_sector_label(report.get("sector", "")))
    generated = escape(_fmt_date(report.get("generated_at", "")))
    summary = report.get("summary", {})
    disclaimer = escape(report.get("disclaimer", ""))
    source_titles = {
        s.get("id", ""): s.get("title", s.get("id", "").replace("_", " "))
        for s in report.get("legal_sources", [])
    }

    obligations_html = ""
    current_category = ""
    for ob in report.get("obligations", []):
        if ob.get("status") == "not_applicable":
            continue
        cat = ob.get("category", "")
        if cat != current_category:
            current_category = cat
            obligations_html += f'<h2 class="category">{escape(cat)}</h2>\n'

        status = ob.get("status", "")
        status_label = _STATUS_LABELS.get(status, status)
        color = _STATUS_COLORS.get(status, "#333")

        citations_html = ""
        for c in ob.get("citations", []):
            excerpt = escape(c.get("excerpt", ""))
            source_id = c.get("source_id", "")
            sid = escape(
                source_titles.get(source_id, source_id.replace("_", " "))
            )
            dl = f'{base_url}{c.get("download_url", "")}'
            link = f'<a href="{dl}">Download source PDF</a>' if base_url else sid
            citations_html += f"""
            <blockquote>
              <p>"{excerpt}"</p>
              <small>Source: {sid} — {link}</small>
            </blockquote>"""

        obligations_html += f"""
        <div class="obligation" style="border-left-color:{color}">
          <div class="ob-row">
            <div class="ob-title">{escape(ob.get("title", ""))}</div>
            <div class="badge" style="background:{color}">{status_label}</div>
          </div>
          <p class="refs">{" · ".join(ob.get("act_sections", []))} · {" · ".join(ob.get("rule_references", []))} · Due {escape(ob.get("deadline", ""))}</p>
          <p class="ob-field requirement"><strong>Requirement:</strong> {escape(ob.get("description", ""))}</p>
          <p class="ob-field"><strong>Assessment:</strong> {escape(ob.get("gap_summary", ""))}</p>
          <p class="ob-field"><strong>Recommended Action:</strong> {escape(ob.get("recommended_action", ""))}</p>
          {citations_html}
        </div>"""

    plan_html = ""
    for phase in report.get("prioritized_action_plan", []):
        items = "".join(f"<li>{escape(i)}</li>" for i in phase.get("items", []))
        deadline = phase.get("deadline", "")
        dl_text = f' <span style="color:#64748b;font-weight:400">(by {escape(deadline)})</span>' if deadline else ""
        plan_html += f'<div class="phase-block"><h3>{escape(phase.get("phase", ""))}{dl_text}</h3><ul>{items}</ul></div>'

    questionnaire_html = ""
    sections: dict[str, list[dict[str, Any]]] = {}
    for row in report.get("questionnaire_responses", []):
        section = row.get("section", "")
        sections.setdefault(section, []).append(row)

    for section, rows in sections.items():
        section_rows = ""
        for row in rows:
            answered = row.get("answered", False)
            answer = escape(row.get("answer_display", "Not answered"))
            answer_style = "color:#0f172a" if answered else "color:#64748b;font-style:italic"
            section_rows += f"""
        <div class="question-row">
          <p class="question-prompt">{escape(row.get("prompt", ""))}</p>
          <p class="question-answer" style="{answer_style}"><strong>Response:</strong> {answer}</p>
        </div>"""
        answered_count = sum(1 for r in rows if r.get("answered"))
        meta = f"{len(rows)} questions · {answered_count} answered"
        if for_pdf:
            questionnaire_html += f'<h3 class="category">{escape(section)}</h3>\n{section_rows}'
        else:
            questionnaire_html += f"""
        <details class="question-accordion">
          <summary>{escape(section)} <span style="font-weight:400;color:#64748b">({meta})</span></summary>
          <div class="question-body">{section_rows}</div>
        </details>"""

    sources_html = ""
    for s in report.get("legal_sources", []):
        if not s.get("file_available"):
            continue
        dl = f'{base_url}{s.get("download_url", "")}'
        official = escape(s.get("official_url", ""))
        dl_link = f'<a href="{dl}">Download PDF</a>' if base_url else "See application"
        sources_html += f"""
        <li>
          <strong>{escape(s.get("title", ""))}</strong>
          <span style="color:#64748b"> ({escape(s.get("type", ""))})</span><br/>
          <small style="color:#64748b">{escape(s.get("publisher", ""))}</small><br/>
          {dl_link} · <a href="{official}">Official source</a>
        </li>"""

    timeline_rows = ""
    for t in report.get("regulatory_timeline", []):
        timeline_rows += f"""<tr>
          <td><strong>{escape(t.get("phase", ""))}</strong></td>
          <td>{escape(t.get("effective_date", ""))}</td>
          <td>{escape(t.get("description", ""))}</td>
        </tr>"""

    sources_break = '<div class="page-break"></div>' if for_pdf else ""
    questionnaire_break = '<div class="page-break"></div>' if for_pdf else ""
    obligations_break = '<div class="page-break"></div>' if for_pdf else ""
    response_intro = (
        ""
        if for_pdf
        else '<p class="response-intro">Expand each section below to review your questionnaire responses.</p>'
    )

    return f"""
  <div class="legal-report-body">
  {render_report_cover(company, sector, generated, "Legal Assessment", include_logo=for_pdf)}

  <h2 class="section-title">Executive Summary</h2>
  <div class="prose">{_paragraphs(_legal_executive_overview(report))}</div>
  <div class="summary-card">
    <div class="summary-row">
      <div class="stat">
        <span class="stat-value">{summary.get("obligations_assessed", summary.get("total_obligations", 0))}</span>
        <span class="stat-label">Obligations Assessed</span>
      </div>
      <div class="stat">
        <span class="stat-value">{summary.get("gaps_found", 0)}</span>
        <span class="stat-label">Gaps Identified</span>
      </div>
      <div class="stat">
        <span class="stat-value critical">{summary.get("critical_gaps", 0)}</span>
        <span class="stat-label">Critical Gaps</span>
      </div>
    </div>
  </div>
  <div class="summary-intro">{escape(report.get("obligation_explainer", ""))}</div>

  <h2 class="section-title">Regulatory Timeline</h2>
  <table class="timeline-table">
    <thead><tr><th>Phase</th><th>Date</th><th>Requirement</th></tr></thead>
    <tbody>{timeline_rows}</tbody>
  </table>

  <h2 class="section-title">Prioritized Action Plan</h2>
  {plan_html}

  {sources_break}
  <h2 class="section-title">Legal Source Documents</h2>
  <p style="font-size:9pt;color:#64748b">Primary and secondary sources used to ground this assessment.</p>
  <ul class="sources-list">{sources_html}</ul>

  {questionnaire_break}
  <h2 class="section-title">Questionnaire Responses</h2>
  <p style="font-size:9pt;color:#64748b;margin-bottom:1rem">
    Complete record of your assessment answers for reference. Items without a recorded response are
    marked <em>Not answered</em>.
    ({summary.get("questions_answered", 0)} of {summary.get("questions_total", 0)} responses recorded)
  </p>
  {response_intro}
  {questionnaire_html}

  {obligations_break}
  <h2 class="section-title">Detailed Obligation Assessment</h2>
  <p style="font-size:9pt;color:#64748b;margin-bottom:0.75rem">
    {escape(report.get("obligation_assessment_intro", ""))}
  </p>
  <div class="summary-intro">{escape(report.get("obligation_relationship_note", ""))}</div>
  {_render_obligation_field_legend(report)}
  {obligations_html}

  <p class="disclaimer">{disclaimer}</p>
  </div>"""


def render_html_report(report: dict[str, Any], base_url: str = "", for_pdf: bool = False) -> str:
    body = render_legal_report_body(report, base_url=base_url, for_pdf=for_pdf)
    styles = _report_styles(for_pdf=for_pdf)
    company = escape(report.get("company_name", ""))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>DPDP Compliance Gap Report — {company}</title>
  <style>{styles}</style>
</head>
<body>{body}</body>
</html>"""


def render_pdf_report(report: dict[str, Any], base_url: str = "") -> bytes:
    """Convert the HTML report to a professional PDF."""
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise RuntimeError(
            "PDF generation requires weasyprint. Use Docker or: pip install weasyprint"
        ) from exc

    html = render_html_report(report, base_url=base_url, for_pdf=True)
    return HTML(string=html).write_pdf()
