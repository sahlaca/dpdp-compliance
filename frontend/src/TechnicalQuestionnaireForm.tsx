import type { TechnicalAnswer, TechnicalQuestionnaireResponse } from "./types";
import type { QuestionOption } from "./types";

export type TechnicalAnswers = Record<string, TechnicalAnswer | undefined>;

export function TechnicalQuestionnaireForm({
  questionnaire,
  sectors,
  companyName,
  sector,
  answers,
  formKey,
  loading,
  error,
  onCompanyNameChange,
  onSectorChange,
  onAnswerChange,
  onSubmit,
}: {
  questionnaire: TechnicalQuestionnaireResponse;
  sectors: QuestionOption[];
  companyName: string;
  sector: string;
  answers: TechnicalAnswers;
  formKey: number;
  loading: boolean;
  error: string | null;
  onCompanyNameChange: (v: string) => void;
  onSectorChange: (v: string) => void;
  onAnswerChange: (questionId: string, val: TechnicalAnswer | undefined) => void;
  onSubmit: (e: React.FormEvent) => void;
}) {
  const questionsByDomain = questionnaire.domains.reduce<
    Record<string, { domain: (typeof questionnaire.domains)[number]; questions: typeof questionnaire.questions }>
  >((acc, domain) => {
    acc[domain.id] = {
      domain,
      questions: questionnaire.questions.filter((q) => q.domain_id === domain.id),
    };
    return acc;
  }, {});

  return (
    <form key={formKey} className="questionnaire-form" onSubmit={onSubmit}>
      <section className="card form-card">
        <h2>Your business</h2>
        <div className="scoring-guide">
          <p className="scoring-guide-title">How responses are scored</p>
          <ul className="scoring-criteria">
            {questionnaire.scoring_criteria.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="field-grid">
          <label>
            Company name
            <input
              className="text-input"
              required
              value={companyName}
              onChange={(e) => onCompanyNameChange(e.target.value)}
              placeholder="e.g. Sunrise Hotel"
            />
          </label>
          <label>
            Sector
            <select className="text-input" value={sector} onChange={(e) => onSectorChange(e.target.value)}>
              {sectors.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </label>
        </div>
      </section>

      {Object.values(questionsByDomain).map(({ domain, questions }) => (
        <section key={domain.id} className="card form-card">
          <h2>
            Domain {domain.number}: {domain.name}
          </h2>
          <p className="section-note">{domain.description}</p>
          {questions.map((q) => (
            <fieldset key={q.id} className="question">
              <legend>
                <span className="question-code">{q.code}</span> {q.prompt}
              </legend>
              <div className="choice-col">
                {q.options.map((opt) => (
                  <label key={opt.value} className="choice-item">
                    <input
                      type="radio"
                      name={q.id}
                      checked={answers[q.id] === opt.value}
                      onChange={() =>
                        onAnswerChange(q.id, answers[q.id] === opt.value ? undefined : opt.value)
                      }
                    />
                    <span>{opt.label}</span>
                  </label>
                ))}
              </div>
            </fieldset>
          ))}
        </section>
      ))}

      {error && <p className="error-banner">{error}</p>}

      <button className="btn submit-btn" type="submit" disabled={loading}>
        {loading ? "Generating report…" : "Generate technical gap report"}
      </button>
    </form>
  );
}
