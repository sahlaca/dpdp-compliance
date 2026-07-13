from app.questionnaire.schema import Question, QuestionOption, QuestionType, QuestionnaireResponse
from app.questionnaire.sectors import SECTORS

_QUESTIONS: list[Question] = [
    # Business profile
    Question(
        id="data_form",
        section="Business profile",
        prompt="In what form do you collect or store personal data?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="digital_only", label="Digital only (forms, apps, databases)"),
            QuestionOption(value="mixed", label="Mixed — some paper, later digitised"),
            QuestionOption(value="non_digital_only", label="Paper/physical only, never digitised"),
        ],
    ),
    Question(
        id="estimated_data_subjects",
        section="Business profile",
        prompt="Approximately how many individuals' data do you process per year?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="under_10k", label="Under 10,000"),
            QuestionOption(value="10k_100k", label="10,000 – 100,000"),
            QuestionOption(value="100k_1m", label="100,000 – 1 million"),
            QuestionOption(value="over_1m", label="Over 1 million"),
        ],
    ),
    # Data collection
    Question(
        id="collects_personal_data",
        section="Data collection",
        prompt="Do you collect personal data from customers, guests, patients, employees, or website visitors?",
        type=QuestionType.BOOLEAN,
    ),
    Question(
        id="data_types",
        section="Data collection",
        prompt="What types of personal data do you collect?",
        help_text="Select all that apply.",
        type=QuestionType.MULTI_CHOICE,
        options=[
            QuestionOption(value="name_contact", label="Name, phone, email, address"),
            QuestionOption(value="identity", label="Government ID (Aadhaar, passport, etc.)"),
            QuestionOption(value="payment", label="Payment / financial details"),
            QuestionOption(value="health", label="Health or medical information"),
            QuestionOption(value="children", label="Data relating to children under 18"),
            QuestionOption(value="cctv", label="CCTV / video footage"),
            QuestionOption(value="online_behavior", label="Website cookies / online behaviour"),
        ],
    ),
    Question(
        id="collects_employee_data",
        section="Data collection",
        prompt="Do you process personal data of employees or contractors?",
        type=QuestionType.BOOLEAN,
    ),
    Question(
        id="processing_basis",
        section="Data collection",
        prompt="What is your primary legal basis for processing personal data?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="consent_only", label="Consent (primary basis)"),
            QuestionOption(value="legitimate_use_only", label="Legitimate uses under Section 7 (no consent)"),
            QuestionOption(value="mixed", label="Mix of consent and legitimate uses"),
        ],
    ),
    Question(
        id="purpose_documented",
        section="Data collection",
        prompt="Is the specific purpose for each type of data collected documented?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes_all", label="Yes — for all data collected"),
            QuestionOption(value="some", label="Only for some data types"),
            QuestionOption(value="no", label="No — purposes not documented"),
        ],
    ),
    Question(
        id="legitimate_use_documented",
        section="Data collection",
        prompt="If you rely on legitimate uses (Section 7), are they documented?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes — each use mapped to Section 7"),
            QuestionOption(value="partial", label="Partially documented"),
            QuestionOption(value="no", label="No / not applicable"),
            QuestionOption(value="not_applicable", label="We rely on consent only"),
        ],
    ),
    Question(
        id="parental_consent",
        section="Data collection",
        prompt="If you collect children's data (under 18), how is parental consent obtained?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="verifiable", label="Verifiable parental/guardian consent"),
            QuestionOption(value="not_verifiable", label="Consent obtained but not verifiable"),
            QuestionOption(value="none", label="No parental consent process"),
            QuestionOption(value="not_applicable", label="We do not collect children's data"),
        ],
    ),
    Question(
        id="children_tracking_ads",
        section="Data collection",
        prompt="Do you use behavioural tracking or targeted advertising directed at users under 18?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="none", label="No — none directed at children"),
            QuestionOption(value="unsure", label="Unsure / not audited"),
            QuestionOption(value="yes", label="Yes"),
            QuestionOption(value="not_applicable", label="We do not process children's data"),
        ],
    ),
    Question(
        id="cctv_notice",
        section="Data collection",
        prompt="If you use CCTV, do you have notice/signage about video surveillance?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="notice_and_signage", label="Signage and privacy notice both cover CCTV"),
            QuestionOption(value="signage_only", label="Signage only"),
            QuestionOption(value="no", label="No notice or signage"),
            QuestionOption(value="not_applicable", label="No CCTV"),
        ],
    ),
    # Notice & consent
    Question(
        id="has_privacy_notice",
        section="Notice & consent",
        prompt="Do you publish a privacy notice?",
        type=QuestionType.BOOLEAN,
    ),
    Question(
        id="notice_elements",
        section="Notice & consent",
        prompt="Which elements does your privacy notice include?",
        help_text="Per Rule 3 — select all that apply.",
        type=QuestionType.MULTI_CHOICE,
        options=[
            QuestionOption(value="data_collected", label="Specific personal data collected"),
            QuestionOption(value="purpose", label="Purpose(s) of processing"),
            QuestionOption(value="rights", label="Data Principal rights and how to exercise them"),
            QuestionOption(value="withdrawal", label="How to withdraw consent"),
            QuestionOption(value="grievance", label="Grievance officer / contact details"),
            QuestionOption(value="complaint_board", label="How to complain to the Data Protection Board"),
        ],
    ),
    Question(
        id="consent_practice",
        section="Notice & consent",
        prompt="How do you obtain consent before collecting personal data?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="explicit_opt_in", label="Explicit opt-in (unchecked checkbox, signed form)"),
            QuestionOption(value="implied", label="Implied / pre-ticked / bundled with T&C only"),
            QuestionOption(value="none", label="No formal consent process"),
            QuestionOption(value="not_applicable", label="Not applicable — legitimate use only"),
        ],
    ),
    Question(
        id="consent_records",
        section="Notice & consent",
        prompt="Do you maintain records of when and how consent was given?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes — complete records"),
            QuestionOption(value="partial", label="Partial records"),
            QuestionOption(value="no", label="No records"),
            QuestionOption(value="not_applicable", label="Not applicable"),
        ],
    ),
    Question(
        id="consent_withdrawal",
        section="Notice & consent",
        prompt="How can individuals withdraw consent?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="easy_withdrawal", label="Same ease as consent (web, email, account settings)"),
            QuestionOption(value="manual_only", label="Only via phone or in-person"),
            QuestionOption(value="none", label="No withdrawal mechanism"),
            QuestionOption(value="not_applicable", label="Not applicable"),
        ],
    ),
    Question(
        id="consent_manager_plan",
        section="Notice & consent",
        prompt="Have you assessed Consent Manager provisions (effective Nov 2026)?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="assessed_ready", label="Yes — assessed and plan in place"),
            QuestionOption(value="aware_not_assessed", label="Aware but not yet assessed"),
            QuestionOption(value="not_assessed", label="Not yet assessed"),
        ],
    ),
    # Data lifecycle
    Question(
        id="data_accuracy_process",
        section="Data lifecycle",
        prompt="Do you have processes to keep personal data accurate and up to date?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes — formal process"),
            QuestionOption(value="informal", label="Informal / ad hoc"),
            QuestionOption(value="no", label="No process"),
        ],
    ),
    Question(
        id="retention_policy",
        section="Data lifecycle",
        prompt="Do you have a documented data retention and deletion policy?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="documented_enforced", label="Yes — documented and enforced"),
            QuestionOption(value="informal", label="Informal practices"),
            QuestionOption(value="no", label="No policy"),
        ],
    ),
    # Data Principal rights
    Question(
        id="data_principal_requests",
        section="Data Principal rights",
        prompt="Can individuals request access to their personal data?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="documented_process", label="Yes — documented process"),
            QuestionOption(value="ad_hoc", label="Handled ad hoc"),
            QuestionOption(value="no", label="No process"),
        ],
    ),
    Question(
        id="correction_process",
        section="Data Principal rights",
        prompt="Can individuals request correction of inaccurate data?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="documented", label="Yes — documented process"),
            QuestionOption(value="ad_hoc", label="Handled ad hoc"),
            QuestionOption(value="no", label="No process"),
        ],
    ),
    Question(
        id="erasure_process",
        section="Data Principal rights",
        prompt="Can individuals request erasure of their data?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="documented", label="Yes — documented process"),
            QuestionOption(value="ad_hoc", label="Handled ad hoc"),
            QuestionOption(value="no", label="No process"),
        ],
    ),
    Question(
        id="grievance_officer",
        section="Data Principal rights",
        prompt="Have you appointed a grievance officer and published their contact?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="appointed_published", label="Yes — appointed and published"),
            QuestionOption(value="appointed_not_published", label="Appointed but not published"),
            QuestionOption(value="no", label="Not appointed"),
        ],
    ),
    Question(
        id="nomination_supported",
        section="Data Principal rights",
        prompt="Can Data Principals nominate someone to exercise rights on their behalf?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes — supported"),
            QuestionOption(value="planned", label="Planned but not yet live"),
            QuestionOption(value="no", label="Not supported"),
        ],
    ),
    Question(
        id="identity_verification",
        section="Data Principal rights",
        prompt="Is your method for verifying identity before fulfilling rights requests published?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="documented", label="Yes — published method"),
            QuestionOption(value="informal", label="Verified informally"),
            QuestionOption(value="no", label="No published method"),
        ],
    ),
    Question(
        id="rights_timeline",
        section="Data Principal rights",
        prompt="Are response timelines for rights/grievance requests defined (max 90 days)?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="documented_90", label="Yes — documented within 90 days"),
            QuestionOption(value="informal", label="Informal timelines"),
            QuestionOption(value="no", label="No defined timelines"),
        ],
    ),
    # Transparency & contact
    Question(
        id="contact_published",
        section="Transparency & contact",
        prompt="Is your business contact or DPO details published on website/app?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes — on website/app and notice"),
            QuestionOption(value="partial", label="On some channels only"),
            QuestionOption(value="no", label="Not published"),
        ],
    ),
    # Processors & transfers
    Question(
        id="uses_processors",
        section="Processors & transfers",
        prompt="Do third-party vendors process personal data on your behalf?",
        type=QuestionType.BOOLEAN,
    ),
    Question(
        id="processor_agreements",
        section="Processors & transfers",
        prompt="Do you have written Data Processor contracts with all vendors?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes_all", label="Yes — all relevant vendors"),
            QuestionOption(value="some", label="Some vendors only"),
            QuestionOption(value="no", label="No contracts"),
            QuestionOption(value="not_applicable", label="No processors"),
        ],
    ),
    Question(
        id="processor_monitoring",
        section="Processors & transfers",
        prompt="Do you monitor processor compliance with data protection obligations?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes — regular reviews"),
            QuestionOption(value="partial", label="Occasional / informal"),
            QuestionOption(value="no", label="No monitoring"),
            QuestionOption(value="not_applicable", label="No processors"),
        ],
    ),
    Question(
        id="cross_border_transfer",
        section="Processors & transfers",
        prompt="Is personal data stored or processed outside India?",
        type=QuestionType.BOOLEAN,
    ),
    Question(
        id="transfer_country_check",
        section="Processors & transfers",
        prompt="Have you verified destination countries are not on the government restricted list?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="verified", label="Yes — verified"),
            QuestionOption(value="not_checked", label="No — not checked"),
            QuestionOption(value="not_applicable", label="No cross-border transfers"),
        ],
    ),
    # Security & breach
    Question(
        id="security_safeguards",
        section="Security & breach",
        prompt="Which security measures are in place?",
        type=QuestionType.MULTI_CHOICE,
        options=[
            QuestionOption(value="access_controls", label="Role-based access controls"),
            QuestionOption(value="encryption", label="Encryption at rest or in transit"),
            QuestionOption(value="logging", label="Access / activity logging (1-year retention)"),
            QuestionOption(value="backups", label="Regular backups"),
            QuestionOption(value="none", label="None of the above"),
        ],
    ),
    Question(
        id="breach_response",
        section="Security & breach",
        prompt="Do you have a documented data breach response plan?",
        type=QuestionType.BOOLEAN,
    ),
    Question(
        id="breach_board_process",
        section="Security & breach",
        prompt="Does your breach plan include immediate notification to the Data Protection Board?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes"),
            QuestionOption(value="no", label="No"),
            QuestionOption(value="not_applicable", label="No breach plan"),
        ],
    ),
    Question(
        id="breach_principal_process",
        section="Security & breach",
        prompt="Does your breach plan include notifying affected Data Principals?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes"),
            QuestionOption(value="no", label="No"),
            QuestionOption(value="not_applicable", label="No breach plan"),
        ],
    ),
    # Employment & SDF
    Question(
        id="employee_data_safeguards",
        section="Employment & SDF",
        prompt="Are privacy notice and security safeguards applied to employee data?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="yes", label="Yes — same safeguards as customer data"),
            QuestionOption(value="partial", label="Partial safeguards"),
            QuestionOption(value="no", label="No"),
            QuestionOption(value="not_applicable", label="No employee data"),
        ],
    ),
    Question(
        id="sdf_preparation",
        section="Employment & SDF",
        prompt="If designated a Significant Data Fiduciary, are you prepared (DPO, DPIA, audit)?",
        type=QuestionType.SINGLE_CHOICE,
        options=[
            QuestionOption(value="prepared", label="Yes — preparation underway or complete"),
            QuestionOption(value="in_progress", label="In progress"),
            QuestionOption(value="not_started", label="Not started"),
            QuestionOption(value="not_applicable", label="Unlikely to be designated SDF"),
        ],
    ),
]


def get_questionnaire() -> QuestionnaireResponse:
    sections = list(dict.fromkeys(q.section for q in _QUESTIONS))
    sectors = [QuestionOption(**s) for s in SECTORS]
    return QuestionnaireResponse(sections=sections, sectors=sectors, questions=_QUESTIONS)
