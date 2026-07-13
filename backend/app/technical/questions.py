from __future__ import annotations

from app.technical.schema import (
    SCORE_LABELS,
    TechnicalDomain,
    TechnicalQuestion,
    TechnicalQuestionOption,
    TechnicalQuestionnaireResponse,
)

_OPTIONS = [
    TechnicalQuestionOption(value="yes", label=SCORE_LABELS["yes"], points=3),
    TechnicalQuestionOption(value="partial", label=SCORE_LABELS["partial"], points=1),
    TechnicalQuestionOption(value="no", label=SCORE_LABELS["no"], points=0),
    TechnicalQuestionOption(value="na", label=SCORE_LABELS["na"], points=None),
]

_DOMAINS: list[TechnicalDomain] = [
    TechnicalDomain(
        id="domain_1",
        number=1,
        name="Data Inventory & Mapping",
        description="The foundation — knowing where personal data lives across your ecosystem.",
    ),
    TechnicalDomain(
        id="domain_2",
        number=2,
        name="Notice & Consent Architecture",
        description="Explicit, itemized consent and auditable consent records.",
    ),
    TechnicalDomain(
        id="domain_3",
        number=3,
        name="Data Principal Rights Workflows",
        description="Operational workflows for access, correction, erasure, and grievance handling.",
    ),
    TechnicalDomain(
        id="domain_4",
        number=4,
        name="Technical Security Safeguards",
        description="Encryption, identity governance, logging, and defensive testing.",
    ),
    TechnicalDomain(
        id="domain_5",
        number=5,
        name="Breach Management & Regulatory Reporting",
        description="Incident response and Board notification compliance.",
    ),
    TechnicalDomain(
        id="domain_6",
        number=6,
        name="Data Retention & Vendor Management",
        description="Automated deletion and processor agreements.",
    ),
    TechnicalDomain(
        id="domain_7",
        number=7,
        name="Specialized Compliance (Children & Governance)",
        description="Minors protection and privacy leadership.",
    ),
]

_QUESTIONS: list[TechnicalQuestion] = [
    TechnicalQuestion(
        id="q1_1",
        domain_id="domain_1",
        domain_name="Data Inventory & Mapping",
        code="Q1.1",
        prompt=(
            "Data Lineage: Does your organization maintain a centralized, up-to-date Data Inventory Map "
            "that tracks where digital personal data is collected, stored, and processed across your "
            "ecosystem (databases, cloud, SaaS, email)?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q1_2",
        domain_id="domain_1",
        domain_name="Data Inventory & Mapping",
        code="Q1.2",
        prompt=(
            "Digitization Scope: Do you have a formal process to track and safeguard personal data originally "
            "collected on paper and subsequently scanned or typed into digital systems?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q1_3",
        domain_id="domain_1",
        domain_name="Data Inventory & Mapping",
        code="Q1.3",
        prompt=(
            "Data Minimization: Do you actively enforce data minimization — collecting only what is required "
            "for the immediate business transaction?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q2_1",
        domain_id="domain_2",
        domain_name="Notice & Consent Architecture",
        code="Q2.1",
        prompt=(
            "Notice Clarity: Is your Privacy Notice in clear, plain language and ready to be provided in "
            "English and scheduled Indian languages if requested?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q2_2",
        domain_id="domain_2",
        domain_name="Notice & Consent Architecture",
        code="Q2.2",
        prompt=(
            "Itemized Consent: Do your applications capture separate, itemized consent for different "
            "processing purposes through clear affirmative action (not pre-checked boxes)?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q2_3",
        domain_id="domain_2",
        domain_name="Notice & Consent Architecture",
        code="Q2.3",
        prompt=(
            "Easy Withdrawal: Is withdrawing consent as simple, accessible, and fast as giving it?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q2_4",
        domain_id="domain_2",
        domain_name="Notice & Consent Architecture",
        code="Q2.4",
        prompt=(
            "Consent Auditing: Does your backend maintain a tamper-proof Consent Log recording what was "
            "consented to, when (timestamped), and how?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q3_1",
        domain_id="domain_3",
        domain_name="Data Principal Rights Workflows",
        code="Q3.1",
        prompt=(
            "Access Summary: Can you provide a user with a summary of their personal data processed and "
            "third-party processors it has been shared with upon request?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q3_2",
        domain_id="domain_3",
        domain_name="Data Principal Rights Workflows",
        code="Q3.2",
        prompt=(
            "Correction & Erasure: Can your systems process requests to correct, complete, or permanently "
            "erase personal data across active databases?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q3_3",
        domain_id="domain_3",
        domain_name="Data Principal Rights Workflows",
        code="Q3.3",
        prompt=(
            "Grievance Redressal: Is there a clearly designated, easy-to-find grievance mechanism published "
            "on your app or website?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q4_1",
        domain_id="domain_4",
        domain_name="Technical Security Safeguards",
        code="Q4.1",
        prompt=(
            "Encryption Standards: Is digital personal data encrypted at rest (e.g. AES-256) and in transit "
            "(e.g. TLS 1.2+)?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q4_2",
        domain_id="domain_4",
        domain_name="Technical Security Safeguards",
        code="Q4.2",
        prompt=(
            "Access Governance: Do you enforce least privilege with centralized IAM and mandatory MFA for "
            "personnel accessing user data?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q4_3",
        domain_id="domain_4",
        domain_name="Technical Security Safeguards",
        code="Q4.3",
        prompt=(
            "Log Retention: Are security and access audit logs aggregated and retained for at least one "
            "rolling year?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q4_4",
        domain_id="domain_4",
        domain_name="Technical Security Safeguards",
        code="Q4.4",
        prompt=(
            "Offensive Testing: Do you regularly validate defenses through VAPT or red-team exercises?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q5_1",
        domain_id="domain_5",
        domain_name="Breach Management & Regulatory Reporting",
        code="Q5.1",
        prompt=(
            "Documented Playbook: Do you have a formal, tested Incident Response Plan for personal data breaches?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q5_2",
        domain_id="domain_5",
        domain_name="Breach Management & Regulatory Reporting",
        code="Q5.2",
        prompt=(
            "72-Hour Response: Can security operations detect a breach and compile a reporting dossier for "
            "the DPBI and affected individuals without undue delay (target within 72 hours)?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q6_1",
        domain_id="domain_6",
        domain_name="Data Retention & Vendor Management",
        code="Q6.1",
        prompt=(
            "Automated Deletion: When the business purpose ends, do policy rules or automation erase data safely?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q6_2",
        domain_id="domain_6",
        domain_name="Data Retention & Vendor Management",
        code="Q6.2",
        prompt=(
            "Vendor Flow-Downs: Do you have DPAs or legal clauses binding every vendor handling your data to "
            "DPDP standards?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q7_1",
        domain_id="domain_7",
        domain_name="Specialized Compliance (Children & Governance)",
        code="Q7.1",
        prompt=(
            "Minors Protection: If accessible to users under 18, do you verify age, obtain verifiable parental "
            "consent, and disable behavioural advertising for minors?"
        ),
        options=_OPTIONS,
    ),
    TechnicalQuestion(
        id="q7_2",
        domain_id="domain_7",
        domain_name="Specialized Compliance (Children & Governance)",
        code="Q7.2",
        prompt=(
            "Corporate Privacy Lead: Has your organization appointed a designated privacy head or DPO as the "
            "main compliance contact?"
        ),
        options=_OPTIONS,
    ),
]

SERVICE_OPPORTUNITIES: dict[str, str] = {
    "domain_1": "Data Governance Consulting: automated data discovery, classification, and mapping.",
    "domain_2": "Application Modernization: Consent Management Platform (CMP) integration and privacy portals.",
    "domain_3": "Privacy portal build-out: self-service access, correction, and erasure workflows.",
    "domain_4": "Cybersecurity & Cloud: SIEM logging (1-year retention), IAM, MFA, and VAPT.",
    "domain_5": "Managed Security: incident response playbooks, alerting, and SOC-lite structure.",
    "domain_6": "Data lifecycle automation and vendor DPA / contract remediation.",
    "domain_7": "Children's data controls and DPO / privacy governance appointment support.",
}


def get_technical_questionnaire() -> TechnicalQuestionnaireResponse:
    return TechnicalQuestionnaireResponse(domains=_DOMAINS, questions=_QUESTIONS)
