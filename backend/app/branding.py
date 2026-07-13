"""Shared Aroha branding assets for reports."""

from __future__ import annotations

import base64
from functools import lru_cache
from html import escape
from pathlib import Path

LOGO_PATH = Path(__file__).resolve().parent / "static" / "aroha_logo.png"
COVER_LOGO_HEIGHT_PX = 52


@lru_cache(maxsize=1)
def logo_data_uri() -> str:
    if not LOGO_PATH.is_file():
        return ""
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def logo_html_img(class_name: str = "cover-logo") -> str:
    uri = logo_data_uri()
    if not uri:
        return ""
    return f'<img src="{uri}" alt="Aroha" class="{class_name}" />'


def cover_logo_block() -> str:
    img = logo_html_img()
    if not img:
        return ""
    return f'<div class="cover-brand">{img}</div>'


def report_cover_styles() -> str:
    return f"""
    .cover {{
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
      color: #fff;
      padding: 2rem 1.75rem;
      border-radius: 8px;
      margin-bottom: 1.75rem;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      line-height: 1.5;
      box-sizing: border-box;
    }}
    .cover *,
    .cover *::before,
    .cover *::after {{
      box-sizing: border-box;
    }}
    .cover-brand {{
      display: inline-block;
      margin-bottom: 1rem;
      line-height: 0;
      background: #fff;
      padding: 8px 12px;
      border-radius: 6px;
    }}
    .cover-logo {{
      height: {COVER_LOGO_HEIGHT_PX}px;
      width: auto;
      max-height: {COVER_LOGO_HEIGHT_PX}px;
      display: block;
      object-fit: contain;
    }}
    .cover-eyebrow {{
      font-size: 9pt;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: #93c5fd;
      margin: 0 0 0.5rem;
      line-height: 1.5;
    }}
    .cover h1 {{
      margin: 0 0 0.35rem;
      font-size: 22pt;
      font-weight: 700;
      border: none;
      color: #fff;
      line-height: 1.2;
      font-family: inherit;
    }}
    .cover-meta {{
      margin: 0;
      font-size: 10pt;
      color: #cbd5e1;
      line-height: 1.5;
    }}
    .cover-meta strong {{ color: #fff; }}
    """


def render_report_cover(
    company: str,
    sector: str,
    generated: str,
    assessment_label: str,
    *,
    include_logo: bool = True,
) -> str:
    logo = cover_logo_block() if include_logo else ""
    return f"""<div class="cover">
    {logo}
    <p class="cover-eyebrow">DPDP Act 2023 · Rules 2025 · {escape(assessment_label)}</p>
    <h1>Compliance Gap Report</h1>
    <p class="cover-meta">
      <strong>{company}</strong><br/>
      Sector: {sector}<br/>
      Generated: {generated}
    </p>
  </div>"""
