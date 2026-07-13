export type QuestionType = "text" | "single_choice" | "multi_choice" | "boolean" | "number";

export interface QuestionOption {
  value: string;
  label: string;
}

export interface Question {
  id: string;
  section: string;
  prompt: string;
  help_text?: string | null;
  type: QuestionType;
  required: boolean;
  options?: QuestionOption[] | null;
}

export interface QuestionnaireResponse {
  version: string;
  sections: string[];
  sectors: QuestionOption[];
  questions: Question[];
}

export interface LegalSource {
  id: string;
  title: string;
  type: "primary" | "secondary";
  filename: string;
  official_url: string;
  publisher: string;
  description: string;
  effective_date: string;
  gazette_reference?: string | null;
  download_url?: string | null;
  file_available: boolean;
  file_size_bytes?: number | null;
}

export interface SourcesCatalog {
  version: string;
  last_updated: string;
  sources: LegalSource[];
  implementation_phases: Array<{
    phase: string;
    effective_date: string;
    description: string;
  }>;
}

export interface Citation {
  source_id: string;
  chunk_id: string;
  excerpt: string;
  relevance_score: number;
  download_url: string;
}

export interface GapReport {
  generated_at: string;
  assessment_type?: "legal";
  company_name: string;
  sector: string;
  summary: {
    total_obligations: number;
    obligations_assessed?: number;
    gaps_found: number;
    critical_gaps: number;
    questions_total?: number;
    questions_answered?: number;
    questions_not_answered?: number;
    obligations_not_answered?: number;
    obligations_in_scope?: number;
  };
  regulatory_timeline: Array<{
    phase: string;
    effective_date: string;
    description: string;
  }>;
  legal_sources: LegalSource[];
  questionnaire_responses?: Array<{
    id: string;
    section: string;
    prompt: string;
    answered: boolean;
    answer_display: string;
  }>;
  obligations: Array<{
    id: string;
    title: string;
    category: string;
    status: string;
    act_sections: string[];
    rule_references: string[];
    deadline: string;
    priority: number;
    description: string;
    gap_summary: string;
    recommended_action: string;
    source_ids: string[];
    citations: Citation[];
  }>;
  prioritized_action_plan: Array<{
    phase: string;
    deadline?: string;
    items: string[];
  }>;
  disclaimer: string;
  obligation_explainer?: string;
  executive_overview?: string;
  obligation_assessment_intro?: string;
  obligation_relationship_note?: string;
  obligation_field_legend?:
    | {
        title: string;
        items: Array<{ label: string; description: string }>;
      }
    | string[];
}

export type TechnicalAnswer = "yes" | "partial" | "no" | "na";

export interface TechnicalQuestionOption {
  value: TechnicalAnswer;
  label: string;
  points: number | null;
}

export interface TechnicalQuestion {
  id: string;
  domain_id: string;
  domain_name: string;
  code: string;
  prompt: string;
  options: TechnicalQuestionOption[];
}

export interface TechnicalDomain {
  id: string;
  name: string;
  number: number;
  description: string;
}

export interface TechnicalQuestionnaireResponse {
  version: string;
  title: string;
  scoring_criteria: string[];
  domains: TechnicalDomain[];
  questions: TechnicalQuestion[];
}

export interface TechnicalReport {
  generated_at: string;
  assessment_type: "technical";
  report_title: string;
  survey_title: string;
  company_name: string;
  sector: string;
  executive_overview?: string;
  summary: {
    overall_compliance_pct: number;
    total_score: number;
    max_points: number;
    risk_level: string;
    scorecard_note?: string;
    questions_total: number;
    questions_answered: number;
  };
  domains: Array<{
    id: string;
    name: string;
    number: number;
    score: number;
    max_points: number;
    compliance_pct: number;
    status: string;
    service_opportunity: string;
    questions: Array<{
      id: string;
      code: string;
      prompt: string;
      answer: TechnicalAnswer | null;
      answer_label: string;
      points: number | null;
      answered: boolean;
    }>;
  }>;
  questionnaire_responses: Array<{
    id: string;
    code: string;
    domain_id: string;
    prompt: string;
    answer: TechnicalAnswer | null;
    answer_label: string;
    points: number | null;
    answered: boolean;
  }>;
  critical_gaps: Array<{
    id?: string;
    code: string;
    domain: string;
    domain_number?: number;
    title?: string;
    prompt: string;
    gap?: string;
    legal_risk?: string;
    recommended_service?: string;
    service_opportunity?: string;
  }>;
  remediation_pathway: Array<{
    phase: string;
    timeline?: string;
    deadline?: string;
    summary?: string;
    deliverables?: string[];
    items: string[];
  }>;
  disclaimer: string;
}

export type SavedReport = GapReport | TechnicalReport;

export function isTechnicalReport(report: SavedReport): report is TechnicalReport {
  return report.assessment_type === "technical";
}
