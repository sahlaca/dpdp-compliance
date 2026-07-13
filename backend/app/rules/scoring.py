"""Deterministic scoring logic for each DPDP obligation."""

from __future__ import annotations

from typing import Any

from app.rules.models import ComplianceStatus


def _collects(answers: dict[str, Any]) -> bool:
    return answers.get("collects_personal_data") is True


def _collects_children(answers: dict[str, Any]) -> bool:
    types = answers.get("data_types") or []
    return "children" in types


def _collects_cctv(answers: dict[str, Any]) -> bool:
    types = answers.get("data_types") or []
    return "cctv" in types


def _uses_processors(answers: dict[str, Any]) -> bool:
    return answers.get("uses_processors") is True


def _cross_border(answers: dict[str, Any]) -> bool:
    return answers.get("cross_border_transfer") is True


def _likely_sdf(answers: dict[str, Any]) -> bool:
    volume = answers.get("estimated_data_subjects")
    types = answers.get("data_types") or []
    sensitive = any(t in types for t in ("health", "identity", "children"))
    return volume in ("100k_1m", "over_1m") or (volume == "10k_100k" and sensitive)


def _employee_data(answers: dict[str, Any]) -> bool:
    return answers.get("collects_employee_data") is True


def _na(msg: str, action: str = "No action required unless practices change.") -> tuple[ComplianceStatus, str, str]:
    return ComplianceStatus.NOT_APPLICABLE, msg, action


def _any_key_answered(answers: dict[str, Any], keys: list[str]) -> bool:
    return any(k in answers for k in keys)


# Questionnaire keys that drive scoring — if none are answered, obligation is not assessed.
OBLIGATION_QUESTIONS: dict[str, list[str]] = {
    "scope_digital_personal_data": ["data_form", "collects_personal_data"],
    "lawful_basis_consent": ["processing_basis", "consent_practice"],
    "lawful_basis_legitimate_use": ["processing_basis", "legitimate_use_documented"],
    "purpose_limitation": ["purpose_documented"],
    "notice_to_principal": ["has_privacy_notice"],
    "notice_required_elements": ["has_privacy_notice", "notice_elements"],
    "consent_specific_informed": ["consent_practice", "processing_basis"],
    "consent_records": ["consent_records"],
    "consent_withdrawal": ["consent_withdrawal"],
    "consent_manager_readiness": ["consent_manager_plan"],
    "data_accuracy": ["data_accuracy_process"],
    "retention_erasure": ["retention_policy"],
    "erasure_pre_notification": ["retention_policy"],
    "deletion_on_withdrawal": ["consent_withdrawal", "retention_policy"],
    "right_of_access": ["data_principal_requests"],
    "right_of_correction": ["correction_process"],
    "right_of_erasure": ["erasure_process"],
    "right_of_grievance": ["grievance_officer"],
    "right_of_nomination": ["nomination_supported"],
    "rights_request_verification": ["identity_verification"],
    "rights_response_timeline": ["rights_timeline"],
    "contact_publication": ["contact_published"],
    "grievance_officer_appointed": ["grievance_officer"],
    "processor_contracts": ["uses_processors", "processor_agreements"],
    "processor_oversight": ["uses_processors", "processor_monitoring"],
    "cross_border_transfer": ["cross_border_transfer", "transfer_country_check"],
    "security_safeguards": ["security_safeguards"],
    "security_logging": ["security_safeguards"],
    "breach_response_plan": ["breach_response"],
    "breach_notify_board": ["breach_response", "breach_board_process"],
    "breach_notify_principals": ["breach_response", "breach_principal_process"],
    "children_verifiable_consent": ["parental_consent", "data_types"],
    "children_no_harmful_tracking": ["children_tracking_ads", "data_types"],
    "sdf_assessment": ["estimated_data_subjects", "data_types"],
    "sdf_dpo_appointment": ["sdf_preparation"],
    "sdf_dpia": ["sdf_preparation"],
    "sdf_audit": ["sdf_preparation"],
    "employee_data_safeguards": ["collects_employee_data", "employee_data_safeguards"],
    "cctv_processing": ["cctv_notice", "data_types"],
}


def _not_assessed() -> tuple[ComplianceStatus, str, str]:
    return (
        ComplianceStatus.NOT_ANSWERED,
        "Related questionnaire items not answered.",
        "Complete the relevant questions to assess this obligation.",
    )


def _not_processing(obligation_id: str) -> tuple[ComplianceStatus, str, str] | None:
    if obligation_id == "scope_digital_personal_data":
        return None
    if obligation_id == "sdf_assessment":
        return None
    return _na("No personal data processing reported..")


def score_obligation(obligation_id: str, answers: dict[str, Any]) -> tuple[ComplianceStatus, str, str]:
    if not _collects(answers):
        skip = _not_processing(obligation_id)
        if skip:
            return skip
        if obligation_id == "scope_digital_personal_data":
            return _na("No digital personal data processing reported.", "Confirm whether any data is digitised..")
        if obligation_id == "sdf_assessment":
            return _na(
                "No personal data processing reported — SDF assessment not required.",
                "Reassess if processing volume or sensitivity increases.",
            )

    qkeys = OBLIGATION_QUESTIONS.get(obligation_id)
    if qkeys and not _any_key_answered(answers, qkeys):
        return _not_assessed()

    # --- Scope ---
    if obligation_id == "scope_digital_personal_data":
        digital = answers.get("data_form")
        if digital in ("digital_only", "mixed"):
            return ComplianceStatus.MET, "Digital personal data processing confirmed.", "Maintain inventory of all digital data flows."
        if digital == "non_digital_only":
            return ComplianceStatus.NOT_APPLICABLE, "Only non-digitised data reported; Act scope is limited.", "Monitor if data is later digitised."
        return ComplianceStatus.PARTIAL, "Data form not fully specified.", "Document whether data is collected in digital form or later digitised."

    # --- Lawful basis ---
    if obligation_id == "lawful_basis_consent":
        basis = answers.get("processing_basis")
        practice = answers.get("consent_practice")
        if basis == "legitimate_use_only":
            return ComplianceStatus.NOT_APPLICABLE, "Processing relies on legitimate uses, not consent.", "Ensure each use falls under Section 7."
        if practice == "explicit_opt_in":
            return ComplianceStatus.MET, "Explicit opt-in consent mechanism in place.", "Maintain consent records and purpose-specific notices."
        if practice == "implied":
            return ComplianceStatus.NOT_MET, "Implied consent does not meet DPDP standard of free, specific, informed, unambiguous consent.", "Implement clear affirmative opt-in before collection."
        if practice == "none":
            return ComplianceStatus.NOT_MET, "No consent mechanism for consent-based processing.", "Implement explicit consent or establish legitimate use under Section 7."
        return ComplianceStatus.NOT_MET, "Consent mechanism inadequate or not specified.", "Implement explicit consent aligned with Section 6."

    if obligation_id == "lawful_basis_legitimate_use":
        basis = answers.get("processing_basis")
        if basis in ("consent_only", None):
            return _na("Processing appears consent-based only.", "Reassess if any processing qualifies under Section 7..")
        documented = answers.get("legitimate_use_documented")
        if documented == "yes":
            return ComplianceStatus.MET, "Legitimate uses documented.", "Review documentation when processing purposes change."
        if documented == "partial":
            return ComplianceStatus.PARTIAL, "Some legitimate uses may be undocumented.", "Document each Section 7 ground relied upon."
        return ComplianceStatus.NOT_MET, "Legitimate use claimed but not documented.", "Map each non-consent processing activity to a Section 7 ground."

    if obligation_id == "purpose_limitation":
        documented = answers.get("purpose_documented")
        if documented == "yes_all":
            return ComplianceStatus.MET, "Processing purposes documented for all data collected.", "Review when adding new data types or uses."
        if documented == "some":
            return ComplianceStatus.PARTIAL, "Purposes documented for only some data.", "Document specific purpose for each data element collected."
        return ComplianceStatus.NOT_MET, "Processing purposes not documented.", "Define and communicate specific purpose before collection."

    # --- Notice ---
    if obligation_id == "notice_to_principal":
        if answers.get("has_privacy_notice"):
            return ComplianceStatus.PARTIAL, "Privacy notice exists; full Rule 3 compliance must be verified.", "Audit notice against Rule 3 checklist."
        return ComplianceStatus.NOT_MET, "No privacy notice published.", "Publish notice before or at point of consent."

    if obligation_id == "notice_required_elements":
        elements = set(answers.get("notice_elements") or [])
        required = {"data_collected", "purpose", "rights", "withdrawal", "grievance", "complaint_board"}
        if not answers.get("has_privacy_notice"):
            return ComplianceStatus.NOT_MET, "No privacy notice to assess.", "Publish notice with all Rule 3 elements."
        missing = required - elements
        if not missing:
            return ComplianceStatus.MET, "All key Rule 3 notice elements reported present.", "Review notice when processing changes."
        if len(missing) <= 2:
            return ComplianceStatus.PARTIAL, f"Notice may be missing: {', '.join(sorted(missing))}.", "Add missing elements to privacy notice."
        return ComplianceStatus.NOT_MET, f"Notice missing critical elements: {', '.join(sorted(missing))}.", "Revise notice to include all Rule 3 requirements."

    # --- Consent ---
    if obligation_id == "consent_specific_informed":
        practice = answers.get("consent_practice")
        if answers.get("processing_basis") == "legitimate_use_only":
            return _na("Consent not the primary basis.", "Ensure legitimate use applies..")
        if practice == "explicit_opt_in":
            return ComplianceStatus.MET, "Explicit affirmative consent reported.", "Avoid pre-ticked boxes; keep consent separate from T&C."
        if practice == "implied":
            return ComplianceStatus.NOT_MET, "Implied/bundled consent fails Section 6(1) specificity requirement.", "Use unambiguous affirmative action for each purpose."
        return ComplianceStatus.NOT_MET, "Consent not specific and informed.", "Implement purpose-specific opt-in consent."

    if obligation_id == "consent_records":
        records = answers.get("consent_records")
        if records == "yes":
            return ComplianceStatus.MET, "Consent records maintained.", "Retain records demonstrating consent scope and timing."
        if records == "partial":
            return ComplianceStatus.PARTIAL, "Consent records incomplete.", "Log consent timestamp, purpose, and channel for all data principals."
        return ComplianceStatus.NOT_MET, "No consent records maintained.", "Implement consent logging system."

    if obligation_id == "consent_withdrawal":
        w = answers.get("consent_withdrawal")
        if w == "easy_withdrawal":
            return ComplianceStatus.MET, "Accessible withdrawal mechanism in place.", "Ensure withdrawal triggers erasure workflow."
        if w == "manual_only":
            return ComplianceStatus.PARTIAL, "Withdrawal possible but may not be as easy as giving consent.", "Provide online self-service withdrawal matching consent channel."
        return ComplianceStatus.NOT_MET, "No consent withdrawal mechanism.", "Implement withdrawal at least as easy as consent per Section 6(4)."

    if obligation_id == "consent_manager_readiness":
        plan = answers.get("consent_manager_plan")
        if plan == "assessed_ready":
            return ComplianceStatus.MET, "Consent Manager framework assessed.", "Monitor MeitY registrations from Nov 2026."
        if plan == "aware_not_assessed":
            return ComplianceStatus.PARTIAL, "Aware of Consent Manager provisions but not yet assessed.", "Evaluate Consent Manager integration before Nov 2026."
        return ComplianceStatus.PARTIAL, "Consent Manager provisions not yet assessed.", "Review Rule 4 and Section 6(9) before Nov 13, 2026."

    # --- Data quality ---
    if obligation_id == "data_accuracy":
        acc = answers.get("data_accuracy_process")
        if acc == "yes":
            return ComplianceStatus.MET, "Data accuracy measures in place.", "Periodic review of critical data fields."
        if acc == "informal":
            return ComplianceStatus.PARTIAL, "Accuracy checks informal.", "Formalise validation at collection and update points."
        return ComplianceStatus.NOT_MET, "No data accuracy process.", "Implement reasonable efforts to keep data accurate per Section 8(3)."

    if obligation_id == "retention_erasure":
        pol = answers.get("retention_policy")
        if pol == "documented_enforced":
            return ComplianceStatus.MET, "Retention and erasure policy documented and enforced.", "Align retention with Third Schedule where applicable."
        if pol == "informal":
            return ComplianceStatus.PARTIAL, "Retention practices informal.", "Document retention periods and automate deletion."
        return ComplianceStatus.NOT_MET, "No retention or erasure policy.", "Define retention limits and erasure triggers per Rule 5."

    if obligation_id == "erasure_pre_notification":
        pol = answers.get("retention_policy")
        if pol == "documented_enforced":
            return ComplianceStatus.PARTIAL, "Policy exists; verify 48-hour pre-erasure notice per Rule 5.", "Add 48-hour notification step before scheduled deletion."
        return ComplianceStatus.NOT_MET, "No process for pre-erasure notification.", "Implement 48-hour notice before Third Schedule deletion."

    if obligation_id == "deletion_on_withdrawal":
        w = answers.get("consent_withdrawal")
        pol = answers.get("retention_policy")
        if w == "easy_withdrawal" and pol == "documented_enforced":
            return ComplianceStatus.MET, "Withdrawal and deletion processes linked.", "Test end-to-end withdrawal-to-erasure flow."
        if w in ("easy_withdrawal", "manual_only"):
            return ComplianceStatus.PARTIAL, "Withdrawal exists but erasure workflow may be incomplete.", "Automate erasure within reasonable time after withdrawal."
        return ComplianceStatus.NOT_MET, "No process to delete data on consent withdrawal.", "Link withdrawal to erasure per Section 6(4) and 8(4)."

    # --- Rights ---
    if obligation_id == "right_of_access":
        p = answers.get("data_principal_requests")
        if p == "documented_process":
            return ComplianceStatus.MET, "Access request process documented.", "Publish how to submit access requests."
        if p == "ad_hoc":
            return ComplianceStatus.PARTIAL, "Access handled ad hoc.", "Formalise access request intake and response."
        return ComplianceStatus.NOT_MET, "No access request process.", "Establish process for Section 11 access rights."

    if obligation_id == "right_of_correction":
        p = answers.get("correction_process")
        if p == "documented":
            return ComplianceStatus.MET, "Correction process documented.", "Train staff on correction workflows."
        if p == "ad_hoc":
            return ComplianceStatus.PARTIAL, "Corrections handled informally.", "Document correction request handling."
        return ComplianceStatus.NOT_MET, "No correction process.", "Implement Section 12 correction mechanism."

    if obligation_id == "right_of_erasure":
        p = answers.get("erasure_process")
        if p == "documented":
            return ComplianceStatus.MET, "Erasure process documented.", "Test erasure across all systems and processors."
        if p == "ad_hoc":
            return ComplianceStatus.PARTIAL, "Erasure handled informally.", "Formalise erasure with defined timelines."
        return ComplianceStatus.NOT_MET, "No erasure process.", "Implement Section 13 erasure mechanism."

    if obligation_id == "right_of_grievance":
        g = answers.get("grievance_officer")
        if g == "appointed_published":
            return ComplianceStatus.MET, "Grievance mechanism published.", "Respond within 90 days per Rules."
        if g == "appointed_not_published":
            return ComplianceStatus.PARTIAL, "Grievance officer exists but not published.", "Publish grievance contact on website/notice."
        return ComplianceStatus.NOT_MET, "No grievance redressal mechanism.", "Appoint and publish grievance officer per Section 14."

    if obligation_id == "right_of_nomination":
        n = answers.get("nomination_supported")
        if n == "yes":
            return ComplianceStatus.MET, "Nomination right supported.", "Publish how Data Principals can nominate."
        if n == "planned":
            return ComplianceStatus.PARTIAL, "Nomination support planned but not live.", "Implement Section 15 nomination before deadline."
        return ComplianceStatus.NOT_MET, "Nomination right not supported.", "Enable Data Principals to nominate per Section 15."

    if obligation_id == "rights_request_verification":
        v = answers.get("identity_verification")
        if v == "documented":
            return ComplianceStatus.MET, "Identity verification method published.", "Publish required identifiers per Rule 9."
        if v == "informal":
            return ComplianceStatus.PARTIAL, "Verification done informally.", "Document and publish verification requirements."
        return ComplianceStatus.NOT_MET, "No identity verification for rights requests.", "Publish verification method per Rule 8/9."

    if obligation_id == "rights_response_timeline":
        t = answers.get("rights_timeline")
        if t == "documented_90":
            return ComplianceStatus.MET, "Rights response timelines documented within 90 days.", "Monitor and log all request SLAs."
        if t == "informal":
            return ComplianceStatus.PARTIAL, "Timelines informal.", "Define and publish maximum response times."
        return ComplianceStatus.NOT_MET, "No defined timelines for rights requests.", "Set timelines not exceeding 90 days for grievances."

    # --- Contact ---
    if obligation_id == "contact_publication":
        c = answers.get("contact_published")
        if c == "yes":
            return ComplianceStatus.MET, "Business contact / DPO details published.", "Keep contact current on all channels."
        if c == "partial":
            return ComplianceStatus.PARTIAL, "Contact published on some channels only.", "Display on website, app, and privacy notice."
        return ComplianceStatus.NOT_MET, "Business contact not published.", "Publish DPO or authorised contact per Section 8(9)."

    if obligation_id == "grievance_officer_appointed":
        g = answers.get("grievance_officer")
        if g == "appointed_published":
            return ComplianceStatus.MET, "Grievance officer appointed and published.", "Ensure officer is reachable and trained."
        if g == "appointed_not_published":
            return ComplianceStatus.NOT_MET, "Grievance officer not publicly accessible.", "Publish grievance officer contact immediately."
        return ComplianceStatus.NOT_MET, "No grievance officer appointed.", "Appoint grievance officer per Section 8(9) and 14."

    # --- Processors ---
    if obligation_id == "processor_contracts":
        if not _uses_processors(answers):
            return _na("No Data Processors reported..")
        a = answers.get("processor_agreements")
        if a == "yes_all":
            return ComplianceStatus.MET, "Written processor contracts in place.", "Review contracts annually."
        if a == "some":
            return ComplianceStatus.NOT_MET, "Processor contracts missing for some vendors.", "Execute DPA with every processor handling personal data."
        return ComplianceStatus.NOT_MET, "No processor contracts.", "Sign Rule 6 compliant contracts with all processors.."

    if obligation_id == "processor_oversight":
        if not _uses_processors(answers):
            return _na("No Data Processors reported..")
        m = answers.get("processor_monitoring")
        if m == "yes":
            return ComplianceStatus.MET, "Processor compliance monitored.", "Conduct periodic vendor assessments."
        if m == "partial":
            return ComplianceStatus.PARTIAL, "Limited processor oversight.", "Implement regular security and compliance reviews."
        return ComplianceStatus.NOT_MET, "No processor oversight.", "Monitor processor compliance per Section 8(2).."

    if obligation_id == "cross_border_transfer":
        if not _cross_border(answers):
            return _na("No cross-border transfer reported..")
        check = answers.get("transfer_country_check")
        if check == "verified":
            return ComplianceStatus.MET, "Transfer destinations verified against restricted list.", "Re-check when government updates country list."
        if check == "not_checked":
            return ComplianceStatus.NOT_MET, "Cross-border transfers without country restriction check.", "Verify destinations per Section 16 and Rule 15."
        return ComplianceStatus.PARTIAL, "Cross-border processing with incomplete transfer assessment.", "Document legal basis and verify country restrictions.."

    # --- Security ---
    if obligation_id == "security_safeguards":
        s = set(answers.get("security_safeguards") or [])
        if "none" in s or not s:
            return ComplianceStatus.NOT_MET, "No security safeguards reported.", "Implement encryption, access controls, and logging per Rule 12."
        has_encryption = "encryption" in s
        has_access = "access_controls" in s
        has_logging = "logging" in s
        if has_encryption and has_access and has_logging:
            return ComplianceStatus.MET, "Core security safeguards (encryption, access control, logging) in place.", "Document and test security measures periodically."
        if len(s) >= 2:
            return ComplianceStatus.PARTIAL, "Some safeguards present but gaps remain.", "Add missing controls: encryption, access management, audit logs."
        return ComplianceStatus.NOT_MET, "Insufficient security safeguards.", "Implement reasonable safeguards per Section 8(5) and Rule 12.."

    if obligation_id == "security_logging":
        s = set(answers.get("security_safeguards") or [])
        if "logging" in s:
            return ComplianceStatus.MET, "Access logging in place.", "Retain logs for at least one year per Rule 12."
        return ComplianceStatus.NOT_MET, "No access/activity logging.", "Implement logging with one-year retention per Rule 12.."

    if obligation_id == "breach_response_plan":
        if answers.get("breach_response"):
            return ComplianceStatus.PARTIAL, "Breach plan exists; validate against Rule 13 requirements.", "Test plan with tabletop exercise."
        return ComplianceStatus.NOT_MET, "No breach response plan.", "Create breach playbook with roles and timelines."

    if obligation_id == "breach_notify_board":
        if answers.get("breach_board_process") == "yes":
            return ComplianceStatus.MET, "Board notification process defined.", "Notify without undue delay; detailed report within 72 hours."
        if answers.get("breach_response"):
            return ComplianceStatus.PARTIAL, "Breach plan exists but Board notification not confirmed.", "Add immediate Board notification step per Rule 13."
        return ComplianceStatus.NOT_MET, "No Board breach notification process.", "Define Board notification workflow per Section 8(6).."

    if obligation_id == "breach_notify_principals":
        if answers.get("breach_principal_process") == "yes":
            return ComplianceStatus.MET, "Data Principal breach notification process defined.", "Use clear language; include impact and remedial steps."
        if answers.get("breach_response"):
            return ComplianceStatus.PARTIAL, "Breach plan exists but principal notification not confirmed.", "Add affected individual notification per Rule 13."
        return ComplianceStatus.NOT_MET, "No Data Principal breach notification process.", "Define individual notification workflow.."

    # --- Children ---
    if obligation_id == "children_verifiable_consent":
        if not _collects_children(answers):
            return _na("Children's data not collected..")
        p = answers.get("parental_consent")
        if p == "verifiable":
            return ComplianceStatus.MET, "Verifiable parental consent in place.", "Maintain verification records."
        if p == "not_verifiable":
            return ComplianceStatus.NOT_MET, "Parental consent not verifiable.", "Implement verifiable consent per Rule 10."
        return ComplianceStatus.NOT_MET, "No parental consent for children's data.", "Obtain verifiable parental consent before processing."

    if obligation_id == "children_no_harmful_tracking":
        if not _collects_children(answers):
            return _na("Children's data not collected..")
        tracking = answers.get("children_tracking_ads")
        if tracking == "none":
            return ComplianceStatus.MET, "No behavioural tracking or targeted ads for children.", "Audit marketing and analytics tools."
        if tracking == "unsure":
            return ComplianceStatus.PARTIAL, "Unclear whether tracking/ads target children.", "Audit all child-facing services for prohibited processing."
        return ComplianceStatus.NOT_MET, "Behavioural tracking or targeted ads may reach children.", "Disable tracking and targeted ads for users under 18."

    # --- SDF ---
    if obligation_id == "sdf_assessment":
        if _likely_sdf(answers):
            return ComplianceStatus.PARTIAL, "May qualify for Significant Data Fiduciary designation.", "Monitor government notifications; prepare enhanced obligations."
        return ComplianceStatus.NOT_APPLICABLE, "Unlikely SDF based on reported scale and sensitivity.", "Reassess if volume or risk profile increases.."

    if obligation_id in ("sdf_dpo_appointment", "sdf_dpia", "sdf_audit"):
        if not _likely_sdf(answers):
            return _na("SDF obligations apply only if designated by government..")
        prep = answers.get("sdf_preparation")
        labels = {
            "sdf_dpo_appointment": "DPO appointment",
            "sdf_dpia": "DPIA programme",
            "sdf_audit": "annual audit",
        }
        if prep == "prepared":
            return ComplianceStatus.MET, f"SDF compliance assessment: {labels[obligation_id]} prepared.", "Maintain compliance posture pending designation."
        if prep == "in_progress":
            return ComplianceStatus.PARTIAL, f"SDF compliance assessment: {labels[obligation_id]} in progress.", f"Complete {labels[obligation_id]} before designation."
        return ComplianceStatus.NOT_MET, f"SDF compliance assessment: {labels[obligation_id]} not started.", f"Begin {labels[obligation_id]} preparation per Section 10.."

    # --- Special ---
    if obligation_id == "employee_data_safeguards":
        if not _employee_data(answers):
            return _na("No employee personal data reported..")
        emp = answers.get("employee_data_safeguards")
        if emp == "yes":
            return ComplianceStatus.MET, "Employee data safeguards in place.", "Apply notice and security to employee data."
        if emp == "partial":
            return ComplianceStatus.PARTIAL, "Partial safeguards for employee data.", "Extend privacy notice and security to HR systems."
        return ComplianceStatus.NOT_MET, "No safeguards for employee personal data.", "Apply Section 8 obligations to employee data under Section 7(c).."

    if obligation_id == "cctv_processing":
        if not _collects_cctv(answers):
            return _na("No CCTV / video surveillance reported..")
        cctv = answers.get("cctv_notice")
        if cctv == "notice_and_signage":
            return ComplianceStatus.MET, "CCTV notice and signage in place.", "Define retention period for footage."
        if cctv == "signage_only":
            return ComplianceStatus.PARTIAL, "Signage present but formal notice may be missing.", "Add CCTV purpose and rights to privacy notice."
        return ComplianceStatus.NOT_MET, "No notice for CCTV processing.", "Publish notice and signage for video surveillance.."

    return ComplianceStatus.PARTIAL, "Requires manual review.", "Consult qualified counsel for this obligation."
