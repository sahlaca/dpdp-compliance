"""Narrative gap content for technical assessment reports."""

from __future__ import annotations

# Per-question narratives when the client answers "No"
GAP_NARRATIVES: dict[str, dict[str, str]] = {
    "q1_1": {
        "title": "Lack of Centralized Data Inventory",
        "gap": (
            "Personal data (PII) flows across production databases, development environments, and SaaS "
            "tools without a formal, up-to-date inventory map showing where data is collected, stored, "
            "and processed."
        ),
        "legal_risk": (
            "In the event of a data audit or erasure request, the organization cannot reliably verify "
            "that all copies of a citizen's data have been located and addressed — a core DPDP obligation."
        ),
        "recommended_service": (
            "Deploy automated data discovery tools to scan cloud environments, databases, and file shares. "
            "Build and maintain a living Data Lineage Map that shows where Indian citizen PII resides across "
            "your entire ecosystem."
        ),
    },
    "q1_2": {
        "title": "Uncontrolled Digitization of Paper Records",
        "gap": (
            "Personal data originally collected on paper and later scanned or typed into digital systems "
            "is not tracked through a formal safeguarding and inventory process."
        ),
        "legal_risk": (
            "Paper-to-digital conversions create shadow data stores that are often missed during access, "
            "correction, or erasure requests — exposing the business to incomplete compliance responses."
        ),
        "recommended_service": (
            "Extend your data inventory programme to cover digitization workflows. Tag scanned records at "
            "ingestion, link them to source documents, and apply the same retention and access controls as "
            "born-digital data."
        ),
    },
    "q1_3": {
        "title": "Data Minimization Not Enforced",
        "gap": (
            "Applications and forms collect more personal data than is strictly required for the immediate "
            "business transaction, with no technical or policy enforcement of minimization."
        ),
        "legal_risk": (
            "Collecting excessive personal data increases breach impact and makes it harder to justify "
            "processing purpose under DPDP — widening regulatory exposure if challenged."
        ),
        "recommended_service": (
            "Review data collection fields across customer-facing systems. Remove non-essential fields, "
            "implement validation rules, and document the lawful purpose for every data element retained."
        ),
    },
    "q2_1": {
        "title": "Privacy Notice Not Ready for Statutory Standards",
        "gap": (
            "The privacy notice is not consistently available in clear, plain language, and multilingual "
            "delivery (English plus scheduled Indian languages on request) is not operationally ready."
        ),
        "legal_risk": (
            "Data principals must receive transparent notice before processing. An inadequate notice "
            "undermines the legal basis for consent and increases the risk of regulatory challenge."
        ),
        "recommended_service": (
            "Rewrite the privacy notice in plain language, map each processing activity to a clear purpose, "
            "and prepare translated versions or a process to provide them promptly when requested."
        ),
    },
    "q2_2": {
        "title": "Consent Not Itemized or Affirmative",
        "gap": (
            "Applications do not capture separate, itemized consent for distinct processing purposes. "
            "Consent may rely on bundled terms or pre-checked boxes rather than clear affirmative action."
        ),
        "legal_risk": (
            "Under the DPDP Act, the burden of proof for valid consent rests entirely on the business. "
            "Bundled or implied consent is difficult to defend during an audit or dispute."
        ),
        "recommended_service": (
            "Refactor registration, checkout, and onboarding workflows to present itemized consent options. "
            "Require an explicit opt-in for each purpose and store the user's selection in a consent log."
        ),
    },
    "q2_3": {
        "title": "Consent Withdrawal Not Equally Accessible",
        "gap": (
            "Withdrawing consent is not as simple, visible, or fast as giving it. Users lack a clear "
            "self-service path to revoke previously granted permissions."
        ),
        "legal_risk": (
            "DPDP requires that withdrawal of consent be as easy as giving it. Friction in withdrawal "
            "can be treated as a compliance failure and may invalidate ongoing processing."
        ),
        "recommended_service": (
            "Add a dedicated consent management section to your app or website. Mirror the consent-giving "
            "flow so users can withdraw specific purposes in one or two steps without contacting support."
        ),
    },
    "q2_4": {
        "title": "Missing Consent Logging & Revocation Audit Trail",
        "gap": (
            "Backend systems do not maintain immutable, timestamped logs of what specific clauses users "
            "consented to, when they consented, and how consent was captured."
        ),
        "legal_risk": (
            "Without auditable consent records, the organization cannot prove explicit consent was given — "
            "a critical evidentiary requirement under the DPDP Act."
        ),
        "recommended_service": (
            "Integrate a Consent Management Platform (CMP) API or build an internal consent ledger. Record "
            "consent version, purpose, timestamp, channel, and user identifier for every acceptance event."
        ),
    },
    "q3_1": {
        "title": "No Operational Access Summary Workflow",
        "gap": (
            "The organization cannot readily provide a data principal with a summary of personal data "
            "processed and the third-party processors it has been shared with."
        ),
        "legal_risk": (
            "The right of access is a statutory data principal right. Failure to fulfil access requests "
            "within the prescribed framework exposes the business to complaints and penalties."
        ),
        "recommended_service": (
            "Build a data principal request workflow backed by your inventory map. Automate extraction of "
            "user records across systems and generate a structured access summary within your SLA."
        ),
    },
    "q3_2": {
        "title": "Correction and Erasure Not System-Wide",
        "gap": (
            "Systems cannot reliably process requests to correct, complete, or permanently erase personal "
            "data across all active databases, backups, and downstream copies."
        ),
        "legal_risk": (
            "Incomplete erasure or correction leaves residual PII in production or backup stores — "
            "creating direct non-compliance with data principal rights and breach-of-duty findings."
        ),
        "recommended_service": (
            "Define erasure and correction playbooks tied to your data map. Implement APIs or runbooks "
            "that propagate changes to replicas, caches, SaaS tools, and archived backups."
        ),
    },
    "q3_3": {
        "title": "Grievance Redressal Mechanism Not Published",
        "gap": (
            "There is no clearly designated, easy-to-find grievance channel published on the app or website "
            "for data principal complaints."
        ),
        "legal_risk": (
            "A visible grievance mechanism is a DPDP Rules requirement. Absence of one is a straightforward "
            "compliance gap that regulators and customers can identify immediately."
        ),
        "recommended_service": (
            "Publish a grievance contact (email, web form, or portal) on every customer touchpoint. Assign "
            "an owner, define response timelines, and track cases to resolution."
        ),
    },
    "q4_1": {
        "title": "Encryption Standards Not Applied Consistently",
        "gap": (
            "Digital personal data is not consistently encrypted at rest (e.g. AES-256) and in transit "
            "(e.g. TLS 1.2+) across all systems handling Indian citizen PII."
        ),
        "legal_risk": (
            "Sub-standard encryption is treated as a failure to maintain reasonable security safeguards — "
            "a key factor in DPBI penalty assessments following a breach."
        ),
        "recommended_service": (
            "Conduct an encryption posture review. Enable at-rest encryption on databases and object "
            "storage, enforce TLS 1.2+ on all public endpoints, and document exceptions with risk acceptance."
        ),
    },
    "q4_2": {
        "title": "Weak Identity and Access Governance",
        "gap": (
            "Least-privilege access is not enforced uniformly. Centralized IAM and mandatory MFA are not "
            "required for all personnel who access user personal data."
        ),
        "legal_risk": (
            "Over-privileged accounts and missing MFA are common root causes of data breaches. Regulators "
            "expect demonstrable access governance as part of reasonable security safeguards."
        ),
        "recommended_service": (
            "Roll out centralized Identity and Access Management (IAM) with role-based access and mandatory "
            "MFA for every account that can view or export personal data."
        ),
    },
    "q4_3": {
        "title": "Inadequate Audit Log Retention",
        "gap": (
            "Server and database access logs are overwritten, rotated, or purged before a one-year rolling "
            "retention period — limiting forensic visibility after an incident."
        ),
        "legal_risk": (
            "Short log retention undermines forensic readiness during a security incident and signals "
            "failure to maintain reasonable safeguards — increasing vulnerability to maximum DPBI penalties."
        ),
        "recommended_service": (
            "Set up a secure, centralized log repository (SIEM or cloud logging) with immutable or "
            "WORM-backed storage and a mandatory one-year retention policy for access and security events."
        ),
    },
    "q4_4": {
        "title": "No Regular Offensive Security Testing",
        "gap": (
            "Defences are not regularly validated through Vulnerability Assessment and Penetration Testing "
            "(VAPT) or red-team exercises focused on systems holding personal data."
        ),
        "legal_risk": (
            "Without proactive testing, unknown vulnerabilities may persist until exploited in a breach — "
            "after which the organization faces both incident costs and regulatory action."
        ),
        "recommended_service": (
            "Schedule annual VAPT on internet-facing applications and quarterly automated scanning. Remediate "
            "critical findings on a defined SLA and retain reports for audit evidence."
        ),
    },
    "q5_1": {
        "title": "No Tested Breach Response Playbook",
        "gap": (
            "There is no formal, documented, and tested Incident Response Plan specific to personal data "
            "breaches, including roles, escalation paths, and communication templates."
        ),
        "legal_risk": (
            "Delayed or chaotic breach response increases harm to data principals and attracts regulatory "
            "scrutiny. DPBI expects timely, structured notification when breaches occur."
        ),
        "recommended_service": (
            "Develop a DPDP-specific incident response playbook. Run tabletop exercises, define DPBI and "
            "data principal notification steps, and assign accountable owners for each stage."
        ),
    },
    "q5_2": {
        "title": "72-Hour Breach Reporting Not Achievable",
        "gap": (
            "Security operations cannot reliably detect a personal data breach and compile a reporting "
            "dossier for the DPBI and affected individuals within 72 hours."
        ),
        "legal_risk": (
            "Late breach notification is a standalone compliance failure under DPDP Rules and compounds "
            "penalties when combined with inadequate safeguards."
        ),
        "recommended_service": (
            "Integrate alerting with your log platform, pre-build breach assessment templates, and establish "
            "a rapid-response team with authority to escalate to leadership within hours of detection."
        ),
    },
    "q6_1": {
        "title": "No Automated Data Deletion on Purpose Expiry",
        "gap": (
            "When the business purpose for holding personal data ends, policy rules or automation do not "
            "reliably erase data from production systems and backups."
        ),
        "legal_risk": (
            "Retaining personal data beyond its stated purpose violates storage limitation principles and "
            "inflates breach scope and erasure request complexity."
        ),
        "recommended_service": (
            "Define retention schedules per data category. Implement automated deletion jobs, backup expiry "
            "rules, and periodic attestation that dormant records have been purged."
        ),
    },
    "q6_2": {
        "title": "Vendor Data Processing Agreements Missing",
        "gap": (
            "Not every vendor or processor handling the organization's personal data is bound by a Data "
            "Processing Agreement (DPA) or contract clause aligned to DPDP standards."
        ),
        "legal_risk": (
            "The data fiduciary remains accountable for processor conduct. Missing DPAs create ungoverned "
            "data flows and direct regulatory exposure if a vendor mishandles PII."
        ),
        "recommended_service": (
            "Inventory all processors, prioritise those handling Indian citizen data, and execute DPDP-aligned "
            "DPAs with flow-down security and breach notification obligations."
        ),
    },
    "q7_1": {
        "title": "Children's Data Controls Not Implemented",
        "gap": (
            "Where services are accessible to users under 18, age verification, verifiable parental consent, "
            "and restrictions on behavioural advertising for minors are not in place."
        ),
        "legal_risk": (
            "Processing children's personal data without verifiable parental consent is a high-priority "
            "DPDP compliance area with elevated regulatory attention and penalty exposure."
        ),
        "recommended_service": (
            "Implement age-gating at registration, parental consent workflows, and disable profiling or "
            "behavioural advertising for confirmed minor accounts."
        ),
    },
    "q7_2": {
        "title": "No Designated Privacy Lead or DPO",
        "gap": (
            "The organization has not appointed a designated privacy head or Data Protection Officer (DPO) "
            "as the accountable compliance contact for DPDP matters."
        ),
        "legal_risk": (
            "Without clear ownership, compliance tasks fragment across teams, grievances go unanswered, and "
            "the business cannot demonstrate governance maturity to regulators or enterprise customers."
        ),
        "recommended_service": (
            "Appoint a privacy lead or DPO with board visibility. Publish their contact details, define "
            "their mandate across assessments, vendor reviews, and data principal requests."
        ),
    },
}

REMEDIATION_PHASES: list[dict[str, str | list[str]]] = [
    {
        "phase": "Phase 1: Automated Data Discovery & Asset Mapping",
        "timeline": "Weeks 1–2",
        "summary": (
            "Establish the foundation by discovering where personal data lives across your technology estate. "
            "Without an accurate inventory, every subsequent compliance control — consent, erasure, breach "
            "response — operates on incomplete information."
        ),
        "deliverables": [
            "Deploy automated data discovery tools across cloud environments, databases, and file shares.",
            "Construct a dynamic Data Lineage Map identifying all locations where Indian citizen PII resides.",
            "Classify data by sensitivity and processing purpose to support minimization and retention rules.",
            "Extend the inventory to digitized paper records and shadow SaaS tools used by business teams.",
        ],
    },
    {
        "phase": "Phase 2: Identity Governance & Log Aggregation",
        "timeline": "Weeks 3–5",
        "summary": (
            "Strengthen the security layer that protects discovered data assets. Centralized identity controls "
            "and long-retention audit logs are essential both for day-to-day governance and for forensic "
            "readiness if a breach occurs."
        ),
        "deliverables": [
            "Implement centralized Identity and Access Management (IAM) with role-based least privilege.",
            "Enforce Multi-Factor Authentication (MFA) for every account that can access personal data.",
            "Enable encryption at rest and in transit on all systems identified in Phase 1.",
            "Set up a secure log repository with mandatory one-year immutable retention for access and security events.",
            "Schedule VAPT on critical applications and remediate high-severity findings.",
        ],
    },
    {
        "phase": "Phase 3: Consent Management Integration & Privacy Portals",
        "timeline": "Weeks 6–8",
        "summary": (
            "Close the gap between legal obligations and user-facing operations. Itemized consent, withdrawal "
            "workflows, and self-service privacy portals turn compliance requirements into working product "
            "features that data principals can actually use."
        ),
        "deliverables": [
            "Refactor registration and checkout flows to capture itemized, affirmative consent per purpose.",
            "Integrate a Consent Management Platform (CMP) API to record timestamped consent strings.",
            "Build a front-end Privacy Dashboard for access summaries, correction, erasure, and consent withdrawal.",
            "Publish a grievance mechanism and assign an accountable privacy lead or DPO.",
            "Execute Data Processing Agreements with all vendors handling personal data on your behalf.",
        ],
    },
]

CONCLUSION_TEMPLATE = (
    "Achieving DPDP compliance is not merely a legal checkbox; it directly secures your brand's market "
    "reputation and protects you from business-halting penalties. By executing the Technical Remediation "
    "Pathway outlined above, {company} will establish demonstrable safeguards, respond confidently to "
    "data principal rights requests, and turn data privacy into a competitive business advantage."
)

NEXT_STEP = (
    "Schedule a technical review meeting to walk through Phase 1 scope, resource allocation, and "
    "implementation timelines with your technology and compliance stakeholders."
)
