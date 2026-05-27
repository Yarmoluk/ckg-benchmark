## META
name: Cybersecurity
version: 1.0.0
domain: cybersecurity
description: Enterprise cybersecurity concepts spanning attack vectors, defense mechanisms, frameworks, and incident response.
nodes: 51
edges: 121
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|threat_actor|Threat Actor
  |An individual, group, or state-sponsored entity that initiates attacks against systems or data. Threat actors are categorized by motivation (financial, espionage, disruption), capability, and targeting patterns, which inform threat modeling decisions.]

[CONCEPT|phishing|Phishing
  |A social engineering attack delivered via email, SMS, or voice that impersonates a trusted entity to trick recipients into revealing credentials or executing malware. Phishing is the most common initial access vector in enterprise breaches.]

[CONCEPT|social_engineering|Social Engineering
  |Manipulation of human psychology to bypass security controls without exploiting technical vulnerabilities. Techniques include pretexting, baiting, vishing, and quid pro quo attacks. Effective because humans are often the weakest link in a security chain.]

[CONCEPT|credential_theft|Credential Theft
  |The acquisition of authentication material — usernames, passwords, session tokens, or cryptographic keys — through phishing, keylogging, or memory scraping. Stolen credentials are the primary mechanism for initial foothold establishment.]

[CONCEPT|malware|Malware
  |Malicious software designed to disrupt, damage, or gain unauthorized access to systems. Categories include viruses, trojans, worms, spyware, and adware. Delivered via phishing attachments, drive-by downloads, or supply chain compromise.]

[CONCEPT|ransomware|Ransomware
  |Malware that encrypts victim files and demands payment for the decryption key. Modern ransomware operations use double extortion — also exfiltrating data and threatening to publish it — to increase leverage and ransom compliance rates.]

[CONCEPT|zero_day|Zero-Day Exploit
  |A cyberattack that targets a previously unknown vulnerability for which no vendor patch exists. Zero-days are highly valuable because defenders have zero days to prepare; they are typically used by nation-state actors or sold on exploit markets.]

[CONCEPT|vulnerability|Vulnerability
  |A flaw in software, hardware, or configuration that could be exploited to compromise confidentiality, integrity, or availability. Vulnerabilities are disclosed via CVE identifiers and scored by severity using the CVSS scoring system.]

[CONCEPT|cve|CVE (Common Vulnerabilities and Exposures)
  |A standardized identifier assigned to a publicly known vulnerability, formatted as CVE-YEAR-NNNNN. CVE IDs enable consistent reference across vendor advisories, security tools, and patch management systems.]

[CONCEPT|sql_injection|SQL Injection
  |An injection attack in which malicious SQL statements are inserted into an input field that is executed against a database. Allows attackers to read, modify, or delete database contents; one of the OWASP Top 10 most critical web application risks.]

[CONCEPT|xss|Cross-Site Scripting (XSS)
  |A web vulnerability where an attacker injects malicious scripts into content delivered to other users' browsers. Stored XSS persists in the database; reflected XSS is triggered via a crafted URL. Enables session hijacking and credential theft.]

[CONCEPT|csrf|Cross-Site Request Forgery (CSRF)
  |An attack that tricks an authenticated user's browser into submitting unauthorized requests to a web application. Exploits the browser's automatic cookie inclusion to forge actions on behalf of the victim without their knowledge.]

[CONCEPT|supply_chain_attack|Supply Chain Attack
  |A compromise that targets a trusted software vendor, build pipeline, or third-party library to inject malicious code into products distributed to downstream customers. The SolarWinds and XZ Utils incidents are canonical examples.]

[CONCEPT|lateral_movement|Lateral Movement
  |Techniques used by an attacker after initial compromise to traverse a network and reach additional systems or higher-value targets. Methods include pass-the-hash, remote services exploitation, and credential reuse across systems.]

[CONCEPT|privilege_escalation|Privilege Escalation
  |The process of gaining elevated access rights beyond what was initially obtained — moving from a standard user account to administrator or SYSTEM-level access. Required to perform most high-impact actions within a compromised environment.]

[CONCEPT|data_exfiltration|Data Exfiltration
  |The unauthorized transfer of sensitive data from a compromised environment to attacker-controlled infrastructure. Common channels include DNS tunneling, HTTPS beaconing, and cloud storage uploads to blend with legitimate traffic.]

[CONCEPT|apt|Advanced Persistent Threat (APT)
  |A sophisticated, long-term intrusion campaign typically conducted by nation-state or state-sponsored actors who maintain persistent access to a target network over months or years to achieve intelligence or sabotage objectives.]

[CONCEPT|ioc|Indicator of Compromise (IOC)
  |Artifacts observed on a network or system that indicate a potential intrusion — such as malicious IP addresses, file hashes, domain names, or registry keys. IOCs are shared via threat intelligence feeds to enable proactive detection.]

[CONCEPT|threat_intelligence|Threat Intelligence
  |Analyzed, contextualized information about adversary tactics, techniques, and procedures (TTPs) that helps defenders anticipate and counter attacks. Consumed as IOC feeds, finished intelligence reports, or integrated into SIEM and EDR platforms.]

[CONCEPT|kill_chain|Cyber Kill Chain
  |A model developed by Lockheed Martin describing the seven stages of a cyberattack: Reconnaissance, Weaponization, Delivery, Exploitation, Installation, Command and Control, and Actions on Objectives. Breaking any link disrupts the attack.]

[CONCEPT|credential_stuffing|Credential Stuffing
  |An automated attack that uses large lists of username-password pairs — obtained from prior data breaches — to attempt login on other services. Succeeds because users reuse passwords across multiple accounts.]

[CONCEPT|man_in_the_middle|Man-in-the-Middle Attack
  |An attack where the adversary secretly intercepts and potentially alters communications between two parties who believe they are communicating directly. Enabled by ARP spoofing, rogue Wi-Fi access points, or SSL stripping.]

[CONCEPT|unauthorized_access|Unauthorized Access
  |Access to systems, data, or resources without permission from the owner. The proximate consequence of successful credential theft or exploit execution; triggers incident response and breach notification obligations.]

[CONCEPT|anomalous_behavior|Anomalous Behavior
  |Activity that deviates significantly from an established baseline of normal user or system behavior. SIEM and UBA tools flag anomalous behavior — such as off-hours logins or large data transfers — as potential indicators of compromise.]

[CONCEPT|firewall|Firewall
  |A network security device that monitors and filters incoming and outgoing traffic based on predefined rules. Next-generation firewalls (NGFW) add deep packet inspection, application awareness, and intrusion prevention capabilities.]

[CONCEPT|ids_ips|IDS/IPS (Intrusion Detection/Prevention System)
  |Network security controls that analyze traffic for attack signatures or anomalies. IDS alerts on detected threats; IPS actively blocks them. Positioned inline or at network chokepoints to cover east-west and north-south traffic.]

[CONCEPT|siem|SIEM (Security Information and Event Management)
  |A platform that aggregates, normalizes, and correlates log and event data from across the enterprise to detect security incidents. SIEM enables real-time alerting, historical investigation, and compliance reporting from a centralized console.]

[CONCEPT|waf|Web Application Firewall (WAF)
  |A security control that filters HTTP/HTTPS traffic to and from a web application, blocking common attacks such as SQL injection, XSS, and CSRF before they reach the application server. Can operate in detection-only or blocking mode.]

[CONCEPT|mfa|Multi-Factor Authentication (MFA)
  |An authentication mechanism requiring two or more independent verification factors — something you know, have, or are — to establish identity. MFA dramatically reduces the risk of credential-based account takeover.]

[CONCEPT|zero_trust|Zero Trust Architecture
  |A security model that eliminates implicit trust by requiring continuous verification of every user, device, and request regardless of network location. Based on the principle "never trust, always verify" with least-privilege access enforcement.]

[CONCEPT|encryption|Encryption
  |The transformation of plaintext data into ciphertext using a cryptographic algorithm and key, making it unintelligible to unauthorized parties. Protects data in transit (TLS) and at rest (AES-256). A foundational control for data confidentiality.]

[CONCEPT|vpn|VPN (Virtual Private Network)
  |A technology that creates an encrypted tunnel between a client and a private network over a public network. Protects data in transit from eavesdropping and provides remote workers with access to internal resources as if on-premises.]

[CONCEPT|patch_management|Patch Management
  |The systematic process of identifying, testing, and deploying software updates that remediate known vulnerabilities. Timely patching closes the window of exploitation between CVE disclosure and attacker weaponization.]

[CONCEPT|incident_response|Incident Response
  |A structured process for detecting, containing, eradicating, and recovering from security incidents. The NIST IR lifecycle phases are: Preparation, Detection and Analysis, Containment/Eradication/Recovery, and Post-Incident Activity.]

[CONCEPT|security_awareness|Security Awareness Training
  |Structured programs that educate employees to recognize and resist social engineering, phishing, and unsafe behaviors. Human risk reduction through training is cost-effective and required by most compliance frameworks.]

[CONCEPT|nist_csf|NIST Cybersecurity Framework (CSF)
  |A voluntary risk-based framework published by the US National Institute of Standards and Technology organizing cybersecurity activities into five functions: Identify, Protect, Detect, Respond, and Recover. Widely adopted by enterprises globally.]

[CONCEPT|mitre_attack|MITRE ATT&CK
  |A globally accessible knowledge base of adversary tactics and techniques based on real-world observations. Organized as a matrix of TTPs, ATT&CK is used for threat modeling, red team planning, detection engineering, and gap analysis.]

[CONCEPT|owasp_top10|OWASP Top 10
  |A standard awareness document published by the Open Web Application Security Project listing the ten most critical web application security risks. Used as a baseline requirement for secure development and application security testing.]

[CONCEPT|iso_27001|ISO/IEC 27001
  |An international standard specifying requirements for establishing, implementing, maintaining, and continually improving an Information Security Management System (ISMS). Certification demonstrates systematic management of security risks to customers and regulators.]

[CONCEPT|soc2|SOC 2
  |An auditing standard developed by the AICPA that evaluates a service organization's controls relevant to security, availability, processing integrity, confidentiality, and privacy. SOC 2 Type II reports are required by many enterprise procurement teams.]

[CONCEPT|risk_assessment|Risk Assessment
  |A systematic process of identifying assets, enumerating threats and vulnerabilities, estimating likelihood and impact, and prioritizing remediation. The foundation for allocating security resources where they reduce the most risk.]

[CONCEPT|threat_model|Threat Model
  |A structured analysis of a system that identifies what can go wrong, who might attack it, and what mitigations are appropriate. Common methodologies include STRIDE, PASTA, and Attack Trees. Performed during design to find issues early.]

[CONCEPT|penetration_testing|Penetration Testing
  |An authorized simulated cyberattack conducted to evaluate the security of a system by attempting to exploit its vulnerabilities. Produces a prioritized findings report that guides remediation and validates defense effectiveness.]

[CONCEPT|red_team|Red Team
  |A dedicated adversarial group that simulates realistic threat actor behavior against an organization's defenses to uncover gaps that automated tools and compliance checks miss. Red team exercises are scenario-driven and goal-oriented.]

[CONCEPT|blue_team|Blue Team
  |The defensive security team responsible for monitoring, detecting, and responding to attacks — including those simulated by the red team. Purple teaming refers to structured collaboration between red and blue teams to improve detection coverage.]

[CONCEPT|vulnerability_scanning|Vulnerability Scanning
  |Automated assessment of systems against a database of known vulnerabilities to identify unpatched software, misconfigurations, and exposed services. Provides continuous visibility into the attack surface without manual effort.]

[CONCEPT|csf_identify|CSF: Identify Function
  |The NIST CSF function focused on developing organizational understanding of systems, assets, data, and risks. Activities include asset inventory, risk assessment, and governance — the prerequisite for all other framework functions.]

[CONCEPT|csf_protect|CSF: Protect Function
  |The NIST CSF function covering safeguards that limit the impact of potential security events. Includes access control, data security, training, and protective technology deployment.]

[CONCEPT|csf_detect|CSF: Detect Function
  |The NIST CSF function defining activities to identify cybersecurity events in a timely manner. Includes continuous monitoring, anomaly detection, and security event logging.]

[CONCEPT|csf_respond|CSF: Respond Function
  |The NIST CSF function covering actions taken after a detected cybersecurity incident — communications, analysis, mitigation, and improvement activities.]

[CONCEPT|csf_recover|CSF: Recover Function
  |The NIST CSF function defining activities to restore capabilities impaired by a cybersecurity incident, including recovery planning, improvements, and communications to restore stakeholder trust.]

---

## EDGES

threat_actor             -[USES]->                  phishing
threat_actor             -[USES]->                  social_engineering
threat_actor             -[USES]->                  supply_chain_attack
threat_actor             -[USES]->                  zero_day
threat_actor             -[INSTANCE_OF]->            apt

phishing                 -[INSTANCE_OF]->            social_engineering
phishing                 -[ENABLES]->                credential_theft
phishing                 -[DELIVERS]->               malware
phishing                 -[MITIGATED_BY]->           security_awareness
phishing                 -[MITIGATED_BY]->           mfa

social_engineering       -[EXPLOITS]->               credential_theft
social_engineering       -[MITIGATED_BY]->           security_awareness

credential_theft         -[ENABLES]->                unauthorized_access
credential_theft         -[ENABLES]->                lateral_movement
credential_stuffing      -[ENABLES]->                credential_theft
credential_stuffing      -[MITIGATED_BY]->           mfa

malware                  -[INSTANCE_OF]->            ransomware
malware                  -[ENABLES]->                data_exfiltration
malware                  -[ENABLES]->                lateral_movement
malware                  -[DETECTED_BY]->            ids_ips
malware                  -[PREVENTED_BY]->           patch_management

ransomware               -[CAUSES]->                 data_exfiltration
ransomware               -[TRIGGERS]->               incident_response

zero_day                 -[EXPLOITS]->               vulnerability
zero_day                 -[BYPASSES]->               patch_management
zero_day                 -[ENABLES]->                unauthorized_access

vulnerability            -[IDENTIFIED_BY]->          cve
vulnerability            -[QUANTIFIED_BY]->          risk_assessment
vulnerability            -[DETECTED_BY]->            vulnerability_scanning
vulnerability            -[MITIGATED_BY]->           patch_management

sql_injection            -[INSTANCE_OF]->            vulnerability
sql_injection            -[GOVERNED_BY]->            owasp_top10
sql_injection            -[PREVENTED_BY]->           waf

xss                      -[INSTANCE_OF]->            vulnerability
xss                      -[GOVERNED_BY]->            owasp_top10
xss                      -[PREVENTED_BY]->           waf

csrf                     -[INSTANCE_OF]->            vulnerability
csrf                     -[GOVERNED_BY]->            owasp_top10
csrf                     -[PREVENTED_BY]->           waf

supply_chain_attack      -[EXPLOITS]->               vulnerability
supply_chain_attack      -[ENABLES]->                malware
supply_chain_attack      -[MITIGATED_BY]->           risk_assessment

lateral_movement         -[REQUIRES]->               privilege_escalation
lateral_movement         -[ENABLES]->                data_exfiltration
lateral_movement         -[PREVENTED_BY]->           zero_trust
lateral_movement         -[DETECTED_BY]->            siem

privilege_escalation     -[ENABLES]->                data_exfiltration
privilege_escalation     -[DETECTED_BY]->            siem

data_exfiltration        -[TRIGGERS]->               incident_response
data_exfiltration        -[PREVENTED_BY]->           encryption
data_exfiltration        -[DETECTED_BY]->            siem

unauthorized_access      -[ENABLES]->                data_exfiltration
unauthorized_access      -[TRIGGERS]->               incident_response
unauthorized_access      -[DETECTED_BY]->            ids_ips

apt                      -[USES]->                   lateral_movement
apt                      -[INDICATED_BY]->           anomalous_behavior
apt                      -[TRACKED_BY]->             mitre_attack

ioc                      -[COMPONENT_OF]->           threat_intelligence
ioc                      -[DETECTED_BY]->            siem

threat_intelligence      -[INFORMS]->                threat_model
threat_intelligence      -[INFORMS]->                incident_response

kill_chain               -[MAPS_TO]->                mitre_attack
kill_chain               -[COMPONENT_OF]->           threat_model

man_in_the_middle        -[PREVENTED_BY]->           encryption
man_in_the_middle        -[PREVENTED_BY]->           vpn

anomalous_behavior       -[DETECTED_BY]->            siem
anomalous_behavior       -[INDICATES]->              apt

firewall                 -[BLOCKS]->                 unauthorized_access
firewall                 -[COMPONENT_OF]->           zero_trust

ids_ips                  -[DETECTS]->                anomalous_behavior
ids_ips                  -[DETECTS]->                malware

siem                     -[DETECTS]->                anomalous_behavior
siem                     -[ENABLES]->                incident_response
siem                     -[CONSUMES]->               threat_intelligence

waf                      -[PREVENTS]->               sql_injection
waf                      -[PREVENTS]->               xss

mfa                      -[MITIGATES]->              credential_stuffing
mfa                      -[REQUIRES]->               zero_trust
mfa                      -[COMPONENT_OF]->           csf_protect

zero_trust               -[REQUIRES]->               mfa
zero_trust               -[PREVENTS]->               lateral_movement
zero_trust               -[APPLIES_TO]->             risk_assessment

encryption               -[PREVENTS]->               man_in_the_middle
encryption               -[COMPONENT_OF]->           vpn
encryption               -[COMPONENT_OF]->           csf_protect

patch_management         -[MITIGATES]->              vulnerability
patch_management         -[COMPONENT_OF]->           csf_protect

incident_response        -[COMPONENT_OF]->           csf_respond
incident_response        -[REQUIRES]->               siem
incident_response        -[FOLLOWS]->                kill_chain

security_awareness       -[MITIGATES]->              phishing
security_awareness       -[COMPONENT_OF]->           csf_protect

nist_csf                 -[COMPONENT_OF]->           csf_identify
nist_csf                 -[COMPONENT_OF]->           csf_protect
nist_csf                 -[COMPONENT_OF]->           csf_detect
nist_csf                 -[COMPONENT_OF]->           csf_respond
nist_csf                 -[COMPONENT_OF]->           csf_recover

mitre_attack             -[INFORMS]->                threat_model
mitre_attack             -[INFORMS]->                red_team
mitre_attack             -[INFORMS]->                blue_team

iso_27001                -[GOVERNS]->                risk_assessment
iso_27001                -[REQUIRES]->               incident_response
iso_27001                -[MAPS_TO]->                nist_csf

soc2                     -[REQUIRES]->               risk_assessment
soc2                     -[REQUIRES]->               incident_response

risk_assessment          -[COMPONENT_OF]->           threat_model
risk_assessment          -[COMPONENT_OF]->           csf_identify

threat_model             -[USES]->                   mitre_attack
threat_model             -[INFORMS]->                penetration_testing

penetration_testing      -[INSTANCE_OF]->            red_team
penetration_testing      -[VALIDATES]->              vulnerability_scanning

red_team                 -[CONTRASTS_WITH]->         blue_team
red_team                 -[USES]->                   mitre_attack

blue_team                -[USES]->                   siem
blue_team                -[USES]->                   ids_ips

vulnerability_scanning   -[DETECTS]->                vulnerability
vulnerability_scanning   -[COMPONENT_OF]->           csf_identify

csf_identify             -[PREREQUISITE_FOR]->       csf_protect
csf_protect              -[PREREQUISITE_FOR]->       csf_detect
csf_detect               -[PREREQUISITE_FOR]->       csf_respond
csf_respond              -[PREREQUISITE_FOR]->       csf_recover
