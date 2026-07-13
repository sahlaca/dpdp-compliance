import { QuestionnaireForm, type Answers } from "./QuestionnaireForm";
import {
  TechnicalQuestionnaireForm,
  type TechnicalAnswers,
} from "./TechnicalQuestionnaireForm";
import type { QuestionnaireResponse, TechnicalQuestionnaireResponse } from "./types";

export type AssessmentTrack = "legal" | "technical";

export function AssessmentHub({
  track,
  onTrackChange,
  legalQuestionnaire,
  technicalQuestionnaire,
  companyName,
  sector,
  legalAnswers,
  technicalAnswers,
  legalFormKey,
  technicalFormKey,
  legalLoading,
  technicalLoading,
  legalError,
  technicalError,
  onCompanyNameChange,
  onSectorChange,
  onLegalAnswerChange,
  onTechnicalAnswerChange,
  onLegalSubmit,
  onTechnicalSubmit,
}: {
  track: AssessmentTrack;
  onTrackChange: (track: AssessmentTrack) => void;
  legalQuestionnaire: QuestionnaireResponse;
  technicalQuestionnaire: TechnicalQuestionnaireResponse | null;
  companyName: string;
  sector: string;
  legalAnswers: Answers;
  technicalAnswers: TechnicalAnswers;
  legalFormKey: number;
  technicalFormKey: number;
  legalLoading: boolean;
  technicalLoading: boolean;
  legalError: string | null;
  technicalError: string | null;
  onCompanyNameChange: (v: string) => void;
  onSectorChange: (v: string) => void;
  onLegalAnswerChange: (questionId: string, val: unknown) => void;
  onTechnicalAnswerChange: (questionId: string, val: TechnicalAnswers[string]) => void;
  onLegalSubmit: (e: React.FormEvent) => void;
  onTechnicalSubmit: (e: React.FormEvent) => void;
}) {
  const trackTitle = track === "legal" ? "Legal Assessment" : "Technical Assessment";
  const trackSubtitle =
    track === "legal"
      ? "Answer questions about your data practices to receive a legal obligation gap report with regulatory citations."
      : "Evaluate infrastructure and operational controls across seven domains to receive a technical gap scorecard and remediation pathway.";

  return (
    <div className="assessment-hub">
      <header className="page-header compact">
        <div>
          <p className="eyebrow">Assessment</p>
          <h1>{trackTitle}</h1>
          <p className="subtitle">{trackSubtitle}</p>
        </div>
      </header>

      <div className="assessment-track-tabs">
        <button
          type="button"
          className={track === "legal" ? "active" : ""}
          onClick={() => onTrackChange("legal")}
        >
          Legal Assessment
        </button>
        <button
          type="button"
          className={track === "technical" ? "active" : ""}
          onClick={() => onTrackChange("technical")}
        >
          Technical Assessment
        </button>
      </div>

      {track === "legal" && (
        <QuestionnaireForm
          questionnaire={legalQuestionnaire}
          companyName={companyName}
          sector={sector}
          answers={legalAnswers}
          formKey={legalFormKey}
          loading={legalLoading}
          error={legalError}
          onCompanyNameChange={onCompanyNameChange}
          onSectorChange={onSectorChange}
          onAnswerChange={onLegalAnswerChange}
          onSubmit={onLegalSubmit}
        />
      )}

      {track === "technical" &&
        (technicalQuestionnaire ? (
          <TechnicalQuestionnaireForm
            questionnaire={technicalQuestionnaire}
            sectors={legalQuestionnaire.sectors}
            companyName={companyName}
            sector={sector}
            answers={technicalAnswers}
            formKey={technicalFormKey}
            loading={technicalLoading}
            error={technicalError}
            onCompanyNameChange={onCompanyNameChange}
            onSectorChange={onSectorChange}
            onAnswerChange={onTechnicalAnswerChange}
            onSubmit={onTechnicalSubmit}
          />
        ) : (
          <p className="section-note">Loading technical questionnaire…</p>
        ))}
    </div>
  );
}
