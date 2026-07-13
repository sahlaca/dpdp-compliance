import type { Question, QuestionnaireResponse } from "./types";

export type Answers = Record<string, unknown>;

function QuestionField({
  question,
  value,
  onChange,
}: {
  question: Question;
  value: unknown;
  onChange: (val: unknown) => void;
}) {
  if (question.type === "boolean") {
    return (
      <div className="choice-row">
        <label className="radio-pill">
          <input
            type="radio"
            checked={value === true}
            onChange={() => onChange(value === true ? undefined : true)}
          />
          Yes
        </label>
        <label className="radio-pill">
          <input
            type="radio"
            checked={value === false}
            onChange={() => onChange(value === false ? undefined : false)}
          />
          No
        </label>
      </div>
    );
  }

  if (question.type === "single_choice" && question.options) {
    return (
      <div className="choice-col">
        {question.options.map((opt) => (
          <label key={opt.value} className="choice-item">
            <input
              type="radio"
              name={question.id}
              checked={value === opt.value}
              onChange={() => onChange(value === opt.value ? undefined : opt.value)}
            />
            <span>{opt.label}</span>
          </label>
        ))}
      </div>
    );
  }

  if (question.type === "multi_choice" && question.options) {
    const selected = Array.isArray(value) ? (value as string[]) : [];
    return (
      <div className="choice-col">
        {question.options.map((opt) => (
          <label key={opt.value} className="choice-item">
            <input
              type="checkbox"
              checked={selected.includes(opt.value)}
              onChange={(e) => {
                const next = e.target.checked
                  ? [...selected, opt.value]
                  : selected.filter((v) => v !== opt.value);
                onChange(next.length > 0 ? next : undefined);
              }}
            />
            <span>{opt.label}</span>
          </label>
        ))}
      </div>
    );
  }

  return (
    <input
      className="text-input"
      type="text"
      value={typeof value === "string" ? value : ""}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

export function QuestionnaireForm({
  questionnaire,
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
  questionnaire: QuestionnaireResponse;
  companyName: string;
  sector: string;
  answers: Answers;
  formKey: number;
  loading: boolean;
  error: string | null;
  onCompanyNameChange: (v: string) => void;
  onSectorChange: (v: string) => void;
  onAnswerChange: (questionId: string, val: unknown) => void;
  onSubmit: (e: React.FormEvent) => void;
}) {
  const questionsBySection = questionnaire.sections.reduce<Record<string, Question[]>>((acc, section) => {
    acc[section] = questionnaire.questions.filter((q) => q.section === section);
    return acc;
  }, {});

  return (
    <form key={formKey} className="questionnaire-form" onSubmit={onSubmit}>
      <section className="card form-card">
        <h2>Your business</h2>
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
              {questionnaire.sectors.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </label>
        </div>
      </section>

      {Object.entries(questionsBySection).map(([section, questions]) => (
        <section key={section} className="card form-card">
          <h2>{section}</h2>
          {questions.map((q) => (
            <fieldset key={q.id} className="question">
              <legend>{q.prompt}</legend>
              {q.help_text && <p className="help">{q.help_text}</p>}
              <QuestionField
                question={q}
                value={answers[q.id]}
                onChange={(val) => onAnswerChange(q.id, val)}
              />
            </fieldset>
          ))}
        </section>
      ))}

      {error && <p className="error-banner">{error}</p>}

      <button className="btn submit-btn" type="submit" disabled={loading}>
        {loading ? "Generating report…" : "Generate gap report"}
      </button>
    </form>
  );
}
