import type { AuthUser } from "./auth";
import { authHeaders } from "./auth";
import type {
  GapReport,
  LegalSource,
  QuestionnaireResponse,
  SourcesCatalog,
  TechnicalQuestionnaireResponse,
  TechnicalReport,
} from "./types";

const API_BASE = import.meta.env.VITE_API_URL ?? "";

async function apiFetch(path: string, init: RequestInit = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(init.headers ?? {}),
    },
  });
  if (res.status === 401) {
    throw new Error("Session expired. Please sign in again.");
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = body.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join(", ")
          : `Request failed (${res.status})`;
    throw new Error(message || `Request failed (${res.status})`);
  }
  return res;
}

export async function login(email: string, password: string): Promise<{ access_token: string; user: AuthUser }> {
  const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = body.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join(", ")
          : "Login failed";
    throw new Error(message);
  }
  return res.json();
}

export async function register(payload: {
  email: string;
  password: string;
  full_name: string;
  company_name?: string;
}): Promise<{ access_token: string; user: AuthUser }> {
  const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = body.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join(", ")
          : "Registration failed";
    throw new Error(message);
  }
  return res.json();
}

export async function fetchQuestionnaire(): Promise<QuestionnaireResponse> {
  const res = await apiFetch("/api/v1/questionnaire");
  return res.json();
}

export async function fetchSources(): Promise<SourcesCatalog> {
  const res = await apiFetch("/api/v1/sources");
  return res.json();
}

export function sourceDownloadUrl(sourceId: string): string {
  return `${API_BASE}/api/v1/sources/${sourceId}/download`;
}

export async function generateReport(payload: {
  company_name: string;
  sector: string;
  answers: Record<string, unknown>;
}): Promise<GapReport> {
  const res = await apiFetch("/api/v1/reports/generate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function downloadReport(payload: {
  company_name: string;
  sector: string;
  answers: Record<string, unknown>;
}): Promise<Blob> {
  const res = await apiFetch("/api/v1/reports/download", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return res.blob();
}

export async function renderLegalReportHtml(report: GapReport): Promise<string> {
  const res = await apiFetch("/api/v1/reports/render-html", {
    method: "POST",
    body: JSON.stringify(report),
  });
  return res.text();
}

export interface ReportHistoryItem {
  id: number;
  company_name: string;
  sector: string;
  assessment_type: "legal" | "technical";
  generated_at: string;
  summary: GapReport["summary"] | TechnicalReport["summary"];
}

export async function fetchReportHistory(): Promise<ReportHistoryItem[]> {
  const res = await apiFetch("/api/v1/auth/reports");
  return res.json();
}

export async function fetchSavedReport(id: number): Promise<GapReport | TechnicalReport> {
  const res = await apiFetch(`/api/v1/auth/reports/${id}`);
  return res.json();
}

export async function fetchTechnicalQuestionnaire(): Promise<TechnicalQuestionnaireResponse> {
  const res = await apiFetch("/api/v1/technical/questionnaire");
  return res.json();
}

export async function generateTechnicalReport(payload: {
  company_name: string;
  sector: string;
  answers: Record<string, string>;
}): Promise<TechnicalReport> {
  const res = await apiFetch("/api/v1/technical/reports/generate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function downloadTechnicalReport(payload: {
  company_name: string;
  sector: string;
  answers: Record<string, string>;
}): Promise<Blob> {
  const res = await apiFetch("/api/v1/technical/reports/download", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return res.blob();
}

export async function renderTechnicalReportHtml(report: TechnicalReport): Promise<string> {
  const res = await apiFetch("/api/v1/technical/reports/render-html", {
    method: "POST",
    body: JSON.stringify(report),
  });
  return res.text();
}

export type { LegalSource };
