## META
name: Prior Authorization
version: 1.0.0
domain: prior-authorization
description: Enterprise knowledge graph of the prior authorization process — workflow, clinical criteria, payer-provider tensions, automation, and regulatory reform.
nodes: 50
edges: 75
source: CMS prior auth rules 2024 (CMS-0057-F); CAQH CORE standards; AMA 2023 PA harm survey; AHIP PA reform white paper; 21st Century Cures Act interoperability provisions
license: MIT

---

## NODES

[CONCEPT|prior_authorization|Prior Authorization (PA)
  |Payer requirement that a provider obtain approval before a drug, procedure, or service will be covered. Designed as a cost-control and utilization management tool. AMA surveys document it as the leading driver of physician administrative burden and patient care delays.]

[CONCEPT|pa_workflow|PA Workflow
  |End-to-end process sequence: drug/procedure ordered → formulary tier check → PA requirement triggered → clinical criteria submitted → payer determination issued → approval/denial communicated → appeal if denied. Each step introduces latency and documentation burden.]

[CONCEPT|formulary|Formulary
  |Payer's tiered preferred drug list specifying coverage level, cost-sharing, and access requirements for each covered drug. Tier placement directly determines whether PA is required and on what clinical basis.]

[CONCEPT|formulary_tier|Formulary Tier
  |Classification level within a formulary (Tier 1 = generic/preferred, Tier 2 = brand preferred, Tier 3 = non-preferred, Tier 4 = specialty). Higher tier drugs carry higher cost-sharing and stricter PA requirements.]

[CONCEPT|pa_requirement|PA Requirement
  |Payer policy mandating pre-approval for a specific drug or procedure. Triggered by formulary tier, drug cost threshold, diagnosis indication, or utilization management protocol. Varies by payer, plan, and benefit year.]

[CONCEPT|drug|Drug
  |Pharmaceutical agent prescribed for a therapeutic indication. Classification (generic/brand/specialty/biologic) determines formulary tier, cost-sharing level, and likelihood of PA requirement. ~30% of all prescriptions now require PA.]

[CONCEPT|specialty_drug|Specialty Drug
  |High-cost biologic, immunotherapy, or complex small-molecule agent (typically >$6,000/month). Almost universally subject to prior authorization. Examples: adalimumab, semaglutide, ustekinumab. Represent 50%+ of drug spend on <5% of patients.]

[CONCEPT|clinical_criterion|Clinical Criterion
  |Specific evidence or condition a provider must document to satisfy a PA requirement. Types include step therapy compliance, diagnosis confirmation, lab value thresholds, age range, specialist attestation, and comorbidity documentation.]

[CONCEPT|step_therapy|Step Therapy
  |PA criterion requiring a patient to try and fail a lower-cost drug (usually generic or preferred brand) before a higher-cost alternative will be approved. Also called "fail first." Standard for specialty drugs and biologics.]

[CONCEPT|quantity_limit|Quantity Limit
  |PA-enforced restriction on the maximum amount of a drug dispensed per fill or per month. Applied to high-risk medications (opioids, benzodiazepines) and specialty drugs. Exceeding the limit triggers a PA requirement for the overage.]

[CONCEPT|age_restriction|Age Restriction
  |PA criterion that limits drug or procedure coverage to patients within a specified age range. Example: GLP-1 agonists may require age ≥18; pediatric indications may require documentation of off-label use rationale.]

[CONCEPT|diagnosis_criterion|Diagnosis Criterion
  |PA requirement that the patient have a specific ICD-coded diagnosis or documented clinical condition before coverage is granted. Prevents off-label prescribing for non-covered indications without explicit approval.]

[CONCEPT|specialty_criterion|Specialty Criterion
  |PA requirement that a drug or procedure be ordered or supervised by a board-certified specialist in the relevant field. Example: biologics for RA requiring rheumatologist attestation; oncology drugs requiring oncologist ordering.]

[CONCEPT|pa_determination|PA Determination
  |Payer's formal decision on a prior authorization request: approval, denial, or partial approval (quantity or duration modification). Must be issued within regulatory timeframes: 72 hours (urgent), 7 days (standard) under CMS rules.]

[CONCEPT|approval|Approval
  |PA determination granting coverage for the requested drug or procedure under specified conditions: authorized quantity, duration, and diagnosis. Approval does not guarantee payment if other claim conditions are not met.]

[CONCEPT|denial|Denial
  |PA determination rejecting coverage for the requested drug or procedure. Must include a specific reason and notice of appeal rights. Appealable first via internal review, then external independent review (IRO) by state mandate.]

[CONCEPT|appeal|Appeal
  |Formal challenge to a PA denial submitted by a provider or patient. First level: internal appeal reviewed by payer's medical director. Second level: external independent review organization (IRO). Success rates: ~40% on internal, ~60% on external.]

[CONCEPT|peer_to_peer_review|Peer-to-Peer Review (P2P)
  |Direct clinician-to-clinician discussion between the prescribing provider and the payer's reviewing medical director. Requested after initial denial. Most effective PA escalation: approximately 60–75% of P2P calls result in overturn to approval.]

[CONCEPT|medical_necessity|Medical Necessity
  |Payer-defined standard that a requested service is appropriate, clinically indicated, evidence-based, and not primarily for the convenience of the provider or patient. The central criterion evaluated in every PA determination. Definitions vary widely by payer.]

[CONCEPT|utilization_management|Utilization Management (UM)
  |Payer's systematic program for controlling healthcare service utilization: prior authorization, concurrent review, retrospective review, and discharge planning. PA is the pre-service component of the UM program.]

[CONCEPT|real_time_pa|Real-Time Prior Authorization (RTPA)
  |Electronic PA process returning a determination in seconds at the point of prescribing, integrated into EHR prescribing workflows. Mandated for Part D drugs under CMS-0057-F (effective 2027). Eliminates phone/fax delays in routine cases.]

[CONCEPT|gold_carding|Gold Carding
  |PA exemption program that waives PA requirements for providers with demonstrated high approval rates (typically >90%) for a specific drug or procedure category. Enacted into law in Texas, Arkansas, and other states. Reduces burden for trusted providers.]

[CONCEPT|pa_reform|PA Reform
  |Legislative and regulatory movement to reduce PA burden: CMS-0057-F (2024), Gold Carding laws, AMA resolution, Improving Seniors' Timely Access to Care Act. Focus areas: decision speed, transparency of criteria, automation mandates, and appeals rights.]

[CONCEPT|administrative_burden|Administrative Burden
  |Time and resource cost imposed on provider practices by PA: form completion, phone/fax submissions, status tracking, appeals. AMA 2023: physicians average 13 PA requests/week, consuming 4.6 physician hours and 9.1 staff hours weekly.]

[CONCEPT|provider_burden|Provider Burden
  |Aggregate effect of administrative requirements on physician practice: PA, documentation, coding, reporting. 35% of physicians report burnout directly attributable to administrative tasks. PA is consistently ranked the top contributor.]

[CONCEPT|patient_harm|Patient Harm
  |Adverse clinical outcome caused by PA-induced delays or denials: disease progression, acute deterioration, hospitalization, death. AMA 2023: 33% of physicians report a PA delay led to a serious adverse event; 9% report a patient death.]

[CONCEPT|care_delay|Care Delay
  |Gap between a provider's clinical decision to initiate treatment and the actual start of therapy due to PA processing time. Average PA turnaround: 1–3 business days standard; urgent requests often exceed regulatory 72-hour limit.]

[CONCEPT|payer|Payer
  |Health insurance organization that finances and administers medical benefits: commercial insurer (Aetna, BCBS, UHC), Medicare Advantage plan, or Medicaid managed care organization. Sets PA policies, formularies, and reimbursement rates.]

[CONCEPT|prescriber|Prescriber
  |Licensed clinician with legal authority to write prescriptions: MD, DO, NP, PA. Bears primary responsibility for PA submission documentation. Subject to PA denial for drugs they have prescribed for years without prior issue.]

[CONCEPT|patient|Patient
  |Individual receiving medical care whose treatment is subject to prior authorization. Often unaware of PA status until prescription cannot be filled. Bears the clinical risk of care delays while having no direct role in the PA process.]

[CONCEPT|cms_pa_rule|CMS Prior Auth Rule (CMS-0057-F)
  |Final rule published January 2024 by CMS governing MA plans, Medicaid, CHIP, and Marketplace QHPs. Key provisions: 72-hour urgent / 7-day standard PA decision timelines; API-based PA status reporting by 2026; RTPA for Part D by 2027.]

[CONCEPT|caqh_core|CAQH CORE Standards
  |Nonprofit-administered operating rules for electronic healthcare administrative transactions under ACA Section 1104. CAQH CORE 360/370 standards specify electronic PA request and response formats using X12 278 transactions.]

[CONCEPT|x12_278|X12 278 Transaction
  |ANSI ASC X12 electronic data interchange standard for healthcare service review requests and responses. The federally mandated transaction format for PA submission under HIPAA. Adoption rate remains low; most PA still conducted by phone/fax/portal.]

[CONCEPT|pa_automation|PA Automation
  |Technology-enabled processing of PA requests without manual payer review: electronic submission, rules-engine auto-adjudication, AI-based clinical documentation extraction, and RTPA at the point of care. Reduces administrative burden and decision latency.]

[CONCEPT|electronic_pa|Electronic Prior Authorization (ePA)
  |PA submitted and processed entirely via electronic health record integration or payer portal, eliminating phone calls and fax. CMS mandates ePA capability for Part D plans by 2027. Current adoption: ~30% of PA requests are fully electronic.]

[CONCEPT|prior_auth_ckg|Prior Authorization CKG
  |Compact Knowledge Graph encoding PA workflow logic, clinical criteria structures, payer-provider relationships, and regulatory rules. Enables multi-hop traversal: drug → tier → PA requirement → criteria → determination pathway.]

[CONCEPT|clinical_decision_support|Clinical Decision Support (CDS)
  |EHR-integrated software providing real-time guidance during prescribing: formulary tier display, PA requirement flagging, alternative drug suggestions, and CDS Hooks-based PA workflow initiation before prescription is sent to pharmacy.]

[CONCEPT|pa_api|Prior Authorization API
  |HL7 FHIR-based API enabling EHR systems to query payer PA requirements, submit requests, and receive determinations programmatically. Required by CMS-0057-F by January 2026. Foundational infrastructure for RTPA and ePA.]

[CONCEPT|fhir|HL7 FHIR
  |Fast Healthcare Interoperability Resources: HL7 standard for health data exchange via RESTful APIs. Used in PA API implementation. CDS Hooks and Da Vinci PDEX Prior Authorization profiles specify FHIR-based PA workflows.]

[CONCEPT|davinci_pas|Da Vinci PAS Implementation Guide
  |HL7 Da Vinci Project's FHIR Implementation Guide for Prior Authorization Support. Defines FHIR R4 profiles for PA request bundles, responses, and subscription notifications. Reference standard for EHR-payer PA API integration.]

[CONCEPT|step_therapy_exception|Step Therapy Exception
  |Regulatory or plan provision allowing a patient to skip step therapy requirements when they have already tried and failed the first-line drug, have a contraindication, or when the required drug is clinically inappropriate. Required in most state laws and CMS rules.]

[CONCEPT|inappropriate_denial|Inappropriate Denial
  |PA denial issued without adequate clinical review, by unqualified reviewers, or contrary to established evidence-based guidelines. OIG audits have found that Medicare Advantage plans deny up to 13% of medically necessary claims inappropriately.]

[CONCEPT|independent_review_organization|Independent Review Organization (IRO)
  |State-certified third-party organization conducting external review of PA denials. Uses independent clinical experts. IRO decisions are binding on payers in most states. Overturn rate ~60%, indicating high inappropriate denial rate at internal level.]

[CONCEPT|gold_carding_law|Gold Carding Law
  |State statute mandating that payers implement gold carding programs for high-performing providers. Texas HB 3459 (2021) was the first. Subsequent states include Arkansas and New Mexico. Creates a provider track record → exemption feedback loop.]

[CONCEPT|pa_transparency|PA Transparency
  |Regulatory and legislative requirement that payers publicly disclose PA criteria, denial reasons, and approval rates. CMS-0057-F requires MA plans to publish PA criteria on public-facing websites. Intended to enable provider and patient decision-making.]

[CONCEPT|concurrent_review|Concurrent Review
  |UM review of ongoing inpatient care to authorize continued hospital days or ongoing treatment. Complements prior authorization (pre-service review). Payer may deny additional inpatient days, triggering immediate appeals.]

[CONCEPT|retrospective_review|Retrospective Review
  |Payer review of services already rendered. Can result in retroactive denial and clawback of payments. Triggered when services were rendered without PA in emergency settings or due to administrative error.]

[CONCEPT|specialty_pharmacy|Specialty Pharmacy
  |Dispensing pharmacy specializing in high-cost, complex specialty drugs requiring cold chain, patient education, and adherence monitoring. Payers often restrict specialty drug coverage to in-network specialty pharmacies, adding another PA-adjacent access barrier.]

[CONCEPT|pa_denial_rate|PA Denial Rate
  |Percentage of PA requests denied by a payer for a given drug, procedure, or plan type. MA plan denial rates for inpatient stays: ~13% (OIG 2022). Commercial PA approval rates: 82–95% depending on drug class. Denominator for quality measurement.]

[CONCEPT|burnout|Physician Burnout
  |Syndrome of emotional exhaustion, depersonalization, and reduced personal accomplishment among physicians. PA administrative burden is the most frequently cited modifiable contributor. Linked to reduced physician workforce and patient access.]

---

## EDGES

prior_authorization      -[COMPONENT_OF]->        pa_workflow
formulary                -[CONTAINS]->            formulary_tier
formulary_tier           -[TRIGGERS]->            pa_requirement
drug                     -[CLASSIFIED_BY]->       formulary_tier
specialty_drug           -[INSTANCE_OF]->         drug
specialty_drug           -[REQUIRES]->            pa_requirement
pa_requirement           -[DEFINED_BY]->          clinical_criterion
pa_requirement           -[EVALUATED_BY]->        utilization_management
clinical_criterion       -[DETERMINES]->          pa_determination
step_therapy             -[INSTANCE_OF]->         clinical_criterion
step_therapy             -[PREREQUISITE_FOR]->    approval
quantity_limit           -[INSTANCE_OF]->         clinical_criterion
age_restriction          -[INSTANCE_OF]->         clinical_criterion
diagnosis_criterion      -[INSTANCE_OF]->         clinical_criterion
specialty_criterion      -[INSTANCE_OF]->         clinical_criterion
pa_determination         -[OUTPUTS]->             approval
pa_determination         -[OUTPUTS]->             denial
denial                   -[TRIGGERS]->            appeal
denial                   -[CAUSES]->              care_delay
denial                   -[INSTANCE_OF]->         inappropriate_denial
appeal                   -[ESCALATES_TO]->        peer_to_peer_review
appeal                   -[REVIEWED_BY]->         independent_review_organization
peer_to_peer_review      -[OVERRIDES]->           denial
medical_necessity        -[DEFINES]->             pa_determination
medical_necessity        -[EVALUATED_BY]->        utilization_management
utilization_management   -[IMPLEMENTS]->          prior_authorization
utilization_management   -[COMPONENT_OF]->        payer
real_time_pa             -[PREVENTS]->            care_delay
real_time_pa             -[IMPLEMENTS]->          pa_automation
real_time_pa             -[REQUIRES]->            pa_api
gold_carding             -[EXEMPTS_FROM]->        pa_requirement
gold_carding             -[REDUCES]->             administrative_burden
gold_carding             -[INSTANCE_OF]->         pa_reform
gold_carding_law         -[GOVERNS]->             gold_carding
pa_reform                -[REDUCES]->             administrative_burden
pa_reform                -[GOVERNED_BY]->         cms_pa_rule
administrative_burden    -[CAUSES]->              provider_burden
administrative_burden    -[CAUSES]->              care_delay
provider_burden          -[CAUSES]->              burnout
care_delay               -[CAUSES]->              patient_harm
patient_harm             -[QUANTIFIED_BY]->       pa_denial_rate
payer                    -[GOVERNS]->             formulary
payer                    -[GOVERNS]->             pa_requirement
prescriber               -[SUBMITS]->             pa_requirement
prescriber               -[REQUESTS]->            peer_to_peer_review
patient                  -[AFFECTED_BY]->         pa_determination
patient                  -[BEARS_RISK_OF]->       patient_harm
cms_pa_rule              -[GOVERNS]->             pa_workflow
cms_pa_rule              -[MANDATES]->            real_time_pa
cms_pa_rule              -[MANDATES]->            pa_api
cms_pa_rule              -[REQUIRES]->            pa_transparency
caqh_core                -[STANDARDIZES]->        pa_workflow
caqh_core                -[DEFINES]->             x12_278
x12_278                  -[IMPLEMENTS]->          electronic_pa
electronic_pa            -[INSTANCE_OF]->         pa_automation
electronic_pa            -[PREREQUISITE_FOR]->    real_time_pa
pa_automation            -[REDUCES]->             administrative_burden
pa_automation            -[USES]->                clinical_decision_support
pa_api                   -[BUILT_ON]->            fhir
pa_api                   -[IMPLEMENTS]->          davinci_pas
fhir                     -[ENABLES]->             pa_api
davinci_pas              -[BUILDS_ON]->           fhir
clinical_decision_support -[INTEGRATES]->         pa_workflow
clinical_decision_support -[SURFACES]->           pa_requirement
prior_auth_ckg           -[ENCODES]->             pa_workflow
prior_auth_ckg           -[ENABLES]->             pa_automation
step_therapy_exception   -[OVERRIDES]->           step_therapy
step_therapy_exception   -[GOVERNED_BY]->         cms_pa_rule
inappropriate_denial     -[TRIGGERS]->            appeal
independent_review_organization -[OVERRIDES]->    inappropriate_denial
specialty_pharmacy       -[DISPENSES]->           specialty_drug
specialty_pharmacy       -[REQUIRES]->            prior_authorization
concurrent_review        -[COMPONENT_OF]->        utilization_management
retrospective_review     -[COMPONENT_OF]->        utilization_management
pa_transparency          -[REDUCES]->             inappropriate_denial
