## META
name: Regulatory Compliance
version: 1.0.0
domain: regulatory-compliance
description: Major enterprise regulatory frameworks covering data privacy, financial controls, healthcare, banking resilience, and payment security.
nodes: 50
edges: 97
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|gdpr|GDPR (General Data Protection Regulation)
  |EU Regulation 2016/679 that governs how organizations collect, process, and store personal data of EU residents, regardless of where the organization is based. Enforced by national Data Protection Authorities with fines up to €20M or 4% of global annual turnover.]

[CONCEPT|hipaa|HIPAA (Health Insurance Portability and Accountability Act)
  |US federal law establishing national standards for protecting sensitive patient health information. Applies to covered entities (providers, payers, clearinghouses) and their business associates. Enforced by the HHS Office for Civil Rights.]

[CONCEPT|sox|SOX (Sarbanes-Oxley Act)
  |US federal law enacted in 2002 following Enron and WorldCom scandals, requiring publicly traded companies to maintain rigorous internal financial controls and mandating executive certification of financial statements. Enforced by the SEC and PCAOB.]

[CONCEPT|basel_iii|Basel III / IV
  |International banking regulatory framework developed by the Basel Committee on Banking Supervision, requiring banks to maintain adequate capital buffers, liquidity reserves, and leverage limits to withstand financial stress. Full implementation by January 2025.]

[CONCEPT|dora|DORA (Digital Operational Resilience Act)
  |EU Regulation 2022/2554 requiring financial entities to demonstrate resilience against ICT disruptions. Mandates ICT risk management, incident reporting, resilience testing, and oversight of third-party ICT providers. Applicable from January 2025.]

[CONCEPT|ccpa|CCPA/CPRA (California Consumer Privacy Act / Privacy Rights Act)
  |California state law granting consumers rights over their personal information including the right to know, delete, opt out of sale, and correct data. CPRA (2023) strengthened enforcement and added sensitive PI protections, establishing the California Privacy Protection Agency.]

[CONCEPT|pci_dss|PCI DSS (Payment Card Industry Data Security Standard)
  |A set of security standards developed by the PCI Security Standards Council (Visa, Mastercard, Amex, Discover) that any entity storing, processing, or transmitting cardholder data must comply with. Non-compliance can result in loss of card processing rights.]

[CONCEPT|data_subject_rights|Data Subject Rights
  |Rights granted to individuals under GDPR including access, rectification, erasure, portability, restriction of processing, and the right to object. Organizations must respond to data subject requests within 30 days and maintain workflows to fulfill them.]

[CONCEPT|consent|Consent
  |Under GDPR, one of six lawful bases for processing personal data. Consent must be freely given, specific, informed, and unambiguous — demonstrated by a clear affirmative action. It must be as easy to withdraw as to give.]

[CONCEPT|phi|PHI (Protected Health Information)
  |Any individually identifiable health information held or transmitted by a HIPAA-covered entity or business associate, in any form. Includes 18 identifiers such as name, geographic data, dates, phone numbers, and account numbers.]

[CONCEPT|baa|Business Associate Agreement (BAA)
  |A legally required contract under HIPAA between a covered entity and a third-party vendor (business associate) that handles PHI. The BAA specifies permitted uses of PHI, security obligations, and breach notification requirements.]

[CONCEPT|breach_notification|Breach Notification
  |The legal obligation to notify affected individuals, regulatory authorities, and in some cases the public when a breach of personal or health data occurs. Timelines and scope vary by regulation — GDPR requires 72 hours to the DPA, HIPAA requires 60 days to individuals.]

[CONCEPT|internal_controls|Internal Controls
  |Processes and procedures implemented by an organization to ensure the reliability of financial reporting, compliance with laws, and effectiveness of operations. SOX Section 404 requires management to assess and certify the effectiveness of internal controls annually.]

[CONCEPT|audit_trail|Audit Trail
  |A chronological record of system activities that enables reconstruction and examination of events. Required by SOX to demonstrate that financial transactions cannot be altered without detection; must be tamper-evident and retained for specified periods.]

[CONCEPT|capital_ratio|Capital Ratio
  |Under Basel III, the ratio of a bank's capital to its risk-weighted assets. The Common Equity Tier 1 (CET1) minimum is 4.5%, plus a 2.5% conservation buffer. Ensures banks can absorb losses without becoming insolvent.]

[CONCEPT|liquidity_coverage|Liquidity Coverage Ratio (LCR)
  |Basel III requirement that banks hold enough High Quality Liquid Assets (HQLA) to survive a 30-day stress scenario. Forces banks to maintain liquid asset buffers against sudden funding withdrawals, preventing bank runs from causing systemic failure.]

[CONCEPT|ict_risk|ICT Risk Management
  |Under DORA, a comprehensive framework financial entities must maintain for managing risks from information and communications technology, covering identification, protection, detection, response, and recovery of ICT systems and data.]

[CONCEPT|incident_reporting|Incident Reporting
  |The obligation to notify regulators of significant ICT disruptions or data breaches within prescribed timeframes. DORA requires major ICT-related incidents to be reported to financial supervisors; GDPR requires personal data breaches reported to the DPA within 72 hours.]

[CONCEPT|third_party_risk|Third-Party Risk
  |The exposure that arises from relying on external vendors, cloud providers, or service partners who have access to systems or data. DORA mandates contractual arrangements for ICT third parties; HIPAA requires BAAs; GDPR requires Data Processing Agreements.]

[CONCEPT|tokenization|Tokenization
  |Replacing sensitive data — such as a 16-digit card number — with a non-sensitive placeholder (token) that has no exploitable value outside a controlled environment. Under PCI DSS, tokenization is accepted as a method to reduce the cardholder data environment scope.]

[CONCEPT|cardholder_data|Cardholder Data
  |The full primary account number (PAN) and any combination of cardholder name, expiration date, and service code. PCI DSS controls apply wherever cardholder data is stored, processed, or transmitted. Minimizing its footprint is a core compliance strategy.]

[CONCEPT|data_retention|Data Retention
  |Policies governing how long personal or regulated data is kept before it must be securely deleted. GDPR requires data not be kept longer than necessary for its stated purpose; HIPAA mandates 6-year medical record retention; SOX requires 7 years for audit records.]

[CONCEPT|right_to_erasure|Right to Erasure (Right to Be Forgotten)
  |GDPR Article 17 right allowing individuals to request deletion of their personal data when it is no longer necessary, consent is withdrawn, or the processing is unlawful. Organizations must propagate deletion to third-party processors within applicable timeframes.]

[CONCEPT|data_portability|Data Portability
  |GDPR Article 20 right allowing individuals to receive their personal data in a structured, commonly used, machine-readable format and transmit it to another controller. Promotes competition and prevents data lock-in by dominant platforms.]

[CONCEPT|dpa|Data Protection Authority (DPA)
  |National supervisory authorities in each EU member state responsible for enforcing GDPR. They investigate complaints, conduct audits, impose fines, and can issue temporary or permanent bans on data processing. Ireland's DPC and France's CNIL are among the most active.]

[CONCEPT|minimum_necessary|Minimum Necessary Standard
  |HIPAA requirement that covered entities and business associates limit uses and disclosures of PHI to the minimum amount necessary to accomplish the intended purpose. Prevents overbroad data sharing and reduces breach impact.]

[CONCEPT|cfo_certification|CFO/CEO Certification
  |SOX Section 302 and 906 require the CEO and CFO to personally certify in each quarterly and annual SEC filing that financial statements are accurate and that internal controls are effective. Personal criminal liability attaches to false certifications.]

[CONCEPT|stress_testing|Stress Testing
  |Supervisory exercises required under Basel III/IV in which banks model their financial performance under severe but plausible economic scenarios. Results inform capital planning, reveal vulnerabilities, and are published to maintain market confidence.]

[CONCEPT|leverage_ratio|Leverage Ratio
  |Basel III requirement that banks maintain Tier 1 capital of at least 3% of total assets (not risk-weighted). Acts as a non-risk-based backstop to prevent excessive balance sheet leverage that amplified losses in the 2008 financial crisis.]

[CONCEPT|opt_out_right|Opt-Out Right
  |CCPA/CPRA right allowing California consumers to direct businesses not to sell or share their personal information. Businesses must honor opt-out requests within 15 days and display a clear "Do Not Sell or Share My Personal Information" link.]

[CONCEPT|data_deletion|Data Deletion Right
  |CCPA/CPRA right allowing consumers to request that a business delete their personal information, subject to exceptions for legal obligations and service delivery. Similar to GDPR's right to erasure but with California-specific scope and exceptions.]

[CONCEPT|sensitive_pi|Sensitive Personal Information
  |CPRA category of personal information requiring heightened protection, including Social Security numbers, financial account data, health and genetic data, biometrics, precise geolocation, and racial or ethnic origin. Consumers have the right to limit its use.]

[CONCEPT|compliance_program|Compliance Program
  |An organization-wide framework of policies, procedures, controls, training, and monitoring designed to ensure adherence to applicable regulatory requirements. Effective compliance programs include a designated compliance officer, risk assessment, and ongoing auditing.]

[CONCEPT|regulatory_audit|Regulatory Audit
  |An examination conducted by a regulator or authorized third-party auditor to verify that an organization's practices, controls, and records conform to regulatory requirements. Outcomes can include findings, corrective action plans, consent orders, or fines.]

[CONCEPT|penalty_framework|Penalty Framework
  |The structured schedule of financial sanctions and other enforcement actions regulators can impose for non-compliance. GDPR: up to €20M or 4% global revenue. HIPAA: up to $1.9M/violation/year. PCI DSS: $5K–$100K/month. Severity tiers incentivize investment in compliance.]

[CONCEPT|vendor_risk|Vendor Risk Management
  |The process of identifying, assessing, and mitigating risks introduced by third-party suppliers and service providers. Includes due diligence questionnaires, contract controls, ongoing monitoring, and exit planning. Required explicitly by DORA, HIPAA, and GDPR.]

[CONCEPT|network_segmentation|Network Segmentation
  |The practice of dividing a network into isolated zones to contain breaches and limit the scope of regulated data exposure. PCI DSS requires segmentation to restrict the cardholder data environment from other network zones, reducing compliance scope.]

[CONCEPT|data_processing_agreement|Data Processing Agreement (DPA/DPA Contract)
  |A legally required contract under GDPR Article 28 between a data controller and a data processor specifying the scope, nature, purpose, and duration of processing, as well as processor obligations including security measures and sub-processor disclosure.]

[CONCEPT|lawful_basis|Lawful Basis for Processing
  |GDPR requires one of six lawful bases to process personal data: consent, contract, legal obligation, vital interests, public task, or legitimate interests. Controllers must document their chosen basis and inform data subjects.]

[CONCEPT|data_minimization|Data Minimization
  |GDPR principle requiring that only the personal data necessary for the specified purpose be collected and processed. Limits breach exposure, simplifies compliance, and reinforces the broader privacy-by-design philosophy.]

[CONCEPT|privacy_by_design|Privacy by Design
  |GDPR Article 25 requirement that data protection be embedded into systems and processes from the outset rather than added as an afterthought. Includes default privacy settings, minimal data collection, and purpose limitation built into product architecture.]

[CONCEPT|scoping|PCI DSS Scoping
  |The process of identifying all system components that store, process, or transmit cardholder data, and all systems that could impact their security. Accurate scoping determines compliance obligations; segmentation and tokenization reduce scope.]

[CONCEPT|penetration_testing_pci|PCI DSS Penetration Testing
  |PCI DSS Requirement 11.4 mandates annual penetration testing of the cardholder data environment and network segmentation controls. Must be performed by qualified internal staff or an approved third party, with findings remediated and retested.]

[CONCEPT|hipaa_security_rule|HIPAA Security Rule
  |45 CFR Parts 164.302–318 establishing national standards for protecting electronic PHI (ePHI). Organized into administrative, physical, and technical safeguards. Covered entities must implement required safeguards and assess addressable ones based on risk.]

[CONCEPT|sox_section_404|SOX Section 404
  |The most operationally demanding SOX provision, requiring management's annual assessment of internal control over financial reporting (ICFR) and an independent auditor attestation for large accelerated filers. Drives significant investment in ERP controls and IT general controls.]

[CONCEPT|dora_testing|DORA Resilience Testing
  |DORA Article 26 requires financial entities to conduct advanced Threat Led Penetration Testing (TLPT) at least every three years, coordinated with financial supervisors. Tests the real resilience of production systems against realistic attack scenarios.]

[CONCEPT|72_hour_window|72-Hour Notification Window
  |GDPR Article 33 requirement to notify the competent DPA within 72 hours of becoming aware of a personal data breach that poses a risk to individuals. If notification is delayed, the controller must explain why. The clock starts when a controller-level employee becomes aware.]

[CONCEPT|right_to_access|Right of Access
  |GDPR Article 15 allows data subjects to obtain confirmation of whether their personal data is being processed and receive a copy of it along with supplementary information about the processing — purposes, categories, recipients, and retention periods.]

[CONCEPT|data_controller|Data Controller
  |The natural or legal person that determines the purposes and means of processing personal data. Controllers bear primary GDPR accountability: they must appoint DPOs where required, conduct DPIAs, maintain records of processing activities, and respond to data subject rights.]

[CONCEPT|data_processor|Data Processor
  |An entity that processes personal data on behalf of and under instruction from a data controller. Processors have direct GDPR obligations including security, breach notification to the controller, sub-processor controls, and deletion upon instruction.]

---

## EDGES

gdpr                     -[MANDATES]->               breach_notification
gdpr                     -[MANDATES]->               data_subject_rights
gdpr                     -[MANDATES]->               consent
gdpr                     -[MANDATES]->               data_minimization
gdpr                     -[MANDATES]->               privacy_by_design
gdpr                     -[DEFINES]->                right_to_erasure
gdpr                     -[DEFINES]->                data_portability
gdpr                     -[DEFINES]->                right_to_access
gdpr                     -[DEFINES]->                lawful_basis
gdpr                     -[GOVERNS]->                data_controller
gdpr                     -[GOVERNS]->                data_processor
gdpr                     -[ENFORCED_BY]->            dpa
gdpr                     -[QUANTIFIED_BY]->          penalty_framework
gdpr                     -[REQUIRES]->               data_processing_agreement

hipaa                    -[DEFINES]->                phi
hipaa                    -[REQUIRES]->               baa
hipaa                    -[MANDATES]->               breach_notification
hipaa                    -[MANDATES]->               minimum_necessary
hipaa                    -[COMPONENT_OF]->           hipaa_security_rule
hipaa                    -[QUANTIFIED_BY]->          penalty_framework
hipaa                    -[REQUIRES]->               third_party_risk
hipaa                    -[MANDATES]->               data_retention

sox                      -[MANDATES]->               internal_controls
sox                      -[MANDATES]->               audit_trail
sox                      -[MANDATES]->               cfo_certification
sox                      -[COMPONENT_OF]->           sox_section_404
sox                      -[REQUIRES]->               regulatory_audit
sox                      -[MANDATES]->               data_retention

basel_iii                -[REQUIRES]->               capital_ratio
basel_iii                -[REQUIRES]->               liquidity_coverage
basel_iii                -[REQUIRES]->               leverage_ratio
basel_iii                -[REQUIRES]->               stress_testing
basel_iii                -[QUANTIFIED_BY]->          penalty_framework

dora                     -[MANDATES]->               ict_risk
dora                     -[MANDATES]->               incident_reporting
dora                     -[MANDATES]->               third_party_risk
dora                     -[MANDATES]->               vendor_risk
dora                     -[REQUIRES]->               dora_testing
dora                     -[QUANTIFIED_BY]->          penalty_framework

ccpa                     -[DEFINES]->                opt_out_right
ccpa                     -[DEFINES]->                data_deletion
ccpa                     -[DEFINES]->                sensitive_pi
ccpa                     -[REQUIRES]->               compliance_program
ccpa                     -[QUANTIFIED_BY]->          penalty_framework

pci_dss                  -[REQUIRES]->               tokenization
pci_dss                  -[GOVERNS]->                cardholder_data
pci_dss                  -[REQUIRES]->               network_segmentation
pci_dss                  -[REQUIRES]->               scoping
pci_dss                  -[REQUIRES]->               penetration_testing_pci
pci_dss                  -[QUANTIFIED_BY]->          penalty_framework

breach_notification      -[REQUIRES]->               72_hour_window
breach_notification      -[TRIGGERS]->               regulatory_audit
breach_notification      -[GOVERNED_BY]->            dpa

data_subject_rights      -[COMPONENT_OF]->           right_to_erasure
data_subject_rights      -[COMPONENT_OF]->           data_portability
data_subject_rights      -[COMPONENT_OF]->           right_to_access
data_subject_rights      -[ENABLED_BY]->             compliance_program

consent                  -[INSTANCE_OF]->            lawful_basis
lawful_basis             -[PREREQUISITE_FOR]->       data_minimization

phi                      -[REQUIRES]->               baa
phi                      -[GOVERNED_BY]->            hipaa_security_rule
phi                      -[PROTECTED_BY]->           minimum_necessary

baa                      -[GOVERNS]->                third_party_risk
baa                      -[CONTRASTS_WITH]->         data_processing_agreement

internal_controls        -[REQUIRES]->               audit_trail
internal_controls        -[COMPONENT_OF]->           sox_section_404
internal_controls        -[VALIDATED_BY]->           regulatory_audit

audit_trail              -[GOVERNED_BY]->            data_retention
audit_trail              -[REQUIRED_BY]->            sox_section_404

tokenization             -[PREVENTS]->               cardholder_data
tokenization             -[REDUCES]->                scoping

cardholder_data          -[GOVERNED_BY]->            pci_dss
cardholder_data          -[PROTECTED_BY]->           network_segmentation

data_retention           -[CONTRASTS_WITH]->         right_to_erasure
data_retention           -[GOVERNED_BY]->            compliance_program

ict_risk                 -[REQUIRES]->               incident_reporting
ict_risk                 -[MITIGATED_BY]->           vendor_risk
ict_risk                 -[TESTED_BY]->              dora_testing

third_party_risk         -[MITIGATED_BY]->           vendor_risk
third_party_risk         -[GOVERNED_BY]->            baa
third_party_risk         -[GOVERNED_BY]->            data_processing_agreement

compliance_program       -[REQUIRES]->               regulatory_audit
compliance_program       -[PREVENTS]->               penalty_framework
compliance_program       -[COMPONENT_OF]->           internal_controls

vendor_risk              -[INSTANCE_OF]->            third_party_risk
vendor_risk              -[MITIGATED_BY]->           compliance_program

data_controller          -[REQUIRES]->               data_processor
data_controller          -[MANDATES]->               data_processing_agreement
data_processor           -[GOVERNED_BY]->            data_processing_agreement

privacy_by_design        -[ENABLES]->                data_minimization
privacy_by_design        -[PREREQUISITE_FOR]->       consent

network_segmentation     -[REDUCES]->                scoping
network_segmentation     -[PREVENTS]->               cardholder_data

sox_section_404          -[REQUIRES]->               cfo_certification
sox_section_404          -[REQUIRES]->               internal_controls

dora_testing             -[VALIDATES]->              ict_risk
dora_testing             -[INSTANCE_OF]->            penetration_testing_pci
