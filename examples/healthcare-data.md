## META
name: Healthcare Data
version: 1.0.0
domain: healthcare-data
description: Core concepts in healthcare data systems — from clinical entities and coding standards to payer logic, AI applications, and data governance.
nodes: 56
edges: 70
source: McCreary modeling-healthcare-data learning graph (UST SEIS corpus); ICD-10-CM, CPT, HIPAA, FHIR R4 standards
license: MIT

---

## NODES

[CONCEPT|graph_database|Graph Database
  |A database that uses nodes and edges as its primary data structure. Natively represents relationships without join tables. Superior to relational models for multi-hop healthcare queries such as drug interaction chains and referral networks.]

[CONCEPT|labeled_property_graph|Labeled Property Graph
  |Graph model where each node and edge carries a label (type) and arbitrary key-value properties. Used in Neo4j and healthcare knowledge graphs to encode clinical entities with rich metadata alongside relationship structure.]

[CONCEPT|relational_database|Relational Database
  |Table-based data storage organized by schemas and enforced foreign-key relationships. Dominant in legacy healthcare IT (Epic, Cerner). Struggles with multi-hop traversals that graph databases handle natively.]

[CONCEPT|database_schema|Database Schema
  |Formal definition of tables, columns, data types, and constraints in a relational system. In healthcare, schemas encode clinical data models such as HL7 FHIR, OMOP CDM, or payer claim formats.]

[CONCEPT|healthcare_system|Healthcare System
  |The organized network of payers, providers, patients, regulators, and institutions that delivers and finances medical care. Characterized by complex multi-party data flows, asymmetric incentives, and heavy regulatory burden.]

[CONCEPT|healthcare_cost|Healthcare Cost
  |Total expenditure for delivering or financing medical care. Driven by utilization volume, unit prices, and administrative overhead. U.S. healthcare spend exceeds 18% of GDP, with administrative costs estimated at 25–30%.]

[CONCEPT|fee_for_service|Fee-For-Service Model
  |Reimbursement model where providers are paid per procedure or visit. Creates volume incentives and is widely blamed for overutilization. Being displaced by value-based care contracting in commercial and Medicare markets.]

[CONCEPT|value_based_care|Value-Based Care
  |Reimbursement model tying provider payment to patient outcomes and cost efficiency rather than volume. Includes ACO models, bundled payments, and HEDIS quality metrics. Requires robust longitudinal data infrastructure.]

[CONCEPT|healthcare_payer|Healthcare Payer
  |Organization that finances medical care: commercial insurers (Aetna, BCBS), Medicare, Medicaid. Controls formularies, prior authorization policies, and claims adjudication. Primary source of administrative burden on providers.]

[CONCEPT|healthcare_provider|Healthcare Provider
  |Clinician or institution delivering patient care: physicians, hospitals, pharmacies. Subject to payer coverage rules, credentialing requirements, and documentation mandates that impose significant administrative overhead.]

[CONCEPT|healthcare_patient|Healthcare Patient
  |Individual receiving medical services. Central entity in clinical data models. Protected under HIPAA. Generates longitudinal data across encounters, prescriptions, labs, and claims that are often siloed across systems.]

[CONCEPT|electronic_health_record|Electronic Health Record (EHR)
  |Digital longitudinal record of a patient's clinical history: diagnoses, medications, labs, notes, and encounters. Mandated by HITECH Act. Dominant platforms: Epic (37% U.S. market), Oracle Cerner, MEDITECH.]

[CONCEPT|medical_coding_system|Medical Coding System
  |Standardized vocabulary for representing diagnoses, procedures, and drugs in billing and clinical data. Enables interoperability across payers and providers. Core systems: ICD, CPT, NDC, SNOMED CT, LOINC.]

[CONCEPT|icd_code|ICD Code
  |International Classification of Diseases code. ICD-10-CM has ~70,000 diagnosis codes. Used universally in U.S. claims for billing, epidemiology, and quality measurement. ICD-11 adoption is underway internationally.]

[CONCEPT|cpt_code|CPT Code
  |Current Procedural Terminology code. AMA-maintained vocabulary of ~10,000 codes for medical procedures and services. Required on all professional claims. Drives fee schedule pricing in Medicare and commercial contracts.]

[CONCEPT|drug_code|Drug Code
  |National Drug Code (NDC): 10-digit FDA identifier for each drug product. Used in pharmacy claims, formulary management, and drug interaction databases. Maps to RxNorm for clinical interoperability.]

[CONCEPT|medical_terminology|Medical Terminology
  |Controlled vocabularies enabling precise clinical communication: SNOMED CT (clinical concepts), LOINC (lab tests), RxNorm (medications), MeSH (literature indexing). Terminological precision prevents semantic ambiguity in data exchange.]

[CONCEPT|medical_encounter|Medical Encounter
  |A discrete interaction between a patient and provider: office visit, ER presentation, hospitalization, telehealth session. The primary unit of clinical activity. Generates claims, notes, orders, and results.]

[CONCEPT|patient_record|Patient Record
  |Longitudinal collection of clinical data for a single patient across encounters. Encompasses diagnoses, medications, labs, vitals, and notes. Aggregating records across systems requires master patient index (MPI) matching.]

[CONCEPT|patient_history|Patient History
  |Chronological account of a patient's past diagnoses, treatments, hospitalizations, allergies, and family history. Critical context for clinical decision-making; incompleteness is a major source of medical error.]

[CONCEPT|disease|Disease
  |Pathological condition with defined etiology, symptoms, and clinical course. Encoded via ICD codes for billing, SNOMED CT for clinical logic. Chronic diseases drive 90% of U.S. healthcare spend.]

[CONCEPT|diagnosis|Diagnosis
  |Clinical determination of a patient's disease or condition. Requires synthesis of history, physical exam, labs, and imaging. Triggers the treatment workflow and must be coded for reimbursement.]

[CONCEPT|treatment_plan|Treatment Plan
  |Provider-authored roadmap of interventions for a patient's condition: medications, procedures, referrals, lifestyle changes, follow-up schedule. Subject to clinical guideline adherence and payer coverage rules.]

[CONCEPT|prescription|Prescription
  |Clinician order authorizing a specific drug, dose, and duration for a patient. Generates a pharmacy claim. Subject to formulary rules, prior authorization requirements, and drug interaction screening.]

[CONCEPT|medication|Medication
  |A drug or therapeutic agent prescribed to treat, prevent, or manage a disease. Classified by drug class, mechanism, and formulary tier. Drug-drug and drug-disease interactions are critical safety concerns.]

[CONCEPT|drug_interaction|Drug Interaction
  |Pharmacokinetic or pharmacodynamic effect when two or more drugs are co-administered. Can reduce efficacy or cause adverse events. Screened via databases (Multum, Medi-Span) integrated into EHR prescribing workflows.]

[CONCEPT|adverse_event|Adverse Event
  |Unintended harmful outcome from a medication or procedure. Includes adverse drug reactions (ADRs), hospital-acquired infections, and procedural complications. Reportable to FDA MedWatch and institutional safety systems.]

[CONCEPT|lab_test|Lab Test
  |Ordered clinical measurement: blood panel, urinalysis, pathology, microbiology culture. Results are the primary quantitative evidence in clinical decision-making. LOINC codes standardize lab test identification.]

[CONCEPT|lab_result|Lab Result
  |Quantitative or qualitative output of a lab test. Includes value, unit, reference range, and interpretive flag (H/L/Critical). Abnormal results trigger clinical alerts and may initiate treatment changes.]

[CONCEPT|patient_journey|Patient Journey
  |End-to-end sequence of encounters, decisions, treatments, and outcomes a patient experiences across a condition episode. Multi-hop data structure: maps diagnosis → referral → treatment → outcome over months or years.]

[CONCEPT|chronic_disease_management|Chronic Disease Management
  |Coordinated, longitudinal care program for conditions such as diabetes, CHF, COPD, and CKD. Requires proactive outreach, care gap identification, medication adherence monitoring, and cross-provider coordination.]

[CONCEPT|primary_care_provider|Primary Care Provider (PCP)
  |Generalist physician (MD/DO), NP, or PA who serves as a patient's first point of contact and longitudinal care coordinator. Manages referrals, preventive care, and chronic disease follow-up. The hub of the patient's care network.]

[CONCEPT|specialist_provider|Specialist Provider
  |Clinician with expertise in a specific organ system or disease area: cardiologist, oncologist, endocrinologist. Typically accessed via referral from PCP. Generates higher-cost encounters and is subject to network tiering by payers.]

[CONCEPT|referral|Referral
  |PCP authorization directing a patient to a specialist or service. Some payers require referral authorization for specialist visits. Referral networks form directed graphs analyzable for care coordination quality.]

[CONCEPT|clinical_guideline|Clinical Guideline
  |Evidence-based recommendation from professional bodies (ACC/AHA, USPSTF, IDSA) specifying diagnosis criteria, treatment protocols, and screening intervals. Basis for prior authorization criteria and quality measure benchmarks.]

[CONCEPT|evidence_based_medicine|Evidence-Based Medicine
  |Practice paradigm integrating best available research evidence, clinical expertise, and patient values in treatment decisions. Randomized controlled trials and systematic reviews are the highest-grade evidence sources.]

[CONCEPT|insurance_claim|Insurance Claim
  |Formal request from a provider to a payer for reimbursement of services rendered. Contains patient ID, provider NPI, date of service, diagnosis codes (ICD), procedure codes (CPT/HCPCS), and charge amounts.]

[CONCEPT|claim_adjudication|Claim Adjudication
  |Payer's automated processing of a submitted claim: eligibility verification, coverage check, medical necessity review, fee schedule application, and payment calculation. Drives the revenue cycle for providers.]

[CONCEPT|claim_denial|Claim Denial
  |Payer decision to reject or reduce a claim payment. Common reasons: lack of prior authorization, medical necessity not established, incorrect coding, eligibility mismatch. Costs providers ~$25B/year in rework.]

[CONCEPT|insurance_policy|Insurance Policy
  |Contract between a payer and enrollee specifying covered services, cost-sharing terms, network restrictions, and benefit limits. The authoritative source for coverage determinations and prior authorization requirements.]

[CONCEPT|coverage|Coverage
  |Specific services, drugs, or supplies a policy will pay for under defined conditions. Coverage decisions depend on formulary tier, medical necessity criteria, network participation, and applicable benefit limits.]

[CONCEPT|formulary|Formulary
  |Payer's preferred drug list organized into tiers by cost-sharing level. Determines which drugs are covered, at what copay, and which require prior authorization or step therapy before approval.]

[CONCEPT|formulary_rule|Formulary Rule
  |Specific policy governing drug coverage: tier placement, quantity limits, age restrictions, step therapy requirements, and prior authorization triggers. Implemented in pharmacy benefit management systems.]

[CONCEPT|pharmacy_benefit_manager|Pharmacy Benefit Manager (PBM)
  |Third-party administrator managing prescription drug benefits for payers: formulary design, drug rebate negotiation, claims adjudication, and pharmacy network management. Largest PBMs: CVS/Caremark, Express Scripts, OptumRx.]

[CONCEPT|prior_authorization|Prior Authorization
  |Payer requirement for provider approval before a drug or procedure is covered. Imposes clinical criteria, step therapy, and documentation requirements. AMA data: 94% of physicians report PA causes care delays.]

[CONCEPT|medical_necessity|Medical Necessity
  |Payer standard for whether a service is appropriate, evidence-based, and not experimental for a given condition. The primary basis for prior authorization approval or denial. Definitions vary by payer and are often opaque to providers.]

[CONCEPT|healthcare_fraud|Healthcare Fraud
  |Intentional misrepresentation in claims, including upcoding, phantom billing, unbundling, and identity theft. Estimated at $100B+ annually in the U.S. Prosecuted under False Claims Act and anti-kickback statutes.]

[CONCEPT|fraud_detection|Fraud Detection
  |Analytical methods for identifying fraudulent billing patterns: network analysis (provider clustering), anomaly detection, predictive models. CMS uses Fraud Prevention System (FPS) to screen claims in real time.]

[CONCEPT|anomaly_detection|Anomaly Detection
  |Statistical or ML method identifying data points that deviate significantly from expected patterns. In healthcare billing, flags unusual procedure volumes, improbable code combinations, or geographic billing outliers.]

[CONCEPT|large_language_model|Large Language Model (LLM)
  |Foundation model trained on text corpora with billions of parameters. Enables natural language querying of clinical records, guideline summarization, and prior authorization letter generation. Requires grounding to prevent hallucination.]

[CONCEPT|knowledge_graph|Knowledge Graph
  |Structured representation of domain entities and their relationships. In healthcare: encodes drug-disease-gene relationships (DrugBank, OMIM), clinical pathways, and payer rules. Enables multi-hop reasoning that RAG cannot perform.]

[CONCEPT|clinical_decision_support|Clinical Decision Support (CDS)
  |Software that uses patient data and clinical knowledge to assist provider decisions: drug alerts, guideline reminders, diagnostic suggestions. Mandated in certified EHRs under ONC rules. Accuracy depends on knowledge base quality.]

[CONCEPT|risk_stratification|Risk Stratification
  |Predictive analytics process categorizing patients by likelihood of future high-cost events: hospitalizations, ED visits, disease progression. Enables payers and ACOs to direct care management resources proactively.]

[CONCEPT|hipaa|HIPAA
  |Health Insurance Portability and Accountability Act (1996). Establishes federal privacy and security standards for protected health information. Sets breach notification requirements and imposes civil and criminal penalties for violations.]

[CONCEPT|protected_health_information|Protected Health Information (PHI)
  |Any individually identifiable health information held by a covered entity: name, SSN, diagnosis, dates, geographic data below state level. Subject to HIPAA Privacy and Security Rules. De-identification requires removal of 18 identifiers.]

[CONCEPT|data_governance_framework|Data Governance Framework
  |Policies, standards, roles, and processes ensuring healthcare data is accurate, consistent, secure, and used appropriately. Encompasses data quality, lineage, stewardship, and compliance with HIPAA, state law, and payer contracts.]

---

## EDGES

graph_database           -[CONTRASTS_WITH]->      relational_database
labeled_property_graph   -[INSTANCE_OF]->         graph_database
relational_database      -[DEFINED_BY]->          database_schema
healthcare_system        -[COMPONENT_OF]->        healthcare_payer
healthcare_system        -[COMPONENT_OF]->        healthcare_provider
healthcare_system        -[COMPONENT_OF]->        healthcare_patient
healthcare_cost          -[QUANTIFIED_BY]->       insurance_claim
fee_for_service          -[CONTRASTS_WITH]->      value_based_care
fee_for_service          -[CAUSES]->              healthcare_cost
value_based_care         -[REQUIRES]->            risk_stratification
healthcare_payer         -[GOVERNS]->             formulary
healthcare_payer         -[GOVERNS]->             prior_authorization
healthcare_payer         -[OUTPUTS]->             claim_adjudication
healthcare_provider      -[GENERATES]->           insurance_claim
healthcare_provider      -[GENERATES]->           prescription
healthcare_patient       -[OWNS]->                patient_record
electronic_health_record -[STORES]->              patient_record
electronic_health_record -[STORES]->              lab_result
medical_coding_system    -[COMPONENT_OF]->        insurance_claim
icd_code                 -[INSTANCE_OF]->         medical_coding_system
cpt_code                 -[INSTANCE_OF]->         medical_coding_system
drug_code                -[INSTANCE_OF]->         medical_coding_system
medical_terminology      -[ENABLES]->             medical_coding_system
medical_encounter        -[GENERATES]->           insurance_claim
medical_encounter        -[INVOLVES]->            healthcare_provider
medical_encounter        -[INVOLVES]->            healthcare_patient
patient_record           -[CONTAINS]->            patient_history
patient_record           -[CONTAINS]->            lab_result
patient_history          -[INFORMS]->             diagnosis
disease                  -[ENCODED_BY]->          icd_code
disease                  -[MANAGED_BY]->          chronic_disease_management
diagnosis                -[TRIGGERS]->            treatment_plan
treatment_plan           -[INCLUDES]->            prescription
treatment_plan           -[GUIDED_BY]->           clinical_guideline
prescription             -[REFERENCES]->          drug_code
prescription             -[SUBJECT_TO]->          formulary_rule
medication               -[CLASSIFIED_BY]->       drug_code
medication               -[CAUSES]->              drug_interaction
medication               -[CAUSES]->              adverse_event
drug_interaction         -[PREVENTS]->            adverse_event
lab_test                 -[PRODUCES]->            lab_result
lab_result               -[INFORMS]->             diagnosis
patient_journey          -[BUILT_FROM]->          medical_encounter
chronic_disease_management -[REQUIRES]->          patient_history
primary_care_provider    -[INSTANCE_OF]->         healthcare_provider
specialist_provider      -[INSTANCE_OF]->         healthcare_provider
referral                 -[CONNECTS]->            primary_care_provider
referral                 -[CONNECTS]->            specialist_provider
clinical_guideline       -[BUILDS_ON]->           evidence_based_medicine
clinical_guideline       -[DEFINES]->             medical_necessity
insurance_claim          -[PROCESSED_BY]->        claim_adjudication
claim_adjudication       -[OUTPUTS]->             claim_denial
insurance_policy         -[DEFINES]->             coverage
coverage                 -[INCLUDES]->            formulary
formulary                -[IMPLEMENTS]->          formulary_rule
formulary_rule           -[GOVERNS]->             prior_authorization
pharmacy_benefit_manager -[MANAGES]->             formulary
prior_authorization      -[EVALUATES]->           medical_necessity
medical_necessity        -[DEFINED_BY]->          clinical_guideline
healthcare_fraud         -[DETECTED_BY]->         fraud_detection
fraud_detection          -[USES]->                anomaly_detection
anomaly_detection        -[USES]->                knowledge_graph
large_language_model     -[IMPLEMENTS]->          clinical_decision_support
knowledge_graph          -[ENABLES]->             clinical_decision_support
clinical_decision_support -[INFORMS]->            diagnosis
risk_stratification      -[USES]->                large_language_model
hipaa                    -[GOVERNS]->             protected_health_information
protected_health_information -[STORED_IN]->       electronic_health_record
data_governance_framework -[GOVERNS]->            patient_record
data_governance_framework -[REQUIRES]->           hipaa
