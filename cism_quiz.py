import streamlit as st

st.set_page_config(
    page_title="CISM 500Q Practice",
    page_icon="shield",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #F0F2F6; }

.q-card {
    background: white;
    border-radius: 10px;
    padding: 22px 24px 18px;
    margin-bottom: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
    border-left: 5px solid #E85D26;
}
.q-number {
    font-size: 13px;
    font-weight: 700;
    color: #E85D26;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.q-text {
    font-size: 20px;
    font-weight: 700;
    color: #1A1A2E;
    line-height: 1.6;
}
.domain-badge {
    font-size: 12px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    float: right;
}
.opt-correct {
    background: #E8F5E9;
    border: 2px solid #2E7D32;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 6px 0;
    color: #1B5E20;
    font-weight: 700;
    font-size: 20px;
    line-height: 1.5;
}
.opt-wrong {
    background: #FFEBEE;
    border: 2px solid #C62828;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 6px 0;
    color: #B71C1C;
    font-weight: 700;
    font-size: 20px;
    line-height: 1.5;
}
.opt-neutral {
    background: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 6px 0;
    color: #333;
    font-size: 20px;
    line-height: 1.5;
}
.mem-box {
    background: #FFFDE7;
    border-left: 4px solid #F9A825;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-top: 14px;
    font-size: 20px;
    color: #5D4037;
    line-height: 1.6;
}
.score-card {
    background: #1A1A2E;
    color: white;
    border-radius: 14px;
    padding: 28px;
    text-align: center;
    margin: 16px 0;
}
.score-big {
    font-size: 56px;
    font-weight: 700;
    line-height: 1;
}
.progress-wrap {
    background: #E0E0E0;
    border-radius: 6px;
    height: 7px;
    margin: 6px 0 16px;
}
.progress-fill {
    border-radius: 6px;
    height: 7px;
}
div[data-testid="stRadio"] label {
    font-size: 20px !important;
    padding: 8px 4px !important;
    display: block;
    line-height: 1.5 !important;
}
div[data-testid="stRadio"] > div { gap: 6px !important; }
div[data-testid="stButton"] > button {
    border-radius: 8px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    padding: 14px 18px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
QUESTIONS = [
    (1, "An information security risk analysis BEST assists an organization in ensuring that:", ["the infrastructure has the appropriate level of access control.", "cost-effective decisions are made with regard to which assets need protection.", "an appropriate level of funding is applied to security processes.", "the organization implements appropriate security technologies."], "B", "จำ: risk analysis BEST assists → cost-effective decisions ว่าอะไรควรปกป้อง"),
    (2, "In a multinational organization, local security regulations should be implemented over global security policy because:", ["business objectives are defined by local business unit managers.", "deploying awareness of local regulations is more practical than of global policy.", "global security policies include unnecessary controls for local businesses.", "requirements of local regulations take precedence."], "D", "จำ: local regs vs global policy → Law เหนือกว่า Policy เสมอ"),
    (3, "To gain a clear understanding of the impact that a new regulatory requirement will have on an organization's information security controls, an information security manager should FIRST:", ["conduct a cost-benefit analysis.", "conduct a risk assessment.", "interview senior management.", "perform a gap analysis."], "D", "จำ: new regulation FIRST → gap analysis (ดูว่าขาดอะไร)"),
    (4, "When management changes the enterprise business strategy, which process should be used to evaluate existing security controls and select new ones?", ["Access control management", "Change management", "Configuration management", "Risk management"], "D", "จำ: strategy เปลี่ยน → evaluate controls = Risk management"),
    (5, "Which of the following is the BEST way to build a risk-aware culture?", ["Periodically change risk awareness messages.", "Ensure threats are communicated organization-wide in a timely manner.", "Periodically test compliance with security controls and post results.", "Establish incentives and a channel for staff to report risks."], "D", "จำ: risk-aware culture = incentive + channel to REPORT"),
    (6, "What would be an information security manager's BEST recommendation upon learning that an existing contract with a third party does not clearly identify requirements for safeguarding critical data?", ["Cancel the outsourcing contract.", "Transfer the risk to the provider.", "Create an addendum to the existing contract.", "Initiate an external audit of the provider's data center."], "C", "จำ: contract ขาด safeguard → addendum (ไม่ใช่ cancel หรือ audit)"),
    (7, "An organization has purchased a SIEM tool. Which of the following is MOST important to consider before implementation?", ["Controls to be monitored", "Reporting capabilities", "The contract with the SIEM vendor", "Available technical support"], "A", "จำ: before SIEM → รู้ก่อนว่าจะ monitor controls อะไร"),
    (8, "Which of the following is MOST likely to be included in an enterprise security policy?", ["Definitions of responsibilities", "Retention schedules", "System access specifications", "Organizational risk"], "A", "จำ: enterprise security policy = definitions of responsibilities (ไม่ใช่ technical detail)"),
    (9, "Which should an information security manager do FIRST when a legacy application is not compliant with a regulatory requirement, but the business unit does not have the budget for remediation?", ["Develop a business case for funding remediation efforts.", "Advise senior management to accept the risk of noncompliance.", "Notify legal and internal audit of the noncompliant legacy application.", "Assess the consequences of noncompliance against the cost of remediation."], "D", "จำ: no budget to fix → FIRST = assess consequences vs cost"),
    (10, "Which of the following is the MOST effective way to address security concerns during contract negotiations with a third party?", ["Review the third-party contract with the organization's legal department.", "Communicate security policy with the third-party vendor.", "Ensure security is involved in the procurement process.", "Conduct an information security audit on the third-party vendor."], "C", "จำ: security in contract → security involved in PROCUREMENT process"),
    (11, "Which of the following is the BEST method to protect consumer private information for an online public website?", ["Apply strong authentication to online accounts.", "Encrypt consumer data in transit and at rest.", "Use secure encrypted transport layer.", "Apply a masking policy to the consumer data."], "B", "จำ: protect privacy online = encrypt BOTH transit + at rest"),
    (12, "Which of the following is the MOST important consideration in a BYOD program to protect company data in the event of a loss?", ["The ability to remotely locate devices", "The ability to centrally manage devices", "The ability to restrict unapproved applications", "The ability to classify types of devices"], "B", "จำ: BYOD data loss → central management (ไม่ใช่แค่ locate)"),
    (13, "An information security manager has been asked to determine whether an initiative has reduced risk to an acceptable level. Which activity would provide the BEST information?", ["Initiating a cost-benefit analysis of the implemented controls", "Performing a risk assessment", "Reviewing the risk register", "Conducting a business impact analysis (BIA)"], "B", "จำ: ตรวจว่า risk ลดพอหรือยัง → risk assessment"),
    (14, "An organization using external cloud services extensively is concerned with risk monitoring and timely response. The BEST way to address this is to ensure:", ["the availability of continuous technical support.", "appropriate service level agreements (SLAs) are in place.", "a right-to-audit clause is included in contracts.", "internal security standards are in place."], "B", "จำ: cloud risk monitoring → appropriate SLAs"),
    (15, "Which of the following is the BEST way to ensure organizational security policies comply with data security regulatory requirements?", ["Obtain annual sign-off from executive management.", "Align the policies to the most stringent global regulations.", "Send the policies to stakeholders for review.", "Outsource compliance activities."], "B", "จำ: comply หลายประเทศ → align to MOST STRINGENT"),
    (16, "The PRIMARY reason for defining information security roles and responsibilities of staff is to:", ["comply with security policy.", "increase corporate accountability.", "enforce individual accountability.", "reinforce the need for training."], "C", "จำ: define roles → enforce INDIVIDUAL accountability"),
    (17, "Threat and vulnerability assessments are important PRIMARILY because they are:", ["used to establish security investments.", "needed to estimate risk.", "the basis for setting control objectives.", "elements of the organization's security posture."], "B", "จำ: threat+vuln assessments → needed to ESTIMATE RISK"),
    (18, "Which of the following should be an information security manager's PRIMARY focus during development of a critical system storing highly confidential data?", ["Ensuring the amount of residual risk is acceptable", "Reducing the number of vulnerabilities detected", "Avoiding identified system threats", "Complying with regulatory requirements"], "A", "จำ: dev critical system → PRIMARY = residual risk acceptable"),
    (19, "When evaluating vendors for sensitive data processing, which should be the FIRST step?", ["Develop metrics for vendor performance.", "Include information security criteria as part of vendor selection.", "Review third-party reports of potential vendors.", "Include information security clauses in the vendor contract."], "B", "จำ: vendor for sensitive data → FIRST = security criteria in SELECTION"),
    (20, "An information security team is investigating an alleged breach. Which of the following is the BEST single source of evidence?", ["File integrity monitoring (FIM) software", "Security information and event management (SIEM) tool", "Intrusion detection system (IDS)", "Antivirus software"], "B", "จำ: best single source for breach = SIEM (correlates everything)"),
    (21, "Which criteria is MOST helpful in determining the level of risk for each vendor over the last year?", ["Compliance requirements associated with the regulation", "Criticality of the service to the organization", "Corresponding breaches associated with each vendor", "Compensating controls in place to protect information security"], "B", "จำ: vendor risk level → CRITICALITY of service to org"),
    (22, "Which of the following is the MOST important security consideration when developing an incident response strategy with a cloud provider?", ["Security audit reports", "Recovery time objective (RTO)", "Technological capabilities", "Escalation processes"], "D", "จำ: cloud IR strategy → escalation processes (ใครทำอะไรเมื่อไหร่)"),
    (23, "Implementing a comprehensive security framework poses which GREATEST challenge?", ["Executive leadership becomes involved in decisions about information security governance.", "Executive leadership views information security governance primarily as a concern of the IS team.", "Information security staff has little or no experience with the practice of IS governance.", "Information security management does not fully accept the responsibility for IS governance."], "B", "จำ: governance challenge = exec treats security as IS team's problem ONLY"),
    (24, "Risk scenarios simplify the risk assessment process by:", ["covering the full range of possible risk.", "ensuring business risk is mitigated.", "reducing the need for subsequent risk evaluation.", "focusing on important and relevant risk."], "D", "จำ: risk scenarios = focus on IMPORTANT & RELEVANT risk"),
    (25, "Which of the following is the MOST important consideration when developing information security objectives?", ["They are regularly reassessed and reported to stakeholders.", "They are approved by the IT governance function.", "They are clear and can be understood by stakeholders.", "They are identified using global security frameworks and standards."], "C", "จำ: IS objectives = clear & UNDERSTANDABLE by stakeholders"),
    (26, "A legacy application does not comply with new regulatory requirements to encrypt sensitive data at rest, and remediating would require significant investment. What should the IS manager do FIRST?", ["Assess the business impact to the organization.", "Present the noncompliance risk to senior management.", "Investigate alternative options to remediate the noncompliance.", "Determine the cost to remediate the noncompliance."], "A", "จำ: non-comply + big cost → FIRST = assess BUSINESS IMPACT"),
    (27, "Which of the following BEST enables effective information security governance?", ["Security-aware corporate culture", "Advanced security technologies", "Periodic vulnerability assessments", "Established information security metrics"], "A", "จำ: effective governance = security-aware CULTURE"),
    (28, "Application data integrity risk is MOST directly addressed by a design that includes:", ["strict application of an authorized data dictionary.", "reconciliation routines such as checksums, hash totals, and record counts.", "application log requirements such as field-level audit trails and user activity logs.", "access control technologies such as role-based entitlements."], "B", "จำ: data integrity = reconciliation / checksums / hash"),
    (29, "Deciding the level of protection a particular asset should be given is BEST determined by:", ["the corporate risk appetite.", "a risk analysis.", "a threat assessment.", "a vulnerability assessment."], "B", "จำ: protection level for asset = risk analysis"),
    (30, "What should be an information security manager's FIRST step when developing a business case for a new IDS solution?", ["Calculate the total cost of ownership (TCO).", "Define the issues to be addressed.", "Perform a cost-benefit analysis.", "Conduct a feasibility study."], "B", "จำ: business case FIRST step = define the ISSUES (problem statement)"),
    (31, "Which of the following is the MOST important incident management consideration for an organization subscribing to a cloud service?", ["Decision on the classification of cloud-hosted data", "Expertise of personnel providing incident response", "Implementation of a SIEM in the organization", "An agreement on the definition of a security incident"], "D", "จำ: cloud IR = agree on DEFINITION of security incident"),
    (32, "Which of the following is the BEST way for an organization to determine the maturity level of its information security program?", ["Review the results of information security awareness testing.", "Validate the effectiveness of implemented security controls.", "Benchmark the information security policy against industry standards.", "Track the trending of information security incidents."], "B", "จำ: maturity level = validate EFFECTIVENESS of controls"),
    (33, "An organization has identified an increased threat of external brute force attacks. Which is the MOST effective mitigation?", ["Increase the frequency of log monitoring and analysis.", "Implement a security information and event management system (SIEM).", "Increase the sensitivity of intrusion detection systems.", "Implement multi-factor authentication."], "D", "จำ: brute force → MFA"),
    (34, "When supporting an organization's privacy officer, which is the information security manager's PRIMARY role?", ["Ensuring appropriate controls are in place", "Monitoring the transfer of private data", "Determining data classification", "Conducting privacy awareness programs"], "A", "จำ: IS manager + privacy officer = ensure CONTROLS in place"),
    (35, "The CISO has developed an information security strategy but struggles to obtain senior management commitment for funds. Which is the MOST likely reason?", ["The strategy does not include a cost-benefit analysis.", "There was a lack of engagement with the business during development.", "The strategy does not comply with security standards.", "The CISO reports to the CIO."], "B", "จำ: no funding → lack of BUSINESS ENGAGEMENT during development"),
    (36, "An organization's CIO drafts the charter for an IS steering committee comprised of CIO, IT shared services manager, VP of marketing, and IS manager. Which is the MOST significant issue?", ["The committee consists of too many senior executives.", "The committee lacks sufficient business representation.", "There is a conflict of interest between the business and IT.", "The CIO is not taking charge of the committee."], "B", "จำ: steering committee issue = insufficient BUSINESS representation"),
    (37, "What is the PRIMARY purpose of an unannounced disaster recovery exercise?", ["To provide metrics to senior management", "To evaluate how personnel react to the situation", "To assess service level agreements (SLAs)", "To estimate the recovery time objective (RTO)"], "B", "จำ: unannounced DR = evaluate PERSONNEL REACTION"),
    (38, "Labeling information according to its security classification:", ["reduces the need to identify baseline controls for each classification.", "reduces the number and type of countermeasures required.", "enhances the likelihood of people handling information securely.", "affects the consequences if information is handled insecurely."], "C", "จำ: labeling = ทำให้คนจัดการข้อมูลได้ถูกต้องมากขึ้น"),
    (39, "Which is the MOST effective approach for determining whether an IS program supports the IS strategy?", ["Ensure resources meet information security program needs.", "Audit the information security program to identify deficiencies.", "Identify gaps impacting information security strategy.", "Develop key performance indicators (KPIs) of information security."], "C", "จำ: program vs strategy → identify GAPS"),
    (40, "When drafting the corporate privacy statement for a public web site, which MUST be included?", ["Limited liability clause", "Access control requirements", "Explanation of information usage", "Information encryption requirements"], "C", "จำ: privacy statement MUST = explanation of how we USE your data"),
    (41, "An organization is concerned with the potential for exploitation of server vulnerabilities. Which is the BEST control?", ["Enforcing standard system configurations based on secure configuration benchmarks", "Implementing network and system-based anomaly monitoring software", "Enforcing configurations for secure logging and audit trails", "Implementing host-based intrusion detection systems (IDS)"], "A", "จำ: server vuln → enforce BASELINE CONFIG (benchmarks)"),
    (42, "Which of the following is the MOST important step when establishing guidelines for the use of social networking sites?", ["Identify secure social networking sites.", "Establish disciplinary actions for noncompliance.", "Perform a vulnerability assessment.", "Define acceptable information for posting."], "D", "จำ: social networking guidelines → define ACCEPTABLE INFO for posting"),
    (43, "Regular vulnerability scanning shows many workstations have unpatched software. What is the BEST way to help senior management understand the risk?", ["Include the impact of the risk as part of regular metrics.", "Send regular notifications directly to senior managers.", "Recommend the steering committee conduct a review.", "Update the risk assessment at regular intervals."], "A", "จำ: help senior understand risk = include IMPACT in regular METRICS"),
    (44, "Which of the following BEST prepares a computer incident response team for a variety of IS scenarios?", ["Tabletop exercises", "Forensics certification", "Penetration tests", "Disaster recovery drills"], "A", "จำ: CIRT preparation = tabletop exercises"),
    (45, "Which of the following BEST protects against phishing attacks?", ["Security strategy training", "Email filtering", "Network encryption", "Application whitelisting"], "A", "จำ: phishing defense = security TRAINING (human defense)"),
    (46, "Which of the following is the MOST effective method of preventing deliberate internal security breaches?", ["Well-designed intrusion detection system (IDS)", "Biometric security access control", "Well-designed firewall system", "Screening prospective employees"], "D", "จำ: prevent DELIBERATE internal breach = screening (hire right)"),
    (47, "When designing security controls, it is MOST important to:", ["focus on preventive controls.", "apply controls to confidential information.", "evaluate the costs associated with the controls.", "apply a risk-based approach."], "D", "จำ: designing controls = risk-based approach เสมอ"),
    (48, "An IS team plans to increase password complexity for a customer-facing site, but there are concerns it will negatively impact user experience. What is the BEST course of action?", ["Evaluate business compensating controls.", "Quantify the security risk to the business.", "Assess business impact against security risk.", "Conduct industry benchmarking."], "C", "จำ: security vs UX → assess BUSINESS IMPACT against security risk"),
    (49, "Which is the PRIMARY responsibility of an IS manager when implementing company-owned mobile devices?", ["Review and update existing security policies.", "Enforce passwords and data encryption on the devices.", "Conduct security awareness training.", "Require remote wipe capabilities for devices."], "A", "จำ: new mobile devices → PRIMARY = review/update POLICIES"),
    (50, "Which would be MOST useful to help senior management understand the status of IS compliance?", ["Key performance indicators (KPIs)", "Risk assessment results", "Industry benchmarks", "Business impact analysis (BIA) results"], "A", "จำ: compliance status to senior = KPIs"),
    (51, "Which of the following is the MOST important reason for an organization to develop an IS governance program?", ["Establishment of accountability", "Compliance with audit requirements", "Creation of tactical solutions", "Monitoring of security incidents"], "A", "จำ: IS governance = establish ACCOUNTABILITY"),
    (52, "Which provides the MOST essential input for development of an IS strategy?", ["Results of an information security gap analysis", "Measurement of security performance against IT goals", "Results of a technology risk assessment", "Availability of capable information security resources"], "C", "จำ: IS strategy input = technology RISK ASSESSMENT results"),
    (53, "The MOST important reason for an IS manager to be involved in the change management process is to ensure that:", ["security controls drive technology changes.", "risks have been evaluated.", "security controls are updated regularly.", "potential vulnerabilities are identified."], "B", "จำ: IS in change mgmt = ensure RISKS EVALUATED"),
    (54, "Which should be the PRIMARY focus of a status report on the IS program to senior management?", ["Confirming the organization complies with security policies", "Verifying security costs do not exceed the budget", "Demonstrating risk is managed at the desired level", "Providing evidence that resources are performing as expected"], "C", "จำ: IS report to senior = risk managed at DESIRED LEVEL"),
    (55, "Which of the following is MOST likely to be a component of a security incident escalation policy?", ["Names and telephone numbers of key management personnel", "A severity-ranking mechanism tied only to the duration of the outage", "Sample scripts and press releases for statements to media", "Decision criteria for when to alert various groups"], "D", "จำ: escalation policy = DECISION CRITERIA for when/who to alert"),
    (56, "Which would be an IS manager's PRIMARY challenge when deploying a BYOD mobile program?", ["Configuration management", "Mobile application control", "Inconsistent device security", "End user acceptance"], "C", "จำ: BYOD PRIMARY challenge = INCONSISTENT device security"),
    (57, "Company A is acquiring Company B (cloud provider). Which should be the PRIMARY focus of Company A's IS manager?", ["The cost to align to Company A's security policies", "The organizational structure of Company B", "Company B's security policies", "Company A's security architecture"], "C", "จำ: acquisition = ดู target company (B) SECURITY POLICIES"),
    (58, "Which should be done FIRST when selecting performance metrics to report on vendor risk management?", ["Select the data source.", "Review the confidentiality requirements.", "Identify the intended audience.", "Identify the data owner."], "C", "จำ: selecting metrics → FIRST = identify INTENDED AUDIENCE"),
    (59, "Which BEST determines what information should be shared with different entities during incident response?", ["Escalation procedures", "Communication plan", "Disaster recovery policy", "Business continuity plan (BCP)"], "B", "จำ: what info to share in IR = COMMUNICATION PLAN"),
    (60, "Which is the BEST way to enhance training for incident response teams?", ["Conduct interviews with organizational units.", "Establish incident key performance indicators (KPIs).", "Participate in emergency response activities.", "Perform post-incident reviews."], "C", "จำ: enhance IR training = participate in EMERGENCY RESPONSE activities"),
    (61, "An IS manager wants to improve the ability to identify changes in risk levels affecting systems. Which is the BEST method?", ["Performing business impact analyses (BIA)", "Monitoring key goal indicators (KGIs)", "Monitoring key risk indicators (KRIs)", "Updating the risk register"], "C", "จำ: identify risk level CHANGES = monitor KRIs (leading indicators)"),
    (62, "When developing an escalation process for an IR plan, the IS manager should PRIMARILY consider the:", ["affected stakeholders.", "incident response team.", "availability of technical resources.", "media coverage."], "A", "จำ: IR escalation → PRIMARILY consider affected STAKEHOLDERS"),
    (63, "Which should be an IS manager's MOST important consideration when determining if an information asset has been classified appropriately?", ["Value to the business", "Security policy requirements", "Ownership of information", "Level of protection"], "A", "จำ: asset classified appropriately → VALUE TO BUSINESS"),
    (64, "The effectiveness of an incident response team will be GREATEST when:", ["the incident response process is updated based on lessons learned.", "the incident response team members are trained security personnel.", "the team meets on a regular basis to review log files.", "incidents are identified using a SIEM system."], "A", "จำ: IR team GREATEST effectiveness = updated from LESSONS LEARNED"),
    (65, "An IS manager MUST have an understanding of the organization's business goals to:", ["relate IS to change management.", "develop an IS strategy.", "develop operational procedures.", "define key performance indicators (KPIs)."], "B", "จำ: must understand business goals → develop IS STRATEGY"),
    (66, "Which of the following is MOST important to an IS program?", ["Understanding current and emerging technologies", "Establishing key performance indicators (KPIs)", "Conducting periodic risk assessments", "Obtaining stakeholder input"], "C", "จำ: IS program → conduct PERIODIC RISK ASSESSMENTS"),
    (67, "An attacker gained access to an organization's perimeter firewall and made changes. Which would have BEST provided timely identification?", ["Implementing a data loss prevention (DLP) suite", "Deploying an intrusion prevention system (IPS)", "Deploying a security information and event management (SIEM) system", "Conducting regular system administrator awareness training"], "C", "จำ: firewall config change detected timely = SIEM"),
    (68, "When establishing metrics for an IS program, the BEST approach is to identify indicators that:", ["support major information security initiatives.", "reflect the corporate risk culture.", "reduce information security program spending.", "demonstrate the effectiveness of the security program."], "D", "จำ: IS metrics = DEMONSTRATE EFFECTIVENESS"),
    (69, "For an organization providing web-based services, which security event would MOST likely initiate an IR plan escalated to management?", ["Anti-malware alerts on several employees' workstations", "Several port scans of the web server", "Multiple failed login attempts on an employee's workstation", "Suspicious network traffic originating from the demilitarized zone (DMZ)"], "D", "จำ: web services escalate = suspicious traffic from DMZ"),
    (70, "An IS manager is implementing a BYOD program. Which would BEST ensure users adhere to security standards?", ["Publish the standards on the intranet landing page.", "Deploy a device management solution.", "Establish an acceptable use policy.", "Monitor user activities on the network."], "C", "จำ: BYOD user compliance = acceptable use POLICY"),
    (71, "When monitoring the security of a web-based application, which is MOST frequently reviewed?", ["Audit reports", "Access logs", "Access lists", "Threat metrics"], "B", "จำ: web app monitoring = ACCESS LOGS"),
    (72, "Which is the MOST effective way for an IS manager to ensure security is incorporated into project development?", ["Develop good communications with the project management office (PMO).", "Participate in project initiation, approval, and funding.", "Conduct security reviews during design, testing, and implementation.", "Integrate organization's security requirements into project management."], "D", "จำ: security in project dev = INTEGRATE requirements into PM"),
    (73, "Which provides the MOST relevant information to determine the overall effectiveness of an IS program?", ["SWOT analysis", "Industry benchmarks", "Cost-benefit analysis", "Balanced scorecard"], "D", "จำ: overall IS effectiveness = BALANCED SCORECARD"),
    (74, "An organization finds unauthorized software has been installed on workstations, containing a Trojan. What would have BEST prevented the installation?", ["Banning executable file downloads at the Internet firewall", "Implementing an intrusion detection system (IDS)", "Implementing application blacklisting", "Removing local administrator rights"], "D", "จำ: prevent unauthorized software install = REMOVE local admin rights"),
    (75, "When developing a tabletop test plan for IR testing, the PRIMARY purpose of the scenario should be to:", ["measure management engagement as part of an IR team.", "provide participants with situations to ensure understanding of their roles.", "give the business a measure of the organization's overall readiness.", "challenge the IR team to solve the problem under pressure."], "B", "จำ: tabletop scenario PURPOSE = participants understand their ROLES"),
    (76, "Which is MOST important for an IS manager to consider when identifying IS resource requirements?", ["Availability of potential resources", "Information security incidents", "Current resourcing levels", "Information security strategy"], "D", "จำ: IS resources → align with IS STRATEGY"),
    (77, "Which is the MAIN benefit of performing an assessment of existing incident response processes?", ["Validation of current capabilities", "Benchmarking against industry peers", "Prioritization of action plans", "Identification of threats and vulnerabilities"], "A", "จำ: assess IR processes = VALIDATE current capabilities"),
    (78, "Which of the following BEST describes a buffer overflow?", ["A type of covert channel that captures data", "A function is carried out with more data than the function can handle", "Malicious code designed to interfere with normal operations", "A program contains a hidden and unintended function"], "B", "จำ: buffer overflow = function gets MORE DATA than it can handle"),
    (79, "Which is the MOST important consideration when selecting members for an IS steering committee?", ["Information security expertise", "Tenure in the organization", "Business expertise", "Cross-functional composition"], "D", "จำ: steering committee members = CROSS-FUNCTIONAL composition"),
    (80, "Which BEST validates that security controls are implemented in a new business process?", ["Verify the use of a recognized control framework.", "Review the process for conformance with IS best practices.", "Benchmark the process against industry practices.", "Assess the process according to information security policy."], "D", "จำ: validate controls in new process = assess against IS POLICY"),
    (81, "Which is the MOST effective way to ensure third-party service providers are aware of IS requirements?", ["Including information security clauses within contracts", "Auditing the service delivery of third-party providers", "Providing IS training to third-party personnel", "Requiring third parties to sign confidentiality agreements"], "A", "จำ: third-party IS awareness = IS clauses in CONTRACTS"),
    (82, "The MOST important reason to use a centralized mechanism to identify IS incidents is to:", ["comply with corporate policies.", "detect threats across environments.", "prevent unauthorized changes to networks.", "detect potential fraud."], "B", "จำ: centralized IR mechanism = DETECT THREATS across all environments"),
    (83, "Which should be done FIRST when establishing security measures for personal data on an HR management system?", ["Conduct a vulnerability assessment.", "Move the system into a separate network.", "Conduct a privacy impact assessment (PIA).", "Evaluate data encryption technologies."], "C", "จำ: HR personal data system → FIRST = PIA"),
    (84, "An IS manager is informed of a new vulnerability in an online banking app; patch expected in 72 hours. What should the IS manager do FIRST?", ["Implement mitigating controls.", "Perform a business impact analysis (BIA).", "Perform a risk assessment.", "Notify senior management."], "C", "จำ: new vuln (patch coming) → FIRST = risk assessment"),
    (85, "Which of the following is MOST relevant for an IS manager to communicate to the board of directors?", ["The level of exposure", "Vulnerability assessments", "The level of inherent risk", "Threat assessments"], "A", "จำ: communicate to board = LEVEL OF EXPOSURE (business language)"),
    (86, "Senior management has just accepted the risk of noncompliance with a new regulation. What should the IS manager do NEXT?", ["Report the decision to the compliance officer.", "Reassess the organization's risk tolerance.", "Update details within the risk register.", "Assess the impact of the regulation."], "C", "จำ: risk accepted → NEXT = update RISK REGISTER"),
    (87, "Which BEST provides sufficient assurance that a service provider complies with the organization's IS requirements?", ["A live demonstration of the third-party supplier's security capabilities", "The ability to audit the third-party supplier's IT systems and processes", "Third-party security control self-assessment results", "An independent review report indicating compliance with industry standards"], "B", "จำ: BEST assurance from provider = ability to AUDIT their systems"),
    (88, "Which is the MOST essential element of an IS program?", ["Prioritizing program deliverables based on available resources", "Benchmarking the program with global standards", "Involving functional managers in program development", "Applying project management practices used by the business"], "C", "จำ: IS program essential = involve FUNCTIONAL MANAGERS"),
    (89, "Which is BEST to include in a business case when ROI for an IS initiative is difficult to calculate?", ["Projected increase in maturity level", "Estimated increase in efficiency", "Projected costs over time", "Estimated reduction in risk"], "D", "จำ: hard ROI → use ESTIMATED RISK REDUCTION"),
    (90, "If the inherent risk of a business activity is higher than the acceptable risk level, the IS manager should FIRST:", ["transfer risk to a third party to avoid cost of impact.", "recommend that management avoid the business activity.", "assess the gap between current and acceptable level of risk.", "implement controls to mitigate the risk to an acceptable level."], "C", "จำ: inherent risk > acceptable → FIRST = assess the GAP"),
    (91, "Which BEST enables deployment of consistent security throughout international branches of a multinational organization?", ["Remediation of audit findings", "Decentralization of security governance", "Establishment of security governance", "Maturity of security processes"], "C", "จำ: consistent security globally = GOVERNANCE framework"),
    (92, "What is the PRIMARY benefit of effective configuration management?", ["Standardization of system support", "Reduced frequency of incidents", "Decreased risk to the organization's systems", "Improved vulnerability management"], "C", "จำ: config management benefit = DECREASED RISK to systems"),
    (93, "A large organization is developing its IS program involving complex organizational functions. Which will BEST enable successful implementation?", ["Security governance", "Security policy", "Security metrics", "Security guidelines"], "A", "จำ: complex org IS program = SECURITY GOVERNANCE"),
    (94, "What is the BEST reason to keep IS policies separate from procedures?", ["To keep policies from having to be changed too frequently", "To ensure individual documents do not contain conflicting information", "To keep policy documents from becoming too large", "To ensure policies receive the appropriate approvals"], "A", "จำ: policy ≠ procedure → policy stays STABLE, procedure can change"),
    (95, "A small organization has a contract with a multinational cloud computing vendor. Which would present the GREATEST concern if omitted from the contract?", ["Escrow of software code with conditions for code release", "Right of the subscriber to conduct onsite audits of the vendor", "Authority of the subscriber to approve access to its data", "Commingling of subscribers' data on the same physical server"], "C", "จำ: cloud contract concern = authority to APPROVE ACCESS to your data"),
    (96, "An IS manager has identified a major security event with potential noncompliance implications. Who should be notified FIRST?", ["Internal audit", "Public relations team", "Senior management", "Regulatory authorities"], "C", "จำ: major event + compliance → notify SENIOR MANAGEMENT first"),
    (97, "Which is the PRIMARY purpose of establishing an IS governance framework?", ["To proactively address security objectives", "To reduce security audit issues", "To enhance business continuity planning", "To minimize security risks"], "A", "จำ: IS governance purpose = PROACTIVELY address security objectives"),
    (98, "An organization is leveraging tablets to replace shared desktops; tablets at increased risk of theft. Which will BEST mitigate this risk?", ["Implement remote wipe capability.", "Create an acceptable use policy.", "Conduct a mobile device risk assessment.", "Deploy mobile device management (MDM)."], "D", "จำ: tablets + theft risk = deploy MDM"),
    (99, "When scoping a risk assessment, assets need to be classified by:", ["sensitivity and criticality.", "likelihood and impact.", "threats and opportunities.", "redundancy and recoverability."], "A", "จำ: asset classification = SENSITIVITY + CRITICALITY"),
    (100, "Which would BEST enable effective decision-making?", ["Annualized loss estimates determined from past security events", "A universally applied list of generic threats, impacts, and vulnerabilities", "A consistent process to analyze new and historical information risk", "Formalized acceptance of risk analysis by business management"], "C", "จำ: effective decision-making = CONSISTENT PROCESS to analyze risk"),
    (101, "Which has the GREATEST impact on efforts to improve an organization's security posture?", ["Well-documented security policies and procedures", "Supportive tone at the top regarding security", "Regular reporting to senior management", "Automation of security controls"], "B", "จำ: improve security posture = TONE AT THE TOP"),
    (102, "Which is the BEST strategy to implement an effective operational security posture?", ["Increased security awareness", "Defense in depth", "Threat management", "Vulnerability management"], "B", "จำ: operational security posture = DEFENSE IN DEPTH"),
    (103, "In a cloud environment, which would pose the GREATEST challenge to the investigation of security incidents?", ["Non-standard event logs", "Access to the hardware", "Data encryption", "Compressed customer data"], "B", "จำ: cloud forensics challenge = no ACCESS TO HARDWARE"),
    (104, "The PRIMARY goal of conducting a BIA as part of continuity planning is to:", ["obtain the support of executive management.", "document the disaster recovery process.", "map the business process to supporting IT and other corporate resources.", "identify critical processes and the degree of reliance on support services."], "D", "จำ: BIA goal = identify CRITICAL PROCESSES + degree of reliance"),
    (105, "Which is MOST important when selecting an IS metric?", ["Ensuring the metric is repeatable", "Aligning the metric to the IT strategy", "Defining the metric in qualitative terms", "Defining the metric in quantitative terms"], "B", "จำ: IS metric selection = ALIGN to IT strategy"),
    (106, "Which is the BEST way for an IS manager to justify ongoing IPS maintenance fees?", ["Establish and present metrics that track performance.", "Perform industry research annually and document ranking of the IPS.", "Perform a penetration test to demonstrate ability to protect.", "Provide yearly competitive pricing to illustrate the value of the IPS."], "A", "จำ: justify IPS maintenance = metrics tracking PERFORMANCE"),
    (107, "An organization wants to enable digital forensics for a business-critical application. Which will BEST help?", ["Install biometric access control.", "Develop an incident response plan.", "Define data retention criteria.", "Enable activity logging."], "D", "จำ: enable digital forensics = ACTIVITY LOGGING"),
    (108, "An employee clicked on a phishing link triggering ransomware. What should the IS manager do FIRST?", ["Notify internal legal counsel.", "Isolate the impacted endpoints.", "Wipe the affected system.", "Notify senior management."], "B", "จำ: ransomware → FIRST = ISOLATE endpoints"),
    (109, "A recent audit found new user accounts are not set up uniformly. Which is MOST important to review?", ["Security policies", "Automated controls", "Guidelines", "Standards"], "D", "จำ: accounts not set up uniformly = review STANDARDS"),
    (110, "Which metric is the BEST measure of the effectiveness of an IS program?", ["Reduction in the amount of risk exposure in an organization", "Reduction in the number of threats to an organization", "Reduction in the cost of risk remediation for an organization", "Reduction in the number of vulnerabilities in an organization"], "A", "จำ: IS program effectiveness = reduction in RISK EXPOSURE"),
    (111, "Which is the BEST course of action if residual risk is lower than the acceptable risk level?", ["Update the risk assessment framework.", "Monitor the effectiveness of controls.", "Review the risk probability and impact.", "Review the inherent risk level."], "B", "จำ: residual risk < acceptable → MONITOR effectiveness of controls"),
    (112, "The BEST way to avoid session hijacking is to use:", ["strong password controls.", "a firewall.", "a reverse lookup.", "a secure protocol."], "D", "จำ: session hijacking = use SECURE PROTOCOL (HTTPS/TLS)"),
    (113, "A hospital's critical server has been encrypted by ransomware. Which would MOST effectively allow the hospital to avoid paying the ransom?", ["A continual server replication process", "Employee training on ransomware", "A properly tested offline backup system", "A properly configured firewall"], "C", "จำ: avoid ransomware payment = TESTED OFFLINE BACKUP"),
    (114, "Which function is MOST critical when initiating the removal of system access for terminated employees?", ["Help desk", "Legal", "Information security", "Human resources (HR)"], "D", "จำ: remove access for terminated = HR initiates (knows who left)"),
    (115, "The authorization to transfer the handling of an internal incident to a third-party provider is PRIMARILY defined by the:", ["escalation procedures.", "information security manager.", "chain of custody.", "disaster recovery plan (DRP)."], "A", "จำ: transfer incident to 3rd party = ESCALATION PROCEDURES"),
    (116, "What is the PRIMARY objective of performing a vulnerability assessment following a business system update?", ["Improve the change control process.", "Update the threat landscape.", "Determine operational losses.", "Review the effectiveness of controls."], "D", "จำ: vuln assessment after update = review CONTROL EFFECTIVENESS"),
    (117, "What should an IS manager do FIRST when residual risk has increased?", ["Implement security measures to reduce the risk.", "Assess the business impact.", "Transfer the risk to third parties.", "Communicate the information to senior management."], "B", "จำ: residual risk ↑ → FIRST = ASSESS BUSINESS IMPACT"),
    (118, "What is the PRIMARY reason for an IS manager to present the business case for an IS initiative to senior management?", ["To aid management in the decision-making process for purchasing the solution", "To represent stakeholders who will benefit from enhancements in IS", "To provide management with the status of the IS program", "To demonstrate due diligence involved with selecting the solution"], "A", "จำ: business case to senior = AID DECISION-MAKING"),
    (119, "Security patches were not installed on a critical server because the app owner blocked them to avoid interrupting the application. What should the IS manager do FIRST?", ["Report the risk to the IS steering committee.", "Determine mitigation options with IT management.", "Communicate the potential impact to the application owner.", "Escalate the risk to senior management."], "C", "จำ: patch blocked by app owner → FIRST = communicate IMPACT to app owner"),
    (120, "Which BEST indicates an effective vulnerability management program?", ["Security incidents are reported in a timely manner.", "Threats are identified accurately.", "Controls are managed proactively.", "Risks are managed within acceptable limits."], "D", "จำ: effective vuln mgmt = risks within ACCEPTABLE LIMITS"),
    (121, "An organization experienced multiple instances of privileged users misusing their access. Which process would be MOST helpful in identifying violations?", ["Policy exception review", "Review of access controls", "Security assessment", "Log review"], "D", "จำ: privilege misuse identification = LOG REVIEW"),
    (122, "An IS manager discovers a new policy is not being followed across all departments. Which should be of GREATEST concern?", ["Business unit management has not emphasized the importance of the new policy.", "Different communication methods may be required for each business unit.", "The wording of the policy is not tailored to the audience.", "The corresponding controls are viewed as prohibitive to business operations."], "D", "จำ: policy not followed → GREATEST concern = controls PROHIBITIVE to business"),
    (123, "Which is the BEST defense against a brute force attack?", ["Intruder detection lockout", "Time-of-day restrictions", "Discretionary access control", "Mandatory access control"], "A", "จำ: brute force = ACCOUNT LOCKOUT"),
    (124, "Which is the MOST important reason to involve external forensics experts in evidence collection?", ["To provide the response team with expert training on evidence handling", "To ensure evidence is handled by qualified resources", "To prevent evidence from being disclosed to any internal staff members", "To validate the incident response process"], "B", "จำ: external forensics = evidence handled by QUALIFIED resources (admissible)"),
    (125, "Which is the GREATEST benefit of integrating IS program requirements into vendor management?", ["The ability to meet industry compliance requirements", "The ability to define service level agreements (SLAs)", "The ability to reduce risk in the supply chain", "The ability to improve vendor performance"], "C", "จำ: IS in vendor mgmt = REDUCE SUPPLY CHAIN RISK"),
    (126, "Who should determine data access requirements for an application hosted at an organization's data center?", ["IS manager", "Business owner", "Data custodian", "Systems administrator"], "B", "จำ: data access requirements = BUSINESS OWNER decides"),
    (127, "Which is the MOST important objective of testing a security IR plan?", ["Ensure the thoroughness of the response plan.", "Verify the response assumptions are valid.", "Confirm that systems are recovered in the proper order.", "Validate the business impact analysis (BIA)."], "B", "จำ: IR plan test = VERIFY ASSUMPTIONS are valid"),
    (128, "Which is the MOST important reason for performing a cost-benefit analysis when implementing a security control?", ["To ensure the mitigation effort does not exceed the asset value", "To ensure benefits are aligned with business strategies", "To present a realistic IS budget", "To justify IS program activities"], "A", "จำ: CBA for control = mitigation cost ≤ ASSET VALUE"),
    (129, "An IS manager wants to document requirements for minimum security controls for user workstations. Which resource would be MOST appropriate?", ["Policies", "Standards", "Procedures", "Guidelines"], "B", "จำ: minimum security controls = STANDARDS"),
    (130, "Which information BEST supports risk management decision making?", ["Results of a vulnerability assessment", "Estimated savings resulting from reduced risk exposure", "Average cost of risk events", "Quantification of threats through threat modeling"], "D", "จำ: risk management decisions = THREAT MODELING (quantified)"),
    (131, "Which is MOST important to do after a security incident has been verified?", ["Notify the appropriate law enforcement authorities.", "Follow the escalation process to inform key stakeholders.", "Prevent the incident from creating further damage to the organization.", "Contact forensic investigators to determine the root cause."], "C", "จำ: incident verified → MOST important = PREVENT FURTHER DAMAGE"),
    (132, "Which should be the PRIMARY driver for selecting controls to address risk associated with weak user passwords?", ["The organization's risk tolerance", "The organization's culture", "The cost of risk mitigation controls", "Direction from senior management"], "A", "จำ: control selection = RISK TOLERANCE"),
    (133, "Which is MOST important to consider when determining the effectiveness of the IS governance program?", ["Key performance indicators (KPIs)", "Maturity models", "Risk tolerance levels", "Key risk indicators (KRIs)"], "A", "จำ: governance effectiveness = KPIs"),
    (134, "The business advantage of implementing authentication tokens is that they:", ["provide nonrepudiation.", "reduce overall cost.", "reduce administrative workload.", "improve access security."], "D", "จำ: authentication tokens = IMPROVE ACCESS SECURITY"),
    (135, "In an organization with several independent security tools, which is the BEST way to ensure timely detection of incidents?", ["Implement a log aggregation and correlation solution.", "Ensure the IR plan is endorsed by senior management.", "Ensure staff are cross-trained to manage all security tools.", "Outsource the management of security tools to a service provider."], "A", "จำ: multiple security tools → timely detection = LOG AGGREGATION + CORRELATION"),
    (136, "Which is the MAIN objective of a risk management program?", ["Reduce corporate liability for IS incidents.", "Reduce risk to the level of the organization's risk appetite.", "Reduce risk to the maximum extent possible.", "Reduce costs associated with incident response."], "B", "จำ: risk mgmt objective = reduce to RISK APPETITE level"),
    (137, "An IS manager was informed that a planned penetration test could potentially disrupt services. What should be the FIRST course of action?", ["Estimate the impact and inform the business owner.", "Accept the risk and document it in the risk register.", "Ensure the service owner is available during the penetration test.", "Reschedule the activity during an approved maintenance window."], "A", "จำ: pen test may disrupt → FIRST = estimate impact + inform BUSINESS OWNER"),
    (138, "The PRIMARY advantage of single sign-on (SSO) is that it will:", ["support multiple authentication mechanisms.", "strengthen user passwords.", "increase efficiency of access management.", "increase the security of related applications."], "C", "จำ: SSO = EFFICIENCY of access management"),
    (139, "Which is BEST determined by using technical metrics?", ["Whether controls are operating effectively", "How well security risk is being managed", "Whether security resources are adequately allocated", "How well the security strategy is aligned with organizational objectives"], "A", "จำ: technical metrics = whether CONTROLS OPERATING EFFECTIVELY"),
    (140, "The use of a business case is MOST effective when the business case:", ["relates the investment to the organization's strategic plan.", "realigns IS objectives to organizational strategy.", "articulates management's intent and IS directives in clear language.", "translates IS policies and standards into business requirements."], "A", "จำ: business case MOST effective = relates to STRATEGIC PLAN"),
    (141, "The MOST important objective of security awareness training for business staff is to:", ["understand intrusion methods.", "reduce negative audit findings.", "increase compliance.", "modify behavior."], "D", "จำ: security awareness = MODIFY BEHAVIOR"),
    (142, "Which is the PRIMARY responsibility of an IS steering committee?", ["Setting up password expiration procedures", "Drafting security policies", "Prioritizing security initiatives", "Reviewing firewall rules"], "C", "จำ: steering committee = PRIORITIZE security initiatives"),
    (143, "During a post-incident review, the sequence and correlation of actions must be analyzed PRIMARILY based on:", ["a consolidated event timeline.", "logs from systems involved.", "interviews with personnel.", "documents created during the incident."], "A", "จำ: post-incident sequence analysis = CONSOLIDATED EVENT TIMELINE"),
    (144, "Which is the MOST important element in the evaluation of inherent security risks?", ["Impact to the organization", "Control effectiveness", "Residual risk", "Cost of countermeasures"], "A", "จำ: inherent risk evaluation = IMPACT to organization"),
    (145, "Recovery time objectives (RTOs) are an output of which of the following?", ["Business continuity plan (BCP)", "Business impact analysis (BIA)", "Service level agreement (SLA)", "Disaster recovery plan (DRP)"], "B", "จำ: RTO comes from → BIA"),
    (146, "Which is the MOST relevant information to include in an IS risk report to senior management?", ["Detailed assessment of the security risk profile", "Risks inherent in new security technologies", "Findings from recent penetration testing", "Status of identified key security risks"], "D", "จำ: risk report to senior = STATUS of KEY security risks"),
    (147, "Which is MOST important to include in a contract with a critical service provider?", ["Escalation paths", "Termination language", "Key performance indicators (KPIs)", "Right-to-audit clause"], "D", "จำ: critical provider contract = RIGHT-TO-AUDIT clause"),
    (148, "Which is the BEST way to determine if a recent investment in access control software was successful?", ["Senior management acceptance of the access control software", "A comparison of security incidents before and after software installation", "A BIA of the systems protected by the software", "A review of the number of KRIs implemented for the software"], "B", "จำ: investment success = compare incidents BEFORE vs AFTER"),
    (149, "Which is the MOST effective way to mitigate the risk of confidential data leakage to unauthorized stakeholders?", ["Create a data classification policy.", "Implement role-based access controls.", "Require the use of login credentials and passwords.", "Conduct IS awareness training."], "B", "จำ: data leakage mitigation = ROLE-BASED ACCESS CONTROLS"),
    (150, "Which is the MOST important consideration when reporting the effectiveness of an IS program to key business stakeholders?", ["Linking security metrics to the business impact analysis (BIA)", "Demonstrating a decrease in IS incidents", "Demonstrating cost savings of each control", "Linking security metrics to business objectives"], "D", "จำ: reporting effectiveness = link metrics to BUSINESS OBJECTIVES"),
    (151, "The PRIMARY purpose of establishing an IS governance framework should be to:", ["establish the business case for strategic integration of IS in organizational efforts.", "document and communicate how the IS program functions within the organization.", "align IS strategy and investments to support organizational activities.", "align corporate governance, activities, and investments to IS goals."], "C", "จำ: IS governance = ALIGN IS strategy/investments to SUPPORT org activities"),
    (152, "Senior management is concerned that the IR team took unapproved actions. Which is the BEST way to respond?", ["Update roles and responsibilities of the IR team.", "Train the IR team on escalation procedures.", "Implement a monitoring solution for IR activities.", "Validate that the IS strategy maps to corporate objectives."], "B", "จำ: IR unapproved actions → TRAIN on escalation procedures"),
    (153, "An IR team determined there is a need to isolate a system communicating with a known malicious host. Who should be contacted FIRST?", ["The business owner", "Key customers", "Executive management", "System administrator"], "A", "จำ: isolate system → contact BUSINESS OWNER first"),
    (154, "Which external entities would provide the BEST guidance to an organization facing advanced attacks?", ["Incident response experts from peer organizations", "Open-source reconnaissance", "Recognized threat intelligence communities", "Disaster recovery consultants"], "C", "จำ: advanced attacks guidance = THREAT INTELLIGENCE communities"),
    (155, "Which should be an IS manager's MOST important criterion for determining when to review the IR plan?", ["When recovery time objectives (RTOs) are not met", "When missing information impacts recovery from an incident", "Before an internal audit of the IR process", "At intervals indicated by industry best practice"], "B", "จำ: review IR plan = when MISSING INFO impacts recovery"),
    (156, "During which stage of the SDLC should application security controls FIRST be addressed?", ["Software code development", "Configuration management", "Requirements gathering", "Application system design"], "C", "จำ: security in SDLC = REQUIREMENTS GATHERING (earliest)"),
    (157, "Which should be of MOST concern to an IS manager reviewing an organization's data classification program?", ["The classifications do not follow industry best practices.", "Labeling is not consistent throughout the organization.", "The program allows exceptions to be granted.", "Data retention requirements are not defined."], "B", "จำ: classification program concern = INCONSISTENT LABELING"),
    (158, "Which is PRIMARILY influenced by a business impact analysis (BIA)?", ["Recovery strategy", "Risk mitigation strategy", "Security strategy", "IT strategy"], "A", "จำ: BIA → RECOVERY STRATEGY"),
    (159, "The MAIN purpose of information security guidelines in a large international organization is to:", ["explain the organization's preferred practices for security.", "ensure all business units have the same strategic security goals.", "ensure all business units implement identical security procedures.", "provide evidence for auditors that security practices are adequate."], "B", "จำ: IS guidelines = SAME STRATEGIC GOALS (ไม่ใช่ identical procedures)"),
    (160, "An IS manager discovers the organization lacks several important security capabilities due to budget constraints. What is the BEST course of action?", ["Suggest deployment of open-source security tools.", "Establish a business case to demonstrate ROI of a security tool.", "Recommend that the organization avoid the most severe risks.", "Review the audit report and request funding to address findings."], "B", "จำ: no budget + missing capabilities = establish BUSINESS CASE with ROI"),
    (161, "What is the FIRST line of defense against criminal insider activities?", ["Signing security agreements by critical personnel", "Stringent and enforced access controls", "Validating the integrity of personnel", "Monitoring employee activities"], "C", "จำ: first defense vs insider = VALIDATING INTEGRITY (background check)"),
    (162, "The BEST way to report to the board on the effectiveness of the IS program is to present:", ["a summary of the most recent audit findings.", "a report of cost savings from process improvements.", "peer-group industry benchmarks.", "a dashboard illustrating key performance metrics."], "D", "จำ: board effectiveness report = DASHBOARD with KPMs"),
    (163, "An organization's outsourced firewall was poorly configured, allowing unauthorized access resulting in 48 hours of downtime. What should be the IS manager's NEXT course of action?", ["Reconfigure the firewall in accordance with best practices.", "Obtain supporting evidence that the problem has been corrected.", "Seek damages from the service provider.", "Revisit the contract and improve accountability of the service provider."], "B", "จำ: firewall incident by vendor → NEXT = verify EVIDENCE problem corrected"),
    (164, "Which is the MOST important requirement when establishing a process for responding to zero-day vulnerabilities?", ["The IT team updates antivirus signatures on user systems.", "The IT team implements an emergency patch deployment process.", "Business users stop using the impacted application until a patch is released.", "The IS team implements recommended workarounds."], "D", "จำ: zero-day response = IS team implements WORKAROUNDS"),
    (165, "An IS manager determined the mean time to prioritize IS incidents has increased. Which process would BEST enable addressing this concern?", ["Incident classification", "Incident response", "Forensic analysis", "Vulnerability assessment"], "A", "จำ: slow prioritization = fix INCIDENT CLASSIFICATION process"),
    (166, "An IS manager discovers that newly hired privileged users are not taking necessary steps to protect critical information. What is the BEST way to address this?", ["Publish an acceptable use policy and require signed acknowledgment.", "Turn on logging and record user activity.", "Communicate the responsibility and provide appropriate training.", "Implement a data loss prevention (DLP) solution."], "C", "จำ: new users not protecting info = COMMUNICATE responsibility + TRAIN"),
    (167, "Which should be the MOST important consideration when prioritizing risk remediation?", ["Evaluation of risk", "Duration of exposure", "Comparison to risk appetite", "Impact of compliance"], "C", "จำ: risk remediation priority = COMPARISON TO RISK APPETITE"),
    (168, "To set security expectations across the enterprise, the IS policy should be regularly reviewed and endorsed by:", ["security administrators.", "senior management.", "the chief information security officer (CISO).", "the IT steering committee."], "B", "จำ: policy endorsed by = SENIOR MANAGEMENT"),
    (169, "Senior management wants to provide mobile devices to its sales force. What should the IS manager do FIRST?", ["Develop an acceptable use policy.", "Conduct a vulnerability assessment on the devices.", "Assess risks introduced by the technology.", "Research mobile device management (MDM) solutions."], "C", "จำ: new mobile devices → FIRST = ASSESS RISKS introduced"),
    (170, "An IS manager needs to ensure security testing is conducted on a new system. Which would provide the HIGHEST level of assurance?", ["The vendor provides the results of a penetration test and code review.", "An independent party is directly engaged to conduct testing.", "The internal audit team runs a vulnerability assessment.", "The security team conducts a self-assessment against a recognized framework."], "B", "จำ: highest assurance = INDEPENDENT PARTY conducts testing"),
    (171, "An organization found a large number of assets with low-impact vulnerabilities. The NEXT action should be to:", ["transfer the risk to a third party.", "determine appropriate countermeasures.", "report to management.", "quantify the aggregated risk."], "D", "จำ: many small risks → QUANTIFY AGGREGATED risk"),
    (172, "Organization A offers e-commerce services. To confirm communication with Organization A, which would be BEST for a client to verify?", ["The URL of the e-commerce server", "The certificate of the e-commerce server", "The IP address of the e-commerce server", "The browser's indication of SSL use"], "B", "จำ: verify e-commerce identity = CERTIFICATE"),
    (173, "Which provides the MOST useful information for identifying security control gaps on an application server?", ["Risk assessments", "Penetration testing", "Threat models", "Internal audit reports"], "B", "จำ: control gaps on app server = PENETRATION TESTING"),
    (174, "Which component of an IS risk assessment is MOST valuable to senior management?", ["Residual risk", "Return on investment (ROI)", "Mitigation actions", "Threat profile"], "A", "จำ: risk assessment → senior mgmt cares about RESIDUAL RISK"),
    (175, "Which is the PRIMARY benefit of implementing a maturity model for IS management?", ["Gaps between current and desirable levels will be addressed.", "IS management costs will be optimized.", "IS strategy will be in line with industry best practice.", "Staff awareness of IS compliance will be promoted."], "A", "จำ: maturity model = GAPS between current and desired levels addressed"),
    (176, "An IS manager notes that security incidents are not being escalated appropriately by the help desk. Which is the BEST automated control?", ["Integrating automated SLA reporting into the help desk ticketing system", "Changing the default setting for all security incidents to the highest priority", "Integrating incident response workflow into the help desk ticketing system", "Implementing automated vulnerability scanning in the help desk workflow"], "C", "จำ: help desk not escalating → IR WORKFLOW integrated into ticketing"),
    (177, "An IS manager's PRIMARY objective for presenting key risks to the board of directors is to:", ["ensure appropriate IS governance.", "quantify reputational risks.", "meet IS compliance requirements.", "re-evaluate the risk appetite."], "A", "จำ: key risks to board = ensure IS GOVERNANCE"),
    (178, "Which should be the PRIMARY consideration when implementing a DLP solution?", ["Data ownership", "Data storage capabilities", "Data classification", "Selection of tools"], "C", "จำ: DLP PRIMARY = DATA CLASSIFICATION"),
    (179, "Which is the MOST important function of an IS steering committee?", ["Evaluating the effectiveness of IS controls on a periodic basis", "Defining the objectives of the IS framework", "Conducting regular independent reviews of the state of security", "Approving security awareness content prior to publication"], "B", "จำ: steering committee = DEFINE OBJECTIVES of IS framework"),
    (180, "When determining an acceptable risk level, which is the MOST important consideration?", ["Vulnerability scores", "System criticalities", "Risk matrices", "Threat profiles"], "B", "จำ: acceptable risk level = SYSTEM CRITICALITIES"),
    (181, "Which is MOST important to include when reporting IS risk to executive leadership?", ["Key performance objectives and budget trends", "Security awareness training participation and residual risk exposures", "Risk analysis results and key risk indicators (KRIs)", "IS risk management plans and control compliance"], "C", "จำ: IS risk to exec = RISK ANALYSIS RESULTS + KRIs"),
    (182, "During which development phase is it MOST challenging to implement security controls?", ["Implementation phase", "Post-implementation phase", "Design phase", "Development phase"], "B", "จำ: hardest to add security = POST-IMPLEMENTATION"),
    (183, "An employee is found using external cloud storage to share corporate info against policy. What should the IS manager do FIRST?", ["Block access to the cloud storage service.", "Determine the classification level of the information.", "Seek business justification from the employee.", "Inform higher management of a security breach."], "B", "จำ: policy violation (cloud share) → FIRST = determine DATA CLASSIFICATION"),
    (184, "Which is the MOST effective method of determining security priorities?", ["Vulnerability assessment", "Gap analysis", "Threat assessment", "Impact analysis"], "D", "จำ: determine security priorities = IMPACT ANALYSIS"),
    (185, "A measure of the effectiveness of the incident response capabilities of an organization is the:", ["number of incidents detected.", "number of employees receiving IR training.", "reduction of the annual loss expectancy (ALE).", "time to closure of incidents."], "D", "จำ: IR capability effectiveness = TIME TO CLOSURE"),
    (186, "An IS manager has determined a defense in depth strategy should be used. Which BEST describes this strategy?", ["Separate security controls for applications, platforms, programs, and endpoints", "Multi-factor login requirements for cloud service applications", "Deployment of nested firewalls within the infrastructure", "Strict enforcement of role-based access control (RBAC)"], "A", "จำ: defense in depth = SEPARATE controls at every layer"),
    (187, "Which is an IS manager's BEST approach when selecting cost-effective controls to meet business objectives?", ["Conduct a gap analysis.", "Focus on preventive controls.", "Align with industry best practice.", "Align with the risk appetite."], "D", "จำ: cost-effective controls = ALIGN WITH RISK APPETITE"),
    (188, "A business process owner has chosen to accept a risk because cost of remediation is greater than worst-case scenario. What should be the IS manager's NEXT course of action?", ["Document and schedule a date to revisit the issue.", "Document and escalate to senior management.", "Shut down the business application.", "Determine a lower-cost approach to remediation."], "A", "จำ: risk accepted (cost > impact) → DOCUMENT + schedule REVISIT date"),
    (189, "An organization wants to integrate IS into HR management processes. What should be the FIRST step?", ["Identify IS risk associated with the processes.", "Assess the business objectives of the processes.", "Evaluate the cost of IS integration.", "Benchmark the processes with best practice to identify gaps."], "B", "จำ: integrate IS into HR → FIRST = assess BUSINESS OBJECTIVES"),
    (190, "The MOST effective way to continuously monitor an organization's cybersecurity posture is to evaluate its:", ["compliance with industry regulations.", "key performance indicators (KPIs).", "level of support from senior management.", "timeliness in responding to attacks."], "B", "จำ: continuous monitoring cybersecurity posture = KPIs"),
    (191, "Which would provide the HIGHEST level of confidence in the integrity of data sent from one party to another?", ["Harden the communication infrastructure.", "Require files to be digitally signed before transmitted.", "Enforce multi-factor authentication on both ends.", "Require data to be transmitted over a secure connection."], "B", "จำ: highest confidence in data integrity = DIGITALLY SIGNED"),
    (192, "Which is MOST important to the successful implementation of an IS program?", ["Establishing key performance indicators (KPIs)", "Obtaining stakeholder input", "Understanding current and emerging technologies", "Conducting periodic risk assessments"], "B", "จำ: IS program success = STAKEHOLDER INPUT"),
    (193, "Which is the BEST way to strengthen the alignment of an IS program with business strategy?", ["Establishing an IS steering committee", "Increasing the frequency of control assessments", "Providing organizational training on IS policies", "Increasing budget for risk assessments"], "A", "จำ: align IS with business strategy = IS STEERING COMMITTEE"),
    (194, "Which is necessary to determine what would constitute a disaster for an organization?", ["Recovery strategy analysis", "Backup strategy analysis", "Risk analysis", "Threat probability analysis"], "C", "จำ: define 'disaster' = RISK ANALYSIS"),
    (195, "Management announced acquisition of a new company. IS manager is concerned about conflicting access rights during integration. What is the BEST approach?", ["Escalate concerns for conflicting access rights to management.", "Review access rights as the acquisition integration occurs.", "Implement consistent access control standards.", "Perform a risk assessment of the access rights."], "D", "จำ: acquisition + conflicting access rights → RISK ASSESSMENT"),
    (196, "Which metric provides the BEST measurement of the effectiveness of a security awareness program?", ["Variance of program cost to allocated budget", "The number of security breaches", "Mean time between incident detection and remediation", "The number of reported security incidents"], "D", "จำ: awareness effectiveness = # REPORTED incidents (aware = can report)"),
    (197, "The ULTIMATE responsibility for ensuring IS framework objectives are met belongs to:", ["the board of directors.", "the information security officer.", "the steering committee.", "the internal audit manager."], "A", "จำ: ULTIMATE responsibility = BOARD OF DIRECTORS"),
    (198, "Which is MOST likely to affect an organization's ability to respond to security incidents in a timely manner?", ["Lack of senior management buy-in", "Inadequate detective control performance", "Misconfiguration of SIEM tool", "Complexity of network segmentation"], "A", "จำ: timely IR affected by = lack of SENIOR MANAGEMENT BUY-IN"),
    (199, "After a server has been attacked, which is the BEST course of action?", ["Isolate the system.", "Initiate incident response.", "Conduct a security audit.", "Review vulnerability assessment."], "B", "จำ: server attacked → INITIATE INCIDENT RESPONSE"),
    (200, "When establishing classifications of security incidents for IR plan development, which provides the MOST valuable input?", ["Business impact analysis (BIA) results", "Recommendations from senior management", "The business continuity plan (BCP)", "Vulnerability assessment results"], "A", "จำ: incident classification input = BIA RESULTS"),
    (201, "What is the PRIMARY responsibility of the security steering committee?", ["Implement information security control.", "Develop information security policy.", "Set direction and monitor performance.", "Provide IS training to employees."], "C", "จำ: steering committee = SET DIRECTION + MONITOR performance"),
    (202, "The PRIMARY objective of a risk response strategy should be:", ["threat reduction.", "senior management buy-in.", "appropriate control selection.", "regulatory compliance."], "C", "จำ: risk response strategy = APPROPRIATE CONTROL SELECTION"),
    (203, "What should an IS manager do FIRST after a new cybersecurity regulation has been introduced?", ["Consult corporate legal counsel.", "Conduct a cost-benefit analysis.", "Update the IS policy.", "Perform a gap analysis."], "D", "จำ: new regulation → FIRST = GAP ANALYSIS"),
    (204, "Which is the MOST important security feature for an MDM program?", ["Ability to inventory devices", "Ability to remotely wipe devices", "Ability to locate devices", "Ability to push updates to devices"], "B", "จำ: MDM MOST important = REMOTE WIPE"),
    (205, "Which is the MOST relevant factor when determining the appropriate escalation process in the IR plan?", ["Significance of the affected systems", "Number of resources allocated to respond", "Resilience capability of the affected systems", "Replacement cost of the affected systems"], "A", "จำ: IR escalation = SIGNIFICANCE of affected systems"),
    (206, "Management expressed concerns that shadow IT may be a risk. What is the FIRST step?", ["Block the end user's ability to use shadow IT.", "Update the security policy to address shadow IT.", "Determine the value of shadow IT projects.", "Determine the extent of shadow IT usage."], "D", "จำ: shadow IT risk → FIRST = DETERMINE EXTENT of usage"),
    (207, "The PRIMARY purpose for defining key risk indicators (KRIs) for a security program is to:", ["support investments in the security program.", "compare security program effectiveness to benchmarks.", "provide information needed to take action.", "ensure mitigating controls meet specifications."], "C", "จำ: KRI purpose = provide info needed to TAKE ACTION"),
    (208, "Which is the MOST effective way to protect the authenticity of data in transit?", ["Digital signature", "Hash value", "Private key", "Public key"], "A", "จำ: data authenticity in transit = DIGITAL SIGNATURE"),
    (209, "An organization shares customer information across globally dispersed branches. Which should be the GREATEST concern?", ["Conflicting data protection regulations", "Cross-cultural differences between branches", "Insecure wide area networks (WANs)", "Decentralization of IS"], "A", "จำ: global data sharing = CONFLICTING DATA PROTECTION regulations"),
    (210, "An IS manager is assisting with RFP development for a new outsourced service requiring access to critical business information. The security manager should focus PRIMARILY on:", ["security requirements for the process being outsourced.", "risk-reporting methodologies.", "service level agreements (SLAs).", "security metrics."], "A", "จำ: RFP + critical data → PRIMARILY = SECURITY REQUIREMENTS"),
    (211, "Following a risk assessment, new countermeasures have been approved. Which should be performed NEXT?", ["Schedule the target end date for implementation activities.", "Develop an implementation strategy.", "Budget the total cost of implementation activities.", "Calculate the cost for each countermeasure."], "B", "จำ: countermeasures approved → NEXT = develop IMPLEMENTATION STRATEGY"),
    (212, "Which is the MOST effective defense against malicious insiders compromising confidential information?", ["Regular audits of access controls", "Strong background checks when hiring staff", "Prompt termination procedures", "Role-based access control"], "D", "จำ: malicious insiders + confidential info = ROLE-BASED ACCESS CONTROL"),
    (213, "An IS manager is asked for a short presentation on the current IT risk posture to the board of directors. Which would be MOST effective?", ["Gap analysis results", "Risk register", "Threat assessment results", "Risk heat map"], "D", "จำ: risk to board = RISK HEAT MAP (visual)"),
    (214, "Which provides the BEST assurance that a contracted third-party provider meets security requirements?", ["Continuous monitoring", "Due diligence questionnaires", "Right-to-audit clause in the contract", "Performance metrics"], "C", "จำ: BEST assurance of provider = RIGHT-TO-AUDIT clause"),
    (215, "Senior management is encouraging employees to use social media for promotional purposes. What should be the IS manager's FIRST step?", ["Incorporate social media into the security awareness program.", "Develop a guideline on the acceptable use of social media.", "Employ the use of a web content filtering solution.", "Develop a business case for a DLP solution."], "B", "จำ: social media for promo → FIRST = ACCEPTABLE USE guideline"),
    (216, "In addition to executive sponsorship and business alignment, which is MOST critical for IS governance?", ["Ownership of security", "Auditability of systems", "Allocation of training resources", "Compliance with policies"], "A", "จำ: IS governance critical = OWNERSHIP of security"),
    (217, "Which is a PRIMARY responsibility of the IS governance function?", ["Administering IS awareness training", "Advising senior management on optimal levels of risk appetite", "Defining security strategies to support organizational programs", "Ensuring adequate support for solutions using emerging technologies"], "C", "จำ: IS governance function = DEFINE SECURITY STRATEGIES"),
    (218, "Which is MOST important to the successful implementation of an IS program?", ["Key performance indicators (KPIs) are defined.", "Adequate security resources are allocated to the program.", "A balanced scorecard is approved by the steering committee.", "The program is developed using global security standards."], "B", "จำ: IS program success = ADEQUATE RESOURCES allocated"),
    (219, "To address the issue that IT performance pressures may conflict with IS controls, it is MOST important that:", ["the steering committee provides guidance and dispute resolution.", "the security policy is changed to accommodate IT performance pressure.", "IT policies and procedures are better aligned to security policies.", "noncompliance issues are reported to senior management."], "A", "จำ: IT vs IS conflict = STEERING COMMITTEE resolves"),
    (220, "Information security awareness programs are MOST effective when they are:", ["sponsored by senior management.", "reinforced by computer-based training.", "customized for each target audience.", "conducted at employee orientation."], "C", "จำ: awareness MOST effective = CUSTOMIZED per audience"),
    (221, "Which would BEST help an organization's ability to manage advanced persistent threats (APTs)?", ["Having a skilled IS team", "Increasing the IS budget", "Using multiple security vendors", "Having network detection tools in place"], "A", "จำ: APT management = SKILLED IS TEAM"),
    (222, "An employee has just reported the loss of a personal mobile device containing corporate information. What should the IS manager do FIRST?", ["Initiate incident response.", "Initiate a device reset.", "Conduct a risk assessment.", "Disable remote access."], "A", "จำ: lost mobile with corporate data → FIRST = INITIATE INCIDENT RESPONSE"),
    (223, "An organization fell victim to a spear-phishing attack that compromised MFA code. What is the MOST important follow-up action?", ["Communicate the threat to users.", "Install client anti-malware solutions.", "Implement firewall blocking of known attack signatures.", "Implement an advanced email filtering system."], "A", "จำ: MFA bypassed via phishing → COMMUNICATE THREAT to users"),
    (224, "Which is MOST important to communicate to stakeholders when approving exceptions to the IS policy?", ["Impact on the risk profile", "Need for compensating controls", "Time period for review", "Requirements for senior management reporting"], "A", "จำ: policy exception → communicate IMPACT ON RISK PROFILE"),
    (225, "To implement effective continuous monitoring of IT controls, an IS manager needs to FIRST ensure:", ["security alerts are centralized.", "periodic scanning of IT systems is in place.", "metrics are communicated to senior management.", "information assets have been classified."], "D", "จำ: continuous monitoring → FIRST = CLASSIFY information assets"),
    (226, "Which would provide the BEST evidence to senior management that security control performance has improved?", ["Demonstrated return on security investment", "Review of security metrics trends", "Results of an emerging threat analysis", "Reduction in inherent risk"], "B", "จำ: evidence of improved controls = SECURITY METRICS TRENDS"),
    (227, "Which is MOST important to consider when determining additional controls to be implemented for new legislation?", ["The IS strategy", "The organization's risk appetite", "The cost of noncompliance", "The IS policy"], "B", "จำ: new legislation controls = RISK APPETITE"),
    (228, "The PRIMARY benefit of a centralized time server is that it:", ["decreases the likelihood of an unrecoverable systems failure.", "reduces individual time-of-day requests by client applications.", "allows decentralized logs to be kept in synchronization.", "is required by password synchronization programs."], "C", "จำ: centralized time server = LOG SYNCHRONIZATION"),
    (229, "Which is MOST appropriate to communicate to senior management regarding information risk?", ["Risk profile changes", "Vulnerability scanning progress", "Defined risk appetite", "Emerging security technologies"], "A", "จำ: communicate to senior = RISK PROFILE CHANGES"),
    (230, "A new IS manager finds the organization uses short-term solutions, resources not tracked, and no assurance of compliance. What should be done FIRST to reverse this bottom-up approach?", ["Implement an IS awareness training program.", "Conduct a threat analysis.", "Establish an audit committee.", "Create an IS steering committee."], "D", "จำ: bottom-up security → reverse = CREATE STEERING COMMITTEE"),
    (231, "An IS manager has been tasked with developing materials to update the board, regulatory agencies, and the media about a security incident. What should be done FIRST?", ["Invoke the organization's IR plan.", "Set up communication channels for the target audience.", "Create a comprehensive singular communication.", "Determine the needs and requirements of each audience."], "D", "จำ: communicate to board/regulators/media → FIRST = know each AUDIENCE'S NEEDS"),
    (232, "Which is MOST appropriate to add to a dashboard illustrating risk level to senior management?", ["Results of risk and control testing", "Number of reported incidents", "Budget variance for IS", "Risk heat map"], "D", "จำ: dashboard for senior risk = RISK HEAT MAP"),
    (233, "When establishing escalation processes for a CSIRT, the organization's procedures should:", ["require events to be escalated whenever possible.", "provide unrestricted communication channels to executive leadership.", "specify step-by-step escalation paths to ensure an appropriate chain of command.", "recommend the same communication path for events to ensure consistency."], "C", "จำ: CSIRT escalation = STEP-BY-STEP escalation paths (chain of command)"),
    (234, "Which is the MOST beneficial outcome of testing an IR plan?", ["The response includes escalation to senior management.", "Test plan results are documented.", "Incident response time is improved.", "The plan is enhanced to reflect the findings of the test."], "D", "จำ: IR plan testing benefit = PLAN ENHANCED from findings"),
    (235, "The PRIMARY goal of a post-incident review should be to:", ["identify policy changes to prevent a recurrence.", "establish the cost of the incident to the business.", "determine why the incident occurred.", "determine how to improve the incident handling process."], "D", "จำ: post-incident review = improve INCIDENT HANDLING PROCESS"),
    (236, "Which will MOST effectively minimize the chance of inadvertent disclosure of confidential information?", ["Applying data classification rules", "Following the principle of least privilege", "Restricting the use of removable media", "Enforcing penalties for security policy violations"], "B", "จำ: inadvertent disclosure = LEAST PRIVILEGE"),
    (237, "Which type of control is an incident response team?", ["Detective", "Directive", "Corrective", "Preventive"], "C", "จำ: IR team = CORRECTIVE control"),
    (238, "It is MOST important for an IS manager to ensure that security risk assessments are performed:", ["during a root cause analysis.", "as part of the security business case.", "consistently throughout the enterprise.", "in response to the threat landscape."], "C", "จำ: risk assessments = CONSISTENTLY throughout enterprise"),
    (239, "Which BEST indicates the effectiveness of the vendor risk management process?", ["Increase in % of vendors certified to a globally recognized security standard", "Increase in % of vendors with a completed due diligence review", "Increase in % of vendors conducting mandatory security training", "Increase in % of vendors that have reported security breaches"], "B", "จำ: vendor risk effectiveness = % vendors with COMPLETED DUE DILIGENCE"),
    (240, "An organization has decided to store production data in a cloud environment. What should be the FIRST consideration?", ["Data transfer", "Data classification", "Data backup", "Data isolation"], "B", "จำ: cloud data → FIRST = DATA CLASSIFICATION"),
    (241, "Which is the PRIMARY reason an IS manager would contract with an external provider to perform penetration testing?", ["To obtain an independent network security certification", "To mitigate gaps in technical skills", "To obtain an independent view of vulnerabilities", "To obtain the full list of system vulnerabilities"], "C", "จำ: external pen test = INDEPENDENT VIEW of vulnerabilities"),
    (242, "An organization has outsourced its disaster recovery function. Which is the MOST important consideration when drafting the SLA?", ["Testing requirements", "Authorization chain", "Recovery time objectives (RTOs)", "Recovery point objectives (RPOs)"], "C", "จำ: DR SLA = RECOVERY TIME OBJECTIVES (RTOs)"),
    (243, "What is the PRIMARY objective of implementing standard security configurations?", ["Maintain a flexible approach to mitigate potential risk to unsupported systems.", "Minimize the operational burden of managing unsupported systems.", "Compare configurations between supported and unsupported systems.", "Control vulnerabilities and reduce threats from changed configurations."], "D", "จำ: standard security configs = CONTROL VULNERABILITIES + reduce change threats"),
    (244, "Which is MOST important to ensure when considering exceptions to an IS policy?", ["Exceptions are approved by executive management.", "Exceptions undergo regular review.", "Exceptions reflect the organizational risk appetite.", "Exceptions are based on data classification."], "C", "จำ: policy exceptions = REFLECT RISK APPETITE"),
    (245, "An external security audit reported multiple instances of control noncompliance. Which is MOST important for the IS manager to communicate to senior management?", ["The impact of noncompliance on the organization's risk profile", "An accountability report to initiate remediation activities", "Control owner responses based on root cause analysis", "A plan for mitigating the risk due to noncompliance"], "A", "จำ: non-compliance audit → communicate = IMPACT ON RISK PROFILE"),
    (246, "Which is the STRONGEST justification for granting a USB exception to policy?", ["Users accept the risk of noncompliance.", "The benefit is greater than the potential risk.", "USB storage devices are enabled based on user roles.", "Access is restricted to read-only."], "B", "จำ: exception justification = BENEFIT > RISK"),
    (247, "Which is an IS manager's FIRST priority after a high-profile system has been compromised?", ["Implement improvements to prevent recurrence.", "Identify the malware that compromised the system.", "Restore the compromised system.", "Preserve incident-related data."], "D", "จำ: system compromised → FIRST = PRESERVE evidence"),
    (248, "Which has the MOST direct impact on the usability of an organization's asset classification policy?", ["The granularity of classifications in the hierarchy", "The support of IT management for the classification scheme", "The frequency of updates to the organization's risk register", "The business objectives of the organization"], "A", "จำ: classification usability = GRANULARITY"),
    (249, "A corporate IS program is BEST positioned for success when:", ["staff is receptive to the program.", "senior management supports the program.", "security is thoroughly assessed in the program.", "the program aligns with industry best practice."], "B", "จำ: IS program success = SENIOR MANAGEMENT SUPPORT"),
    (250, "Following a significant change to the underlying code of an application, it is MOST important for the IS manager to:", ["inform senior management.", "update the risk assessment.", "validate the user acceptance testing (UAT).", "modify key risk indicators (KRIs)."], "B", "จำ: significant code change → UPDATE RISK ASSESSMENT"),
    (251, "Which is the PRIMARY responsibility of an IS steering committee composed of business unit management representation?", ["Oversee the execution of the IS strategy.", "Perform business impact analyses (BIAs).", "Manage the implementation of the IS plan.", "Monitor the treatment of IS risk."], "A", "จำ: steering committee (with business reps) = OVERSEE IS STRATEGY execution"),
    (252, "Audit trails of changes to source code and object code are BEST tracked through:", ["use of compilers.", "code review.", "program library software.", "job control statements."], "C", "จำ: code change audit trail = PROGRAM LIBRARY SOFTWARE"),
    (253, "Which should be determined FIRST when preparing a risk communication plan?", ["Reporting content", "Communication channel", "Target audience", "Reporting frequency"], "C", "จำ: risk communication plan → FIRST = TARGET AUDIENCE"),
    (254, "Which will protect the confidentiality of data transmitted over the Internet?", ["Message digests", "Encrypting file system", "Network address translation", "IPsec protocol"], "D", "จำ: Internet data confidentiality = IPsec protocol"),
    (255, "Which would MOST effectively communicate the benefits of an IS program to executive management?", ["Key performance indicators (KPIs)", "Threat models", "Key risk indicators (KRIs)", "Industry benchmarks"], "A", "จำ: IS program benefits to exec = KPIs"),
    (256, "Which process can be used to remediate identified technical vulnerabilities?", ["Updating the BIA", "Performing penetration testing", "Enforcing baseline configurations", "Conducting a risk assessment"], "C", "จำ: remediate technical vulns = ENFORCE BASELINE CONFIGURATIONS"),
    (257, "Which BEST enables the detection of advanced persistent threats (APTs)?", ["Vulnerability scanning", "SIEM system", "Internet gateway filtering", "Periodic reviews of IPS"], "B", "จำ: APT detection = SIEM (long-term correlation)"),
    (258, "Which is the BEST way to strengthen the security of corporate data on a personal mobile device?", ["Implementing a strong password policy", "Using containerized software", "Mandating use of pre-approved devices", "Implementing multi-factor authentication"], "B", "จำ: corporate data on personal device = CONTAINERIZATION"),
    (259, "An organization implemented a new security control, but several employees say it disrupts their ability to work. What is the IS manager's BEST course of action?", ["Evaluate compensating control options.", "Educate users about the vulnerability.", "Accept the vulnerability.", "Report the control risk to senior management."], "A", "จำ: control disrupts business = EVALUATE COMPENSATING controls"),
    (260, "Which would be MOST helpful when determining appropriate access controls for an application?", ["Industry best practices", "Gap analysis results", "End-user input", "Data criticality"], "D", "จำ: access controls for app = DATA CRITICALITY"),
    (261, "An IS manager became aware that a third-party provider is not in compliance with the SOW. What is the BEST course of action?", ["Assess the extent of the issue.", "Report the issue to legal personnel.", "Notify senior management of the issue.", "Initiate contract renegotiation."], "A", "จำ: SOW non-compliance → ASSESS EXTENT first"),
    (262, "An IR team encountered an unfamiliar type of cyber event that took significant time to identify. What is the BEST way to ensure similar incidents are identified more quickly?", ["Establish performance metrics for the team.", "Perform a post-incident review.", "Perform a threat analysis.", "Implement a SIEM solution."], "B", "จำ: slow identification of unfamiliar event → POST-INCIDENT REVIEW"),
    (263, "Who should an IS manager contact FIRST upon discovering that a cloud-based payment system may be infected with malware?", ["Senior management", "Affected customers", "Cloud service provider", "The incident response team"], "D", "จำ: possible cloud malware → FIRST = INCIDENT RESPONSE TEAM"),
    (264, "Operations were significantly impacted by a cyberattack resulting in data loss. Once the attack has been contained, what should the security team do NEXT?", ["Update the IR plan.", "Perform a root cause analysis.", "Implement compensating controls.", "Conduct a lessons learned exercise."], "B", "จำ: attack contained → NEXT = ROOT CAUSE ANALYSIS"),
    (265, "Which would BEST help ensure an organization's security program is aligned with business objectives?", ["The organization's board includes a dedicated IS advisor.", "The security strategy is reviewed and approved by the steering committee.", "Security policies are reviewed and approved by the CIO.", "Business leaders receive annual IS awareness training."], "B", "จำ: IS aligned to business = strategy reviewed by STEERING COMMITTEE"),
    (266, "When defining roles and responsibilities between an organization and cloud service provider, which situation would present the GREATEST risk?", ["The service agreement uses a custom-developed RACI instead of an industry standard RACI.", "The organization believes the provider accepted responsibility for issues that the provider did not accept.", "The organization and provider identified multiple IS responsibilities that neither party was planning to provide.", "The service agreement results in unnecessary duplication of effort."], "B", "จำ: cloud RACI risk = org ASSUMES provider covers what they DON'T"),
    (267, "An IT department plans to migrate an application to the public cloud. What is the IS manager's MOST important action?", ["Review cloud provider independent assessment reports.", "Provide cloud security requirements.", "Evaluate service level agreements (SLAs).", "Calculate security implementation costs."], "B", "จำ: cloud migration → IS manager = PROVIDE CLOUD SECURITY REQUIREMENTS"),
    (268, "An executive's personal mobile device used for business purposes is reported lost. The IS manager should respond based on:", ["the acceptable use policy.", "asset management guidelines.", "the BIA.", "incident classification."], "D", "จำ: lost exec mobile → respond based on INCIDENT CLASSIFICATION"),
    (269, "What is the BEST approach for an IS manager to reduce the impact on a security program due to turnover within the security staff?", ["Recruit certified staff", "Revise the IS program", "Document security procedures", "Ensure everyone is trained in their roles"], "C", "จำ: IS staff turnover impact = DOCUMENT security procedures"),
    (270, "Which role is BEST suited to validate user access requirements during an annual user access review?", ["Access manager", "System administrator", "Business owner", "IT director"], "C", "จำ: validate access requirements = BUSINESS OWNER"),
    (271, "For an organization experiencing outages due to malicious code, which is the BEST index of the effectiveness of countermeasures?", ["Number of virus infections detected", "Average recovery time per incident", "Amount of infection-related downtime", "Number of downtime-related help desk calls"], "C", "จำ: malware countermeasure effectiveness = INFECTION-RELATED DOWNTIME"),
    (272, "Which should be the MOST important consideration when reviewing an IS strategy?", ["Changes to the security budget", "New business initiatives", "Internal audit findings", "Recent security incidents"], "B", "จำ: review IS strategy = NEW BUSINESS INITIATIVES"),
    (273, "Human resources is evaluating potential SaaS cloud services. What should the IS manager do FIRST?", ["Perform a cost-benefit analysis of using cloud services.", "Conduct a security audit on the cloud service providers.", "Review the cloud service providers' control reports.", "Perform a risk assessment of adopting cloud services."], "D", "จำ: HR evaluating SaaS → IS FIRST = RISK ASSESSMENT of cloud adoption"),
    (274, "Which is the BEST way to evaluate the impact of threat events on an organization's IT operations?", ["Risk assessment", "Penetration testing", "Scenario analysis", "Controls review"], "C", "จำ: evaluate threat event impact = SCENARIO ANALYSIS"),
    (275, "Which BEST demonstrates that an anti-phishing campaign is effective?", ["Improved staff attendance in awareness sessions", "Decreased number of incidents that have occurred", "Decreased number of phishing emails received", "Improved feedback on the anti-phishing campaign"], "B", "จำ: anti-phishing effective = DECREASED INCIDENTS"),
    (276, "The GREATEST benefit resulting from well-documented IS procedures is that they:", ["facilitate security training of new staff.", "ensure that security policies are consistently applied.", "provide a basis for auditing security practices.", "ensure processes can be followed by temporary staff."], "B", "จำ: well-documented procedures = CONSISTENTLY APPLIED policies"),
    (277, "Which is the MOST reliable way to ensure network security incidents are identified as soon as possible?", ["Install stateful inspection firewalls.", "Conduct workshops and training sessions with end users.", "Collect and correlate IT infrastructure event logs.", "Train help desk staff to identify and prioritize security incidents."], "C", "จำ: network incidents ASAP = COLLECT + CORRELATE event logs"),
    (278, "Which would BEST help ensure compliance with an organization's IS requirements by an IT service provider?", ["Requiring an external security audit of the IT service provider", "Defining the business recovery plan with the IT service provider", "Defining IS requirements with internal IT", "Requiring regular reporting from the IT service provider"], "A", "จำ: ensure provider compliance = EXTERNAL SECURITY AUDIT"),
    (279, "Which is MOST important to include in an IS status report to senior management?", ["Review of IS policies", "List of recent security events", "Key risk indicators (KRIs)", "IS budget requests"], "C", "จำ: IS status to senior = KRIs"),
    (280, "Which MOST effectively allows for disaster recovery testing without interrupting business operations?", ["Structured walk-through", "Simulation testing", "Parallel testing", "Full interruption testing"], "C", "จำ: DR testing without interruption = PARALLEL testing"),
    (281, "The PRIMARY goal of the eradication phase in an IR process is to:", ["provide effective triage and containment of the incident.", "remove the threat and restore affected systems.", "maintain a strict chain of custody.", "obtain forensic evidence from the affected system."], "B", "จำ: eradication phase = REMOVE THREAT + RESTORE"),
    (282, "Which is MOST important to ensuring that incident management plans are executed effectively?", ["Management support and approval has been obtained.", "An IR maturity assessment has been conducted.", "A reputable managed security services provider has been engaged.", "The IR team has the appropriate training."], "D", "จำ: IR plans executed effectively = TRAINED IR TEAM"),
    (283, "To inform a risk treatment decision, which should the IS manager compare with the organization's risk appetite?", ["Gap analysis results", "Level of risk treatment", "Configuration parameters", "Level of residual risk"], "D", "จำ: risk treatment decision = compare RESIDUAL RISK vs risk appetite"),
    (284, "Which would be the MOST effective countermeasure against malicious programming that rounds down transaction amounts and transfers them to the perpetrator's account?", ["Set up an agent to run a virus-scanning program across platforms.", "Ensure that proper controls exist for code review and release management.", "Implement controls for continuous monitoring of middleware transactions.", "Apply the latest patch programs to the production operating systems."], "C", "จำ: salami attack (rounding) = CONTINUOUS MONITORING of transactions"),
    (285, "Which is the PRIMARY responsibility of an IS governance committee?", ["Reviewing the IS risk register", "Approving changes to the IS strategy", "Discussing upcoming IS projects", "Reviewing monthly IS metrics"], "B", "จำ: IS governance committee = APPROVE CHANGES to IS strategy"),
    (286, "The MOST important information for influencing management's support of IS is:", ["a report of a successful attack on a competitor.", "a demonstration of alignment with the business strategy.", "an identification of the overall threat landscape.", "an identification of organizational risks."], "B", "จำ: management support = DEMONSTRATE BUSINESS ALIGNMENT"),
    (287, "What should be an IS manager's MOST important consideration when reviewing a proposed upgrade to a production database?", ["Ensuring the application inventory is updated", "Ensuring residual risk is within appetite", "Ensuring a cost-benefit analysis is completed", "Ensuring senior management is aware of associated risk"], "B", "จำ: DB upgrade review = RESIDUAL RISK within appetite"),
    (288, "Prior to implementing a BYOD program, it is MOST important to:", ["review currently utilized applications.", "survey employees for requested applications.", "select mobile device management (MDM) software.", "develop an acceptable use policy."], "D", "จำ: before BYOD = ACCEPTABLE USE POLICY"),
    (289, "When developing an incident escalation process, the BEST approach is to classify incidents based on:", ["their root causes.", "information assets affected.", "recovery point objectives (RPOs).", "estimated time to recover."], "B", "จำ: incident escalation classification = INFORMATION ASSETS affected"),
    (290, "Which is the PRIMARY objective of defining a severity hierarchy for security incidents?", ["To streamline the risk analysis process", "To facilitate the classification of an organization's IT assets", "To prioritize available incident response resources", "To facilitate root cause analysis of incidents"], "C", "จำ: severity hierarchy = PRIORITIZE IR RESOURCES"),
    (291, "For an enterprise implementing a BYOD program, which would provide the BEST security of corporate data on unsecured mobile devices?", ["Device certification process", "Acceptable use policy", "Containerization solution", "Data loss prevention (DLP)"], "C", "จำ: BYOD corporate data on unsecured = CONTAINERIZATION"),
    (292, "Which should be the PRIMARY driver for delaying the delivery of an IS awareness program?", ["Change in senior management", "High employee turnover", "Employee acceptance", "Risk appetite"], "A", "จำ: delay awareness = CHANGE IN SENIOR MANAGEMENT"),
    (293, "An organization is developing a DR strategy and needs to identify each application's criticality to establish the recovery sequence. What is the BEST course of action?", ["Restore applications with the shortest recovery times first.", "Document the data flow and review the dependencies.", "Perform a BIA on each application.", "Identify which applications contribute the most cash flow."], "C", "จำ: recovery sequence + app criticality = BIA per application"),
    (294, "An organization's IT department needs to implement security patches. Reports indicate these patches could result in stability issues. What is the IS manager's BEST recommendation?", ["Research alternative software solutions.", "Evaluate the patches in a test environment.", "Increase monitoring after patch implementation.", "Research compensating security controls."], "B", "จำ: risky patches = EVALUATE IN TEST ENVIRONMENT"),
    (295, "An organization established a BYOD program. Which is the MOST important security consideration when allowing employees to use personal devices for corporate applications remotely?", ["Mandatory controls for maintaining security policy", "Mobile operating systems support", "Security awareness training", "Secure application development"], "A", "จำ: BYOD remote = MANDATORY controls for security policy"),
    (296, "What is the BEST way for an IS manager to ensure critical assets are prioritized in a new IS program?", ["Update operating procedures to include new requirements.", "Conduct security awareness training.", "Conduct an inventory of information assets.", "Backup information assets and store them offsite."], "C", "จำ: prioritize critical assets = ASSET INVENTORY"),
    (297, "Which would provide the MOST useful information when prioritizing controls to be added to a system?", ["The risk register", "Balanced scorecard", "Compliance requirements", "Baseline to industry standards"], "A", "จำ: control prioritization = RISK REGISTER"),
    (298, "An organization recently acquired a smaller company in a different geographic region. The BEST approach for addressing conflicts between parent security standards and local regulations is to:", ["Adopt the standards of the newly acquired company.", "Give precedence to the parent organization's standards.", "Create a local version of the parent organization's standards.", "Create a global version of the local regulations."], "C", "จำ: standards conflict post-acquisition = CREATE LOCAL VERSION of parent standards"),
    (299, "A new regulatory requirement affecting an organization's IS program is released. What should be the IS manager's FIRST course of action?", ["Conduct benchmarking.", "Perform a gap analysis.", "Notify the legal department.", "Determine the disruption to the business."], "B", "จำ: new regulatory requirement → FIRST = GAP ANALYSIS"),
    (300, "An organization wants to ensure its confidential data is isolated in a multi-tenanted cloud environment. What is the BEST way to ensure adequate protection?", ["Verify the provider follows a cloud service framework standard.", "Review the provider's IS policies and procedures.", "Obtain documentation of encryption management practices.", "Ensure an audit of the provider is conducted to identify control gaps."], "D", "จำ: multi-tenant cloud data = AUDIT the provider"),
    (301, "The BEST indication of a change in risk that may negatively impact an organization is an increase in:", ["security incidents reported by staff to the IS team.", "malware infections detected by anti-virus software.", "alerts triggered by the SIEM solution.", "events logged by the intrusion detection system (IDS)."], "A", "จำ: risk change indicator = STAFF-REPORTED incidents"),
    (302, "Which is MOST important when determining the criticality and sensitivity of an information asset?", ["Results of business continuity testing", "Number of threats that can impact the asset", "Investment required to protect the asset", "Business functions supported by the asset"], "D", "จำ: asset criticality/sensitivity = BUSINESS FUNCTIONS it supports"),
    (303, "To prevent ransomware attacks, it is MOST important to ensure:", ["adequate backup and restoration processes are in place.", "regular security awareness training is conducted.", "the latest security appliances are installed.", "updated firewall software is installed."], "A", "จำ: prevent ransomware = BACKUP + RESTORATION processes"),
    (304, "A security policy exception is leading to an unexpected increase in alerts about suspicious Internet traffic. What is the BEST course of action?", ["Remove the rules that trigger the increased number of alerts.", "Present a risk analysis with recommendations to senior management.", "Update the risk register so that senior management is kept informed.", "Evaluate and update the enterprise network security architecture."], "B", "จำ: exception causing risk ↑ → PRESENT RISK ANALYSIS to senior mgmt"),
    (305, "The MAIN purpose of documenting IS guidelines for use within a large international organization is to:", ["explain the organization's preferred practices for security.", "ensure that all business units have the same strategic security goals.", "ensure that all business units implement identical security procedures.", "provide evidence for auditors that security practices are adequate."], "A", "จำ: IS guidelines = PREFERRED PRACTICES (ไม่ใช่ mandatory)"),
    (306, "Senior management launched an initiative to streamline processes and reduce costs including security. What should the IS manager rely on MOST to allocate resources efficiently?", ["Capability maturity assessment", "Risk classification", "Return on investment (ROI)", "Internal audit reports"], "B", "จำ: allocate security resources efficiently = RISK CLASSIFICATION"),
    (307, "Which would be of GREATEST assistance in determining whether to accept residual risk of a critical security system?", ["Maximum tolerable outage (MTO)", "Recovery time objective (RTO)", "Available annual budget", "Cost-benefit analysis of mitigating controls"], "D", "จำ: accept residual risk? = CBA of mitigating controls"),
    (308, "Which should an IS manager do FIRST to address complaints that a newly implemented security control has slowed business operations?", ["Conduct user awareness training.", "Remove the control and identify alternatives.", "Discuss the issue with senior management for direction.", "Validate whether the control is operating as intended."], "D", "จำ: control slows business → FIRST = VALIDATE it's working correctly"),
    (309, "An IS manager is preparing IR plans for an organization that processes personal and financial information. Which is the MOST important consideration?", ["Aligning with an established industry framework", "Determining budgetary constraints", "Identifying regulatory requirements", "Aligning with enterprise architecture (EA)"], "C", "จำ: IR plan for PII/financial org = REGULATORY REQUIREMENTS"),
    (310, "An IS manager identified that security risks are not being treated in a timely manner. What is the BEST way to address this?", ["Assign a risk owner to each risk.", "Create mitigating controls to manage the risks.", "Provide regular updates about the current state of the risks.", "Re-perform risk analysis at regular intervals."], "A", "จำ: risks not treated timely = ASSIGN RISK OWNER"),
    (311, "Which would be MOST useful in determining how an organization will be affected by a new regulatory requirement for cloud services?", ["Data loss protection plan", "Risk assessment", "Information asset inventory", "Data classification policy"], "B", "จำ: new cloud regulation impact = RISK ASSESSMENT"),
    (312, "Which provides the BEST evidence that a newly implemented security awareness program has been effective?", ["There have been no reported successful phishing attempts.", "Employees from each department have completed the required training.", "There has been an increase in the number of phishing attempts reported.", "Senior management supports funding for ongoing awareness training."], "C", "จำ: awareness effective = ↑ PHISHING ATTEMPTS REPORTED"),
    (313, "An organization is considering deployment of encryption software organization-wide. The MOST important consideration should be whether:", ["a classification policy has been developed to incorporate need for encryption.", "the business strategy includes exceptions to the encryption standard.", "data can be recovered if encryption keys are misplaced.", "the implementation supports the business strategy."], "D", "จำ: encryption deployment = SUPPORTS BUSINESS STRATEGY"),
    (314, "From an IS perspective, legal issues associated with transborder flow of technology-related items are MOST often related to:", ["website transactions and taxation.", "encryption tools and personal data.", "lack of competition and free trade.", "software patches and corporate data."], "B", "จำ: transborder legal issues = ENCRYPTION tools + PERSONAL DATA"),
    (315, "Recovery time objectives (RTOs) are BEST determined by:", ["database administrators (DBAs).", "business managers.", "executive management.", "business continuity officers."], "B", "จำ: RTO determined by = BUSINESS MANAGERS"),
    (316, "Embedding security responsibilities into job descriptions is important PRIMARILY because it:", ["simplifies development of the security awareness program.", "aligns security to the HR function.", "strengthens employee accountability.", "supports access management."], "C", "จำ: security in job descriptions = EMPLOYEE ACCOUNTABILITY"),
    (317, "An IS manager finds a legacy application has no defined data owner. Who would be MOST helpful in identifying the appropriate data owner?", ["The individual responsible for providing support for the application", "The individual who manages the process supported by the application", "The individual who manages users of the application", "The individual who has the most privileges within the application"], "B", "จำ: find data owner = person who MANAGES the PROCESS the app supports"),
    (318, "An online trading company discovers a network attack has penetrated the firewall. What should be the IS manager's FIRST response?", ["Evaluate the impact to the business.", "Examine firewall logs to identify the attacker.", "Notify the regulatory agency of the incident.", "Implement mitigating controls."], "A", "จำ: network attack → FIRST = EVALUATE BUSINESS IMPACT"),
    (319, "Which is the BEST method for determining whether a firewall has been configured to provide comprehensive perimeter defense?", ["A port scan of the firewall from an internal source", "A simulated denial of service (DoS) attack against the firewall", "A validation of the current firewall rule set", "A ping test from an external source"], "C", "จำ: firewall perimeter defense = VALIDATE RULE SET"),
    (320, "To ensure a new application complies with IS policy, the BEST approach is to:", ["perform a vulnerability analysis.", "review security of the application before implementation.", "integrate security functionality during the development stage.", "periodically audit the security of the application."], "C", "จำ: app complies with IS policy = INTEGRATE SECURITY in DEVELOPMENT"),
    (321, "Which is the PRIMARY driver for determining the classification of application systems?", ["The cost of repairing damage to system elements", "The extent that compromise can affect revenue", "The cost to implement regulatory requirements", "Controlling access based on the need to know"], "B", "จำ: app classification = REVENUE impact from compromise"),
    (322, "Which department should be responsible for classifying CRM system data on a database maintained by IT?", ["Sales", "IS", "Human resources (HR)", "IT"], "A", "จำ: CRM data classification = SALES dept (business owner)"),
    (323, "What is the role of the IS manager in finalizing contract negotiations with service providers?", ["To perform a risk analysis on the outsourcing process", "To obtain a security standard certification from the provider", "To update security standards for the outsourced process", "To ensure that clauses for periodic audits are included"], "D", "จำ: IS manager in contract = ENSURE AUDIT CLAUSES included"),
    (324, "Which is the BEST justification for making a revision to a password policy?", ["A risk assessment", "Industry best practice", "Audit recommendation", "Vendor recommendation"], "A", "จำ: password policy revision = RISK ASSESSMENT justifies"),
    (325, "Which is MOST important for an IS manager to verify before conducting full-functional continuity testing?", ["IR and recovery plans are documented in simple language.", "Copies of recovery and IR plans are kept offsite.", "Teams and individuals responsible for recovery have been identified.", "Risk acceptance by the business has been documented."], "C", "จำ: before DR test = TEAMS & INDIVIDUALS identified"),
    (326, "The BEST indicator of the effectiveness of a security program conducted for users is an increase in the number of:", ["social engineering attempts reported to IS", "requests for more security training information", "participants in the security awareness program", "threats detected by IS staff"], "A", "จำ: security program effectiveness = ↑ SOCIAL ENGINEERING REPORTED"),
    (327, "When preventive controls to mitigate risk are not feasible, which is the MOST important action for the IS manager?", ["Identifying unacceptable risk levels", "Assessing vulnerabilities", "Evaluating potential threats", "Managing the impact"], "D", "จำ: no preventive controls = MANAGE THE IMPACT"),
    (328, "Which is MOST effective in reducing the financial impact following a security breach leading to data disclosure?", ["Backup and recovery strategy", "A business continuity plan (BCP)", "A data loss prevention (DLP) solution", "An incident response plan"], "D", "จำ: financial impact after breach = INCIDENT RESPONSE PLAN"),
    (329, "Which is the MOST effective way to prevent IS incidents?", ["Deploying intrusion detection tools in the network environment", "Deploying a consistent incident response approach", "Implementing a SIEM tool", "Implementing a security awareness training program for employees"], "D", "จำ: PREVENT IS incidents = SECURITY AWARENESS TRAINING"),
    (330, "Which is the MOST important consideration when updating procedures for managing security devices?", ["Updates based on changes in risk, technology, and process", "Review and approval of procedures by management", "Updates based on the organization's security framework", "Notification to management of the procedural changes"], "A", "จำ: procedure updates = changes in RISK + TECHNOLOGY + PROCESS"),
    (331, "Which is the MAJOR advantage of conducting a post-incident review?", ["Helps develop business cases for security monitoring tools", "Provides continuous process improvement", "Facilitates reporting on actions taken during the incident process", "Helps identify current and desired level of risk"], "B", "จำ: post-incident review = CONTINUOUS PROCESS IMPROVEMENT"),
    (332, "A modification to a critical system was not detected until the system was compromised. Which will BEST help prevent future occurrences?", ["Conducting continuous network monitoring", "Improving the change control process", "Conducting continuous risk assessments", "Baselining server configurations"], "B", "จำ: undetected modification → IMPROVE CHANGE CONTROL process"),
    (333, "What would be the MAIN purpose of an immediate post-incident review after a comprehensive test of the IR plan?", ["To reduce costs associated with IR efforts", "To determine ways to improve IR plan processes", "To document weaknesses for the next IR plan test", "To revalidate IR plan activities"], "B", "จำ: post-IR test review = IMPROVE IR PLAN PROCESSES"),
    (334, "An organization recently activated its BCP. All employees were notified, but some did not fully follow the communications plan. What is the BEST way to prevent a recurrence?", ["Perform tabletop testing with appropriate employees.", "Reprimand employees for not following the plan.", "Enhance external communication instructions in the BCP.", "Incorporate BCP communication expectations in job descriptions."], "A", "จำ: BCP comms failure → prevent recurrence = TABLETOP TESTING"),
    (335, "Which is MOST helpful in determining an organization's current capacity to mitigate risks?", ["Capability maturity model", "Vulnerability assessment", "Business impact analysis (BIA)", "IT security risk and exposure"], "A", "จำ: capacity to mitigate = CAPABILITY MATURITY MODEL"),
    (336, "Which is the BEST way to present the status of an IS program to senior management?", ["Detail latest security trends", "Display concise dashboards", "Provide detailed information regarding risk exposure", "Report on root causes of security incidents"], "B", "จำ: IS program status to senior = CONCISE DASHBOARDS"),
    (337, "Which should be the PRIMARY basis for an IS strategy?", ["Audit and regulatory requirements", "IS policies", "The organization's vision and mission", "Results of a comprehensive gap analysis"], "C", "จำ: IS strategy PRIMARY basis = VISION AND MISSION"),
    (338, "What should an IS manager do FIRST to establish a roadmap for security investments?", ["Perform cost-benefit analyses of the investments.", "Gain a thorough understanding of the organization's operating processes.", "Establish business cases for proposed security investments.", "Ensure investments are strategically aligned with business objectives."], "B", "จำ: security investment roadmap → FIRST = understand OPERATING PROCESSES"),
    (339, "Which is the MOST effective way to detect security incidents?", ["Analyze penetration test results", "Analyze security anomalies", "Analyze recent security risk assessments", "Analyze vulnerability assessments"], "B", "จำ: detect security incidents = ANALYZE ANOMALIES"),
    (340, "Which should be the PRIMARY outcome of an IS program?", ["Threat reduction", "Strategic alignment", "Risk elimination", "Cost reduction"], "B", "จำ: IS program PRIMARY outcome = STRATEGIC ALIGNMENT"),
    (341, "Which is the MOST effective way to help ensure web developers understand web application security risks?", ["Standardize secure web development practices.", "Integrate security into the early phases of the development life cycle.", "Incorporate security requirements into job descriptions.", "Implement a tailored security awareness training program."], "D", "จำ: developers understand web app risks = TAILORED TRAINING"),
    (342, "When collecting admissible evidence, which is the MOST important requirement?", ["Need to know", "Due diligence", "Chain of custody", "Preserving audit logs"], "C", "จำ: admissible evidence = CHAIN OF CUSTODY"),
    (343, "Which is the MOST effective way to detect IS incidents?", ["Establishing proper policies for response to threats and vulnerabilities", "Performing regular testing of the IR program", "Providing regular and up-to-date training for the IR team", "Educating end users on threat awareness and timely reporting"], "D", "จำ: detect IS incidents = EDUCATE END USERS on reporting"),
    (344, "During the due diligence phase of an acquisition, the MOST important course of action for an IS manager is to:", ["review the state of security awareness.", "review IS policies.", "perform a risk assessment.", "perform a gap analysis."], "C", "จำ: M&A due diligence = RISK ASSESSMENT"),
    (345, "After a major IS incident, which will BEST help an IS manager determine corrective actions?", ["Preserving the evidence", "Performing an impact analysis", "Calculating cost of the incident", "Conducting a postmortem assessment"], "D", "จำ: determine corrective actions after incident = POSTMORTEM"),
    (346, "An IS manager reads on social media that a recently purchased vendor product has been compromised and customer data has been posted online. What should be done FIRST?", ["Activate the IR program.", "Validate the risk to the organization.", "Perform a BIA.", "Notify local law enforcement agencies of a breach."], "B", "จำ: social media vendor breach report → FIRST = VALIDATE risk to org"),
    (347, "Which analysis will BEST identify the external influences to an organization's IS?", ["Threat analysis", "Business impact analysis (BIA)", "Gap analysis", "Vulnerability analysis"], "A", "จำ: external influences = THREAT ANALYSIS"),
    (348, "Which would provide the MOST value to senior management when presenting risk assessment results?", ["Mapping the risks to existing controls", "Illustrating risk on a heat map", "Providing a technical risk assessment report", "Mapping the risks to the security classification scheme"], "B", "จำ: risk assessment to senior = HEAT MAP"),
    (349, "Which is the MOST effective approach to ensure IT processes are performed in compliance with IS policies?", ["Ensuring that key controls are embedded in the processes", "Providing IS policy training to the process owners", "Allocating sufficient resources", "Identifying risks in the processes and managing those risks"], "A", "จำ: IT process compliance = CONTROLS EMBEDDED in processes"),
    (350, "An organization's HR department is planning to migrate a legacy application to the cloud. What is the BEST way for the IS manager to support this effort?", ["Encrypt the data to the cloud so that data is secure.", "Conduct vulnerability scans on the cloud provider.", "Update the policies to add controls for protecting the data.", "Conduct a security assessment on the cloud provider."], "D", "จำ: legacy to cloud migration → SECURITY ASSESSMENT of cloud provider"),
    (351, "What is the PRIMARY goal of an incident management program?", ["Contain the incident", "Communicate to external entities", "Minimize impact to the organization", "Identify root cause"], "C", "จำ: incident management goal = MINIMIZE IMPACT"),
    (352, "Which backup method requires the MOST time to restore data for an application?", ["Disk mirroring", "Differential", "Incremental", "Full backup"], "C", "จำ: MOST restore time = INCREMENTAL"),
    (353, "The PRIMARY advantage of performing black-box control tests as opposed to white-box tests is that they:", ["require less IT staff preparation.", "identify more threats.", "simulate real-world attacks.", "cause fewer potential production issues."], "C", "จำ: black-box = SIMULATE REAL-WORLD attacks"),
    (354, "Which is the GREATEST inherent risk when performing a DRP test?", ["Lack of communication to affected users", "Poor documentation of results and lessons learned", "Lack of coordination among departments", "Disruption to the production environment"], "D", "จำ: DRP test GREATEST risk = PRODUCTION DISRUPTION"),
    (355, "Inadvertent disclosure of internal business information on social media is BEST minimized by which of the following?", ["Implementing DLP solutions", "Limiting access to social media sites", "Developing social media guidelines", "Educating users on social media risks"], "D", "จำ: inadvertent social media disclosure = EDUCATE USERS"),
    (356, "Conflicting objectives are MOST likely to compromise the effectiveness of IS when IS management is:", ["partially staffed by external security consultants.", "combined with the change management function.", "reporting to the network infrastructure manager.", "outside of IT."], "C", "จำ: IS compromised by conflict = when IS reports to IT INFRA MANAGER"),
    (357, "Which is MOST important to the effectiveness of an IS program?", ["Organizational culture", "Risk management", "IT governance", "Security metrics"], "A", "จำ: IS program effectiveness = ORGANIZATIONAL CULTURE"),
    (358, "An IS manager has been asked to provide contract guidance for outsourcing payroll processing. Which is MOST important to address?", ["Vendor compliance with the most stringent data security regulations", "Vendor compliance with the organization's IS policies", "Vendor compliance with organizational SLA requirements", "Vendor compliance with recognized industry security standards"], "B", "จำ: outsource payroll = vendor comply with OUR IS POLICIES"),
    (359, "Which should include contact information for representatives of equipment and software vendors?", ["Business continuity plan (BCP)", "Service level agreements (SLAs)", "IS program charter", "Business impact analysis (BIA)"], "A", "จำ: vendor contact info in crisis = BCP"),
    (360, "Organization A offers e-commerce services. To confirm communication with Organization A, which would be BEST for a client to verify?", ["The certificate of the e-commerce server", "The browser's indication of SSL use", "The IP address of the e-commerce server", "The URL of the e-commerce server"], "A", "จำ: verify e-commerce identity = CERTIFICATE"),
    (361, "During the eradication phase of incident response, it is MOST important to:", ["identify the root cause.", "restore from the most recent backup.", "notify affected users.", "wipe the affected system."], "A", "จำ: eradication MOST important = IDENTIFY ROOT CAUSE"),
    (362, "Which should be an IS manager's FIRST course of action when a newly introduced privacy regulation affects the business?", ["Identify and assess the risk in the context of business objectives.", "Consult with IT staff and assess risk based on their recommendations.", "Update the security policy based on regulatory requirements.", "Propose relevant controls to ensure the business complies."], "A", "จำ: new privacy regulation → FIRST = ASSESS RISK in business context"),
    (363, "Which should be done FIRST once a cybersecurity attack has been confirmed?", ["Isolate the affected system.", "Power down the system.", "Notify senior management.", "Contact legal authorities."], "A", "จำ: attack confirmed → FIRST = ISOLATE"),
    (364, "Which is an IS manager's BEST course of action to gain approval for investment in a technical control?", ["Calculate the exposure factor.", "Perform a cost-benefit analysis.", "Conduct a risk assessment.", "Conduct a BIA."], "B", "จำ: gain approval for control investment = COST-BENEFIT ANALYSIS"),
    (365, "Which is an important criterion for developing effective key risk indicators (KRIs)?", ["The indicator provides a retrospective view of risk impacts and is measured annually.", "The indicator focuses on IT and accurately represents risk variances.", "The indicator aligns with KPIs and measures root causes of process performance issues.", "The indicator possesses a high correlation with a specific risk and is measured on a regular basis."], "D", "จำ: effective KRI = HIGH CORRELATION to specific risk + MEASURED REGULARLY"),
    (366, "A health care IS manager is notified of a possible breach of critical patient data. What should be done FIRST?", ["Notify health care regulators.", "Escalate the breach to senior management.", "Validate whether the breach occurred.", "Assess the possible impact of the breach."], "C", "จำ: POSSIBLE breach → FIRST = VALIDATE whether breach occurred"),
    (367, "Which presents the GREATEST risk associated with use of a SIEM system?", ["Low number of false negatives", "High number of false negatives", "Low number of false positives", "High number of false positives"], "B", "จำ: SIEM GREATEST risk = HIGH FALSE NEGATIVES (missed real incidents)"),
    (368, "Who should the IS manager consult FIRST when determining the severity level of a security incident involving a third-party vendor?", ["Risk manager", "Business partners", "IT process owners", "Business process owners"], "D", "จำ: incident severity with vendor = BUSINESS PROCESS OWNERS"),
    (369, "Recommendations for enterprise investment in security technology should be PRIMARILY based on:", ["availability of financial resources.", "alignment with business needs.", "the organization's risk tolerance.", "adherence to international standards."], "B", "จำ: security tech investment = ALIGNMENT WITH BUSINESS NEEDS"),
    (370, "When implementing a security policy for an organization handling PII, the MOST important objective should be:", ["strong encryption.", "regulatory compliance.", "security awareness training.", "data availability."], "B", "จำ: PII security policy = REGULATORY COMPLIANCE"),
    (371, "An IS manager received confirmation that the organization's e-commerce website was breached. What should be done FIRST?", ["Inform affected customers.", "Perform a vulnerability assessment.", "Execute the incident response plan.", "Take the affected systems offline."], "C", "จำ: confirmed breach → FIRST = EXECUTE IR PLAN"),
    (372, "Which would be MOST useful when illustrating to senior management the status of a recently implemented IS governance framework?", ["Periodic testing results", "A risk assessment", "A maturity model", "A threat assessment"], "C", "จำ: governance framework status = MATURITY MODEL"),
    (373, "An organization outsourced its incident management capabilities and just discovered a significant privacy breach. What is the MOST important action of the IS manager?", ["Follow the outsourcer's response plan.", "Refer to the organization's response plan.", "Notify the outsourcer of the privacy breach.", "Alert the appropriate law enforcement authorities."], "B", "จำ: outsourced IR but own breach → follow OWN RESPONSE PLAN"),
    (374, "Which would BEST support an IS manager's efforts to obtain management approval for an IAM system?", ["A recent security incident involving access authorization", "An established security policy with access management requirements", "A third-party audit finding based on regulatory requirements", "A business case proposal for the solution"], "D", "จำ: IAM approval = BUSINESS CASE proposal"),
    (375, "Internal audit reported a number of IS issues that are not in compliance with regulatory requirements. What should the IS manager do FIRST?", ["Create a security exception.", "Assess the risk to business operations.", "Perform a vulnerability assessment.", "Perform a gap analysis to determine needed resources."], "B", "จำ: audit non-compliance → FIRST = ASSESS RISK to business"),
    (376, "An organization is about to purchase a rival organization. The PRIMARY reason for performing IS due diligence prior to making the purchase is to:", ["determine the security exposures.", "assess the ability to integrate the security department operations.", "ensure compliance with international standards.", "evaluate the security policy and standards."], "A", "จำ: M&A IS due diligence = DETERMINE SECURITY EXPOSURES"),
    (377, "When considering whether to adopt BYOD, it is MOST important for the IS manager to ensure that:", ["the applications are tested prior to implementation.", "security controls are applied to each device when joining the network.", "users have read and signed acceptable use agreements.", "business leaders have an understanding of security risks."], "D", "จำ: BYOD adoption = BUSINESS LEADERS understand security risks"),
    (378, "The security baselines of an organization should be based on:", ["procedures.", "standards.", "policies.", "guidelines."], "B", "จำ: security baselines = STANDARDS"),
    (379, "Which would be MOST effective in changing the security culture and behavior of staff?", ["Promoting the IS mission within the enterprise", "Enforcing strict technical IS controls", "Auditing compliance with the IS policy", "Developing procedures to enforce the IS policy"], "A", "จำ: change culture/behavior = PROMOTE IS MISSION internally"),
    (380, "Which MUST be performed once risk has been accepted?", ["Reassess the risk on a regular basis.", "Calculate the business impact of acceptance.", "Flag the risk to avoid future reassessment.", "Remove the risk from the risk register."], "A", "จำ: risk accepted → MUST = REASSESS REGULARLY"),
    (381, "Which is the FIRST step in developing a business continuity plan (BCP)?", ["Identify critical business processes.", "Determine the business recovery strategy.", "Determine available resources.", "Identify the applications with the shortest RTOs."], "A", "จำ: BCP FIRST step = IDENTIFY CRITICAL BUSINESS PROCESSES"),
    (382, "A multinational organization is required to follow governmental regulations with different security requirements at each operating location. The CISO should be MOST concerned with:", ["developing a security program that meets global and regional requirements.", "ensuring effective communication with local regulatory bodies.", "monitoring compliance with defined security policies and standards.", "using industry best practice to meet local legal regulatory requirements."], "A", "จำ: multinational CISO = program meets GLOBAL + REGIONAL requirements"),
    (383, "Which is the MOST important consideration when defining security configuration baselines?", ["The baselines address applicable regulatory standards.", "The baselines are proportionate to risk.", "The baselines address known system vulnerabilities.", "The baselines align with lines of business."], "B", "จำ: security config baselines = PROPORTIONATE TO RISK"),
    (384, "An anomaly-based IDS operates by gathering data on:", ["normal network behavior and using it as a baseline for measuring abnormal activity.", "abnormal network behavior and using it as a baseline for measuring normal activity.", "abnormal network behavior and issuing instructions to the firewall to drop rogue connections.", "attack pattern signatures from historical data."], "A", "จำ: anomaly IDS = NORMAL BEHAVIOR baseline → detect deviations"),
    (385, "Which factor would have the MOST significant impact on an organization's IS governance model?", ["Corporate culture", "Outsourced processes", "Number of employees", "Security budget"], "A", "จำ: IS governance model = CORPORATE CULTURE"),
    (386, "A newly appointed IS manager of a retailer discovers an HVAC vendor has remote access to stores. What should be the FIRST course of action?", ["Disconnect the real-time access.", "Conduct a penetration test of the vendor.", "Review the vendor contract.", "Review the vendor's technical security controls."], "C", "จำ: unknown vendor access → FIRST = REVIEW VENDOR CONTRACT"),
    (387, "Reverse lookups can be used to prevent successful:", ["denial of service (DoS) attacks.", "phishing attacks.", "session hacking.", "Internet protocol (IP) spoofing."], "D", "จำ: reverse lookups prevent = IP SPOOFING"),
    (388, "A post-incident review revealed that key stakeholders took longer than acceptable to decide whether an application should be shut down. What is the BEST course of action to rectify this?", ["Improve incident response criteria.", "Improve incident response testing.", "Define incident classification.", "Establish containment procedures."], "A", "จำ: slow shutdown decision → IMPROVE IR CRITERIA"),
    (389, "To help ensure that an IS training program is MOST effective, its contents should be:", ["aligned to business processes.", "based on employees' roles.", "based on recent incidents.", "focused on IS policy."], "B", "จำ: IS training effective = ROLE-BASED content"),
    (390, "A technical vulnerability assessment on a personnel information management server should be performed when:", ["the data owner leaves the organization unexpectedly.", "the number of unauthorized access attempts increases.", "changes are made to the system configuration.", "an unexpected server outage has occurred."], "C", "จำ: vuln assessment on server = when SYSTEM CONFIGURATION changes"),
    (391, "An organization purchased an Internet sales company. The IS manager's FIRST step to ensure the security policy framework encompasses the new business model is to:", ["perform a gap analysis.", "implement both companies' policies separately.", "merge both companies' policies.", "perform a vulnerability assessment."], "A", "จำ: new acquisition + policy → FIRST = GAP ANALYSIS"),
    (392, "Relationships between critical systems are BEST understood by:", ["performing a BIA.", "developing a system classification scheme.", "evaluating key performance indicators (KPIs).", "evaluating the RTOs."], "A", "จำ: critical system relationships = BIA"),
    (393, "Determining the risk for a particular threat/vulnerability pair before controls are applied can be expressed as:", ["the likelihood of a given threat attempting to exploit a vulnerability.", "the magnitude of the impact should a threat exploit a vulnerability.", "a function of the cost and effectiveness of controls over a vulnerability.", "a function of the likelihood and impact should a threat exploit a vulnerability."], "D", "จำ: risk = function of LIKELIHOOD × IMPACT (inherent)"),
    (394, "When making decisions on prioritizing risk mitigation activities, which would provide senior management with the MOST comprehensive information?", ["Risk assessment report", "Risk action plan", "Risk register", "Internal audit report"], "C", "จำ: risk mitigation prioritization = RISK REGISTER"),
    (395, "What is the PRIMARY benefit of using key performance indicators (KPIs) for IS risk management?", ["Set targets against which the organization's IS function can be evaluated.", "Prevent potential undesirable events from affecting IS.", "Identify risk events that have already occurred.", "Establish the process for setting organizational objectives."], "A", "จำ: KPIs benefit = SET EVALUATION TARGETS"),
    (396, "Which is the MOST important consideration when reporting on the status of IS activities?", ["The report is comprehensive.", "The report is updated on a regular basis.", "The report is tailored to stakeholder needs.", "The report structure is consistent with industry standards."], "C", "จำ: IS status reporting = TAILORED TO STAKEHOLDER needs"),
    (397, "Which is the MOST important element when developing an IS strategy?", ["Identifying and classifying information assets", "Determining the needs of the business", "Aligning to applicable laws and regulations", "Determining the risk management methodology"], "B", "จำ: IS strategy element = BUSINESS NEEDS"),
    (398, "Which has the GREATEST influence on an organization's IS strategy?", ["Industry security standards", "The organizational structure", "The organization's risk tolerance", "IS awareness"], "C", "จำ: IS strategy influence = RISK TOLERANCE"),
    (399, "Which is the MOST effective way to demonstrate alignment of IS strategy with business objectives?", ["Balanced scorecard", "Benchmarking", "Heat map", "Risk matrix"], "A", "จำ: IS-business alignment = BALANCED SCORECARD"),
    (400, "An employee has reported losing a smartphone that contains sensitive information. The BEST step to address this situation is to:", ["remotely wipe the device.", "terminate the device connectivity.", "disable the user's access to corporate resources.", "escalate to the user's management."], "A", "จำ: lost smartphone with sensitive data = REMOTE WIPE"),
    (401, "Which BEST determines the allocation of resources during a security IR?", ["Defined levels of severity", "Senior management commitment", "A BCP", "An established escalation process"], "A", "จำ: IR resource allocation = SEVERITY LEVELS"),
    (402, "During the response to a serious security breach, who is the BEST organizational staff member to communicate with external entities?", ["The resource designated by senior management", "The incident response team leader", "The resource specified in the incident response plan", "A dedicated public relations spokesperson"], "C", "จำ: external comms during breach = RESOURCE IN IR PLAN"),
    (403, "Which is the BEST way to demonstrate the alignment of the IS strategy with the business strategy?", ["Show the relationship between IS goals and corporate goals.", "Compare the allocated budget for business with the IS budget.", "Present senior management's approval of IS policies.", "Provide evidence that IS is included in the change management process."], "A", "จำ: IS strategy alignment = show IS goals ↔ CORPORATE GOALS"),
    (404, "A newly appointed IS manager has been asked to update all security-related policies that have been static for five years or more. What is the BEST next step?", ["Gain an understanding of the current business direction.", "Update in accordance with the best business practices.", "Perform a risk assessment of the current IT environment.", "Assess corporate culture."], "A", "จำ: update static policies → FIRST = understand CURRENT BUSINESS DIRECTION"),
    (405, "Implementing the principle of least privilege PRIMARILY requires the identification of:", ["job duties.", "primary risk factors.", "authentication controls.", "data owners."], "A", "จำ: least privilege = identify JOB DUTIES"),
    (406, "Which is MOST helpful in preventing cybersecurity incidents?", ["Testing the backup plan according to a defined schedule", "Documenting and testing incident response plans", "Delivering periodic end-user security awareness training", "Implementing best practice password parameters"], "C", "จำ: prevent cybersecurity incidents = END-USER AWARENESS TRAINING"),
    (407, "Which is the MOST important consideration when determining which type of failover site to employ?", ["Disaster recovery test results", "Reciprocal agreements", "Recovery time objectives (RTOs)", "Data retention requirements"], "C", "จำ: failover site = RTO drives selection"),
    (408, "A risk owner has accepted a large amount of risk due to the high cost of controls. What should be the IS manager's PRIMARY focus?", ["Conducting an independent review of risk responses", "Establishing a strong ongoing risk monitoring process", "Presenting the risk profile for approval by the risk owner", "Updating the IS standards to include the accepted risk"], "B", "จำ: large risk accepted → MONITOR continuously"),
    (409, "Which is the MOST important constraint to be considered when developing an IS strategy?", ["Established security policies and standards", "IS architecture", "Compliance with an international security standard", "Legal and regulatory requirements"], "D", "จำ: IS strategy constraint = LEGAL + REGULATORY requirements"),
    (410, "Which would BEST justify continued investment in an IS program?", ["Speed of implementation", "Reduction in residual risk", "Industry peer benchmarking", "Security framework alignment"], "B", "จำ: justify IS investment = REDUCTION IN RESIDUAL RISK"),
    (411, "Which BEST facilitates the effective execution of an IR plan?", ["The plan is based on industry best practice.", "The IR plan aligns with the IT disaster recovery plan (DRP).", "The plan is based on risk assessment results.", "The response team is trained on the plan."], "D", "จำ: IR plan execution = TRAINED TEAM"),
    (412, "Which is the PRIMARY reason that an IS manager should restrict the use of generic administrator accounts?", ["To prevent accountability issues", "To ensure segregation of duties is maintained", "To ensure system audit trails are not bypassed", "To prevent unauthorized user access"], "A", "จำ: restrict generic accounts = prevent ACCOUNTABILITY issues"),
    (413, "Which document should contain the INITIAL prioritization of recovery of services?", ["Threat assessment", "IT risk analysis", "Business impact analysis (BIA)", "Business process map"], "C", "จำ: initial recovery prioritization = BIA"),
    (414, "A department head accepted risks from a recent assessment. No recommendations will be implemented even though required by regulatory oversight. What should the IS manager do NEXT?", ["Formally document the decision.", "Review the regulations.", "Review the risk monitoring plan.", "Perform a risk reassessment."], "A", "จำ: compliance gap risk accepted → FORMALLY DOCUMENT the decision"),
    (415, "A company has a remote office in a different country. The CISO just learned of a new regulatory requirement mandated by that country. What should be the NEXT step?", ["Integrate new requirements into the corporate policies.", "Evaluate whether the new regulation impacts IS.", "Create separate security policies for the new regulation.", "Implement the requirement at the remote office location."], "B", "จำ: foreign regulation → NEXT = EVALUATE impact on IS"),
    (416, "When integrating security risk management into an organization, it is MOST important to ensure:", ["the risk management methodology follows an established framework.", "business units approve the risk management methodology.", "the risk treatment process is defined.", "IS policies are documented and understood."], "B", "จำ: integrate risk mgmt = BUSINESS UNITS APPROVE methodology"),
    (417, "Mitigating technology risks to acceptable levels should be based PRIMARILY upon:", ["business process requirements.", "business process reengineering.", "legal and regulatory requirements.", "IS budget."], "A", "จำ: mitigate tech risks = BUSINESS PROCESS REQUIREMENTS"),
    (418, "For the IS manager, integrating the various assurance functions is important PRIMARILY to enable:", ["consistent security.", "a security-aware culture.", "compliance with policy.", "comprehensive audits."], "A", "จำ: integrate assurance functions = CONSISTENT SECURITY"),
    (419, "An organization has concerns regarding a potential APT. To ensure risk is appropriately managed, what should be the organization's FIRST action?", ["Implement additional controls.", "Report to senior management.", "Initiate IR processes.", "Conduct an impact analysis."], "D", "จำ: APT concern → FIRST = IMPACT ANALYSIS"),
    (420, "Which role is accountable for ensuring the impact of a new regulatory framework on a business system is assessed?", ["Senior management", "Application owner", "Legal representative", "IS manager"], "A", "จำ: regulatory impact assessment accountability = SENIOR MANAGEMENT"),
    (421, "During the initiation phase of the SDLC for a software project, IS activities should address:", ["baseline security controls.", "security objectives.", "cost-benefit analyses.", "benchmarking security metrics."], "B", "จำ: SDLC initiation = SECURITY OBJECTIVES"),
    (422, "Which is the BEST way to reduce the risk associated with a successful social engineering attack targeting help desk staff?", ["Conduct security awareness training.", "Implement two-factor authentication.", "Block access to social media sites.", "Enforce role-based access to help desk systems."], "A", "จำ: social engineering at help desk = SECURITY AWARENESS TRAINING"),
    (423, "During implementation of a new system, which process proactively minimizes the likelihood of disruption and unauthorized alterations?", ["Password management", "Version management", "Change management", "Configuration management"], "C", "จำ: minimize disruption during implementation = CHANGE MANAGEMENT"),
    (424, "When evaluating risk from external hackers, the maximum exposure time would be the difference between:", ["log refresh and restoration.", "identification and resolution.", "detection and response.", "compromise and containment."], "D", "จำ: max exposure time = COMPROMISE → CONTAINMENT"),
    (425, "What should be the FIRST step when implementing data loss prevention (DLP) technology?", ["Build a business case.", "Perform due diligence with vendor candidates.", "Classify the organization's data.", "Perform a cost-benefit analysis."], "C", "จำ: DLP implementation FIRST = CLASSIFY data"),
    (426, "When creating an IR plan, the PRIMARY benefit of establishing a clear definition of a security incident is that it helps to:", ["develop effective escalation and response procedures.", "make tabletop testing more effective.", "adequately staff and train IR teams.", "communicate the IR process to stakeholders."], "A", "จำ: clear incident definition = DEVELOP EFFECTIVE ESCALATION procedures"),
    (427, "A financial company executive is concerned about recently increasing cyberattacks. The organization would BEST respond by:", ["increasing budget and staffing levels for the IR team.", "revalidating and mitigating risks to an acceptable level.", "implementing an intrusion detection system (IDS).", "testing the BCP."], "B", "จำ: increasing cyberattacks = REVALIDATE + MITIGATE risks to acceptable level"),
    (428, "The effectiveness of an IS governance framework will BEST be enhanced if:", ["consultants review the IS governance framework.", "IS auditors are empowered to evaluate governance activities.", "a culture of legal and regulatory compliance is promoted by management.", "risk management is built into operational and strategic activities."], "D", "จำ: governance enhanced = RISK MANAGEMENT built into operations + strategy"),
    (429, "Which should be an IS manager's FIRST course of action when developing an incident management and response plan?", ["Reassess management's risk appetite.", "Conduct a gap analysis.", "Update the current risk register.", "Revise the BCP."], "B", "จำ: developing IR plan → FIRST = GAP ANALYSIS"),
    (430, "An IS manager has observed multiple exceptions for a number of different security controls. What should be the FIRST course of action?", ["Prioritize the risk and implement treatment options.", "Report the noncompliance to the board of directors.", "Inform respective risk owners of the impact of exceptions.", "Design mitigating controls for the exceptions."], "C", "จำ: multiple exceptions → FIRST = INFORM RISK OWNERS of impact"),
    (431, "Who is accountable for ensuring proper controls are in place to address confidentiality and availability of an information system?", ["Information owner", "Business manager", "Senior management", "IS manager"], "C", "จำ: accountability for system controls = SENIOR MANAGEMENT"),
    (432, "Which is the MOST effective way to help assure the integrity of an organization's accounting system?", ["Performing frequent security reviews of the audit log", "Implementing two-factor authentication", "Conducting an annual security audit of the system", "Providing security awareness training to accounting staff"], "A", "จำ: accounting system integrity = FREQUENT AUDIT LOG reviews"),
    (433, "An organization faces severe fines if not in compliance with local regulatory requirements by a deadline. Senior management asked the IS manager to prepare an action plan. Which would provide the MOST useful information for planning?", ["Results from a BIA", "Results from a gap analysis", "An inventory of security controls currently in place", "Deadlines and penalties for noncompliance"], "B", "จำ: compliance action plan = GAP ANALYSIS results"),
    (434, "An organization's HR department requires employee account privileges to be removed within three days of termination, but it currently takes up to four weeks. Which would BEST enable regulatory compliance?", ["Identity and access management (IAM) system", "Privileged access management (PAM) system", "Multi-factor authentication (MFA) system", "Governance risk and compliance (GRC) system"], "A", "จำ: multi-system access removal within deadline = IAM SYSTEM"),
    (435, "The IS manager of a multinational organization has been asked to consolidate IS policies of its regional locations. Which would be of GREATEST concern?", ["Varying threat environments", "Disparate reporting lines", "Conflicting legal requirements", "Differences in work culture"], "C", "จำ: consolidate multinational policies = CONFLICTING LEGAL requirements"),
    (436, "Which is the MOST important requirement for a successful security program?", ["Management decision on asset value", "Penetration testing on key systems", "Nondisclosure agreements (NDA) with employees", "Mapping security processes to baseline security standards"], "D", "จำ: successful security program = MAP processes to BASELINE STANDARDS"),
    (437, "Which is the GREATEST value provided by a SIEM system?", ["Facilitating the monitoring of risk occurrences", "Measuring impact of exploits on business processes", "Maintaining a repository base of security policies", "Redirecting event logs to an alternate location for BCP"], "A", "จำ: SIEM greatest value = MONITOR RISK OCCURRENCES"),
    (438, "A critical vulnerability is found on a server hosting applications from different business units. One BU finds its application won't function with the patch and chooses to accept the risk. What should the IS manager do NEXT?", ["Update the risk register.", "Develop a business case for compensating controls.", "Update the IS policy.", "Consult the incident management process."], "A", "จำ: risk accepted (won't patch) → NEXT = UPDATE RISK REGISTER"),
    (439, "The MOST important element in achieving executive commitment to an IS governance program is:", ["identified business drivers.", "a process improvement model.", "established security strategies.", "a defined security framework."], "A", "จำ: exec commitment to governance = IDENTIFIED BUSINESS DRIVERS"),
    (440, "Which recovery approach generally has the LOWEST periodic cost?", ["Shared contingency center", "Reciprocal agreement", "Redundant site", "Cold site"], "D", "จำ: LOWEST cost recovery = COLD SITE"),
    (441, "Which task should be performed once a DRP has been developed?", ["Identify recovery time objectives (RTOs).", "Develop the test plan.", "Analyze the business impact.", "Define response team roles."], "B", "จำ: after DRP developed = DEVELOP TEST PLAN"),
    (442, "Which should be the MOST important consideration of business continuity management?", ["Ensuring human safety", "Securing critical information assets", "Ensuring the reliability of backup data", "Identifying critical business processes"], "A", "จำ: BCP MOST important = HUMAN SAFETY"),
    (443, "Which should be the FIRST step of incident response procedures?", ["Classify the event depending on severity and type.", "Perform a risk assessment to determine the business impact.", "Evaluate the cause of the control failure.", "Identify if there is a need for additional technical assistance."], "A", "จำ: IR procedures FIRST = CLASSIFY the event"),
    (444, "Which is the BEST method for reducing the risk of data loss due to phishing attacks?", ["Changing passwords frequently", "Implementing data loss prevention.", "Using spam filtering solutions.", "Educating users."], "D", "จำ: phishing data loss = EDUCATE USERS"),
    (445, "Which tool provides an IR team with the GREATEST insight into insider threat activity across multiple systems?", ["An IAM system", "A VPN with multi-factor authentication", "A SIEM system", "An intrusion prevention system (IPS)"], "C", "จำ: insider threat across systems = SIEM"),
    (446, "Which is MOST important to the effectiveness of an IS program?", ["The program is aligned to legal and regulatory requirements.", "The program is aligned to a security control framework.", "Annual audits of the program are conducted.", "Users are trained on security policies and procedures."], "D", "จำ: IS program effectiveness = USERS TRAINED on policies/procedures"),
    (447, "Conducting a BIA BEST helps to identify:", ["asset inventory.", "mitigation costs.", "residual risk.", "system criticality."], "D", "จำ: BIA identifies = SYSTEM CRITICALITY"),
    (448, "An employee who denies accusations of downloading inappropriate material has been discharged. Legal evidence is required. What is the IS manager's BEST recommendation?", ["Delete all inappropriate material after taking a local copy.", "Create a forensic image of the original file system.", "Log in to the employee's device and create a local copy to USB.", "Rely on server backup allowing strict access control."], "B", "จำ: legal evidence for misconduct = FORENSIC IMAGE of original"),
    (449, "An IS manager wants to implement a SIEM system. Which would BEST support the business case to senior management?", ["Industry examples of threats detected using a SIEM system", "Alignment with industry best practices", "Independent evidence of a SIEM system's ability to reduce risk", "Metrics related to the number of systems to be consolidated"], "C", "จำ: SIEM business case = INDEPENDENT EVIDENCE of risk reduction"),
    (450, "The PRIMARY objective of performing a post-incident review is to:", ["identify control improvements.", "identify vulnerabilities.", "re-evaluate the impact of incidents.", "identify the root cause."], "A", "จำ: PIR PRIMARY = IDENTIFY CONTROL IMPROVEMENTS"),
    (451, "In a call center, the BEST reason to conduct a social engineering exercise is to:", ["gain funding for IS initiatives.", "identify candidates for additional security training.", "improve password policy.", "minimize the likelihood of successful attacks."], "D", "จำ: SE exercise in call center = MINIMIZE successful attacks"),
    (452, "The PRIMARY purpose of a penetration test is to:", ["test network load capability.", "validate firewall and router configuration.", "provide assurance of the security of the network.", "identify vulnerabilities at a particular point in time."], "D", "จำ: pen test PRIMARY = IDENTIFY VULNERABILITIES at point in time"),
    (453, "An IS policy was amended to support a new IS strategy. What should be the IS manager's NEXT step?", ["Evaluate the alignment with business strategy.", "Update standards and procedures.", "Review technical controls.", "Refresh the security training program."], "B", "จำ: policy amended → NEXT = UPDATE STANDARDS + PROCEDURES"),
    (454, "Which needs to be established FIRST in order to categorize data properly?", ["A data protection policy", "A data flow diagram", "A data classification framework", "A data custodian"], "C", "จำ: categorize data → FIRST = DATA CLASSIFICATION FRAMEWORK"),
    (455, "Which is the BEST course of action when confidential information is inadvertently disseminated outside the organization?", ["Change the encryption keys.", "Declare an incident.", "Review compliance requirements.", "Communicate the exposure."], "B", "จำ: confidential info leaked outside = DECLARE AN INCIDENT"),
    (456, "An organization is performing an annual risk review. Which anticipated change will have the MOST significant impact on the IS strategy?", ["The renewal and renegotiation of the contract with its managed security services provider", "Migration of personal data to a new database system on a different server platform", "The expansion to an international location with unfamiliar security and privacy regulations", "Replacement of the aging enterprise-wide core firewall with a new solution"], "C", "จำ: IS strategy MOST impacted = expansion to NEW COUNTRY with UNFAMILIAR regulations"),
    (457, "Which provides the MOST assurance that a third-party hosting provider will be able to meet availability requirements?", ["The third party's BCP", "The third party's IR plan", "Right-to-audit clause", "Service level agreement (SLA)"], "D", "จำ: availability assurance from provider = SLA"),
    (458, "An organization permits storage of critical and sensitive information on employee-owned smartphones. Which is the BEST security control?", ["Monitoring how often the smartphone is used.", "Developing security awareness training.", "Requiring the backup of the organization's data by the user.", "Establishing the authority to remote wipe."], "D", "จำ: sensitive on personal device = AUTHORITY TO REMOTE WIPE"),
    (459, "A spear phishing attack tricked a user into installing a Trojan. Which would have been MOST effective in preventing this?", ["Application control", "Website blocking", "Internet filtering", "Network encryption"], "A", "จำ: Trojan install via phishing = APPLICATION CONTROL (whitelist)"),
    (460, "An IS manager has been asked to provide regular status reports to senior management regarding the IS program. Which would provide the MOST helpful information?", ["A list detailing the latest threats", "Number of phishing incidents per month", "Remediation activities performed", "Key performance indicators (KPIs)"], "D", "จำ: status reports to senior = KPIs"),
    (461, "Which would be the GREATEST threat posed by a DDoS attack on a public-facing web server?", ["Execution of unauthorized commands", "Unauthorized access to resources", "Defacement of website content", "Prevention of authorized access"], "D", "จำ: DDoS threat = PREVENT AUTHORIZED ACCESS (availability)"),
    (462, "Which is the BEST indication of IS strategy alignment with the business?", ["Number of business executives who attended IS awareness sessions", "Percentage of corporate budget allocated to IS initiatives", "Percentage of IS incidents resolved within defined SLAs", "Number of business objectives directly supported by IS initiatives"], "D", "จำ: IS-business alignment = # BUSINESS OBJECTIVES IS directly supports"),
    (463, "Which would BEST mitigate accidental data loss events?", ["Enforce a data hard drive encryption policy.", "Conduct a DLP audit.", "Conduct periodic user awareness training.", "Obtain senior management support for the IS strategy."], "C", "จำ: accidental data loss = USER AWARENESS TRAINING"),
    (464, "Which is a PRIMARY function of an incident response team?", ["To provide a single point of contact for critical incidents", "To provide a risk assessment for zero-day vulnerabilities", "To provide a BIA", "To provide effective incident mitigation"], "D", "จำ: IR team PRIMARY function = EFFECTIVE INCIDENT MITIGATION"),
    (465, "Using which metrics will BEST help to determine the resiliency of IT infrastructure security controls?", ["Percentage of outstanding high-risk audit issues", "Number of incidents resulting in disruptions", "Number of successful disaster recovery tests", "Frequency of updates to system software"], "B", "จำ: IT infrastructure resiliency = # INCIDENTS resulting in DISRUPTIONS"),
    (466, "Which is the MAIN reason for integrating an organization's IR plan with its business continuity process?", ["Incidents can escalate into disasters needing proper response.", "RTOs need to be determined.", "Incidents will be reported more timely when categorized as a disaster.", "Integration of the plan will reduce resource costs."], "A", "จำ: IR + BCP integration = INCIDENTS CAN ESCALATE TO DISASTERS"),
    (467, "Which should be the PRIMARY basis for a severity hierarchy for IS incident classification?", ["Legal and regulatory requirements", "Root cause analysis results", "Availability of resources", "Adverse effects on the business"], "D", "จำ: incident severity hierarchy = ADVERSE EFFECTS ON BUSINESS"),
    (468, "Which would BEST enable the timely execution of an IR plan?", ["Definition of trigger events", "Centralized service desk", "The introduction of a decision support tool", "Clearly defined data classification process"], "A", "จำ: timely IR execution = DEFINED TRIGGER EVENTS"),
    (469, "Which is the BEST approach to identify new security issues with IT systems and applications in a timely manner?", ["Requiring periodic security audits of IT systems", "Comparing current state to established industry benchmarks", "Performing a vulnerability assessment for each change to IT systems", "Integrating risk assessments into the change management process"], "D", "จำ: identify new security issues timely = risk assessment in CHANGE MANAGEMENT"),
    (470, "Which is MOST important to include in an IS strategy?", ["Industry benchmarks", "Stakeholder requirements", "Risk register", "Regulatory requirements"], "B", "จำ: IS strategy MOST important = STAKEHOLDER REQUIREMENTS"),
    (471, "The PRIMARY reason to create and externally store the disk hash value when performing forensic data acquisition is to:", ["validate the integrity during analysis.", "provide backup in case of media failure.", "reinstate original data when accidental changes occur.", "validate the confidentiality during analysis."], "A", "จำ: store hash externally = VALIDATE INTEGRITY during analysis"),
    (472, "Which is the MOST important issue in a penetration test?", ["Performing the test without any insider knowledge", "Having an independent group perform the test", "Having a defined goal as well as success and failure criteria", "Obtaining permission from audit"], "C", "จำ: pen test MOST important = DEFINED GOAL + success/failure criteria"),
    (473, "An organization conducted a postmortem analysis after experiencing a loss from an IS attack. The PRIMARY purpose should be to:", ["evaluate the impact.", "prepare for criminal prosecution.", "document lessons learned.", "update IS policies."], "C", "จำ: postmortem PRIMARY = DOCUMENT LESSONS LEARNED"),
    (474, "When a critical system incident is reported, the FIRST step of the incident handler should be to:", ["power off the system.", "determine the scope of the incident.", "validate the incident.", "notify the appropriate parties."], "C", "จำ: incident reported → FIRST = VALIDATE the incident"),
    (475, "A multinational organization is introducing a security governance framework. The IS manager's concern is that regional security practices differ. Which should be evaluated FIRST?", ["Training requirements of the framework", "Global framework standards", "Cross-border data mobility", "Local regulatory requirements"], "D", "จำ: multinational governance framework → FIRST evaluate = LOCAL REGULATORY requirements"),
    (476, "Several months after installing a new firewall with intrusion prevention features, a breach was discovered that came in through the firewall shortly after installation. This breach could have been detected earlier by implementing firewall:", ["web surfing controls.", "packet filtering.", "application awareness.", "log monitoring."], "D", "จำ: earlier breach detection via firewall = LOG MONITORING"),
    (477, "Which BEST enables successful identification of a potential IT security incident?", ["Configuration management standards", "Event correlation", "Network intrusion detection systems (NIDS)", "File integrity monitoring"], "B", "จำ: identify security incident = EVENT CORRELATION"),
    (478, "Which is MOST important when providing updates during a security incident?", ["Responding immediately to questions from the public", "Validating the reliability of information prior to dissemination", "Designating a communications representative", "Ensuring timely IS incident information to internal stakeholders"], "B", "จำ: incident updates = VALIDATE reliability BEFORE disseminating"),
    (479, "Which BEST demonstrates the added value of an IS program?", ["Security baselines", "A gap analysis", "A SWOT analysis", "A balanced scorecard"], "D", "จำ: IS program added value = BALANCED SCORECARD"),
    (480, "To overcome the perception that security is a hindrance to business activities, it is important for an IS manager to:", ["focus on compliance.", "reiterate the necessity of security.", "promote the relevance and contribution of security.", "rely on senior management to enforce security."], "C", "จำ: overcome security hindrance perception = PROMOTE RELEVANCE + CONTRIBUTION"),
    (481, "Which is the BEST indication of a mature IS program?", ["Security spending is below budget.", "Security incidents are managed properly.", "Security resources are optimized.", "Security audit findings are reduced."], "C", "จำ: mature IS program = SECURITY RESOURCES OPTIMIZED"),
    (482, "An organization recently updated and published its IS policy and standards. What should the IS manager do NEXT?", ["Update the organization's risk register.", "Develop a policy exception process.", "Communicate the changes to stakeholders.", "Conduct a risk assessment."], "C", "จำ: policy updated → NEXT = COMMUNICATE to stakeholders"),
    (483, "Which type of recovery site is MOST reliable and can support stringent recovery requirements?", ["Cold site", "Warm site", "Mobile site", "Hot site"], "D", "จำ: MOST reliable recovery site = HOT SITE"),
    (484, "Which has the MOST influence on the IS investment process?", ["Security key performance indicators (KPIs)", "Organizational risk appetite", "IT governance framework", "IS policy"], "B", "จำ: IS investment influenced by = RISK APPETITE"),
    (485, "An IS manager is performing a post-incident review. Which could have been prevented by conducting regular IR testing?", ["Stolen data", "The server being compromised", "The brute force attack", "Ignored alert messages"], "D", "จำ: regular IR testing prevents = IGNORED ALERTS"),
    (486, "Which is MOST important when designing an IS governance framework?", ["Assessing the availability of IS resources", "Assessing the current state of IS", "Aligning with the IS strategy", "Aligning with industry best practice frameworks"], "C", "จำ: design IS governance = ALIGN WITH IS STRATEGY"),
    (487, "A serious vulnerability was detected in a business application that can be exploited by external attackers. What is the IS manager's BEST course of action?", ["Implement temporary remediation.", "Request an immediate shutdown of the application.", "Report the risk to the business application owner.", "Ask the business application owner to apply the fix immediately."], "C", "จำ: app vuln = REPORT TO APPLICATION OWNER (they decide)"),
    (488, "Which is MOST important to consider when defining escalation processes for IR procedures?", ["Key risk indicators (KRIs)", "Business continuity plans (BCPs)", "Recovery time objectives (RTOs)", "Key performance indicators (KPIs)"], "C", "จำ: IR escalation = RTO drives urgency"),
    (489, "To optimize the implementation of IS governance in an organization, an IS manager should:", ["implement processes consistent with international standards.", "utilize existing governance structures when possible.", "ensure changes are consistent with existing standards.", "make gradual changes to governance to minimize employee resistance."], "B", "จำ: optimize IS governance = UTILIZE EXISTING governance structures"),
    (490, "Which should be the PRIMARY goal of IS?", ["Business alignment", "Regulatory compliance", "Data governance", "IS management"], "A", "จำ: IS PRIMARY goal = BUSINESS ALIGNMENT"),
    (491, "Which clause would represent the MOST significant potential exposure if included in a contract with a third-party service provider?", ["Provider responsibility in a disaster limited to best reasonable efforts", "Provider liability for loss of data limited to cost of physical media", "Audit rights limited to customer data and supporting infrastructure", "Access to escrowed software restricted to specific conditions"], "B", "จำ: worst contract clause = liability capped at COST OF PHYSICAL MEDIA only"),
    (492, "Which should be the PRIMARY basis for determining IS objectives?", ["Business strategy", "Regulatory requirements", "IS strategy", "Data classification"], "A", "จำ: IS objectives basis = BUSINESS STRATEGY"),
    (493, "Which is the BEST method to ensure compliance with password standards?", ["A user-awareness program", "Implementing password-synchronization software", "Using password-cracking software", "Automated enforcement of password syntax rules"], "D", "จำ: password standards compliance = AUTOMATED ENFORCEMENT"),
    (494, "The PRIMARY purpose for deploying IS metrics is to:", ["ensure that technical operations meet specifications.", "compare program effectiveness to benchmarks.", "support ongoing security budget requirements.", "provide information needed to make decisions."], "D", "จำ: IS metrics PRIMARY purpose = PROVIDE INFO FOR DECISIONS"),
    (495, "Which would BEST demonstrate the status of an organization's IS program to the board of directors?", ["The IS operations matrix", "Changes to IS risks", "IS program metrics", "Results of a recent external audit"], "C", "จำ: IS program status to board = IS PROGRAM METRICS"),
    (496, "An intrusion has been detected and contained. Which step BEST ensures the integrity of the recovered system?", ["Restore the application and data from a forensic copy.", "Install the OS, patches, and application from the original source.", "Restore the OS, patches, and application from a backup.", "Remove all signs of the intrusion from the OS and application."], "B", "จำ: post-intrusion system integrity = INSTALL FROM ORIGINAL SOURCE"),
    (497, "Which should an IS manager do FIRST when informed that customer data has been breached within a third-party vendor's environment?", ["Communicate the breach to leadership.", "Request and verify evidence of the breach.", "Notify the IR team.", "Review vendor obligations in the contract."], "B", "จำ: third-party breach reported → FIRST = VERIFY EVIDENCE"),
    (498, "Which is the GREATEST benefit of using cyber threat intelligence to improve an organization's patch management program?", ["It allows the organization to define its risk tolerance and appetite.", "It identifies when to use workarounds rather than patching.", "It reduces the number of patches the organization needs to apply.", "It provides information about exploited vulnerabilities to expedite patching."], "D", "จำ: threat intel + patch mgmt = INFO ON EXPLOITED vulns to prioritize"),
    (499, "Which method enables the MOST rigorous testing while avoiding disruption of normal business operations?", ["Walk-through test", "Full interruption test", "Parallel test", "Checklist review test"], "C", "จำ: rigorous testing without disruption = PARALLEL TEST"),
    (500, "An empowered security steering committee has decided to accept a critical risk. What is the IS manager's BEST course of action?", ["Notify the chief risk officer (CRO) and internal audit.", "Determine the impact to IS objectives.", "Remove the specific risk item from the risk register.", "Document the risk acceptance and justification."], "D", "จำ: steering committee accepts risk → IS manager = DOCUMENT acceptance + justification"),
]

# ── Q501-550 (Dump) ───────────────────────────────────────────────────────────
QUESTIONS += [
(501,"Which of the following is the PRIMARY benefit of implementing an information security governance framework?",
["The framework provides a roadmap to maximize revenue through the secure use of technology.",
"The framework is able to confirm the validity of business goals and strategies.",
"The framework defines managerial responsibilities for risk impacts to business goals.",
"The framework provides direction to meet business goals while balancing risks and controls."],"D",
"จำ: IS governance PRIMARY benefit → direction to meet business goals while BALANCING risks and controls"),

(502,"Which of the following is the BEST way to prevent insider threats?",
["Implement strict security policies and password controls.",
"Conduct organization-wide security awareness training.",
"Enforce segregation of duties and least privilege access.",
"Implement logging for all access activities."],"C",
"จำ: prevent insider threats → segregation of duties + least privilege (LIMIT access)"),

(503,"Which of the following should be done FIRST to ensure a new critical cloud application can be supported by internal personnel?",
["Establish a capability maturity model.",
"Develop a training plan.",
"Conduct a risk assessment.",
"Perform a skills gap analysis."],"D",
"จำ: support new app → FIRST = skills GAP ANALYSIS (รู้ก่อนว่าขาดอะไร)"),

(504,"An organization is conducting a post-incident review to determine root cause. Which situation would be MOST harmful to this investigation?",
["Unencrypted logs of the affected systems were saved on magnetic tapes.",
"Antivirus signature update processes failed on the affected systems.",
"Systems logs were cleared by the administrator to free up space on the affected systems.",
"The incident response plan has not been updated during the past year."],"C",
"จำ: MOST harmful to investigation → logs CLEARED (ทำลายหลักฐาน)"),

(505,"When building support for an information security program, which of the following elements is MOST important?",
["Business impact analysis (BIA)",
"Identification of existing vulnerabilities",
"Threat analysis",
"Information risk assessment"],"A",
"จำ: building support for IS program → BIA (แสดง business impact ให้ mgmt เห็น)"),

(506,"Capacity planning would prevent:",
["system downtime for scheduled security maintenance.",
"file system overload arising from distributed denial of service (DDoS) attacks.",
"application failures arising from insufficient hardware resources.",
"software failures arising from exploitation of buffer capacity vulnerabilities."],"C",
"จำ: capacity planning prevents → app failures from INSUFFICIENT HARDWARE resources"),

(507,"Which of the following is the MOST effective way to ensure information security policies are understood?",
["Implement a whistle-blower program.",
"Document security procedures.",
"Include security responsibilities in job descriptions.",
"Provide regular security awareness training."],"D",
"จำ: policies UNDERSTOOD → regular security AWARENESS TRAINING"),

(508,"Which of the following is the MOST effective method for testing an incident response plan?",
["Disaster recovery testing",
"Risk assessment",
"Tabletop exercises",
"Industry benchmarking"],"C",
"จำ: test IR plan MOST effective → TABLETOP EXERCISES"),

(509,"A penetration test was conducted by an accredited third party. What should be the IS manager's FIRST course of action?",
["Request funding needed to resolve the top vulnerabilities.",
"Ensure a risk assessment is performed to evaluate the findings.",
"Report findings to senior management.",
"Ensure vulnerabilities found are resolved within acceptable timeframes."],"B",
"จำ: after pen test → FIRST = risk assessment to EVALUATE findings"),

(510,"An IS steering committee must approve a key control. Which of the following is the MOST important input to assist the committee?",
["IT strategy",
"Security architecture",
"Risk assessment",
"Business case"],"D",
"จำ: steering committee approve control → BUSINESS CASE (ไม่ใช่ risk assessment)"),

(511,"What should a global IS manager do FIRST when a new regulation with significant impact will go into effect soon?",
["Perform a vulnerability assessment.",
"Perform a business impact analysis (BIA).",
"Perform a privacy impact assessment.",
"Perform a gap analysis."],"D",
"จำ: new regulation → FIRST = GAP ANALYSIS"),

(512,"Which of the following will have the MOST negative impact to the effectiveness of incident response processes?",
["High organizational risk tolerance",
"Decentralized incident monitoring",
"Ambiguous severity criteria",
"Manual incident reporting processes"],"C",
"จำ: IR effectiveness MOST negative → AMBIGUOUS SEVERITY CRITERIA (ไม่รู้จะ escalate เมื่อไหร่)"),

(513,"Which of the following tasks would provide a newly appointed IS manager with the BEST view of the organization's existing security posture?",
["Performing a business impact analysis (BIA)",
"Reviewing policies and procedures",
"Performing a risk assessment",
"Interviewing business managers and employees"],"C",
"จำ: BEST view of security posture → RISK ASSESSMENT"),

(514,"Which of the following is the MOST important consideration when developing incident classification methods?",
["Data classification",
"Data owner input",
"Service level agreements (SLAs)",
"Business impact"],"D",
"จำ: incident classification → MOST important = BUSINESS IMPACT"),

(515,"Which of the following should be the PRIMARY goal of an IS manager when designing information security policies?",
["Minimizing the cost of security controls",
"Reducing organizational security risk",
"Improving the protection of information",
"Achieving organizational objectives"],"D",
"จำ: IS policy PRIMARY goal → ACHIEVING ORGANIZATIONAL OBJECTIVES"),

(516,"An organization outsourced app development to a third party using contract programmers. Which provides BEST assurance that contractors comply with the organization's security policies?",
["Perform periodic security assessments of the contractors' activities.",
"Conduct periodic vulnerability scans of the application.",
"Require annual signed agreements of adherence to security policies.",
"Include penalties for noncompliance in the contracting agreement."],"A",
"จำ: contractors comply with policies → PERIODIC SECURITY ASSESSMENTS (verify จริง)"),

(517,"How does an IS steering committee facilitate the achievement of IS program objectives?",
["Monitoring information security resources",
"Making decisions on security priorities",
"Enforcing regulatory and policy compliance",
"Evaluating information security metrics"],"B",
"จำ: steering committee facilitates → MAKING DECISIONS on security priorities"),

(518,"Which of the following is the BEST reason to consolidate security operations teams across a global organization?",
["Compliance with regulatory requirements",
"Enhanced visibility of threats",
"Detection of fraud",
"Cost reduction"],"B",
"จำ: consolidate global security ops → ENHANCED VISIBILITY of threats"),

(519,"The business value of an information asset is derived from:",
["its replacement cost.",
"the risk assessment.",
"its criticality.",
"the threat profile."],"C",
"จำ: business value of asset → CRITICALITY (ไม่ใช่ cost)"),

(520,"A business unit handles sensitive PII with significant financial liability. Which is the BEST way to mitigate the risk?",
["Implementing audit logging on systems",
"Including indemnification into customer contracts",
"Contracting the process to a third party",
"Purchasing insurance"],"A",
"จำ: mitigate PII breach risk → AUDIT LOGGING (detect + evidence)"),

(521,"Which of the following would be impacted the MOST by a business decision to move from traditional computing to cloud computing?",
["Security awareness",
"Security standards",
"Security policies",
"Security strategy"],"D",
"จำ: move to cloud MOST impacts → SECURITY STRATEGY"),

(522,"Key risk indicators (KRIs) are MOST effective when they:",
["are mapped to core strategic initiatives.",
"allow for comparison with industry peers.",
"are redefined on a regular basis.",
"assess progress toward declared goals."],"A",
"จำ: KRIs MOST effective → mapped to CORE STRATEGIC INITIATIVES"),

(523,"An organization's IPS detected an unusually large number of external intrusion attempts in 24 hours. What should be the IS manager's FIRST course of action?",
["Perform security assessments on Internet-facing systems.",
"Identify the source and nature of the attempts.",
"Review the server and firewall audit logs.",
"Report the issue to senior management."],"B",
"จำ: large intrusion attempts → FIRST = IDENTIFY source and nature"),

(524,"Which should be the GREATEST consideration when determining the RTO for an in-house critical application?",
["Direction from senior management",
"Results of recovery testing",
"Determination of recovery point objective (RPO)",
"Impact of service interruption"],"D",
"จำ: determine RTO → GREATEST consideration = IMPACT of service interruption"),

(525,"Which of the following is the PRIMARY purpose of implementing information security standards?",
["To provide a basis for developing information security policies",
"To provide step-by-step instructions for performing security-related tasks",
"To provide management direction with a specific security objective",
"To establish a minimum acceptable security baseline"],"D",
"จำ: IS standards PRIMARY purpose → MINIMUM ACCEPTABLE security baseline"),

(526,"Which of the following should be the FIRST step in patch management procedures when receiving an emergency security patch?",
["Validate the authenticity of the patch.",
"Conduct comprehensive testing of the patch.",
"Schedule patching based on the criticality.",
"Install the patch immediately to eliminate the vulnerability."],"A",
"จำ: emergency patch FIRST → VALIDATE AUTHENTICITY (ของปลอมมีอยู่)"),

(527,"The MOST effective tools for responding to new and advanced attacks are those that detect attacks based on:",
["behavior analysis.",
"penetration testing.",
"signature analysis.",
"data packet analysis."],"A",
"จำ: detect new/advanced attacks → BEHAVIOR ANALYSIS (signatures ไม่รู้จัก zero-day)"),

(528,"When developing security processes for handling credit card data, the IS manager should FIRST:",
["ensure that systems that handle credit card data are segmented.",
"review industry best practices for handling secure payments.",
"ensure alignment with industry encryption standards.",
"review corporate policies regarding credit card information."],"D",
"จำ: handling credit card data FIRST → review CORPORATE POLICIES (align กับ org ก่อน)"),

(529,"What is the PRIMARY objective of information security involvement in the change management process?",
["To narrow the threat landscape",
"To ensure changes are not applied without prior authorization",
"To reduce the likelihood of control failure",
"To meet obligations for regulatory and legal compliance"],"C",
"จำ: IS in change management PRIMARY → REDUCE LIKELIHOOD of control failure"),

(530,"Which of the following is MOST likely to trigger an update and revision of information security policies?",
["Engagement with a new service provider",
"Replacement of the information security manager",
"Attainment of business process maturity",
"Changes in the organization's risk appetite"],"D",
"จำ: trigger policy update → CHANGES IN RISK APPETITE"),

(531,"A small org with limited budget has one IT staff member assigned to system admin, security admin, DBA, and app admin roles. What is the manager's BEST course of action?",
["Formally document IT administrator activities.",
"Automate user provisioning activities.",
"Maintain strict control over user provisioning activities.",
"Implement monitoring of IT administrator activities."],"D",
"จำ: one person has all roles (no SoD possible) → MONITOR all activities"),

(532,"What should an IS manager do FIRST when assessing conflicting requirements between global security standards and local regulations?",
["Conduct a gap analysis against local regulations.",
"Perform a cost-benefit analysis of compliance.",
"Create a local version of the organizational standards.",
"Prioritize the organizational standards over local regulations."],"A",
"จำ: global vs local regulation conflict → FIRST = GAP ANALYSIS against local regs"),

(533,"Which of the following is the BEST method to reduce the risk of an IS breach due to spear phishing?",
["Implementing a vulnerability management program",
"Deploying an intrusion protection system (IPS)",
"Establishing a company-wide information security awareness plan",
"Reviewing log files daily to identify any suspicious activity"],"C",
"จำ: spear phishing → SECURITY AWARENESS PLAN (human = target)"),

(534,"A desktop computer is being used to perpetrate a fraud, and data must be secured for evidence. What should be done FIRST?",
["Encrypt the content of the hard drive using a strong algorithm.",
"Obtain a hash of the desktop computer's internal hard drive.",
"Copy the data on the computer to an external hard drive.",
"Capture a forensic image of the computer."],"B",
"จำ: secure evidence FIRST → OBTAIN HASH (prove integrity before touching anything)"),

(535,"The PRIMARY purpose of an IS governance framework is to ensure that the IS strategy is an extension of:",
["organizational strategies.",
"information technology strategies.",
"formal enterprise architecture.",
"approved business cases."],"A",
"จำ: IS governance framework → IS strategy extends from ORGANIZATIONAL STRATEGIES"),

(536,"Which is the MOST important consideration for a global organization designing an IS awareness program?",
["National regulations",
"Program costs",
"Cultural backgrounds",
"Local languages"],"C",
"จำ: global awareness program → MOST important = CULTURAL BACKGROUNDS"),

(537,"Changes proposed to an ERP system would violate existing security standards. What should be done FIRST?",
["Perform a cost-benefit analysis.",
"Calculate business impact levels.",
"Validate current standards.",
"Implement updated standards."],"C",
"จำ: change violates standards → FIRST = VALIDATE CURRENT STANDARDS (อาจ outdated)"),

(538,"What should an IS manager do NEXT after creating a roadmap to execute the strategy for an IS program?",
["Develop a project plan to implement the strategy.",
"Obtain consensus on the strategy from the executive board.",
"Define organizational risk tolerance.",
"Review alignment with business goals."],"A",
"จำ: after roadmap created → NEXT = DEVELOP PROJECT PLAN to implement"),

(539,"An organization updated its backup capability to a new cloud-based solution. Which test will MOST effectively verify this change is working as intended?",
["Simulation testing",
"Tabletop testing",
"Parallel testing",
"Black box testing"],"C",
"จำ: verify new backup solution → PARALLEL TESTING (run old + new simultaneously)"),

(540,"Which of the following is the MOST important function of an IS steering committee?",
["Assigning data classifications to organizational assets",
"Defining security standards for logical access controls",
"Developing organizational risk assessment processes",
"Obtaining multiple perspectives from the business"],"D",
"จำ: steering committee MOST important → MULTIPLE PERSPECTIVES from business"),

(541,"Which is the BEST way to obtain reliable information to help an IR team maintain awareness of emerging threats and vulnerabilities?",
["Subscribe to a reputed threat intelligence group.",
"Assign staff to engage with social media hacking groups.",
"Review alerts from a SIEM system.",
"Implement vulnerability scanners."],"A",
"จำ: awareness of emerging threats → SUBSCRIBE to threat intelligence group"),

(542,"Which is the MOST effective approach to ensure seamless integration between BCP and the IR plan?",
["The BCP manager is included in the core IR team.",
"Criteria for escalating to the BCP manager are in the IR plan.",
"Both response teams contain the same members.",
"Consistent event classifications are used in both plans."],"D",
"จำ: BCP + IR plan integration → CONSISTENT EVENT CLASSIFICATIONS in both"),

(543,"Which is an IS manager's BEST course of action when a potential business breach is discovered in a critical business system?",
["Update the incident response plan.",
"Inform affected stakeholders.",
"Inform IT management.",
"Implement mitigating actions immediately."],"B",
"จำ: potential breach in critical system → INFORM AFFECTED STAKEHOLDERS"),

(544,"Which of the following is MOST important to include in a report of an organization's information security risk?",
["Control risk",
"Mitigated risk",
"Residual risk",
"Inherent risk"],"C",
"จำ: IS risk report MOST important → RESIDUAL RISK (หลัง controls แล้ว)"),

(545,"Which is an IS manager's BEST recommendation to senior management following a breach at the organization's SaaS vendor?",
["Engage legal counsel",
"Terminate the relationship with the vendor",
"Renegotiate the vendor contract",
"Update the vendor risk assessment"],"A",
"จำ: SaaS vendor breach → BEST recommendation = ENGAGE LEGAL COUNSEL"),

(546,"Which of the following is MOST important to consider when determining asset valuation?",
["Potential business loss",
"Asset classification level",
"Asset recovery cost",
"Cost of insurance premiums"],"A",
"จำ: asset valuation → POTENTIAL BUSINESS LOSS"),

(547,"What should an IS manager do FIRST to address the risk associated with a new third-party cloud app that will not meet organizational security requirements?",
["Restrict application network access temporarily.",
"Update the risk register.",
"Consult with the business owner.",
"Include security requirements in the contract."],"C",
"จำ: new cloud app won't meet security reqs → FIRST = CONSULT BUSINESS OWNER"),

(548,"BCP was activated and employees followed the plan, but two major suppliers missed deadlines because they were not aware of the disruption. What is the BEST way to prevent a similar situation?",
["Ensure service level agreements (SLAs) with suppliers are enforced.",
"Conduct a vulnerability assessment.",
"Perform testing of the BCP communication plan.",
"Provide suppliers with access to the BCP document."],"C",
"จำ: suppliers not notified in BCP → TEST BCP COMMUNICATION PLAN (include suppliers)"),

(549,"When performing a data classification project, an IS manager should:",
["assign information criticality and sensitivity.",
"identify information custodians.",
"identify information owners.",
"assign information access privileges."],"C",
"จำ: data classification project → IS manager = IDENTIFY INFORMATION OWNERS"),

(550,"Which of the following provides the MOST comprehensive information related to an organization's current risk profile?",
["Gap analysis results",
"Risk register",
"Heat map",
"Risk assessment results"],"B",
"จำ: MOST comprehensive risk profile → RISK REGISTER"),
]

# ── Q551-600 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(551,"Which of the following has the GREATEST impact on the viability of an information security roadmap?",
["Regulatory requirements","Management support","Threat landscape","Resource availability"],"B",
"จำ: IS roadmap viability → MANAGEMENT SUPPORT"),

(552,"An IS manager is recommending investment in a new security initiative to address recently published threats. Which is MOST important to include in the business case?",
["Alignment with the approved IT strategy","Potential impact of threat realization","Availability of resources to implement the initiative","Peer group threat intelligence report"],"B",
"จำ: business case for new security initiative → POTENTIAL IMPACT of threat realization"),

(553,"Which of the following is the MOST important output from a post-incident review?",
["Documentation of lessons learned","Repository of digital forensic artifacts","Revised business impact analysis (BIA)","Compilation of incident-related costs"],"A",
"จำ: post-incident review MOST important output → LESSONS LEARNED"),

(554,"Which of the following is the GREATEST benefit of using a network-based intrusion prevention system (IPS)?",
["The ability to review and monitor data streams by network segment","The ability to shut down or block suspicious connections","Increased visibility into user web surfing","Centralized controls for incident handling"],"B",
"จำ: IPS GREATEST benefit → SHUT DOWN or BLOCK suspicious connections"),

(555,"What should be the GREATEST concern for an IS manager of a large multinational organization when outsourcing data processing to a cloud service provider?",
["Local laws and regulations","Backup and restoration of data","Vendor service level agreements (SLAs)","Independent review of the vendor"],"A",
"จำ: cloud outsourcing multinational GREATEST concern → LOCAL LAWS AND REGULATIONS"),

(556,"Which should be an IS manager's MAIN concern if the same digital signing certificate is able to be used by two or more users?",
["Potential to decrypt digital hash values","Inability to validate identity of sender","Certificate alteration","Segregation of duties"],"B",
"จำ: shared digital signing cert → cannot VALIDATE IDENTITY of sender (non-repudiation lost)"),

(557,"Signature based anti-malware controls are MOST effective against:",
["poorly configured firewall rules.","reused virus code.","known threats.","zero-day exploits."],"C",
"จำ: signature-based anti-malware = KNOWN THREATS only (ไม่ใช่ zero-day)"),

(558,"Which of the following is the PRIMARY objective of a business impact analysis (BIA)?",
["Confirm control effectiveness.","Determine recovery priorities.","Define the recovery point objective (RPO).","Analyze vulnerabilities."],"B",
"จำ: BIA PRIMARY objective → DETERMINE RECOVERY PRIORITIES"),

(559,"A common drawback of email software packages that provide native encryption of messages is that the encryption:",
["has an insufficient key length.","cannot interoperate across product domains.","cannot encrypt attachments.","has no key-recovery mechanism."],"B",
"จำ: native email encryption drawback → CANNOT INTEROPERATE across product domains"),

(560,"Which of the following is the MOST important outcome of effective risk treatment?",
["Implementation of corrective actions","Elimination of risk","Timely reporting of incidents","Reduced cost of acquiring controls"],"B",
"จำ: effective risk treatment MOST important outcome → ELIMINATION OF RISK"),

(561,"Which of the following is MOST important to the successful management of an information security program?",
["Compliance with regulatory requirements","Adequate security budget","Support from key stakeholders","Continuous controls monitoring"],"C",
"จำ: IS program success MOST important → SUPPORT FROM KEY STAKEHOLDERS"),

(562,"A newly hired IS manager discovers that the cleanup of accounts for terminated employees happens only once a year. What should be the FIRST course of action?",
["Design and document a new process.","Perform a risk assessment.","Report the issue to senior management.","Update the security policy."],"B",
"จำ: accounts cleaned only annually → FIRST = RISK ASSESSMENT"),

(563,"Which of the following BEST conveys minimum information security requirements to an organization in alignment with policies?",
["Procedures","Regulations","Baselines","Standards"],"D",
"จำ: minimum IS requirements aligned with policies → STANDARDS"),

(564,"Which of the following security initiatives should be the FIRST step in helping an organization maintain compliance with privacy regulations?",
["Implementing a data classification framework","Implementing SIEM","Installing a DLP solution","Developing security awareness training"],"A",
"จำ: comply with privacy regulations FIRST → DATA CLASSIFICATION FRAMEWORK"),

(565,"Which of the following is MOST important to consider when developing a business case to support investment in an IS program?",
["Senior management support","Results of a risk assessment","Results of a cost-benefit analysis","Impact on the risk profile"],"C",
"จำ: business case for IS program → COST-BENEFIT ANALYSIS results"),

(566,"The PRIMARY reason for using metrics as part of an information security program is to help management:",
["determine whether objectives are being met.","visualize security trends.","develop an information security baseline.","track financial impact of the program."],"A",
"จำ: metrics PRIMARY reason → determine whether OBJECTIVES ARE BEING MET"),

(567,"After an IS incident has been detected and its priority established, which should be the NEXT course of action?",
["Gathering evidence","Eradicating the incident","Performing a risk assessment","Containing the incident"],"D",
"จำ: after detection + priority → NEXT = CONTAIN the incident"),

(568,"Which of the following is the MOST important input to the development of an effective IS strategy?",
["Well-defined security policies and procedures","Current and desired state of security","Business processes and requirements","Risk and business impact assessments"],"B",
"จำ: IS strategy MOST important input → CURRENT AND DESIRED STATE of security (gap)"),

(569,"Which of the following is MOST important to review following a security incident?",
["Incident response procedures","Response tools and techniques","Incident response plan","Lessons learned"],"D",
"จำ: review following security incident → LESSONS LEARNED"),

(570,"Which of the following is necessary to ensure consistent protection for an organization's information assets?",
["Control assessment","Data ownership","Regulatory requirements","Classification mode"],"A",
"จำ: consistent protection for information assets → CONTROL ASSESSMENT"),

(571,"A new law requires an organization to implement specific security controls. What should the IS manager do FIRST?",
["Integrate the new requirements into the security policy.","Perform a gap analysis on the new requirements.","Develop a control implementation plan.","Assess the risk of noncompliance with the new requirements."],"B",
"จำ: new law requires controls → FIRST = GAP ANALYSIS"),

(572,"Which of the following BEST demonstrates that security controls are effective?",
["Audit report","Tabletop simulation","Risk and control self-assessment","Business impact analysis (BIA) results"],"A",
"จำ: demonstrate controls effective → AUDIT REPORT"),

(573,"Which of the following activities provides the GREATEST insight into the level of threat exposure within an IT environment?",
["Executing an organization-wide security audit","Performing penetration testing","Performing technical vulnerability assessments","Conducting a red team exercise"],"D",
"จำ: GREATEST insight into threat exposure → RED TEAM EXERCISE"),

(574,"Which of the following is MOST important to ensure when an organization is moving portions of its sensitive database to the cloud?",
["The conversion has been approved by the IS team.","A right to audit clause is included in the contract.","Input from data owners is included in the requirements definition.","Data encryption is used in the cloud hosting solution."],"C",
"จำ: moving sensitive DB to cloud → INPUT FROM DATA OWNERS in requirements"),

(575,"Which of the following is the BEST way to determine the gap between the present and desired state of an IS program?",
["Determine whether critical success factors (CSFs) have been defined.","Review and update current operational procedures.","Perform a risk analysis for critical applications.","Conduct a capability maturity model evaluation."],"D",
"จำ: gap between present and desired state → CAPABILITY MATURITY MODEL evaluation"),

(576,"The PRIMARY goal of information security governance is to:",
["reduce risk to an acceptable level.","align with business processes.","align with business objectives.","establish a security strategy."],"C",
"จำ: IS governance PRIMARY goal → ALIGN WITH BUSINESS OBJECTIVES"),

(577,"An IS manager is reviewing BCP review results. Which finding should be the MOST immediate concern?",
["The cost of a recent recovery test exceeded budget expectations.","The annual BIA has been delayed.","The BCP has not been recently tested.","The RTO was not met during a recent power outage."],"D",
"จำ: BCP MOST immediate concern → RTO NOT MET during actual outage"),

(578,"If an organization does not have an IS governance framework in place, which would BEST facilitate adoption of a future governance program?",
["Audit recommendations","IT department support","IS funding","Involvement of business stakeholders"],"D",
"จำ: facilitate IS governance adoption → INVOLVEMENT OF BUSINESS STAKEHOLDERS"),

(579,"Which would provide the GREATEST assurance that IS incidents will be detected and contained in a timely manner without jeopardizing the organization's mission?",
["Network security penetration testing program","Continuous vulnerability scanning solution","Security information and event management (SIEM) system","Fully operational security operations center (SOC)"],"D",
"จำ: GREATEST assurance for timely detection + containment → FULLY OPERATIONAL SOC"),

(580,"Which would BEST provide stakeholders with information to determine the appropriate response to a disaster?",
["Vulnerability assessment","SWOT analysis","Business impact analysis (BIA)","Risk assessment"],"C",
"จำ: determine appropriate disaster response → BIA"),

(581,"Which of the following provides the BEST guidance when establishing a security program?",
["Risk assessment methodology","Security audit report","IS budget","Information security framework"],"D",
"จำ: BEST guidance for establishing security program → IS FRAMEWORK"),

(582,"Which should be of MOST concern to an IS manager reviewing the organization's DRP?",
["Organization-wide training for DR has not occurred.","The response team has contracted with an external consultant.","Six months have elapsed since the most recent test.","The response plan document has not been updated with the latest notification list details."],"D",
"จำ: DRP MOST concern → notification list NOT UPDATED (ติดต่อไม่ได้ตอน disaster)"),

(583,"Which of the following is the GREATEST risk of centralized IS administration within a multinational organization?",
["Slower turnaround","Less uniformity","Less objectivity","Violation of local law"],"D",
"จำ: centralized IS in multinational GREATEST risk → VIOLATION OF LOCAL LAW"),

(584,"Which would BEST enable an organization to aggregate information from different systems for centralized categorization of incidents?",
["Intrusion detection system (IDS)","Application program interfaces (APIs)","Intrusion prevention system (IPS)","Security information and event management (SIEM)"],"D",
"จำ: aggregate + centralized incident categorization → SIEM"),

(585,"When preparing an IS policy for a global organization, how should an IS manager BEST address local legislation in multiple countries?",
["Rely on local interpretation of the global policy.",
"Create a policy exception process for each country.",
"Enforce the same global policy in every country.",
"Establish local policies for each country that supplement the global policy."],"D",
"จำ: global IS policy + local legislation → local policies SUPPLEMENT global policy"),

(586,"Which is the MOST important control to implement when senior managers use smartphones to access sensitive company information?",
["Centralized device administration","Remote wipe capability","Anti-malware on the devices","Strong passwords"],"A",
"จำ: senior mgr smartphones + sensitive info → CENTRALIZED DEVICE ADMINISTRATION"),

(587,"Which is the MOST appropriate resource to determine whether a particular solution should utilize encryption based on its location and data classification?",
["Guidelines","Procedures","Standards","Policies"],"C",
"จำ: determine encryption requirement by location/classification → STANDARDS"),

(588,"An organization globally is planning to use a third-party to process payroll. Which issue poses the GREATEST risk?",
["The third party has not provided evidence of compliance with local regulations where data is generated.",
"The third party does not have an independent assessment of controls available.",
"The third party's SLA does not include guarantees of uptime.",
"The third-party contract does not include an indemnity clause."],"A",
"จำ: global payroll 3rd party GREATEST risk → no evidence of LOCAL REGULATION compliance"),

(589,"The PRIMARY objective of timely declaration of a disaster is to:",
["ensure the continuity of the organization's essential services.","protect critical physical assets from further loss.","ensure engagement of business management in the recovery process.","assess and correct disaster recovery process deficiencies."],"A",
"จำ: timely disaster declaration PRIMARY → ENSURE CONTINUITY of essential services"),

(590,"Which of the following BEST enables the design of an effective incident escalation process?",
["A well-defined organizational hierarchy","Enforceable control baselines","A comprehensive risk register","Controls designed for defense in depth"],"A",
"จำ: effective escalation process → WELL-DEFINED ORGANIZATIONAL HIERARCHY"),

(591,"An IS manager is notified that two senior executives can elevate their own privileges in the corporate accounting system, in violation of policy. What is the FIRST step?",
["Notify the CISO of the security policy violation.",
"Perform a system access review.",
"Perform a full review of all system transactions over the past 90 days.",
"Immediately suspend the executives' access privileges."],"D",
"จำ: execs can elevate own privileges → FIRST = IMMEDIATELY SUSPEND access"),

(592,"Which of the following is MOST useful to display on a dashboard to demonstrate security performance?",
["Number of hours spent per vulnerability remediated","Number of vulnerabilities detected over time","Severity of currently unremediated vulnerabilities","Average time to identify vulnerabilities"],"C",
"จำ: dashboard security performance → SEVERITY OF CURRENTLY UNREMEDIATED vulnerabilities"),

(593,"Which should be done FIRST when establishing an IS governance framework?",
["Gain an understanding of the business and cultural attributes.","Contract a third party to conduct an independent review.","Conduct a cost-benefit analysis of the framework.","Evaluate IS tools and skills relevant for the environment."],"A",
"จำ: establish IS governance framework FIRST → understand BUSINESS AND CULTURAL attributes"),

(594,"Which is the BEST approach to make strategic IS decisions?",
["Establish periodic senior management meetings.","Establish regular IS status reporting.","Establish an IS steering committee.","Establish business unit security working groups."],"C",
"จำ: strategic IS decisions BEST approach → IS STEERING COMMITTEE"),

(595,"Which type of incident response test is the MOST efficient way to verify that backup power generators are functioning?",
["Operational full test","Simulation failure test","Parallel recovery test","Full interruption test"],"C",
"จำ: verify backup power generators → PARALLEL RECOVERY TEST"),

(596,"Which is the MOST important action to prepare for a ransomware attack?",
["Back up data regularly and verify the integrity of backups.","Scan emails to detect threats and filter out executable files.","Configure access controls with least privilege in mind.","Execute operating systems and programs in a virtualized environment."],"A",
"จำ: prepare for ransomware → BACK UP + VERIFY INTEGRITY of backups"),

(597,"Which should be the MAIN outcome from monitoring key performance indicators (KPIs) for a corporate security management program?",
["A balanced scorecard","An effective security awareness program","Data for the organization to assess progress","Optimal level of value delivery"],"C",
"จำ: monitoring KPIs MAIN outcome → data to ASSESS PROGRESS"),

(598,"An organization is considering using a third party to host sensitive archived data. Which is MOST important to verify before entering the relationship?",
["Independent audits of the vendor's operations are regularly conducted.","The vendor's controls are in line with the organization's security standards.","The encryption keys are not provided to the vendor.","The vendor's data centers are in the same geographic region."],"B",
"จำ: 3rd party host sensitive data → vendor controls ALIGNED WITH ORG STANDARDS"),

(599,"When creating an IR plan, which is MOST important to include during the preparation phase?",
["Communication plan","Response procedures","Risk management plan","Forensic analysis procedures"],"A",
"จำ: IR plan preparation phase → COMMUNICATION PLAN"),

(600,"A software vendor announced a zero-day vulnerability exposing critical systems. The vendor released an emergency patch. What should be the IS manager's PRIMARY concern?",
["Ability to test the patch prior to deployment","Adequacy of the incident response plan","Availability of resources to implement controls","Documentation of patching procedures"],"A",
"จำ: zero-day emergency patch → PRIMARY concern = ABILITY TO TEST before deployment"),
]

# ── Q601-650 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(601,"What is the MOST important reason to regularly report information security risk to relevant stakeholders?",
["To enable risk-informed decision making","To reduce the impact of IS risk","To ensure IS controls are effective","To achieve compliance with regulatory requirements"],"A",
"จำ: report IS risk to stakeholders MOST important → ENABLE RISK-INFORMED DECISION MAKING"),

(602,"Which is MOST important to ensure ongoing senior management commitment to an organization's IS strategy?",
["Effective and reliable security reporting","A well-defined IS control framework","A detailed and documented BIA","Strategic alignment to an industry framework"],"A",
"จำ: ongoing senior mgmt commitment → EFFECTIVE AND RELIABLE security reporting"),

(603,"A pen test of a new system found critical vulnerabilities. The system owner asks the IS manager to approve an exception to allow go-live without fixing. What is the MOST appropriate course of action?",
["Implement a log monitoring process.","Perform a risk assessment.","Develop a set of compensating controls.","Approve and document the exception."],"B",
"จำ: critical vulns + exception request → FIRST = RISK ASSESSMENT"),

(604,"Which IS activity is MOST helpful to support compliance with IS policy?",
["Conducting IS awareness programs","Creating monthly trend metrics","Performing periodic IT reviews on new system acquisitions","Obtaining management commitment"],"A",
"จำ: support compliance with IS policy → IS AWARENESS PROGRAMS"),

(605,"Which is MOST important to determine following the discovery and eradication of a malware attack?",
["The creator of the malware","The malware entry path","The type of malware involved","The method of detecting the malware"],"B",
"จำ: after malware eradicated → determine MALWARE ENTRY PATH (prevent recurrence)"),

(606,"Which is MOST helpful in ensuring an IS governance framework continues to support business objectives?",
["A consistent risk assessment methodology","A monitoring strategy","An effective organizational structure","Stakeholder buy-in"],"D",
"จำ: IS governance continues to support business → STAKEHOLDER BUY-IN"),

(607,"Reviewing which would be MOST helpful when a new IS manager is developing an IS strategy for a non-regulated organization?",
["Management's business goals and objectives","Strategies of other non-regulated companies","Industry best practices and control recommendations","Risk assessment results"],"A",
"จำ: new IS manager develops strategy → review MANAGEMENT'S BUSINESS GOALS"),

(608,"In order to understand an organization's security posture, it is MOST important for senior leadership to:",
["review the number of reported security incidents.","evaluate results of the most recent IR test.","ensure established security metrics are reported.","assess progress of risk mitigation efforts."],"C",
"จำ: understand security posture → ensure SECURITY METRICS ARE REPORTED"),

(609,"IS controls should be designed PRIMARILY based on:",
["regulatory requirements.","a vulnerability assessment.","business risk scenarios.","a business impact analysis (BIA)."],"D",
"จำ: IS controls designed PRIMARILY based on → BIA"),

(610,"An e-commerce org in its home country opened a new office in another country with stringent security laws. The overall security strategy should be based on:",
["risk assessment results.","international security standards.","the most stringent requirements.","the security organization structure."],"C",
"จำ: multiple countries' laws → MOST STRINGENT requirements"),

(611,"An IS manager developing an IR plan MUST ensure it includes:",
["critical infrastructure diagrams.","a BIA.","criteria for escalation.","an inventory of critical data."],"C",
"จำ: IR plan MUST include → CRITERIA FOR ESCALATION"),

(612,"Which is the MOST effective way to help staff understand their responsibilities for IS?",
["Require staff to sign confidentiality agreements.","Require staff to participate in IS awareness training.","Communicate disciplinary processes for policy violations.","Include IS responsibilities in job descriptions."],"B",
"จำ: staff understand IS responsibilities → IS AWARENESS TRAINING"),

(613,"Security program development is PRIMARILY driven by which of the following?",
["Regulatory requirements","Business strategy","Risk appetite","Available resources"],"B",
"จำ: security program development PRIMARILY driven by → BUSINESS STRATEGY"),

(614,"An organization identified a risk scenario with low impact but very costly to mitigate. Which risk treatment is MOST appropriate?",
["Transfer","Acceptance","Mitigation","Avoidance"],"B",
"จำ: low impact + costly to mitigate → ACCEPT the risk"),

(615,"Prior to conducting a forensic examination, an IS manager should:",
["boot the original hard disk on a clean system.","create an image of the original data on new media.","duplicate data from the backup media.","shut down and relocate the server."],"B",
"จำ: before forensic examination → CREATE IMAGE of original data on new media"),

(616,"The fundamental purpose of establishing security metrics is to:",
["adopt security best practices.","establish security benchmarks.","provide feedback on control effectiveness.","increase return on investment (ROI)."],"C",
"จำ: security metrics fundamental purpose → FEEDBACK ON CONTROL EFFECTIVENESS"),

(617,"Which presents the GREATEST challenge to a SOC's timely identification of potential security breaches?",
["An organization has a decentralized data center using cloud services.","Operating systems are no longer supported by the vendor.","IT system clocks are not synchronized with the centralized logging server.","The patch management system does not deploy patches in a timely manner."],"C",
"จำ: SOC timely identification GREATEST challenge → CLOCKS NOT SYNCHRONIZED with logging server"),

(618,"An organization plans to utilize SaaS and is selecting a vendor. What should the IS manager do FIRST?",
["Review independent security assessment reports for each vendor.","Benchmark each vendor's services with industry best practices.","Define IS requirements and processes.","Analyze the risks and propose mitigating controls."],"C",
"จำ: SaaS vendor selection → FIRST = DEFINE IS REQUIREMENTS AND PROCESSES"),

(619,"An online bank identifies a successful network attack in progress. The bank should FIRST:",
["report the root cause to the board of directors.","isolate the affected network segment.","shut down the entire network.","assess whether PII is compromised."],"B",
"จำ: network attack in progress → FIRST = ISOLATE affected network segment"),

(620,"Which provides an IS manager with the MOST accurate indication of the organization's ability to respond to a cyber attack?",
["Walk-through of the IR plan","Black box penetration test","Simulated phishing exercise","Red team exercise"],"D",
"จำ: ability to respond to cyber attack MOST accurate → RED TEAM EXERCISE"),

(621,"Which would be MOST helpful to identify worst-case disruption scenarios?",
["Cost-benefit analysis","SWOT analysis","Business process analysis","Business impact analysis (BIA)"],"D",
"จำ: identify worst-case disruption scenarios → BIA"),

(622,"Which BEST enables an organization to appropriately prioritize IS-focused projects?",
["Return on investment (ROI)","Privacy compliance requirements","Organizational risk appetite","Historical security incidents"],"C",
"จำ: prioritize IS projects → ORGANIZATIONAL RISK APPETITE"),

(623,"What should an IS manager do FIRST upon learning that some security hardening settings may negatively impact future business activity?",
["Document a security exception.","Reduce security hardening settings.","Perform a risk assessment.","Inform business management of the risk."],"C",
"จำ: hardening may impact business → FIRST = RISK ASSESSMENT"),

(624,"Which IS activity MUST be performed by an IS manager for change requests?",
["Assess impact on IS risk.","Perform penetration testing on affected systems.","Scan IT systems for OS vulnerabilities.","Review change in business requirements for IS."],"A",
"จำ: IS manager MUST do for change requests → ASSESS IMPACT ON IS RISK"),

(625,"The PRIMARY purpose for continuous monitoring of security controls is to ensure:",
["alignment with compliance requirements.","effectiveness of controls.","control gaps are minimized.","system availability."],"B",
"จำ: continuous monitoring PRIMARY purpose → EFFECTIVENESS OF CONTROLS"),

(626,"Which is the MOST important factor of a successful IS program?",
["The program follows industry best practices.","The program is based on a well-developed strategy.","The program is focused on risk management.","The program is cost-efficient and within budget."],"B",
"จำ: IS program success MOST important factor → BASED ON WELL-DEVELOPED STRATEGY"),

(627,"Which message would be MOST effective in obtaining senior management's commitment to IS management?",
["Security is a business product and not a process.","Effective security eliminates risk to the business.","Adopt a recognized framework with metrics.","Security supports and protects the business."],"D",
"จำ: get senior mgmt commitment → SECURITY SUPPORTS AND PROTECTS THE BUSINESS"),

(628,"When choosing best controls to mitigate risk to acceptable levels, the IS manager's decision should be MAINLY driven by:",
["regulatory requirements.","control framework.","best practices.","cost-benefit analysis."],"D",
"จำ: choose controls to mitigate risk → COST-BENEFIT ANALYSIS"),

(629,"A high-risk issue is found in a legacy app risk assessment. Business is unwilling to allocate resources to remediate. What is the IS manager's BEST course of action?",
["Document risk acceptance from the business.","Recommend discontinuing the use of the legacy application.","Design alternative compensating controls to reduce the risk.","Present the worst-case scenario related to the risk."],"C",
"จำ: high risk + no resources → DESIGN COMPENSATING CONTROLS"),

(630,"The PRIMARY benefit of introducing a single point of administration in network monitoring is that it:",
["reduces unauthorized access to systems.","promotes efficiency in control of the environment.","prevents inconsistencies in information in the distributed environment.","allows administrative staff to make management decisions."],"B",
"จำ: single point of administration → PROMOTES EFFICIENCY in control"),

(631,"Which is the MOST important reason to document IS incidents reported across the organization?",
["Support business investments in security.","Evaluate the security posture of the organization.","Identify unmitigated risk.","Prevent incident recurrence."],"D",
"จำ: document IS incidents MOST important → PREVENT INCIDENT RECURRENCE"),

(632,"Which is MOST important for building a robust IS culture within an organization?",
["Mature IS awareness training across the organization","Security controls embedded within development and operation of IT","Senior management approval of IS policies","Strict enforcement of employee compliance with security policies"],"A",
"จำ: build IS culture → MATURE IS AWARENESS TRAINING"),

(633,"Which is the BEST way for an organization to ensure IR teams are properly prepared?",
["Documenting multiple scenarios and response steps","Providing training from third-party forensics firms","Obtaining industry certifications for the response team","Conducting tabletop exercises appropriate for the organization"],"D",
"จำ: IR teams properly prepared → TABLETOP EXERCISES"),

(634,"Which metric BEST measures the effectiveness of an organization's IS program?",
["Return on IS investment","Number of IS business cases developed","Reduction in IS incidents","Increase in risk assessments completed"],"C",
"จำ: IS program effectiveness metric → REDUCTION IN IS INCIDENTS"),

(635,"Which is MOST important when conducting a forensic investigation?",
["Capturing full system images","Documenting analysis steps","Maintaining a chain of custody","Analyzing system memory"],"C",
"จำ: forensic investigation MOST important → CHAIN OF CUSTODY"),

(636,"Which presents the GREATEST challenge to recovery of critical systems after a ransomware incident?",
["Unavailable or corrupt data backups","Ineffective alert configurations for backup operations","Lack of encryption for backup data in transit","Undefined or undocumented backup retention policies"],"A",
"จำ: ransomware recovery GREATEST challenge → UNAVAILABLE OR CORRUPT BACKUPS"),

(637,"An organization is aligning its IR capability with a public cloud service provider. What should the IS manager do FIRST?",
["Identify the skill set of the provider's IR team.","Update the incident escalation process.","Evaluate the provider's audit logging and monitoring controls.","Review the provider's incident definitions and notification criteria."],"D",
"จำ: align IR with cloud provider → FIRST = REVIEW PROVIDER'S INCIDENT DEFINITIONS and notification criteria"),

(638,"An IS manager is reporting on open items from the risk register to senior management. Which is MOST important to communicate?",
["Key risk indicators (KRIs)","Responsible entities","Compensating controls","Potential business impact"],"D",
"จำ: report risk register to senior → MOST important = POTENTIAL BUSINESS IMPACT"),

(639,"Users are sharing a login account to an app with sensitive info, violating access policy. Business says it creates operational efficiencies. What is the IS manager's BEST course of action?",
["Present the risk to senior management.","Modify the policy.","Create an exception for the deviation.","Enforce the policy."],"A",
"จำ: policy violated + business justification → PRESENT RISK TO SENIOR MANAGEMENT"),

(640,"Which should be the FIRST step to gain approval for outsourcing to address a security gap?",
["Perform a cost-benefit analysis.","Collect additional metrics.","Begin due diligence on the outsourcing company.","Submit funding request to senior management."],"A",
"จำ: gain approval for outsourcing → FIRST = COST-BENEFIT ANALYSIS"),

(641,"Which is MOST helpful for determining which IS policies should be implemented?",
["Business impact analysis (BIA)","Risk assessment","Vulnerability assessment","Industry best practices"],"B",
"จำ: determine which IS policies to implement → RISK ASSESSMENT"),

(642,"Which of the following BEST ensures timely and reliable access to services?",
["Authenticity","Availability","Nonrepudiation","Recovery time objective (RTO)"],"B",
"จำ: timely and reliable access to services → AVAILABILITY"),

(643,"An organization is creating a risk mitigation plan considering redundant power supplies to reduce business risk from critical system outages. Which type of control is being considered?",
["Deterrent","Detective","Preventive","Corrective"],"C",
"จำ: redundant power supplies = PREVENTIVE control"),

(644,"Which BEST enables an IS manager to determine the comprehensiveness of an organization's IS strategy?",
["Internal security audit","Organizational risk appetite","External security audit","Business impact analysis (BIA)"],"B",
"จำ: determine IS strategy comprehensiveness → ORGANIZATIONAL RISK APPETITE"),

(645,"An IS manager sees a threat intel report indicating large ransomware attacks targeting the industry. What is the BEST course of action?",
["Assess the risk to the organization.","Review the mitigating security controls.","Notify staff members of the threat.","Increase the frequency of system backups."],"A",
"จำ: threat intel report on ransomware → FIRST = ASSESS RISK TO THE ORGANIZATION"),

(646,"Whose input is of GREATEST importance in the development of an IS strategy?",
["Security architects","End users","Corporate auditors","Process owners"],"D",
"จำ: IS strategy development GREATEST importance → PROCESS OWNERS"),

(647,"Which risk is introduced when using only sanitized data for testing of applications?",
["Unexpected outcomes may arise in production.","Data disclosure may occur during the migration event.","Breaches of compliance obligations will occur.","Data loss may occur during the testing phase."],"A",
"จำ: sanitized data only for testing → UNEXPECTED OUTCOMES in production"),

(648,"Which is the MOST important consideration when defining a recovery strategy in a BCP?",
["Legal and regulatory requirements","Likelihood of a disaster","Organizational tolerance to service interruption","Geographical location of the backup site"],"C",
"จำ: BCP recovery strategy → ORGANIZATIONAL TOLERANCE to service interruption"),

(649,"Which should be done FIRST when developing an IS program?",
["Establish security policies.","Define the security strategy.","Approve security standards.","Set security baselines."],"B",
"จำ: developing IS program FIRST → DEFINE SECURITY STRATEGY"),

(650,"The BEST way to identify risk associated with a social engineering attack is to:",
["monitor the intrusion detection system (IDS).","review SSO authentication logs.","perform a business risk assessment of the email filtering system.","test user knowledge of IS practices."],"D",
"จำ: identify social engineering risk → TEST USER KNOWLEDGE of IS practices"),
]

# ── Q651-700 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(651,"Which is MOST important to have in place to help ensure an organization's cybersecurity program meets the needs of the business?",
["IS awareness training","Risk assessment program","IS governance","IS metrics"],"C",
"จำ: cybersecurity program meets business needs → IS GOVERNANCE"),

(652,"Which is the GREATEST benefit of including incident classification criteria within an IR plan?",
["More visibility to the impact of disruptions","Ability to monitor and control incident management costs","Effective protection of information assets","Optimized allocation of recovery resources"],"D",
"จำ: incident classification in IR plan GREATEST benefit → OPTIMIZED ALLOCATION of recovery resources"),

(653,"A recovery point objective (RPO) is required in which of the following?",
["Business continuity plan (BCP)","IS plan","Incident response plan","Disaster recovery plan (DRP)"],"D",
"จำ: RPO is required in → DISASTER RECOVERY PLAN (DRP)"),

(654,"Which provides the BEST assurance that security policies are applied across business operations?",
["Organizational standards are enforced by technical controls.","Organizational standards are included in awareness training.","Organizational standards are required to be formally accepted.","Organizational standards are documented in operational procedures."],"A",
"จำ: security policies applied across business → standards ENFORCED BY TECHNICAL CONTROLS"),

(655,"What should an IS manager do FIRST when a mandatory security standard hinders achievement of an identified business objective?",
["Recommend risk acceptance.","Perform a cost-benefit analysis.","Escalate to senior management.","Revisit the business objective."],"C",
"จำ: security standard hinders business objective → FIRST = ESCALATE TO SENIOR MANAGEMENT"),

(656,"A business unit is not complying with a control because it impacts business goals. What is the IS manager's BEST recommendation to senior management?",
["Accept the noncompliance.","Conduct a control assessment.","Implement compensating controls.","Educate the noncompliant users."],"C",
"จำ: control impacts business goals → IMPLEMENT COMPENSATING CONTROLS"),

(657,"Which is MOST helpful for protecting an enterprise from advanced persistent threats (APTs)?",
["Updated security policies","Regular antivirus updates","Defined security standards","Threat intelligence"],"D",
"จำ: protect against APTs → THREAT INTELLIGENCE"),

(658,"Which should be the PRIMARY consideration when developing an IR plan?",
["Previously reported incidents","Management support","Compliance with regulations","The definition of an incident"],"D",
"จำ: developing IR plan PRIMARY consideration → DEFINITION OF AN INCIDENT"),

(659,"A strict new regulation is being finalized to address global cybersecurity concerns. What should the IS manager do FIRST?",
["Monitor industry response to the regulation.","Seek legal counsel on the new regulation.","Validate the applicability of the regulation.","Escalate compliance risk to senior management."],"C",
"จำ: new regulation being finalized → FIRST = VALIDATE APPLICABILITY to org"),

(660,"A post-incident review identified that user error resulted in a major breach. Which is MOST important to determine?",
["The underlying reason for the user error","The time and location that the breach occurred","Appropriate disciplinary procedures for user error","Evidence of previous incidents caused by the user"],"A",
"จำ: user error caused breach → determine UNDERLYING REASON (root cause)"),

(661,"The BEST way to ensure frequently encountered incidents are reflected in user security awareness training is to include:",
["responses to security questionnaires.","previous training sessions.","examples of help desk requests.","results of exit interviews."],"C",
"จำ: frequent incidents in awareness training → include HELP DESK REQUESTS examples"),

(662,"Management decided to take no further action regarding a DoS attack risk. The MOST likely reason is:",
["the cost of implementing controls exceeds the potential financial losses.","the risk assessment has not defined the likelihood of occurrence.","executive management is not aware of the impact potential.","the reported vulnerability has not been validated."],"A",
"จำ: no action on DoS risk → COST OF CONTROLS > potential financial losses"),

(663,"Which is the BEST indication of an effective IS awareness training program?",
["An increase in the identification rate during phishing simulations","An increase in the speed of incident resolution","An increase in positive user feedback","An increase in the frequency of phishing tests"],"A",
"จำ: effective awareness training → ↑ IDENTIFICATION RATE in phishing simulations"),

(664,"Penetration testing is MOST appropriate when a:",
["new system is about to go live.","security incident has occurred.","security policy is being developed.","new system is being designed."],"A",
"จำ: pen test MOST appropriate → NEW SYSTEM ABOUT TO GO LIVE"),

(665,"Which will result in the MOST accurate controls assessment?",
["Mature change management processes","Unannounced testing","Well-defined security policies","Senior management support"],"B",
"จำ: MOST accurate controls assessment → UNANNOUNCED TESTING"),

(666,"The MOST important reason for having an IS manager serve on the change management committee is to:",
["ensure changes are properly documented.","advise on change-related risk.","identify changes to the IS policy.","ensure that changes are tested."],"B",
"จำ: IS manager on change mgmt committee → ADVISE ON CHANGE-RELATED RISK"),

(667,"Who is in the BEST position to evaluate business impacts?",
["Senior management","IS manager","Process manager","IT manager"],"C",
"จำ: evaluate business impacts BEST position → PROCESS MANAGER"),

(668,"Which should be done FIRST when establishing a new data protection program to comply with data privacy regulations?",
["Encrypt all personal data stored on systems and networks.","Evaluate privacy technologies required for data protection.","Create an inventory of systems where personal data is stored.","Update disciplinary processes to address privacy violations."],"C",
"จำ: new data protection program FIRST → CREATE INVENTORY of systems with personal data"),

(669,"Which is the BEST approach to IR for an organization migrating to a cloud-based solution?",
["Transfer responsibility for IR to the cloud provider.","Continue using the existing IR procedures.","Revise IR procedures to encompass the cloud environment.","Adopt the cloud provider's IR procedures."],"C",
"จำ: IR for cloud migration → REVISE IR PROCEDURES to encompass cloud"),

(670,"Which is the BEST way to help ensure risk appetite will be considered as part of the risk treatment process?",
["Establish key risk indicators (KRIs).","Provide regular reporting on risk treatment to senior management.","Require steering committee approval of risk treatment plans.","Use quantitative risk assessment methods."],"C",
"จำ: risk appetite in risk treatment → STEERING COMMITTEE APPROVAL of treatment plans"),

(671,"Which is MOST important to include in a post-incident review following a data breach?",
["An evaluation of the effectiveness of the IS strategy","Documentation of regulatory reporting requirements","A review of the forensics chain of custody","Evaluations of the adequacy of existing controls"],"D",
"จำ: post-incident review after data breach → EVALUATE ADEQUACY OF EXISTING CONTROLS"),

(672,"An org plans to use social networks to promote products. What is the IS manager's BEST course of action?",
["Conduct vulnerability assessments on social network platforms.","Assess the security risk associated with the use of social networks.","Establish processes to publish content on social networks.","Develop security controls for the use of social networks."],"B",
"จำ: org uses social networks → ASSESS SECURITY RISK associated with social networks"),

(673,"Which BEST supports IS management in the event of organizational changes in security personnel?",
["Ensuring current documentation of security processes","Formalizing a security strategy and program","Developing an awareness program for staff","Establishing processes within the security operations team"],"A",
"จำ: security personnel changes → CURRENT DOCUMENTATION of security processes"),

(674,"Which is the BEST tool to monitor the effectiveness of IS governance?",
["Balanced scorecard","Risk profile","BIA","Key performance indicators (KPIs)"],"A",
"จำ: monitor IS governance effectiveness → BALANCED SCORECARD"),

(675,"Management decisions concerning IS investments will be MOST effective when they are based on:",
["a process for identifying and analyzing threats and vulnerabilities.","the formalized acceptance of risk analysis by management.","the reporting of consistent and periodic assessments of risks.","an ALE determined from the history of security events."],"C",
"จำ: IS investment decisions MOST effective → CONSISTENT AND PERIODIC RISK ASSESSMENTS"),

(676,"An org is going through digital transformation in an unfamiliar risk landscape. The IS manager leads IT risk management. Which should be given HIGHEST priority?",
["Identification of risk","Selection of risk treatment options","Analysis of control gaps","Design of key risk indicators (KRIs)"],"A",
"จำ: new risk landscape → HIGHEST priority = IDENTIFICATION OF RISK"),

(677,"Which change management procedure is MOST likely to cause concern to the IS manager?",
["Users are not notified of scheduled system changes.","Fallback processes are tested the weekend before changes are made.","The development manager migrates programs into production.","A manual rather than automated process is used to compare program versions."],"C",
"จำ: change mgmt concern → DEVELOPMENT MANAGER migrates to production (segregation of duties)"),

(678,"Which is the BEST method to evaluate the effectiveness of an alternate processing site when continuous uptime is required?",
["Full interruption test","Tabletop test","Parallel test","Simulation test"],"C",
"จำ: evaluate alternate site + continuous uptime → PARALLEL TEST"),

(679,"Which should be the MOST important consideration when establishing IS policies for an organization?",
["Job descriptions include requirements to read security policies.","Senior management supports the policies.","The policies are aligned to industry best practices.","The policies are updated annually."],"B",
"จำ: establishing IS policies MOST important → SENIOR MANAGEMENT SUPPORT"),

(680,"If civil litigation is a goal for an organizational response to a security incident, the PRIMARY step should be to:",
["capture evidence using standard server-backup utilities.","document the chain of custody.","reboot affected machines in a secure area to search for evidence.","contact law enforcement."],"B",
"จำ: civil litigation goal → PRIMARY = DOCUMENT CHAIN OF CUSTODY"),

(681,"An org's marketing dept wants to use an online collaboration service not compliant with IS policy. Risk acceptance is pursued. Approval should be provided by:",
["business senior management.","the compliance officer.","the IS manager.","the chief risk officer (CRO)."],"A",
"จำ: risk acceptance approval → BUSINESS SENIOR MANAGEMENT"),

(682,"Business management accepted an IS risk in a rapidly changing environment. It is MOST important for the IS manager to ensure:",
["change activities are documented.","compliance with the risk acceptance framework.","the rationale for acceptance is periodically reviewed.","the acceptance is aligned with business strategy."],"C",
"จำ: risk accepted in changing environment → rationale PERIODICALLY REVIEWED"),

(683,"Which is the BEST course of action for an IS manager to align security and business goals?",
["Reviewing the business strategy","Conducting a BIA","Actively engaging with stakeholders","Defining key performance indicators (KPIs)"],"C",
"จำ: align security and business goals → ACTIVELY ENGAGING WITH STAKEHOLDERS"),

(684,"What should be the IS manager's FIRST step when updating an IS program?",
["Review costs and benchmark them against industry norms.","Interview business unit managers and key stakeholders.","Identify program components that do not align with business objectives.","Re-evaluate the organization's business expectations and objectives."],"D",
"จำ: updating IS program FIRST → RE-EVALUATE BUSINESS EXPECTATIONS AND OBJECTIVES"),

(685,"Which of the following defines the triggers within a business continuity plan (BCP)?",
["Disaster recovery plan (DRP)","Needs of the organization","IS policy","Gap analysis"],"B",
"จำ: BCP triggers defined by → NEEDS OF THE ORGANIZATION"),

(686,"A cloud app used by an org is found to have a serious vulnerability. After assessing the risk, what is the IS manager's BEST course of action?",
["Instruct the vendor to conduct penetration testing.","Suspend the connection to the application in the firewall.","Initiate the organization's IR process.","Report the situation to the business owner of the application."],"D",
"จำ: cloud app serious vuln → REPORT TO BUSINESS OWNER of the application"),

(687,"Which is the BEST indication of a successful IS culture?",
["The budget allocated for IS is sufficient","End users know how to identify and report incidents","Individuals are given roles based on job functions","Penetration testing is done regularly and findings remediated"],"B",
"จำ: successful IS culture → END USERS know how to IDENTIFY AND REPORT incidents"),

(688,"Which plan should be invoked by an organization to remain operational during a disaster?",
["IR plan","Disaster recovery plan (DRP)","Business contingency plan","Business continuity plan (BCP)"],"D",
"จำ: remain OPERATIONAL during disaster → BCP"),

(689,"Which source is MOST useful when planning a business-aligned IS program?",
["Business impact analysis (BIA)","IS policy","Security risk register","Enterprise architecture (EA)"],"A",
"จำ: business-aligned IS program MOST useful source → BIA"),

(690,"Which is the BEST technical defense against unauthorized access through social engineering?",
["Requiring multifactor authentication","Requiring challenge/response information","Enforcing frequent password changes","Enforcing complex password formats"],"A",
"จำ: technical defense against social engineering → MULTIFACTOR AUTHENTICATION"),

(691,"What is the BEST way to reduce the impact of a successful ransomware attack?",
["Include provisions to pay ransoms in the IS budget","Monitor the network and provide alerts on intrusions","Perform frequent backups and store them offline","Purchase or renew cyber insurance policies"],"C",
"จำ: reduce ransomware impact → FREQUENT BACKUPS stored OFFLINE"),

(692,"Which is the BEST approach for governing noncompliance with security requirements?",
["Require users to acknowledge the acceptable use policy","Base mandatory review and exception approvals on residual risk","Require the steering committee to review exception requests","Base mandatory review and exception approvals on inherent risk"],"B",
"จำ: govern noncompliance → exceptions based on RESIDUAL RISK"),

(693,"Which is MOST important to ensuring information stored by an organization is protected appropriately?",
["Defining security asset categorization","Assigning information asset ownership","Developing a records retention schedule","Defining information stewardship roles"],"B",
"จำ: information protected appropriately → ASSIGNING INFORMATION ASSET OWNERSHIP"),

(694,"In which cloud model does the cloud service buyer assume the MOST security responsibility?",
["Infrastructure as a Service (IaaS)","Software as a Service (SaaS)","Disaster Recovery as a Service (DRaaS)","Platform as a Service (PaaS)"],"A",
"จำ: MOST security responsibility for buyer → IaaS (ควบคุม OS/app/data)"),

(695,"Which is the GREATEST benefit of conducting an organization-wide security awareness program?",
["More security incidents are detected","Security behavior is improved","The security strategy is promoted","Fewer security incidents are reported"],"B",
"จำ: security awareness program GREATEST benefit → SECURITY BEHAVIOR IS IMPROVED"),

(696,"Which is the FIRST step to establishing an effective IS program?",
["Assign accountability","Perform a BIA","Create a business case","Conduct a compliance review"],"C",
"จำ: establish IS program FIRST → CREATE A BUSINESS CASE"),

(697,"An IS manager believes information has been classified inappropriately, increasing breach risk. What is the BEST action?",
["Re-classify the data and increase the security level.","Complete a risk assessment and refer the results to the data owners.","Instruct the relevant system owners to reclassify the data.","Refer the issue to internal audit for a recommendation."],"B",
"จำ: inappropriate classification → RISK ASSESSMENT + refer to DATA OWNERS"),

(698,"Which BEST supports the incident management process for attacks on an organization's supply chain?",
["Requiring security awareness training for vendor staff","Including SLAs in vendor contracts","Performing integration testing with vendor systems","Establishing communication paths with vendors"],"D",
"จำ: incident mgmt for supply chain attacks → COMMUNICATION PATHS WITH VENDORS"),

(699,"Which is MOST useful to an IS manager when conducting a post-incident review of an attack?",
["Cost of the attack to the organization","Location of the attacker","Details from IDS logs","Method of operation used by the attacker"],"D",
"จำ: post-incident review attack → METHOD OF OPERATION used by attacker"),

(700,"Which is MOST important for an IS manager to verify when selecting a third-party forensics provider?",
["Existence of a right to audit clause","Technical capabilities of the provider","Results of the provider's BCP tests","Existence of the provider's IR plan"],"B",
"จำ: selecting 3rd party forensics provider → TECHNICAL CAPABILITIES"),
]

# ── Q701-750 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(701,"Which security process will BEST prevent the exploitation of system vulnerabilities?",
["Antivirus software","Log monitoring","Intrusion detection","Patch management"],"D",
"จำ: prevent exploitation of system vulnerabilities → PATCH MANAGEMENT"),

(702,"Which is the BEST method to protect against emerging advanced persistent threat (APT) actors?",
["Providing ongoing training to the IR team","Updating IS awareness materials","Implementing a honeypot environment","Implementing proactive systems monitoring"],"D",
"จำ: protect against emerging APTs → PROACTIVE SYSTEMS MONITORING"),

(703,"Measuring which is the MOST accurate way to determine alignment of an IS strategy with organizational goals?",
["Number of blocked intrusion attempts","Number of business cases reviewed by senior management","Trends in the number of identified threats to the business","Percentage of controls integrated into business processes"],"D",
"จำ: IS strategy aligned with org goals → % CONTROLS INTEGRATED INTO BUSINESS PROCESSES"),

(704,"An org outsourced development of a mission-critical app. Which is the BEST way to test for backdoors?",
["Perform security code reviews on the entire application","Scan the entire application using a vulnerability scanning tool","Monitor Internet traffic for sensitive information leakage","Run the application from a high-privileged account on a test system"],"A",
"จำ: test for backdoors in outsourced app → SECURITY CODE REVIEWS"),

(705,"When remote access to confidential info is granted to a vendor for analytics, which is the MOST important security consideration?",
["The vendor must be able to amend data","The vendor must agree to the organization's IS policy","Data is encrypted in transit and at rest at the vendor site","Data is subject to regular access log review"],"B",
"จำ: vendor remote access to confidential info → AGREE TO ORG'S IS POLICY"),

(706,"When investigating an IS incident, details of the incident should be shared:",
["widely to demonstrate positive intent","only as needed","only with management","only with internal audit"],"B",
"จำ: share incident details → ONLY AS NEEDED"),

(707,"The PRIMARY advantage of involving end users in continuity planning is that they:",
["can see the overall impact to the business","are more objective than IS management","can balance the technical and business risks","have a better understanding of specific business needs"],"D",
"จำ: end users in continuity planning → BETTER UNDERSTANDING of specific business needs"),

(708,"A vendor promotes being certified for international security standards. Before relying on this, the IS manager should confirm that the:",
["certification scope is relevant to the service being offered","certification will remain current through the life of the contract","current international standard was used to assess security processes","certification can be extended to cover the client's business"],"A",
"จำ: vendor certification → confirm CERTIFICATION SCOPE IS RELEVANT to service"),

(709,"Which IaaS offering will BEST enable a cloud provider to assist customers when recovering from a security incident?",
["Capability to take a snapshot of virtual machines","Capability of online virtual machine analysis","Availability of web application firewall logs","Availability of current infrastructure documentation"],"A",
"จำ: IaaS incident recovery → SNAPSHOT of virtual machines"),

(710,"Which role is BEST able to influence the security culture within an organization?",
["Chief information security officer (CISO)","Chief information officer (CIO)","Chief operating officer (COO)","Chief executive officer (CEO)"],"D",
"จำ: influence security culture → CEO (tone at the very top)"),

(711,"Which BEST indicates the effectiveness of a recent IS awareness campaign?",
["Increase in the frequency of security incident escalations","Reduction in the impact of security incidents","Decrease in the number of security incidents","Increase in the number of reported security incidents"],"D",
"จำ: IS awareness campaign effectiveness → ↑ NUMBER OF REPORTED incidents"),

(712,"Which is the BEST evidence of alignment between corporate and IS governance?",
["Security key performance indicators (KPIs)","Senior management sponsorship","Regular security policy reviews","Project resource optimization"],"B",
"จำ: corporate + IS governance alignment → SENIOR MANAGEMENT SPONSORSHIP"),

(713,"When designing a DRP, which MUST be available to prioritize system restoration?",
["Key performance indicators (KPIs)","Systems inventory","Recovery procedures","Business impact analysis (BIA) results"],"D",
"จำ: DRP system restoration priority → BIA RESULTS"),

(714,"Which factor has the GREATEST influence on successful implementation of IS strategy goals?",
["Regulatory requirements","Compliance acceptance","Management support","Budgetary approval"],"C",
"จำ: IS strategy goals success GREATEST influence → MANAGEMENT SUPPORT"),

(715,"Which is the BEST approach for managing user access permissions to ensure alignment with data classification?",
["Delegate management to an independent third party","Review access permissions annually or whenever job responsibilities change","Lock out accounts after a set number of unsuccessful login attempts","Enable MFA on user and admin accounts"],"B",
"จำ: user access permissions + data classification → REVIEW ANNUALLY or when job responsibilities change"),

(716,"Which is the MOST critical factor for IS program success?",
["A comprehensive risk assessment program","The IS manager's knowledge of the business","Ongoing audits and addressing open items","Security staff with appropriate training and resources"],"B",
"จำ: IS program success MOST critical → IS MANAGER'S KNOWLEDGE OF THE BUSINESS"),

(717,"Which event would MOST likely require a revision to the IS program?",
["A change in IT management","A merger with another organization","A significant increase in reported incidents","An increase in industry threat level"],"B",
"จำ: IS program revision MOST likely → MERGER WITH ANOTHER ORGANIZATION"),

(718,"Which is the MOST important consideration when establishing an org's IS governance committee?",
["Members represent functions across the organization","Members have knowledge of IS controls","Members are rotated periodically","Members are business risk owners"],"A",
"จำ: IS governance committee → MEMBERS REPRESENT FUNCTIONS across the organization"),

(719,"An IR team is alerted to a suspected security event. Before classifying it as an incident, it is MOST important for the security manager to:",
["follow the IR plan","follow the BCP","conduct an incident forensic analysis","notify the business process owner"],"A",
"จำ: suspected security event → FIRST = FOLLOW THE IR PLAN"),

(720,"Which is the BEST way to ensure capability to restore clean data after a ransomware attack?",
["Purchase cyber insurance","Encrypt sensitive production data","Maintain multiple offline backups","Perform integrity checks on backups"],"C",
"จำ: restore clean data after ransomware → MULTIPLE OFFLINE BACKUPS"),

(721,"Which risk scenario is MOST likely to emerge from a supply chain attack?",
["Unreliable delivery of hardware and software resources","Unavailability of services provided by a supplier","Loss of customers due to unavailability of products","Compromise of critical assets via third-party resources"],"D",
"จำ: supply chain attack risk → COMPROMISE OF CRITICAL ASSETS via third-party"),

(722,"An IS manager learns through threat intel that the org may be targeted for a major emerging threat. What is the FIRST course of action?",
["Conduct an IS audit","Perform a gap analysis","Validate the relevance of the information","Inform senior management"],"C",
"จำ: threat intel about emerging threat → FIRST = VALIDATE RELEVANCE of information"),

(723,"Which BEST indicates that an org has effectively tested its BCP/DRP within stated RTOs?",
["Internal compliance requirements are being met","Regulatory requirements are being met","Risk management objectives are being met","Business needs are being met"],"D",
"จำ: BCP/DRP tested within RTO → BUSINESS NEEDS ARE BEING MET"),

(724,"The MOST important attribute of a security control is that it is:",
["auditable","measurable","scalable","reliable"],"D",
"จำ: MOST important attribute of security control → RELIABLE"),

(725,"Which will BEST enable an effective information asset classification process?",
["Reviewing the RTO requirements of the asset","Assigning ownership","Including security requirements in the classification process","Analyzing audit findings"],"B",
"จำ: asset classification process → ASSIGNING OWNERSHIP"),

(726,"An IS manager is notified about a compromised endpoint device. What is the BEST course of action to prevent further damage?",
["Run a virus scan on the endpoint device","Wipe and reset the endpoint device","Power off the endpoint device","Isolate the endpoint device"],"D",
"จำ: compromised endpoint → ISOLATE the device"),

(727,"During which phase should an IR team document actions required to remove the threat?",
["Eradication","Identification","Containment","Post-incident review"],"A",
"จำ: document actions to REMOVE THREAT → ERADICATION phase"),

(728,"A user reports a stolen personal mobile device storing sensitive corporate data. Which will BEST minimize risk of data exposure?",
["Wipe the device remotely","Remove user's access to corporate data","Prevent the user from using personal mobile devices","Report the incident to the police"],"A",
"จำ: stolen mobile with corporate data → REMOTE WIPE"),

(729,"An org acquired a company in a foreign country. What is the FIRST step the IS manager should take?",
["Evaluate the IS laws that apply to the acquired company","Apply the existing IS program to the acquired company","Merge the two existing IS programs","Determine which country's IS regulations will be used"],"A",
"จำ: acquisition in foreign country → FIRST = EVALUATE IS LAWS that apply"),

(730,"An org's DRP is documented and kept at a DR site. What is the BEST way to ensure the plan can be carried out in an emergency?",
["Require DR documentation be stored with all key decision makers","Provide annual DR training to appropriate staff","Maintain an outsourced contact center in another country","Store DR documentation in a public cloud"],"B",
"จำ: ensure DRP can be carried out → ANNUAL DR TRAINING to appropriate staff"),

(731,"Which is a desired outcome of IS governance?",
["Penetration test","A maturity model","Improved risk management","Business agility"],"C",
"จำ: IS governance desired outcome → IMPROVED RISK MANAGEMENT"),

(732,"When designing an IS risk monitoring framework, it is MOST important to ensure:",
["preservation of forensic evidence is enabled","the monitoring system is patched regularly","feedback is communicated to stakeholders","outlier events are escalated to system administrators"],"C",
"จำ: IS risk monitoring framework → FEEDBACK COMMUNICATED TO STAKEHOLDERS"),

(733,"Which BEST enables staff acceptance of IS policies?",
["Adequate security funding","A robust IR program","Strong senior management support","Computer-based training"],"C",
"จำ: staff acceptance of IS policies → STRONG SENIOR MANAGEMENT SUPPORT"),

(734,"Which is the BEST way to rigorously test a DRP for a mission-critical system without disrupting business operations?",
["Parallel testing","Simulation testing","Checklist review","Structured walk-through"],"A",
"จำ: rigorously test DRP + no disruption → PARALLEL TESTING"),

(735,"An IS manager is concerned with continued policy violations in a business unit despite recent efforts. What is the BEST course of action?",
["Review the business unit's function against the policy","Revise the policy to accommodate the business unit","Report the business unit for policy noncompliance","Enforce sanctions on the business unit"],"A",
"จำ: continued policy violations → REVIEW BUSINESS UNIT'S FUNCTION against policy"),

(736,"Which BEST facilitates an IS manager's efforts to obtain senior management commitment for an IS program?",
["Presenting evidence of inherent risk","Reporting the security maturity level","Presenting compliance requirements","Communicating the residual risk"],"A",
"จำ: obtain senior mgmt commitment → PRESENTING EVIDENCE OF INHERENT RISK"),

(737,"Which is PRIMARILY determined by asset classification?",
["Priority for asset replacement","Level of protection required for assets","Replacement cost of assets","Insurance coverage required for assets"],"B",
"จำ: asset classification PRIMARILY determines → LEVEL OF PROTECTION required"),

(738,"Which is MOST helpful for aligning security operations with the IT governance framework?",
["Business impact analysis (BIA)","Security operations program","IS policy","Security risk assessment"],"C",
"จำ: align security operations with IT governance → IS POLICY"),

(739,"An IS manager learned of a new data protection regulation soon to go into effect. What is the BEST way to manage noncompliance risk?",
["Perform a gap analysis.","Consult with senior management on the best course of action.","Implement a program of work to comply with the new legislation.","Understand the cost of noncompliance."],"A",
"จำ: new data protection regulation → PERFORM GAP ANALYSIS"),

(740,"An IS manager learns of a new standard related to an emerging technology the org wants to implement. What should be recommended FIRST?",
["Perform a risk assessment on the new technology.","Obtain legal counsel's opinion on the standard's applicability.","Determine whether the organization can benefit from the new standard.","Review industry specialists' analyses of the new standard."],"A",
"จำ: new emerging technology standard → FIRST = RISK ASSESSMENT on new technology"),

(741,"Which will provide the MOST guidance when deciding the level of protection for an information asset?",
["Impact on IS program","Cost of controls","Impact to business function","Cost to replace"],"C",
"จำ: level of protection for asset → IMPACT TO BUSINESS FUNCTION"),

(742,"Which BEST demonstrates return on investment (ROI) for an IS initiative?",
["Risk heat map","Business impact analysis (BIA)","Business case","IS program roadmap"],"C",
"จำ: demonstrate ROI for IS initiative → BUSINESS CASE"),

(743,"Which is BEST suited to provide regular reporting to the board regarding compliance to a global security standard?",
["Legal counsel","Quality assurance (QA)","Information security","Internal audit"],"D",
"จำ: report compliance to global security standard → INTERNAL AUDIT"),

(744,"Which would be MOST effective in gaining senior management approval of security investments in network infrastructure?",
["Performing pen tests against the network to demonstrate vulnerability","Highlighting competitor performance regarding network security","Presenting comparable security implementation estimates from several vendors","Demonstrating that targeted security controls tie to business objectives"],"D",
"จำ: gain senior mgmt approval for security investments → controls TIE TO BUSINESS OBJECTIVES"),

(745,"Which is the MOST important reason to implement IS governance?",
["To align the security strategy with the organization's strategy","To monitor the performance of IS resources","To monitor the achievement of business goals and objectives","To provide adequate resources to achieve business goals"],"A",
"จำ: IS governance MOST important reason → ALIGN SECURITY STRATEGY with org strategy"),

(746,"Which is a PRIMARY objective of an IS governance framework?",
["To provide the basis for action plans to achieve IS objectives organization-wide","To achieve the desired IS state as defined by business unit management","To align relationships of stakeholders in developing and executing an IS strategy","To provide assurance that information assets are protected proportionate to inherent risk"],"A",
"จำ: IS governance framework PRIMARY objective → BASIS FOR ACTION PLANS to achieve IS objectives org-wide"),

(747,"Which is the BEST way to reduce risk associated with a BYOD program?",
["Implement a mobile device policy and standard.","Provide employee training on secure mobile device practices.","Implement a mobile device management (MDM) solution.","Require employees to install an effective anti-malware app."],"A",
"จำ: reduce BYOD risk → MOBILE DEVICE POLICY AND STANDARD"),

(748,"An IS manager contracted with a company to design security architecture for an application. Which is accountable for identification associated with this initiative?",
["The project steering committee","The IS manager","The infrastructure management team","The application development team"],"B",
"จำ: accountability for security architecture initiative → IS MANAGER"),

(749,"Which desired outcome BEST supports a decision to invest in a new security initiative?",
["Enhanced security monitoring and reporting","Reduction of organizational risk","Reduced control complexity","Enhanced threat detection capability"],"B",
"จำ: invest in security initiative → REDUCTION OF ORGANIZATIONAL RISK"),

(750,"Which is an IS manager's MOST important consideration when exploring use of a third-party provider to handle an IT function?",
["The provider carries cyber insurance to cover security breaches.","The provider agrees to provide historical security incident data.","The provider's security processes align with the organization's.","The provider has undergone an independent security review."],"C",
"จำ: 3rd party IT function → PROVIDER'S SECURITY PROCESSES ALIGN with organization's"),
]

# ── Q751-800 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(751,"Which MUST be defined for an IS manager to evaluate the appropriateness of controls currently in place?",
["Security policy","Risk management framework","Security standards","Risk appetite"],"D",
"จำ: evaluate appropriateness of controls → RISK APPETITE must be defined"),

(752,"When an organization decides to accept a risk, it should mean the cost to mitigate:",
["exceeds budget allocation.","is higher than the cost to transfer risk.","is less than the residual risk.","is greater than the residual risk."],"D",
"จำ: accept risk = cost to mitigate is GREATER THAN the residual risk"),

(753,"Which is the MOST important reason to conduct interviews as part of the BIA process?",
["To facilitate a qualitative risk assessment following the BIA","To obtain input from as many relevant stakeholders as possible","To ensure the stakeholders providing input own the related risk","To increase awareness of IS among key stakeholders"],"B",
"จำ: BIA interviews MOST important → obtain input from AS MANY RELEVANT STAKEHOLDERS as possible"),

(754,"Due to changes in an org's environment, security controls may no longer be adequate. What is the IS manager's BEST course of action?",
["Perform a new risk assessment.","Review the previous risk assessment and countermeasures.","Transfer the new risk to a third party.","Evaluate countermeasures to mitigate new risks."],"A",
"จำ: environment changes → controls may be inadequate = PERFORM NEW RISK ASSESSMENT"),

(755,"What is the PRIMARY benefit when IS program requirements are aligned with employment and staffing processes?",
["Access is granted based on task requirements.","Information assets are classified appropriately.","Security staff turnover is reduced.","Security incident reporting procedures are followed."],"A",
"จำ: IS aligned with staffing → ACCESS GRANTED BASED ON TASK REQUIREMENTS"),

(756,"When developing an asset classification program, which step should be completed FIRST?",
["Implement a DLP system.","Categorize each asset.","Create a business case for a digital rights management tool.","Create an inventory."],"D",
"จำ: asset classification program FIRST → CREATE AN INVENTORY"),

(757,"Which is the PRIMARY reason to monitor key risk indicators (KRIs) related to IS?",
["To alert on unacceptable risk","To identify residual risk","To reassess risk appetite","To benchmark control performance"],"A",
"จำ: monitor KRIs PRIMARY reason → ALERT ON UNACCEPTABLE RISK"),

(758,"Which is the BEST indicator of an emerging incident?",
["A weakness identified within an organization's information systems","Attempted patching of systems resulting in errors","Customer complaints about lack of website availability","A recent security incident at an industry competitor"],"C",
"จำ: emerging incident BEST indicator → CUSTOMER COMPLAINTS about website unavailability"),

(759,"An org discovered a recurring problem with unsecure code being released into production. What is the IS manager action?",
["Implement segregation of duties between development and production.","Increase the frequency of penetration testing.","Review existing configuration management processes.","Review existing change management processes."],"A",
"จำ: unsecure code released to production → SEGREGATION OF DUTIES between dev and production"),

(760,"When developing a categorization method for security incidents, the categories MUST:",
["be created by the incident handler.","align with reporting requirements.","have agreed-upon definitions.","align with industry standards."],"C",
"จำ: incident categories MUST → HAVE AGREED-UPON DEFINITIONS"),

(761,"Which is MOST likely to be impacted when emerging technologies are introduced to an organization?",
["Risk profile","Security policies","Control effectiveness","Risk assessment approach"],"A",
"จำ: emerging technologies introduced → RISK PROFILE most impacted"),

(762,"An org's SaaS product has a major security vulnerability at the primary cloud provider. Who is PRIMARILY accountable for the associated risk?",
["The data owner","The IS manager","The security engineer","The application owner"],"D",
"จำ: SaaS vulnerability risk accountability → APPLICATION OWNER"),

(763,"Which is the MOST important criterion when deciding whether to accept residual risk?",
["Cost of replacing the asset","Annual loss expectancy (ALE)","Cost of additional mitigation","Annual rate of occurrence"],"B",
"จำ: decide to accept residual risk → ANNUAL LOSS EXPECTANCY (ALE)"),

(764,"An IS manager finds a soon-to-be deployed app will increase risk beyond acceptable levels without necessary controls. What is the BEST course of action?",
["Recommend a different application.","Instruct IT to deploy controls based on urgent business needs.","Solicit bids for compensating control products.","Present a business case for additional controls to senior management."],"D",
"จำ: app increases risk beyond acceptable + no controls → PRESENT BUSINESS CASE to senior mgmt"),

(765,"When developing a business case to justify an IS investment, which would BEST enable an informed decision by senior management?",
["The IS strategy","Security investment trends in the industry","Losses due to security incidents","The results of a risk assessment"],"D",
"จำ: business case for IS investment → RISK ASSESSMENT results"),

(766,"Which is the BEST approach for developing a physical access control policy for a data-hosting org with geographically dispersed customers?",
["Review customers' security policies.","Design SSO or federated access.","Develop access control requirements for each system and application.","Conduct a risk assessment to determine security risks and mitigating controls."],"D",
"จำ: physical access control policy for data-hosting org → RISK ASSESSMENT"),

(767,"Which is a PRIMARY benefit of managed security solutions?",
["Easier implementation across an organization","Greater ability to focus on core business operations","Wider range of capabilities","Lower cost of operations"],"B",
"จำ: managed security solutions PRIMARY benefit → FOCUS ON CORE BUSINESS OPERATIONS"),

(768,"Which is an example of risk mitigation?",
["Improving security controls","Discontinuing the activity associated with the risk","Performing a cost-benefit analysis","Purchasing insurance"],"A",
"จำ: risk mitigation example → IMPROVING SECURITY CONTROLS"),

(769,"Which BEST enables an org to provide ongoing assurance that legal and regulatory compliance requirements can be met?",
["Engaging external experts to provide guidance on changes","Assigning the operations manager accountability for compliance","Embedding compliance requirements within operational processes","Performing periodic audits for compliance"],"C",
"จำ: ongoing compliance assurance → EMBED COMPLIANCE REQUIREMENTS within operational processes"),

(770,"Following a successful attack, an IS manager should be confident malware has not continued to spread at the completion of which IR phase?",
["Recovery","Eradication","Identification","Containment"],"D",
"จำ: malware not spreading confirmed → CONTAINMENT phase"),

(771,"Which is the BEST method to align an IS strategic plan to the corporate strategy?",
["Ensuring the plan complies with business unit expectations","Involving industry experts in the development of the plan","Involving senior management in the development of the plan","Obtaining adequate funds from senior management"],"C",
"จำ: align IS strategic plan to corporate strategy → INVOLVE SENIOR MANAGEMENT in development"),

(772,"Which would BEST ensure that security is integrated during application development?",
["Performing app security testing during acceptance testing","Introducing security requirements during the initiation phase","Employing global security standards during development","Providing training on secure development to programmers"],"B",
"จำ: security integrated during app development → SECURITY REQUIREMENTS in INITIATION PHASE"),

(773,"Which is MOST important in increasing the effectiveness of incident responders?",
["Integrating staff with the IT department","Testing response scenarios","Communicating with the management team","Reviewing the IR plan annually"],"B",
"จำ: increase IR effectiveness → TESTING RESPONSE SCENARIOS"),

(774,"Which should be the PRIMARY objective of the IS IR process?",
["Classifying incidents","Conducting incident triage","Communicating with internal and external parties","Minimizing negative impact to critical operations"],"D",
"จำ: IR process PRIMARY objective → MINIMIZING NEGATIVE IMPACT to critical operations"),

(775,"An IR team from experienced individuals. Which exercise would be MOST beneficial at the first drill?",
["Tabletop exercise","Red team exercise","Disaster recovery exercise","Black box penetration test"],"A",
"จำ: new IR team first drill → TABLETOP EXERCISE"),

(776,"Employees have been issued smartphones with cameras, violating a policy prohibiting cameras at the office. What should be the IS manager's FIRST course of action?",
["Revise the policy.","Conduct a risk assessment.","Communicate the acceptable use policy.","Perform a root cause analysis."],"C",
"จำ: policy violation (cameras) → FIRST = COMMUNICATE ACCEPTABLE USE POLICY"),

(777,"When performing a BIA, who should calculate the recovery time and cost estimates?",
["Business process owner","Business continuity coordinator","IS manager","Senior management"],"A",
"จำ: BIA recovery time and cost estimates → BUSINESS PROCESS OWNER"),

(778,"A PRIMARY purpose of creating security policies is to:",
["implement management's security governance strategy.","establish the way security tasks should be executed.","communicate management's security expectations.","define allowable security boundaries."],"C",
"จำ: security policies PRIMARY purpose → COMMUNICATE MANAGEMENT'S SECURITY EXPECTATIONS"),

(779,"The MAIN benefit of implementing a DLP solution is to:",
["enhance the organization's antivirus controls.","reduce the need for a security awareness program.","complement the organization's detective controls.","eliminate the risk of data loss."],"C",
"จำ: DLP solution MAIN benefit → COMPLEMENT DETECTIVE CONTROLS"),

(780,"Which is the MOST important detail to capture in an organization's risk register?",
["Risk acceptance criteria","Risk severity level","Risk ownership","Risk appetite"],"C",
"จำ: risk register MOST important detail → RISK OWNERSHIP"),

(781,"Which is the GREATEST benefit of information asset classification?",
["Supporting segregation of duties","Defining resource ownership","Providing a basis for implementing a need-to-know policy","Helping to determine the RPO"],"C",
"จำ: asset classification GREATEST benefit → BASIS FOR NEED-TO-KNOW POLICY"),

(782,"While classifying information assets, an IS manager notices several production databases have no owners. What should the IS manager do?",
["Assign the highest classification level to those databases.","Assign responsibility to the DBA.","Prepare a report of the databases for senior management.","Review the databases for sensitive content."],"C",
"จำ: databases without owners → PREPARE REPORT FOR SENIOR MANAGEMENT"),

(783,"An org's research dept plans to apply ML on a data set containing customer names and purchase history. Risk leakage is high impact. Which is the BEST risk treatment?",
["Accept the risk, as the benefits exceed the potential consequences.","Mitigate the risk by applying anonymization on the data set.","Transfer the risk by purchasing insurance.","Mitigate the risk by encrypting the customer names in the data set."],"B",
"จำ: ML on customer data high impact → ANONYMIZATION of data set"),

(784,"IT projects have security controls being added post-production. Which would MOST help ensure controls are relevant to a project?",
["Involving IS at each stage of project management","Creating a data classification framework","Identifying responsibilities during the project business case analysis","Providing stakeholders with minimum IS requirements"],"A",
"จำ: controls added post-production → INVOLVING IS AT EACH STAGE of project management"),

(785,"Which is the BEST approach to reduce unnecessary duplication of compliance activities?",
["Integration of assurance efforts","Automation of controls","Documentation of control procedures","Standardization of compliance requirements"],"A",
"จำ: reduce compliance duplication → INTEGRATION OF ASSURANCE EFFORTS"),

(786,"Which BEST helps ensure a risk response plan will be developed and executed in a timely manner?",
["Establishing risk metrics","Training on risk management procedures","Reporting on documented deficiencies","Assigning a risk owner"],"D",
"จำ: risk response plan timely → ASSIGNING A RISK OWNER"),

(787,"An IS manager learns IT personnel are not adhering to IS policy because it creates process inefficiencies. What should the IS manager do FIRST?",
["Propose that IT update IS policies and procedures.","Request that internal audit conduct a review.","Conduct user awareness training within the IT function.","Determine the risk related to noncompliance with the policy."],"D",
"จำ: IT not following IS policy (inefficiency claim) → FIRST = DETERMINE RISK of noncompliance"),

(788,"Which is MOST important to include in a report to key stakeholders regarding IS program effectiveness?",
["Security incident details","Security metrics","Security risk exposure","Security baselines"],"B",
"จำ: report IS program effectiveness to stakeholders → SECURITY METRICS"),

(789,"An org is increasingly using SaaS. Which would be the MOST effective way to ensure procurement considers IS concerns?",
["Integrate IS risk assessments into the procurement process.","Invite IT members into regular procurement team meetings.","Enforce the right to audit in procurement contracts.","Provide regular IS training to the procurement team."],"A",
"จำ: SaaS procurement IS concerns → INTEGRATE IS RISK ASSESSMENTS into procurement process"),

(790,"Which should be the KEY consideration when creating an IS communication plan with industry peers?",
["Reducing the costs associated with information sharing","Balancing the benefits of information sharing with drawbacks of sharing sensitive info","Notifying the legal department whenever incident-related information is shared","Ensuring information is detailed enough to be of use to other organizations"],"B",
"จำ: IS communication plan with industry peers → BALANCE BENEFITS vs drawbacks of sharing sensitive info"),

(791,"Which is MOST effective for communicating forward-looking trends within security reporting?",
["Key risk indicators (KRIs)","Key performance indicators (KPIs)","Key control indicators (KCIs)","Key goal indicators (KGIs)"],"A",
"จำ: forward-looking trends in security reporting → KRIs (leading indicators)"),

(792,"An org purchased DLP software but discovered it fails to detect or prevent data loss. What should the IS manager do FIRST?",
["Revise the data classification policy.","Review the contract.","Review the configuration.","Implement stricter data loss controls."],"C",
"จำ: DLP not working → FIRST = REVIEW THE CONFIGURATION"),

(793,"Network isolation techniques are immediately implemented after a security breach to:",
["allow time for key stakeholder decision making.","reduce the extent of further damage.","enforce zero trust architecture principles.","preserve evidence as required for forensics."],"B",
"จำ: network isolation after breach → REDUCE EXTENT OF FURTHER DAMAGE"),

(794,"Which IR phase involves actions to help safeguard critical systems while maintaining business operations?",
["Containment","Identification","Preparation","Recovery"],"A",
"จำ: safeguard critical systems while maintaining operations → CONTAINMENT phase"),

(795,"An org received complaints that some files have been encrypted and users are receiving demands for money. What is the BEST course of action?",
["Isolate the affected systems.","Conduct an impact assessment.","Initiate incident response.","Rebuild the affected systems."],"C",
"จำ: files encrypted + ransom demands = ransomware → INITIATE INCIDENT RESPONSE"),

(796,"Which has the GREATEST positive impact on the ability to execute a DRP?",
["Updating the plan periodically","Conducting a walk-through of the plan","Storing the plan at an offsite location","Communicating the plan to all stakeholders."],"B",
"จำ: execute DRP GREATEST positive impact → CONDUCTING A WALK-THROUGH of the plan"),

(797,"Which is MOST important to include in monthly IS reports to the board?",
["Root cause analysis of security incidents","Threat intelligence","Risk assessment results","Trend analysis of security metrics"],"D",
"จำ: monthly IS reports to board → TREND ANALYSIS OF SECURITY METRICS"),

(798,"Which activity is designed to handle a control failure that leads to a breach?",
["Vulnerability management","Incident management","Root cause analysis","Risk assessment"],"B",
"จำ: handle control failure leading to breach → INCIDENT MANAGEMENT"),

(799,"Which is MOST important to consider when aligning a security awareness program with the org's business strategy?",
["Processes and technology","People and culture","Regulations and standards","Executive and board directives"],"B",
"จำ: aligning security awareness with business strategy → PEOPLE AND CULTURE"),

(800,"Which BEST indicates that information assets are classified accurately?",
["An accurate and complete information asset catalog","Appropriate assignment of information asset owners","Appropriate prioritization of information risk treatment","Increased compliance with IS policy"],"C",
"จำ: information assets classified accurately → APPROPRIATE PRIORITIZATION of information risk treatment"),
]

# ── Q801-850 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(801,"Reevaluation of risk is MOST critical when there is:",
["a management request for updated security reports.","resistance to the implementation of mitigating controls.","a change in the threat landscape.","a change in security policy."],"C",
"จำ: risk reevaluation MOST critical → CHANGE IN THREAT LANDSCAPE"),

(802,"Which BEST supports investments in an IS program?",
["Business impact analysis (BIA)","Risk assessment results","Gap analysis results","Business cases"],"D",
"จำ: support IS program investments → BUSINESS CASES"),

(803,"Which is MOST important to ensure when developing escalation procedures for an IR plan?",
["Minimum regulatory requirements are maintained.","The contact list is regularly updated.","Each process is assigned to a responsible party.","Senior management approval has been documented."],"C",
"จำ: IR escalation procedures → EACH PROCESS ASSIGNED TO A RESPONSIBLE PARTY"),

(804,"Which is the PRIMARY benefit of implementing a vulnerability assessment process?",
["Compliance status is improved.","Threat management is enhanced.","Security metrics are enhanced.","Proactive risk management is facilitated."],"D",
"จำ: vulnerability assessment PRIMARY benefit → PROACTIVE RISK MANAGEMENT"),

(805,"An org is implementing an IS governance framework. To communicate program effectiveness to stakeholders, it is MOST important to establish:",
["a control self-assessment (CSA) process.","metrics for each milestone.","automated reporting to stakeholders.","a monitoring process for the security policy."],"B",
"จำ: communicate IS governance effectiveness → METRICS FOR EACH MILESTONE"),

(806,"Which is the MOST effective way to present quarterly reports to the board on IS program status?",
["Detailed analysis of security program KPIs","An IS risk register","An IS dashboard","A capability and maturity assessment"],"C",
"จำ: quarterly report to board on IS program → IS DASHBOARD"),

(807,"Which is the BEST way to obtain support for a new organization-wide IS program?",
["Deliver an IS awareness campaign.","Publish an IS RACI chart.","Benchmark against similar industry organizations.","Establish an IS strategy committee."],"D",
"จำ: obtain support for new IS program → ESTABLISH IS STRATEGY COMMITTEE"),

(808,"To confirm a 3rd party complies with IS requirements, it is MOST important to ensure:",
["contract clauses comply with IS policy.","security metrics are included in the SLA.","the IS policy of the 3rd party is reviewed.","right to audit is included in the SLA."],"D",
"จำ: 3rd party IS compliance confirmation → RIGHT TO AUDIT in SLA"),

(809,"Which BEST enables an org to transform its culture to support IS?",
["Strong management support","Robust technical security controls","Periodic compliance audits","Incentives for security incident reporting"],"A",
"จำ: transform culture to support IS → STRONG MANAGEMENT SUPPORT"),

(810,"An org is close to going live with a cloud app. Pen test results show a high-rated vulnerability. What is the BEST way to proceed?",
["Postpone the implementation until the vulnerability has been fixed.","Commission further pen tests to validate initial results.","Assess whether the vulnerability is within the organization's risk tolerance levels.","Implement the app and request the cloud provider to fix the vulnerability."],"C",
"จำ: high vuln before go-live → ASSESS WHETHER within risk tolerance levels"),

(811,"Which is the BEST way to achieve compliance with new global regulations related to protection of personal information?",
["Review contracts and SOWs with vendors.","Determine current and desired state of controls.","Execute a risk treatment plan.","Implement data regionalization controls."],"B",
"จำ: comply with new privacy regulations → DETERMINE CURRENT AND DESIRED STATE of controls (gap)"),

(812,"Which should be given HIGHEST priority during an IS post-incident review?",
["Evaluating IR effectiveness","Documenting actions taken in sufficient detail","Evaluating the performance of IR team members","Updating key risk indicators (KRIs)"],"A",
"จำ: post-incident review HIGHEST priority → EVALUATING IR EFFECTIVENESS"),

(813,"Which is the BEST course of action when an online company discovers a network attack in progress?",
["Shut off all network access points.","Isolate the affected network segment.","Dump all event logs to removable media.","Enable trace logging on all events."],"B",
"จำ: network attack in progress → ISOLATE affected network segment"),

(814,"Which is the BEST reason for an org to use Disaster Recovery as a Service (DRaaS)?",
["It transfers the risk associated with recovery to a third party.","It eliminates the need for the business to perform testing.","It eliminates the need to maintain offsite facilities.","It lowers the annual cost to the business."],"C",
"จำ: DRaaS BEST reason → ELIMINATES NEED TO MAINTAIN OFFSITE FACILITIES"),

(815,"When properly implemented, secure transmission protocols protect transactions:",
["from eavesdropping.","in the server's database.","from denial of service (DoS) attacks.","on the client desktop."],"A",
"จำ: secure transmission protocols protect → FROM EAVESDROPPING"),

(816,"An org is acquiring a new company. Which is the BEST approach to protect newly acquired data assets prior to integration?",
["Review data architecture.","Include security requirements in the contract.","Perform a risk assessment.","Assess security controls."],"C",
"จำ: protect newly acquired data before integration → RISK ASSESSMENT"),

(817,"The PRIMARY objective of a post-incident review of an IS incident is to:",
["minimize impact.","determine the impact.","prevent recurrence.","update the risk profile."],"C",
"จำ: post-incident review PRIMARY objective → PREVENT RECURRENCE"),

(818,"The MOST appropriate time to conduct a DR test would be after:",
["the security risk profile has been reviewed.","major business processes have been redesigned.","the BCP has been updated.","noncompliance incidents have been filed."],"C",
"จำ: MOST appropriate time for DR test → AFTER BCP HAS BEEN UPDATED"),

(819,"Which method BEST demonstrates that an IS program provides appropriate coverage?",
["Gap assessment","Vulnerability scan report","Maturity assessment","Security risk analysis"],"D",
"จำ: IS program provides appropriate coverage → SECURITY RISK ANALYSIS"),

(820,"Which is an IS manager's MOST important course of action when responding to a major incident that could disrupt the business?",
["Notify law enforcement.","Contact forensic investigators.","Follow the escalation process.","Identify the indicators of compromise."],"C",
"จำ: major incident that could disrupt business → FOLLOW THE ESCALATION PROCESS"),

(821,"An IS manager finds significant exceptions to a newly released industry-required security standard. What should be done NEXT?",
["Document risk acceptances.","Conduct an IS audit.","Assess the consequences of noncompliance.","Revise the organization's security policy."],"C",
"จำ: significant exceptions to required standard → ASSESS CONSEQUENCES OF NONCOMPLIANCE"),

(822,"Which BEST facilitates effective IR testing?",
["Including all business units in testing","Testing after major business changes","Simulating realistic test scenarios","Reviewing test results quarterly"],"C",
"จำ: effective IR testing → SIMULATING REALISTIC TEST SCENARIOS"),

(823,"Which is the BEST indication of effective IS governance?",
["IS is considered the responsibility of the entire IS team.","IS is integrated into corporate governance.","IS governance is based on an external security framework.","IS controls are assigned to risk owners."],"B",
"จำ: effective IS governance → IS INTEGRATED INTO CORPORATE GOVERNANCE"),

(824,"The IS manager is notified of a new vulnerability affecting key data processing systems. What should be done FIRST?",
["Re-evaluate the risk.","Ask the business owner for the new remediation plan.","Inform senior management.","Implement compensating controls."],"A",
"จำ: new vulnerability in key systems → FIRST = RE-EVALUATE THE RISK"),

(825,"Which is the BEST way to assess risk associated with using a SaaS vendor?",
["Require vendors to complete IS questionnaires.","Request customer references from the vendor.","Verify IS requirements are included in the contract.","Review the results of the vendor's independent control reports."],"D",
"จำ: assess SaaS vendor risk → REVIEW VENDOR'S INDEPENDENT CONTROL REPORTS"),

(826,"Security administration efforts will be greatly reduced following deployment of which technique?",
["Access control lists","Distributed access control","Discretionary access control","Role-based access control"],"D",
"จำ: reduce security administration efforts → ROLE-BASED ACCESS CONTROL"),

(827,"Which is the BEST way for an IS manager to improve effectiveness of an org's IS program?",
["Focus on addressing conflicts between security and performance.","Obtain assistance from IT to implement automated security controls.","Include IS requirements in the change control process.","Collaborate with business and IT functions in determining controls."],"D",
"จำ: improve IS program effectiveness → COLLABORATE WITH BUSINESS AND IT in determining controls"),

(828,"What should an IS manager do FIRST upon learning of noncompliance with an impending IS regulatory change?",
["Conduct a business impact and vulnerability analysis.","Report the noncompliance to senior management.","Assess the risk and cost of noncompliance.","Implement the correct measures to become compliant."],"C",
"จำ: noncompliance with IS regulatory change → FIRST = ASSESS RISK AND COST of noncompliance"),

(829,"Which is MOST critical when creating an IR plan?",
["Identifying what constitutes an incident","Identifying vulnerable data assets","Documenting incident notification and escalation processes","Aligning with the risk assessment process"],"C",
"จำ: IR plan MOST critical → DOCUMENTING INCIDENT NOTIFICATION AND ESCALATION PROCESSES"),

(830,"Which would BEST help to ensure appropriate security controls are built into software?",
["Integrating security throughout the development process","Performing security testing prior to deployment","Providing standards for implementation during development","Providing security training to the dev team"],"A",
"จำ: security built into software → INTEGRATING SECURITY THROUGHOUT DEVELOPMENT PROCESS"),

(831,"Which will BEST facilitate integration of IS governance into enterprise governance?",
["Implementing an IS awareness program","Documenting the IS governance framework","Developing an IS policy based on risk assessments","Establishing an IS steering committee"],"D",
"จำ: IS governance into enterprise governance → IS STEERING COMMITTEE"),

(832,"What should an IS manager do FIRST when noncompliance with security standards is identified?",
["Validate the noncompliance","Include the noncompliance in the risk register","Report the noncompliance to senior management","Implement compensating controls"],"A",
"จำ: noncompliance identified → FIRST = VALIDATE THE NONCOMPLIANCE"),

(833,"When recovering a compromised system needing a complete rebuild, which should be considered FIRST?",
["Network system logs","Intrusion detection system (IDS) logs","Patch management files","Configuration management files"],"D",
"จำ: complete rebuild of compromised system → FIRST = CONFIGURATION MANAGEMENT FILES"),

(834,"When deciding to move to a cloud-based model, the FIRST consideration should be:",
["data classification","physical location of the data","storage in a shared environment","availability of the data"],"A",
"จำ: move to cloud FIRST consideration → DATA CLASSIFICATION"),

(835,"Which is the PRIMARY objective of incident triage?",
["Containment of threats","Coordination of communications","Categorization of events","Mitigation of vulnerabilities"],"C",
"จำ: incident triage PRIMARY objective → CATEGORIZATION OF EVENTS"),

(836,"Who is accountable for ensuring risk mitigation is effective?",
["Application owner","Business owner","Risk owner","Control owner"],"C",
"จำ: accountable for risk mitigation effectiveness → RISK OWNER"),

(837,"Which BEST enables an IS manager to obtain organizational support for implementation of security controls?",
["Conducting periodic vulnerability assessments","Defining the organization's risk management framework","Communicating BIA results","Establishing effective stakeholder relationships"],"D",
"จำ: obtain organizational support for controls → ESTABLISHING EFFECTIVE STAKEHOLDER RELATIONSHIPS"),

(838,"To support effective risk decision making, which is MOST important to have in place?",
["An audit committee of mid-level management","Risk reporting procedures","Well-defined and approved controls","Established risk domains"],"B",
"จำ: effective risk decision making → RISK REPORTING PROCEDURES"),

(839,"Which party should be responsible for determining access levels to an app that processes client information?",
["The identity and access management team","The business client","The IS team","Business unit management"],"D",
"จำ: determine access levels to app → BUSINESS UNIT MANAGEMENT"),

(840,"What should be an IS manager's MOST important consideration when developing a multi-year plan?",
["Ensuring contingency plans for potential IS risks","Ensuring alignment with the plans of other business units","Demonstrating projected budget increases year after year","Allowing the IS program to expand its capabilities"],"B",
"จำ: multi-year IS plan MOST important → ALIGNMENT WITH OTHER BUSINESS UNITS"),

(841,"When performing a BIA, who should be responsible for determining the initial RTO?",
["IS manager","External consultant","Business continuity coordinator","Information owner"],"D",
"จำ: determine initial RTO in BIA → INFORMATION OWNER"),

(842,"Which will ensure confidentiality of content when accessing an email system over the Internet?",
["Digital encryption","Multi-factor authentication","Digital signatures","Data masking"],"A",
"จำ: email confidentiality over Internet → DIGITAL ENCRYPTION"),

(843,"Who is BEST suited to determine how the information in a database should be classified?",
["IS analyst","Database analyst","Database administrator (DBA)","Data owner"],"D",
"จำ: determine database classification → DATA OWNER"),

(844,"Which is an incident containment method?",
["Reviewing system logs and audit trails","Removing compromised systems from the network","Analyzing systems for impact from the incident","Mapping the scope of the incident on the network"],"B",
"จำ: incident containment method → REMOVING COMPROMISED SYSTEMS from network"),

(845,"A CISO learns a 3rd party service provider did not notify the org of a data breach affecting the provider's data center. What should the CISO do FIRST?",
["Determine the extent of the impact to the organization.","Request an independent review of the provider's data center.","Notify affected customers of the data breach.","Recommend canceling the outsourcing contract."],"A",
"จำ: 3rd party breach not notified → FIRST = DETERMINE EXTENT OF IMPACT to org"),

(846,"Which is MOST important to include in an IR plan to ensure incidents are responded to by appropriate individuals?",
["Skills required for the IR team","A detailed incident notification process","A list of external resources to assist","Service level agreements (SLAs)"],"B",
"จำ: IR plan → appropriate individuals respond = DETAILED INCIDENT NOTIFICATION PROCESS"),

(847,"Which is the PRIMARY role of an IS manager in a software development project?",
["To identify software security weaknesses","To identify noncompliance in the early design stage","To assess and approve the security application architecture","To enhance awareness for secure software design"],"C",
"จำ: IS manager in software dev project PRIMARY role → ASSESS AND APPROVE SECURITY APP ARCHITECTURE"),

(848,"Which MOST effectively identifies issues related to noncompliance with legal, regulatory, and contractual requirements?",
["Compliance maturity assessment","Compliance benchmarking data","Compliance gap analysis","Independent compliance audit"],"D",
"จำ: identify noncompliance with legal/regulatory requirements → INDEPENDENT COMPLIANCE AUDIT"),

(849,"Which is MOST helpful for fostering an effective IS culture?",
["Obtaining support from key organizational influencers","Implementing comprehensive technical security controls","Conducting regular IS awareness training","Developing procedures to enforce IS policy"],"A",
"จำ: foster effective IS culture → SUPPORT FROM KEY ORGANIZATIONAL INFLUENCERS"),

(850,"Which is MOST important to convey to employees in building a security risk-aware culture?",
["Employee access should be based on least privilege.","Personal info requires different controls than sensitive info.","The responsibility for security rests with all employees.","Understanding an asset's value is critical to risk management."],"C",
"จำ: security risk-aware culture → RESPONSIBILITY FOR SECURITY RESTS WITH ALL EMPLOYEES"),
]

# ── Q851-900 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(851,"Which is the PRIMARY objective of integrating IS governance into corporate governance?",
["To align security goals with the IS program","To ensure the business supports IS goals","To adequately safeguard the business in achieving its mission","To obtain management commitment for sustaining the security program"],"C",
"จำ: integrate IS governance into corporate governance → SAFEGUARD BUSINESS IN ACHIEVING ITS MISSION"),

(852,"Which is an IS manager's MOST important action to mitigate risk associated with malicious software?",
["Disabling end-user computer peripheral access ports","Implementing a multi-layered security program","Ensuring antivirus has the latest definition files","Strengthening security patch implementation processes"],"B",
"จำ: mitigate malicious software risk → MULTI-LAYERED SECURITY PROGRAM"),

(853,"Which is the PRIMARY reason for granting a security exception?",
["The risk is justified by the cost to security.","The risk is justified by the benefit to security.","The risk is justified by the benefit to the business.","The risk is justified by the cost to the business."],"C",
"จำ: grant security exception PRIMARY reason → RISK JUSTIFIED BY BENEFIT TO BUSINESS"),

(854,"Which is MOST effective in preventing vulnerabilities that may disrupt availability of a critical business app?",
["A patch management process","Change management controls","Version control","Logical access controls"],"B",
"จำ: prevent vulnerabilities disrupting critical app → CHANGE MANAGEMENT CONTROLS"),

(855,"An org is outsourcing DR activities. Which is MOST important to include in the outsourcing agreement?",
["Requirements for regularly testing backups","The DR communication plan","Recovery time objectives (RTOs)","Definition of when a disaster should be declared"],"C",
"จำ: outsource DR activities → include RECOVERY TIME OBJECTIVES (RTOs)"),

(856,"Which type of plan is PRIMARILY intended to reduce the potential impact of security events that may occur?",
["Incident response plan","Business continuity plan (BCP)","Security awareness plan","Disaster recovery plan (DRP)"],"A",
"จำ: reduce potential impact of security events → INCIDENT RESPONSE PLAN"),

(857,"Which is the MOST important outcome of strategic alignment of corporate and IS governance?",
["Implementation of IS controls","Development of a common set of IT security policies","Higher acceptance of IS projects","Reduction of adverse impacts on the organization to an acceptable level"],"D",
"จำ: strategic alignment of corporate + IS governance → REDUCE ADVERSE IMPACTS to acceptable level"),

(858,"Which is MOST important as a basis for developing an effective IS program that supports business goals?",
["An IS strategy","A defined security organizational structure","IS policies","Metrics to drive the IS program"],"A",
"จำ: basis for effective IS program → IS STRATEGY"),

(859,"Which BEST enables integration of IS governance into corporate governance?",
["Senior management approval of IS strategy","Clear lines of authority across the organization","An IS steering committee with business representation","Well-documented IS policies and standards"],"C",
"จำ: IS governance into corporate governance → IS STEERING COMMITTEE with business representation"),

(860,"Which contributes MOST to the effectiveness of IS governance?",
["Properly managed risk","Alignment with technology strategy","Stakeholder commitment","A defined security policy"],"C",
"จำ: IS governance effectiveness → STAKEHOLDER COMMITMENT"),

(861,"Which is the BEST approach for addressing noncompliance with security standards?",
["Maintain a security exceptions process.","Apply additional logging and monitoring to affected assets.","Discontinue affected activities until security requirements can be met.","Develop new security standards."],"A",
"จำ: address noncompliance with security standards → MAINTAIN SECURITY EXCEPTIONS PROCESS"),

(862,"Which is the BEST method for managing IS compliance of third-party suppliers?",
["Develop specific IS policies for third parties.","Conduct a vulnerability assessment of the 3rd party.","Include 3rd party details in the risk register.","Ensure IS requirements are addressed in the contract."],"D",
"จำ: 3rd party IS compliance → IS REQUIREMENTS ADDRESSED IN CONTRACT"),

(863,"An org is creating agreement with a cloud provider. Who should determine the 3rd party's destruction schedule for the org's information?",
["The org's IS manager","The cloud provider's IS manager","The org's data owner","The cloud provider's data custodian"],"C",
"จำ: determine destruction schedule for org's info → ORG'S DATA OWNER"),

(864,"Which is the BEST course of action when the org's IR team lacks expertise in forensic analysis?",
["Contract with external forensic experts.","Develop forensic analysis procedures.","Document the shortcoming.","Acquire forensic analysis tools."],"A",
"จำ: IR team lacks forensic expertise → CONTRACT WITH EXTERNAL FORENSIC EXPERTS"),

(865,"What should be the FIRST step when investigating an employee suspected of inappropriately downloading proprietary info?",
["Check for a signed NDA.","Review system access logs.","Conduct a forensic examination of the device.","Discuss the concern with the employee."],"B",
"จำ: investigate employee downloading proprietary info → FIRST = REVIEW SYSTEM ACCESS LOGS"),

(866,"Which is MOST critical to ensure IS incidents are managed properly?",
["Conducting an incident capability maturity assessment","Testing the IR plan","Establishing an incident management performance matrix","Assembling the IR team"],"B",
"จำ: IS incidents managed properly → TESTING THE IR PLAN"),

(867,"The GREATEST challenge when attempting data recovery of a specific file during forensic analysis is when:",
["high-level disk formatting has been performed.","all files in the directory have been deleted.","the partition table on the disk has been deleted.","the file has been overwritten."],"D",
"จำ: forensic data recovery GREATEST challenge → FILE HAS BEEN OVERWRITTEN"),

(868,"Which is MOST helpful in determining the criticality of an organization's business functions?",
["Disaster recovery plan (DRP)","Business continuity plan (BCP)","Security assessment report (SAR)","Business impact analysis (BIA)"],"D",
"จำ: determine criticality of business functions → BIA"),

(869,"The contribution of RPO to disaster recovery is to:",
["eliminate single points of failure.","reduce mean time between failures (MTBF).","define backup strategy.","minimize outage periods."],"C",
"จำ: RPO contribution to DR → DEFINE BACKUP STRATEGY"),

(870,"An IS manager is MOST likely to obtain approval for a new security project when the business case provides evidence of:",
["threats to the organization.","organizational alignment.","existing control costs.","IT strategy alignment."],"B",
"จำ: obtain approval for security project → evidence of ORGANIZATIONAL ALIGNMENT"),

(871,"Which should be established FIRST when implementing an IS governance framework?",
["Security incident management team","Security policies","Security architecture","Security awareness training program"],"B",
"จำ: implement IS governance framework FIRST → SECURITY POLICIES"),

(872,"Which approach is MOST helpful for properly scoping a security assessment of an existing vendor?",
["Review the vendor's security policy.","Review controls listed in the vendor contract.","Focus the review on infrastructure with highest risk.","Determine whether vendor follows selected security framework rules."],"B",
"จำ: scope vendor security assessment → REVIEW CONTROLS LISTED IN VENDOR CONTRACT"),

(873,"A 3rd party audit identified several critical risks. What should the IS manager do NEXT?",
["Assign risk ownership.","Identify mitigating controls.","Report the findings to senior management.","Prioritize the risks."],"D",
"จำ: 3rd party audit found critical risks → NEXT = PRIORITIZE THE RISKS"),

(874,"Which provides the BEST evidence that a recently established IS program is effective?",
["The number of reported incidents has increased.","Regular IT balanced scorecards are communicated.","The number of IT incident tickets stayed consistent.","Senior management reported fewer junk emails."],"A",
"จำ: IS program effective BEST evidence → ↑ NUMBER OF REPORTED INCIDENTS"),

(875,"An investigation found root cause was negligent handling of incident alerts by system admins. What is the BEST way to address?",
["Provide IR training to data owners.","Provide IR training to data custodians.","Conduct a risk assessment and share with senior management.","Revise the IR plan to align with business processes."],"B",
"จำ: negligent incident alert handling by sys admins → IR TRAINING TO DATA CUSTODIANS"),

(876,"An org was victim of a targeted attack undetected until analyst noticed extra user account on firewall. Which would have detected it?",
["Web-application firewall","Security information and event management (SIEM)","Data leakage prevention (DLP)","Network access control"],"B",
"จำ: detect extra user account on firewall → SIEM"),

(877,"Who is accountable for data loss in event of an IS incident at a 3rd party provider?",
["The IS manager","The service provider that hosts the data","The IR team","The business data owner"],"D",
"จำ: data loss accountability at 3rd party → BUSINESS DATA OWNER"),

(878,"Which BEST minimizes IS risk in deploying apps to production?",
["Conducting pen testing post implementation","Having a well-defined change process","Verifying security during the testing process","Integrating security controls in each phase of the life cycle"],"D",
"จำ: minimize IS risk deploying to production → INTEGRATING SECURITY CONTROLS IN EACH PHASE"),

(879,"Which would BEST guide the development and maintenance of an IS program?",
["A business impact assessment","The organization's risk appetite","A comprehensive risk register","An established risk assessment process"],"B",
"จำ: guide IS program development → ORG'S RISK APPETITE"),

(880,"Which BEST indicates effective IS governance?",
["Availability of IS policies","Regular steering committee meetings","Organization-wide attendance at annual security training","Regular testing of the security IR plan"],"B",
"จำ: effective IS governance → REGULAR STEERING COMMITTEE MEETINGS"),

(881,"The MOST useful technique for maintaining management support for the IS program is:",
["informing management about the security of business operations.","identifying risks and consequences of failure to comply.","benchmarking security programs of comparable organizations.","implementing a comprehensive security awareness program."],"A",
"จำ: maintain management support → INFORM MANAGEMENT ABOUT SECURITY OF BUSINESS OPERATIONS"),

(882,"When remote access is granted to a company's internal network, the MOST important consideration should be that access is provided:",
["by the use of a remote access server.","if a robust IT infrastructure exists.","subject to legal and regulatory requirements.","on a need-to-know basis subject to controls."],"D",
"จำ: remote access to internal network → NEED-TO-KNOW basis subject to controls"),

(883,"Which should be triggered FIRST when unknown malware has infected an org's critical system?",
["Disaster recovery plan (DRP)","Vulnerability management plan","Incident response plan","Business continuity plan (BCP)"],"C",
"จำ: unknown malware on critical system → TRIGGER INCIDENT RESPONSE PLAN"),

(884,"Which is the FIRST step in developing a BIA?",
["Identifying interdependencies among critical functions","Determining the minimum resources needed for recovery","Identifying which business functions are critical to the organization","Determining the required RTO of business operations"],"C",
"จำ: BIA FIRST step → IDENTIFY WHICH BUSINESS FUNCTIONS ARE CRITICAL"),

(885,"Which is MOST important when defining how an IS budget should be allocated?",
["Business impact assessment","Regulatory compliance standards","IS strategy","IS policy"],"C",
"จำ: IS budget allocation → IS STRATEGY"),

(886,"A forensic examination of a PC is required but the PC has been switched off. What should be done FIRST?",
["Perform a backup of the computer using the network.","Perform a bit-by-bit backup of the hard disk using a write-blocking device.","Reboot the system using third-party forensic software.","Perform a backup of the hard drive using backup utilities."],"B",
"จำ: forensic exam on switched-off PC → FIRST = BIT-BY-BIT BACKUP with write-blocking device"),

(887,"What should an org do FIRST when confronted with transfer of personal data across borders?",
["Define policies and standards for data processing.","Implement applicable privacy principles.","Research cyber insurance policies.","Assess local or regional regulation."],"D",
"จำ: personal data transfer across borders → FIRST = ASSESS LOCAL/REGIONAL REGULATION"),

(888,"Which BEST enables an org to measure total time operations can be sustained at an alternative site?",
["Recovery point objective (RPO)","Allowable interruption window (AIW)","Maximum tolerable outage (MTO)","Recovery time objective (RTO)"],"C",
"จำ: total time operations sustained at alternative site → MAXIMUM TOLERABLE OUTAGE (MTO)"),

(889,"Which has the GREATEST influence on successful integration of IS within the business?",
["Organizational structure and culture","Risk tolerance and organizational objectives","IS personnel","The desired state of the organization"],"A",
"จำ: IS integration into business GREATEST influence → ORGANIZATIONAL STRUCTURE AND CULTURE"),

(890,"Which is the MOST important consideration to support potential legal action when responding to a security incident?",
["Contacting the appropriate law enforcement agency","Encrypting the documentation being assembled","Maintaining chain-of-custody of evidence","Preparing full forensic system backups"],"C",
"จำ: support potential legal action → MAINTAINING CHAIN-OF-CUSTODY of evidence"),

(891,"An IR team established that an app has been breached. What should be done NEXT?",
["Maintain the affected systems in a forensically acceptable state.","Inform senior management of the breach.","Isolate the impacted systems from the rest of the network.","Conduct a risk assessment on the affected application."],"C",
"จำ: app breached confirmed → NEXT = ISOLATE IMPACTED SYSTEMS"),

(892,"A daily report reveals an IT employee changed a firewall rule outside of change control. The IS manager's FIRST step should be to:",
["perform an analysis of the change.","report the event to senior management.","require that the change be reversed.","review the change management process."],"A",
"จำ: unauthorized firewall change → FIRST = PERFORM ANALYSIS OF THE CHANGE"),

(893,"Which BEST facilitates reporting of useful information about IS program effectiveness?",
["Security benchmark report","Risk heat map","Security metrics dashboard","Key risk indicators (KRIs)"],"C",
"จำ: useful IS program effectiveness reporting → SECURITY METRICS DASHBOARD"),

(894,"Which BEST mitigates risk of information loss caused by a cloud provider becoming insolvent?",
["Contractual provisions for the right to audit","Effective DLP controls","Contractual provisions for data repatriation","Cybersecurity insurance"],"C",
"จำ: cloud provider becomes insolvent → CONTRACTUAL PROVISIONS FOR DATA REPATRIATION"),

(895,"An IS team is identifying confidential data to formalize asset classification. Most relevant input would be from:",
["Business process owners.","The legal department.","The CIO.","Database administrators (DBAs)."],"A",
"จำ: identify confidential data for classification → BUSINESS PROCESS OWNERS"),

(896,"Which is the PRIMARY reason to conduct a post-incident review?",
["To determine whether digital evidence is admissible","To notify regulatory authorities","To improve the response process","To aid in future risk assessments"],"C",
"จำ: post-incident review PRIMARY reason → IMPROVE THE RESPONSE PROCESS"),

(897,"Which is the BEST way to protect against unauthorized access to an encrypted file sent via email?",
["Validating the recipient's identity","Using a digital signature in the email","Utilizing a separate distribution channel for the password","Ensuring a policy exists for encrypting files in transit"],"C",
"จำ: protect encrypted file sent via email → SEPARATE DISTRIBUTION CHANNEL for password"),

(898,"The PRIMARY purpose of implementing IS governance metrics is to:",
["measure alignment with best practices.","refine control operations.","assess operational and program metrics.","guide security towards the desired state."],"D",
"จำ: IS governance metrics PRIMARY purpose → GUIDE SECURITY TOWARDS DESIRED STATE"),

(899,"Which role is PRIMARILY responsible for developing an information classification framework based on business needs?",
["Information owner","IS steering committee","Senior management","IS manager"],"C",
"จำ: develop information classification framework → SENIOR MANAGEMENT"),

(900,"Which should be done FIRST when developing an IS strategy?",
["Establish IS steering committee.","Determine the desired state of IS.","Develop security policies and standards.","Identify owners of information assets."],"B",
"จำ: developing IS strategy FIRST → DETERMINE DESIRED STATE of IS"),
]

# ── Q901-950 ──────────────────────────────────────────────────────────────────
QUESTIONS += [
(901,"A BIA should be periodically executed PRIMARILY to:",
["verify the effectiveness of controls.","check compliance with regulations.","validate vulnerabilities on environmental changes.","analyze the importance of assets."],"D",
"จำ: BIA periodically executed PRIMARILY → ANALYZE THE IMPORTANCE OF ASSETS"),

(902,"While responding to a high-profile incident, an IS manager observed deficiencies in the IR plan. When is the BEST time to update the plan?",
["While responding to the incident","During post-incident review","During a tabletop exercise","After a risk reassessment"],"B",
"จำ: update IR plan deficiencies → DURING POST-INCIDENT REVIEW"),

(903,"Which BEST enables an IS manager to demonstrate effectiveness of IS and risk program to senior management?",
["Updated risk assessments","Audit reports","Counts of IS incidents","Monthly metrics"],"D",
"จำ: demonstrate IS program effectiveness to senior mgmt → MONTHLY METRICS"),

(904,"Which would BEST justify spending for a compensating control?",
["Root cause analysis","Emerging risk trends","Vulnerability assessment","Risk analysis"],"D",
"จำ: justify spending for compensating control → RISK ANALYSIS"),

(905,"Which is the BEST way to monitor for APTs in an organization?",
["Browse the Internet to learn of potential events.","Search for threat signatures in the environment.","Search for anomalies in the environment.","Network with peers in the industry to share information."],"C",
"จำ: monitor for APTs → SEARCH FOR ANOMALIES in environment"),

(906,"Who should be accountable for reviewing a new EDR solution to verify it has been properly deployed and configured?",
["The security analyst","The chief audit executive (CAE)","The CISO","The system administrator"],"C",
"จำ: accountable for EDR solution deployment review → CISO"),

(907,"An organization's quality process can BEST support security management by providing:",
["a repository for security systems documentation.","assurance that security requirements are met.","guidance for security strategy.","security configuration controls."],"B",
"จำ: quality process supports security management → ASSURANCE THAT SECURITY REQUIREMENTS ARE MET"),

(908,"Which is the MOST important consideration when defining an IS framework?",
["IS budget","Industry standards","Business strategy","Organizational culture"],"C",
"จำ: defining IS framework MOST important → BUSINESS STRATEGY"),

(909,"Which is the MOST important consideration for reporting risk assessment results to senior management?",
["Reports should include comparisons to industry benchmarks.","Reports should be presented in business terms.","Reports should use formal methodologies.","Reports should include recommended controls."],"B",
"จำ: report risk assessment to senior mgmt → PRESENTED IN BUSINESS TERMS"),

(910,"Which is the BEST way to determine the effectiveness of an IR plan?",
["Reviewing previous audit reports","Benchmarking the plan against best practices","Performing a penetration test","Conducting a tabletop exercise"],"D",
"จำ: determine IR plan effectiveness → TABLETOP EXERCISE"),

(911,"Which should be an IS manager's MOST important consideration when determining priority for implementing security controls?",
["Availability of security budget","Alignment with industry benchmarks","Results of BIAs","Possibility of reputational loss"],"C",
"จำ: priority for implementing controls → RESULTS OF BIAs"),

(912,"Which is the PRIMARY reason for an IS manager to periodically review existing controls?",
["To prioritize security initiatives","To avoid redundant controls","To align with emerging risk","To address end-user control complaints"],"C",
"จำ: periodically review existing controls → TO ALIGN WITH EMERGING RISK"),

(913,"Which should be done FIRST when implementing a security program?",
["Implement data encryption.","Perform a risk analysis.","Create an information asset inventory.","Determine the value of information assets."],"C",
"จำ: implement security program FIRST → CREATE INFORMATION ASSET INVENTORY"),

(914,"Who is MOST appropriate to own the risk associated with failure of a privileged access control?",
["Data owner","IS manager","Business owner","Compliance manager"],"C",
"จำ: own risk of privileged access control failure → BUSINESS OWNER"),

(915,"Which is an example of a deterrent control?",
["Segregation of responsibilities","A warning banner","An intrusion detection system (IDS)","Periodic data restoration"],"B",
"จำ: deterrent control example → WARNING BANNER"),

(916,"An IS manager completed a risk assessment and determined residual risk. What should be the NEXT step?",
["Implement countermeasures to mitigate risk.","Classify all identified risks.","Conduct an evaluation of controls.","Determine if the risk is within the risk appetite."],"D",
"จำ: after determining residual risk → NEXT = DETERMINE IF WITHIN RISK APPETITE"),

(917,"Which BEST enables an org to maintain an appropriate security control environment?",
["Periodic employee security training","Budgetary support for security","Alignment to an industry security framework","Monitoring of the threat landscape"],"C",
"จำ: maintain appropriate security control environment → ALIGNMENT TO INDUSTRY SECURITY FRAMEWORK"),

(918,"Which is MOST important for responding effectively to security breaches?",
["Chain of custody","Incident classification","Log monitoring","Communication plan"],"B",
"จำ: respond effectively to security breaches → INCIDENT CLASSIFICATION"),

(919,"Which is the BEST method for assisting with incident containment in an IaaS cloud environment?",
["Disabling unnecessary services","Implementing privileged identity management","Establishing automated detection","Implementing network segmentation"],"D",
"จำ: incident containment in IaaS cloud → NETWORK SEGMENTATION"),

(920,"Which should be performed FIRST in response to a new IS regulation?",
["Industry benchmarking","Independent audit","Risk assessment","Gap analysis"],"D",
"จำ: new IS regulation → FIRST = GAP ANALYSIS"),

(921,"To ensure IS of outsourced IT services, which is the MOST critical due diligence activity?",
["Assess the level of security awareness of the service provider.","Review a recent independent audit report of the service provider.","Review samples of service level reports from the service provider.","Request the service provider comply with IS policy."],"B",
"จำ: outsourced IT services IS assurance → REVIEW INDEPENDENT AUDIT REPORT of provider"),

(922,"Which is the MOST important reason to consider org culture when developing an IS program?",
["It helps expedite approval for the IS budget.","It helps the org meet compliance requirements.","Everyone in the org is responsible for IS.","Security incidents have adverse impact on the entire org."],"C",
"จำ: consider org culture in IS program → EVERYONE IS RESPONSIBLE FOR IS"),

(923,"Which process BEST supports the evaluation of IR effectiveness?",
["Post-incident review","Chain of custody","Incident logging","Root cause analysis"],"A",
"จำ: evaluate IR effectiveness → POST-INCIDENT REVIEW"),

(924,"What should an IS manager do FIRST after learning through mass media of a data breach at the org's hosted payroll service provider?",
["Validate the breach with the provider.","Suspend the data exchange with the provider.","Notify appropriate regulatory authorities.","Initiate the BCP."],"A",
"จำ: media reports provider breach → FIRST = VALIDATE THE BREACH with provider"),

(925,"What should an IS manager do FIRST after discovering a business unit bypassed change management to implement a new app?",
["Update the change management process.","Revise the procurement process.","Discuss the issue with senior leadership.","Remove the application from production."],"C",
"จำ: business unit bypassed change management → FIRST = DISCUSS WITH SENIOR LEADERSHIP"),

(926,"Which is MOST important to consider when developing a security awareness strategy?",
["Technical solutions for delivery","Cost to implement","Organizational culture","Organizational maturity"],"C",
"จำ: security awareness strategy → ORGANIZATIONAL CULTURE"),

(927,"A pen test of an org's external web app shows several vulnerabilities. Which presents the GREATEST concern?",
["Vulnerabilities were caused by insufficient UAT.","Exploit code for one of the vulnerabilities is publicly available.","Rules of engagement form was not signed prior to the pen test.","Vulnerabilities were not found by internal tests."],"B",
"จำ: web app pen test vulnerabilities GREATEST concern → EXPLOIT CODE PUBLICLY AVAILABLE"),

(928,"Which is the GREATEST concern from lack of severity criteria in incident classification?",
["The service desk will be staffed incorrectly.","Timely detection of attacks will be impossible.","Statistical reports will be incorrect.","Escalation procedures will be ineffective."],"D",
"จำ: no severity criteria in incident classification → ESCALATION PROCEDURES WILL BE INEFFECTIVE"),

(929,"Which is the BEST way to maintain organization-wide support for an IS strategy?",
["Ensure IS objectives are understood by key stakeholders.","Monitor user activity to identify IS policy violations.","Place IS awareness materials in visible locations.","Ensure IS policies are easily accessible."],"A",
"จำ: org-wide support for IS strategy → IS OBJECTIVES UNDERSTOOD BY KEY STAKEHOLDERS"),

(930,"Several critical systems have been compromised with malware. Which is the BEST strategy to eradicate this incident?",
["Reimage the systems.","Block access to the impacted systems.","Perform malware scanning.","Perform a vulnerability assessment."],"A",
"จำ: eradicate malware on critical systems → REIMAGE THE SYSTEMS"),

(931,"Which is the MOST important success factor for maintaining a security-aware culture?",
["Senior management sign-off on security projects","Regular security training and simulation exercises","Regular org-wide reporting on the risk profile","Employee security policy acknowledgment"],"B",
"จำ: maintain security-aware culture → REGULAR SECURITY TRAINING AND SIMULATION EXERCISES"),

(932,"Senior management is concerned the org's IPS may disrupt business operations. Which BEST indicates the IS manager has tuned the system to address this concern?",
["Decreasing false positives","Decreasing false negatives","Increasing false negatives","Increasing false positives"],"A",
"จำ: IPS disrupts business → tune by DECREASING FALSE POSITIVES"),

(933,"Which metric would BEST monitor how well IS requirements are incorporated into change management?",
["IS incidents caused by unauthorized changes","Unauthorized changes in the environment","Denied changes due to insufficient security details","IS-related changes"],"C",
"จำ: IS in change management → DENIED CHANGES DUE TO INSUFFICIENT SECURITY DETAILS"),

(934,"Which metric is MOST appropriate for evaluating the incident notification process?",
["Elapsed time between detection, reporting, and response","Average number of incidents per reporting period","Average total cost of downtime per reported incident","Elapsed time between response and resolution"],"A",
"จำ: evaluate incident notification process → ELAPSED TIME between detection, reporting, and response"),

(935,"Meeting which security objective BEST ensures information is protected against unauthorized disclosure?",
["Confidentiality","Integrity","Authenticity","Nonrepudiation"],"A",
"จำ: protect against unauthorized disclosure → CONFIDENTIALITY"),

(936,"Which is MOST important when developing a BCP for ransomware attacks?",
["Backups are maintained on multiple sites and regularly reviewed.","Impacted networks can be detached at the network switch level.","Backups are maintained offline and regularly tested.","Production data is continuously replicated between primary and secondary sites."],"C",
"จำ: BCP for ransomware → BACKUPS MAINTAINED OFFLINE and regularly tested"),

(937,"Who should be assigned as owner of a newly identified risk related to an org's new payroll system?",
["Head of IT department","Head of human resources (HR)","IS manager","Data privacy officer"],"B",
"จำ: owner of payroll system risk → HEAD OF HR (business owner)"),

(938,"An org decided to outsource IT operations. Which should be the PRIMARY focus of the IS manager?",
["Business continuity contingency planning is provided.","Security requirements are included in the vendor contract.","External security audit results are reviewed.","SLAs meet operational standards."],"B",
"จำ: outsource IT operations PRIMARY focus → SECURITY REQUIREMENTS IN VENDOR CONTRACT"),

(939,"Which is MOST effective in gaining support for IS strategy from senior management?",
["Cost-benefit analysis results","Third-party security audit results","BIA results","A major breach at a competitor"],"A",
"จำ: gain senior mgmt support for IS strategy → COST-BENEFIT ANALYSIS RESULTS"),

(940,"Management of a financial institution accepted an operational risk leading to deactivation of a critical monitoring process. Which should be the IS manager's GREATEST concern?",
["Deviation from risk management best practices","Impact on the risk culture","Inability to determine short-term impact","Impact on compliance risk"],"D",
"จำ: accepted risk → deactivated monitoring = GREATEST concern → IMPACT ON COMPLIANCE RISK"),

(941,"An employee's BYOD smartphone has been lost with corporate sensitive data. The IS manager's BEST course of action should have been to implement:",
["a requirement of prompt notification in event of loss.","multi-factor authentication for the mobile device.","a board-approved mobile policy and standard.","a securely configured device enforced by an MDM solution."],"D",
"จำ: BYOD lost with sensitive data → SECURELY CONFIGURED DEVICE enforced by MDM"),

(942,"Which is the BEST approach for an IS manager to develop an org's IS strategy?",
["Budget training costs and contingencies for unexpected events.","Determine desired outcomes and perform a gap analysis.","Evaluate the security posture in comparison with competitors.","Estimate operational costs and perform reliability checks."],"B",
"จำ: develop IS strategy → DETERMINE DESIRED OUTCOMES + GAP ANALYSIS"),

(943,"Which is the BEST way to monitor the effectiveness of security controls?",
["Review application and system audit logs.","Conduct regular threat assessments.","Establish and report security metrics.","Benchmark security controls against similar orgs."],"C",
"จำ: monitor security controls effectiveness → ESTABLISH AND REPORT SECURITY METRICS"),

(944,"An org had a data breach affecting clients. Legal counsel only learned after a press release. Which would have been MOST helpful in preventing this?",
["A gap analysis of technical controls","Regular IS policy reviews","Tabletop testing of the IR plan","A comprehensive BCP"],"C",
"จำ: legal not notified before press release → TABLETOP TESTING OF IR PLAN (includes comms)"),

(945,"Which would MOST effectively ensure that a new server is appropriately secured?",
["Enforcing technical security standards","Performing secure code reviews","Initiating security scanning","Conducting penetration testing"],"A",
"จำ: new server appropriately secured → ENFORCING TECHNICAL SECURITY STANDARDS"),

(946,"Spoofing should be prevented because it may be used to:",
["assemble information, track traffic, and identify network vulnerabilities.","predict which way a program will branch when an option is presented.","capture information such as passwords traveling through the network.","gain illegal entry to a secure system by faking the sender's address."],"D",
"จำ: prevent spoofing → GAIN ILLEGAL ENTRY by FAKING SENDER'S ADDRESS"),

(947,"Which is MOST important to have in place for an org's IS program to be effective?",
["Senior management support","A comprehensive IT strategy","Defined and allocated budget","Documented IS processes"],"A",
"จำ: IS program effective → SENIOR MANAGEMENT SUPPORT"),

(948,"When assigning a risk owner, the MOST important consideration is to ensure the owner has:",
["adequate knowledge of risk treatment and related control activities.","decision-making authority and the ability to allocate resources for risk.","sufficient time for monitoring and managing the risk effectively.","risk communication and reporting skills."],"B",
"จำ: assign risk owner → DECISION-MAKING AUTHORITY + ability to allocate resources"),

(949,"After a ransomware incident, systems were restored. Which should be of MOST concern to the IS manager?",
["The SLA was not met.","The RTO was not met.","The root cause was not identified.","Notification to stakeholders was delayed."],"C",
"จำ: post-ransomware restore → MOST concern = ROOT CAUSE NOT IDENTIFIED"),

(950,"To improve efficiency of new software development, security requirements should be defined:",
["based on code review.","based on available security assessment tools.","after functional requirements.","concurrently with other requirements."],"D",
"จำ: security requirements in software dev → CONCURRENTLY WITH OTHER REQUIREMENTS"),
]

# ── Q951-1000 ─────────────────────────────────────────────────────────────────
QUESTIONS += [
(951,"Which would provide the MOST effective security outcome in an org's contract management process?",
["Extending security assessment to cover asset disposal on contract termination","Ensuring security requirements are defined at the RFP stage","Extending security assessment to include random pen testing","Performing vendor security benchmark analyses at the RFP stage"],"B",
"จำ: effective security in contract management → SECURITY REQUIREMENTS AT RFP STAGE"),

(952,"Which is the BEST way to contain an SQL injection attack detected by a web app firewall?",
["Force password changes on the SQL database.","Reconfigure the web app firewall to block the attack.","Update the detection patterns on the web app firewall.","Block the IPs from where the attack originates."],"B",
"จำ: contain SQL injection via WAF → RECONFIGURE WAF TO BLOCK THE ATTACK"),

(953,"Who is accountable for approving an IS governance framework?",
["The board of directors","The CISO","The enterprise risk committee","The CIO"],"A",
"จำ: approve IS governance framework → BOARD OF DIRECTORS"),

(954,"Which is the PRIMARY benefit when IS governance framework is aligned with corporate governance?",
["Protection of business value and assets","Identification of core business strategies","Easier entrance into new businesses and technologies","Improved regulatory compliance posture"],"A",
"จำ: IS governance aligned with corporate governance → PROTECTION OF BUSINESS VALUE AND ASSETS"),

(955,"Which is the BEST method to protect confidentiality of data transmitted over the Internet?",
["Network address translation (NAT)","Message hashing","Transport Layer Security (TLS)","Multi-factor authentication"],"C",
"จำ: protect data confidentiality over Internet → TLS"),

(956,"Which is the FIRST step when conducting a post-incident review?",
["Identify mitigating controls.","Assess the costs of the incident.","Perform root cause analysis.","Assign responsibility for corrective actions."],"C",
"จำ: post-incident review FIRST step → PERFORM ROOT CAUSE ANALYSIS"),

(957,"Which BEST facilitates the effectiveness of cybersecurity IR?",
["Utilizing a SIEM tool","Utilizing industry-leading network pen testing tools","Increasing communication with all IR stakeholders","Continuously updating signatures of anti-malware solution"],"C",
"จำ: cybersecurity IR effectiveness → INCREASING COMMUNICATION WITH ALL IR STAKEHOLDERS"),

(958,"A legacy app cannot be patched. A firewall is implemented in front of it. Which risk treatment has been applied?",
["Accept","Transfer","Mitigate","Avoid"],"C",
"จำ: firewall in front of unpatched legacy app = MITIGATE"),

(959,"An IS manager was notified of potential security risks with a 3rd party service provider. What should be done NEXT?",
["Escalate to the CRO.","Conduct a vulnerability analysis.","Conduct a risk analysis.","Determine compensating controls."],"C",
"จำ: 3rd party security risks → NEXT = CONDUCT RISK ANALYSIS"),

(960,"An email digital signature will:",
["automatically correct unauthorized modification of an email message.","verify to recipients the integrity of an email message.","protect the confidentiality of an email message.","prevent unauthorized modification of an email message."],"B",
"จำ: email digital signature → VERIFY INTEGRITY to recipients"),

(961,"Business leaders encourage increased use of social media. What should be done FIRST to mitigate risk of confidential info disclosure?",
["Establish an organization-wide social media policy.","Develop sanctions for misuse of social media sites.","Monitor social media sites visited by employees.","Restrict social media access on corporate devices."],"A",
"จำ: social media risk → FIRST = ESTABLISH SOCIAL MEDIA POLICY"),

(962,"Which BEST facilitates effective strategic alignment of security initiatives?",
["Procedures and standards are approved by department heads.","Organizational units contribute to and agree on priorities.","Periodic security audits are conducted by a third-party.","The business strategy is periodically updated."],"B",
"จำ: strategic alignment of security initiatives → ORG UNITS CONTRIBUTE AND AGREE ON PRIORITIES"),

(963,"Which is MOST important to maintain integration among IR plan, BCP, and DRP?",
["Asset classification","RTOs","Chain of custody","Escalation procedures"],"D",
"จำ: integrate IR plan + BCP + DRP → ESCALATION PROCEDURES"),

(964,"An IS program is BEST positioned for success when closely aligned with:",
["IS best practices.","recognized industry frameworks.","IS policies.","the IS strategy."],"D",
"จำ: IS program success → closely aligned with IS STRATEGY"),

(965,"What should an IS manager do FIRST after identifying suspicious activity on a PC not in the IT asset inventory?",
["Isolate the PC from the network.","Perform a vulnerability scan.","Determine why the PC is not in inventory.","Reinforce IS training."],"A",
"จำ: suspicious PC not in inventory → FIRST = ISOLATE FROM NETWORK"),

(966,"Which is the MOST important consideration when briefing executives about the current state of the IS program?",
["Including a situational forecast.","Using appropriate language for the target audience.","Including trend charts for metrics.","Using a rating system to demonstrate effectiveness."],"B",
"จำ: brief executives on IS program → APPROPRIATE LANGUAGE FOR TARGET AUDIENCE"),

(967,"An org has multiple data repositories across departments. Which IS initiative should be the HIGHEST priority?",
["Data loss prevention (DLP)","Data retention strategy","Data encryption standards","Data masking"],"A",
"จำ: multiple data repositories → HIGHEST priority = DLP"),

(968,"Which is ESSENTIAL to ensuring effective IR?",
["BCP","Cost-benefit analysis","Classification scheme","Senior management support"],"C",
"จำ: effective IR ESSENTIAL → CLASSIFICATION SCHEME"),

(969,"Which is the BEST indicator of an organization's IS status?",
["Threat analysis","Controls audit","Penetration test","Intrusion detection log analysis"],"B",
"จำ: IS status BEST indicator → CONTROLS AUDIT"),

(970,"Which practice is MOST effective for determining the adequacy of incident management operations?",
["Conducting unannounced external vulnerability testing","Testing current IR plans with relevant stakeholders","Assessing IR team members' skills","Reviewing IR procedures against best practices"],"B",
"จำ: adequacy of incident management → TESTING IR PLANS WITH RELEVANT STAKEHOLDERS"),

(971,"Which MUST happen immediately following identification of a malware incident?",
["Eradication","Containment","Preparation","Recovery"],"B",
"จำ: after malware identified → IMMEDIATELY = CONTAINMENT"),

(972,"Which is MOST effective in monitoring an organization's existing risk?",
["Vulnerability assessment results","SIEM systems","Periodic updates to risk register","Risk management dashboards"],"D",
"จำ: monitor existing risk → RISK MANAGEMENT DASHBOARDS"),

(973,"Which BEST indicates that IS governance and corporate governance are integrated?",
["The IS team is aware of business goals.","A cost-benefit analysis is conducted on all IS initiatives.","The board is regularly informed of IS KPIs.","The IS steering committee is composed of business leaders."],"D",
"จำ: IS + corporate governance integrated → IS STEERING COMMITTEE composed of BUSINESS LEADERS"),

(974,"Which should be the PRIMARY basis for determining the value of assets?",
["Cost of replacing the assets","Total cost of ownership (TCO)","Business cost when assets are not available","Original cost of the assets minus depreciation"],"C",
"จำ: determine asset value → BUSINESS COST WHEN ASSETS ARE NOT AVAILABLE"),

(975,"Which is MOST helpful to identify whether IS policies have been followed?",
["Corrective controls","Directive controls","Detective controls","Preventive controls"],"C",
"จำ: identify whether IS policies followed → DETECTIVE CONTROLS"),

(976,"Which is the MOST important reason to classify an incident after detection?",
["To assign appropriate prioritization levels","To obtain funds for external forensic support","To approve data breach notifications","To ensure management is accurately informed"],"A",
"จำ: classify incident after detection → ASSIGN APPROPRIATE PRIORITIZATION LEVELS"),

(977,"Which principle BEST addresses protection of data from unauthorized modification?",
["Nonrepudiation","Integrity","Availability","Authenticity"],"B",
"จำ: protect from unauthorized modification → INTEGRITY"),

(978,"The MAIN reason for continuous monitoring of the security program is to:",
["validate reduction of incidents.","confirm benefits are being realized.","ensure alignment with industry standards.","optimize resource allocation."],"B",
"จำ: continuous monitoring security program MAIN reason → CONFIRM BENEFITS BEING REALIZED"),

(979,"Which would BEST enable the help desk to recognize an IS incident?",
["Provide the help desk with criteria for security incidents.","Include help desk members on the security IR team.","Require help desk to participate in post-incident reviews.","Train the help desk to review the call logs."],"A",
"จำ: help desk recognize IS incident → PROVIDE CRITERIA FOR SECURITY INCIDENTS"),

(980,"Which would be the GREATEST concern with implementation of KRIs?",
["Inability to measure KRIs","Poorly defined risk appetite","Overly specific KRI definitions","Complex organizational structure"],"B",
"จำ: KRI implementation GREATEST concern → POORLY DEFINED RISK APPETITE"),

(981,"When org lacks internal expertise for technical forensics, what is the BEST way to ensure effective investigations?",
["Purchase forensic SOPs.","Retain a forensics firm prior to experiencing an incident.","Ensure IR policy allows hiring a forensics firm.","Provide forensics training to the IS team."],"B",
"จำ: no forensics expertise → RETAIN FORENSICS FIRM PRIOR TO INCIDENT"),

(982,"Which is MOST important for effective implementation of an IS governance program?",
["IS roles and responsibilities are documented","Program budget approved and monitored by senior management","Employees receive customized IS training","Program goals communicated and understood by the organization"],"D",
"จำ: IS governance program effective → PROGRAM GOALS COMMUNICATED AND UNDERSTOOD by org"),

(983,"Which is the BEST way to maintain ongoing senior management support for implementation of a security monitoring tool?",
["Demonstrate return on investment (ROI).","Update security plans.","Present security monitoring reports.","Communicate risk reduction."],"A",
"จำ: maintain senior mgmt support for monitoring tool → DEMONSTRATE ROI"),

(984,"Which would BEST support a business case to implement an anti-ransomware solution?",
["Industry benchmark of anti-ransomware investments","A threat and vulnerability assessment","Trend analysis of ransomware attacks","A reduction in required backups and associated costs"],"B",
"จำ: business case for anti-ransomware → THREAT AND VULNERABILITY ASSESSMENT"),

(985,"When responding to an incident involving malware on a server, what should be done FIRST?",
["Isolate the server from the network.","Identify the owner of the server.","Locate the most recent backups.","Investigate the source of the malware."],"A",
"จำ: malware on server → FIRST = ISOLATE FROM NETWORK"),

(986,"Which BEST reduces the likelihood of leakage of private information via email?",
["User awareness training","Periodic phishing exercises","Email signature verification","Restricted personal use of company email"],"A",
"จำ: reduce email private info leakage → USER AWARENESS TRAINING"),

(987,"Which BEST determines the data retention strategy and subsequent policy for an org?",
["BIA","Risk appetite","Business requirements","Supplier requirements"],"C",
"จำ: data retention strategy → BUSINESS REQUIREMENTS"),

(988,"Which MUST be established to maintain an effective IS governance framework?",
["Security controls automation","Change management processes","Security policy provisions","Defined security metrics"],"C",
"จำ: maintain IS governance framework → SECURITY POLICY PROVISIONS"),

(989,"Which is the BEST defense-in-depth implementation for protecting high value assets or handling environments with trust concerns?",
["Continuous monitoring","Compartmentalization","Multi-factor authentication","Overlapping redundancy"],"B",
"จำ: defense-in-depth for high value assets → COMPARTMENTALIZATION"),

(990,"IS management and business unit management cannot agree whether to escalate an incident. Which would MOST effectively prevent this from recurring?",
["Develop additional communication channels.","Obtain senior management buy-in for IR processes.","Periodically test the IR plan.","Create a clear definition of incident classifications."],"D",
"จำ: disagreement on escalation → CLEAR DEFINITION OF INCIDENT CLASSIFICATIONS"),

(991,"Which should be done FIRST to ensure IS is integrated in system development projects?",
["Assign resources based on business impact.","Define security requirements.","Review the security policy.","Embed a security representative in each project team."],"B",
"จำ: IS in system development FIRST → DEFINE SECURITY REQUIREMENTS"),

(992,"For which is it MOST important that system administrators be restricted to read-only access?",
["User access log files","Administrator user profiles","System logging options","Administrator log files"],"D",
"จำ: sys admins read-only MOST important → ADMINISTRATOR LOG FILES (prevent tampering)"),

(993,"Which business unit should own the data that populates an identity management system?",
["Legal","Human resources (HR)","IS","IT"],"B",
"จำ: data owner for identity management system → HR"),

(994,"Which BEST indicates senior management support for an IS program?",
["Top-down communication","Regular security awareness training","Participation in a certification program","Steering committee involvement"],"D",
"จำ: senior management support for IS program → STEERING COMMITTEE INVOLVEMENT"),

(995,"When selecting metrics to monitor IS program effectiveness, it is MOST important for an IS manager to:",
["identify the program's risk and compensating controls.","consider the organization's business strategy.","consider the strategic objectives of the program.","leverage industry benchmarks."],"C",
"จำ: select IS metrics → consider STRATEGIC OBJECTIVES OF THE PROGRAM"),

(996,"A BCP should contain:",
["criteria for activation.","hardware and software inventories.","data restoration procedures.","information about eradication activities."],"A",
"จำ: BCP should contain → CRITERIA FOR ACTIVATION"),

(997,"A finance director decided to outsource the budget app and identified potential providers. What should the IS manager do FIRST?",
["Determine the required security controls for the new solution.","Obtain audit reports on service providers' hosting environment.","Review the DRPs of the providers.","Align roles of org's and service providers' staffs."],"A",
"จำ: outsource budget app → IS manager FIRST = DETERMINE REQUIRED SECURITY CONTROLS"),

(998,"What type of control is being implemented when a SIEM system is installed?",
["Corrective","Preventive","Deterrent","Detective"],"D",
"จำ: SIEM = DETECTIVE control"),

(999,"Which should be done FIRST when developing an information asset classification policy?",
["Identify accountability for information assets throughout the org.","Establish the criteria that define an asset's classification level.","Identify existing security measures for protecting assets.","Obtain executive input to identify high-value assets."],"B",
"จำ: asset classification policy FIRST → ESTABLISH CRITERIA for classification level"),

(1000,"Which is the BEST option to lower the cost to implement app security controls?",
["Include standard app security requirements.","Perform security tests in the development environment.","Perform a risk analysis after project completion.","Integrate security activities within the development process."],"D",
"จำ: lower cost of app security → INTEGRATE SECURITY WITHIN DEVELOPMENT PROCESS"),
]

# ── Q1001-1050 ────────────────────────────────────────────────────────────────
QUESTIONS += [
(1001,"Which is the GREATEST benefit of effective IS governance?",
["Treatment priorities are based on risk exposure.","IS standards are communicated to primary stakeholders.","The IS budget is aligned to the organization.","Executive management's strategy is aligned to the IS strategy."],"A",
"จำ: effective IS governance GREATEST benefit → TREATMENT PRIORITIES BASED ON RISK EXPOSURE"),

(1002,"The ability to integrate IS governance into corporate governance is PRIMARILY driven by:",
["the % of corporate budget allocated to IS program.","how often IS metrics are presented to senior mgmt.","how often the IS steering committee reviews security policies.","how well the IS program supports business objectives."],"D",
"จำ: IS governance integration PRIMARILY driven by → IS PROGRAM SUPPORTS BUSINESS OBJECTIVES"),

(1003,"Which presents the GREATEST challenge for protecting IoT devices?",
["IoT vendor reputation","IoT architecture diversity","IoT-specific training","IoT device policies"],"B",
"จำ: protecting IoT GREATEST challenge → IoT ARCHITECTURE DIVERSITY"),

(1004,"Which parameter is MOST helpful when designing a DR strategy?",
["Maximum tolerable downtime (MTD)","Mean time between failures (MTBF)","Allowable interruption window (AIW)","Recovery point objective (RPO)"],"A",
"จำ: design DR strategy → MAXIMUM TOLERABLE DOWNTIME (MTD)"),

(1005,"An IT service desk was not prepared for a ransomware attack. What should be given HIGHEST priority in an action plan?",
["Investing in threat intelligence capability","Implementing KRIs for ransomware attacks","Updating the IS incident response manual","Strengthening the data backup capability"],"C",
"จำ: service desk not prepared for ransomware → UPDATE IS INCIDENT RESPONSE MANUAL"),

(1006,"After a risk has been identified, analyzed, and evaluated, what should be done NEXT?",
["Monitor the risk.","Prioritize the risk for treatment.","Identify the risk owner.","Identify controls for risk mitigation."],"B",
"จำ: after risk identified/analyzed/evaluated → NEXT = PRIORITIZE FOR TREATMENT"),

(1007,"Which will BEST facilitate timely and effective IR?",
["Including pen test results in IR planning","Assessing the risk of compromised assets","Notifying stakeholders when invoking IR plan","Classifying the severity of an incident"],"D",
"จำ: timely and effective IR → CLASSIFYING SEVERITY OF INCIDENT"),

(1008,"Which MOST effectively communicates the current risk profile to senior mgmt after controls are applied?",
["Residual risk","Impact of loss events","Inherent risk","Number of risks avoided"],"A",
"จำ: current risk profile after controls applied → RESIDUAL RISK"),

(1009,"Which process should be done NEXT after completing a BIA?",
["Evaluate the DRP.","Develop requirements for IR plan.","Develop a BCP.","Identify resources for business recovery."],"C",
"จำ: after completing BIA → NEXT = DEVELOP BCP"),

(1010,"Which is MOST important to include in an IS policy?",
["Maturity levels","Baselines","Best practices","Management objectives"],"D",
"จำ: IS policy MOST important → MANAGEMENT OBJECTIVES"),

(1011,"What should an IS manager do FIRST when creating an org's DRP?",
["Develop response and recovery strategies.","Identify response and recovery teams.","Review the communications plan.","Conduct a BIA."],"D",
"จำ: creating DRP FIRST → CONDUCT A BIA"),

(1012,"Which would be the MOST effective use of findings from a post-incident review?",
["Providing input for updates to the IR plan","Developing cost reports regarding the incident","Providing justification for IR plan budget increase","Incorporating results into IS awareness training materials"],"A",
"จำ: post-incident review findings MOST effective use → UPDATE THE IR PLAN"),

(1013,"A known vulnerability was patched on the offending system. What should be done NEXT?",
["Scan to determine whether the vulnerability is present on other systems.","Review the vulnerability management process.","Install patches on all existing systems.","Report the root cause to senior management."],"A",
"จำ: patched known vuln → NEXT = SCAN OTHER SYSTEMS for same vuln"),

(1014,"Which is MOST helpful in determining the realization of benefits from an IS program?",
["Vulnerability assessments","Key risk indicators (KRIs)","BIA","Key performance indicators (KPIs)"],"D",
"จำ: realization of IS program benefits → KPIs"),

(1015,"During compliance review, a critical legacy app cannot meet mandatory security requirements. What should be done FIRST?",
["Update the risk register.","Recommend taking the app out of service.","Implement compensating controls.","Monitor the app until it can be replaced."],"A",
"จำ: legacy app can't meet security requirements → FIRST = UPDATE RISK REGISTER"),

(1016,"Which is the BEST way to improve an org's ability to detect and respond to incidents?",
["Conduct a BIA.","Conduct periodic awareness training.","Perform a security gap analysis.","Perform network pen testing."],"B",
"จำ: improve detect and respond to incidents → PERIODIC AWARENESS TRAINING"),

(1017,"Who would provide the MOST relevant input when aligning IS strategy with organizational goals?",
["Data privacy officer (DPO)","CISO","IS steering committee","Enterprise risk committee"],"C",
"จำ: align IS strategy with org goals → IS STEERING COMMITTEE"),

(1018,"Which is the PRIMARY role of the IS manager in app development?",
["To ensure control procedures address business risk","To ensure enterprise security controls are implemented","To ensure compliance with industry best practice","To ensure security is integrated into the SDLC"],"D",
"จำ: IS manager in app development PRIMARY role → INTEGRATE SECURITY INTO SDLC"),

(1019,"Which action by senior management would BEST enable successful IS governance framework implementation?",
["Demonstrating support for business and IS governance functions","Delegating implementation to IS management","Promoting use of internationally recognized governance framework","Engaging a consulting firm specializing in IS governance"],"A",
"จำ: IS governance success → senior mgmt DEMONSTRATING SUPPORT for IS governance"),

(1020,"Which is the BEST way to reduce risk of security incidents from targeted email attacks?",
["Conduct awareness training across the org.","Require acknowledgment of the acceptable use policy.","Disable all incoming cloud mail services.","Implement a DLP system."],"A",
"จำ: reduce risk from targeted email attacks → AWARENESS TRAINING"),

(1021,"Which is the PRIMARY benefit of an IS awareness training program?",
["Evaluating organizational security culture","Enforcing security policy","Influencing human behavior","Defining risk accountability"],"C",
"จำ: IS awareness training PRIMARY benefit → INFLUENCING HUMAN BEHAVIOR"),

(1022,"Which MOST effectively supports an org's security culture?",
["Business unit security metrics","An IS governance framework","Stakeholder involvement","A security mission statement"],"C",
"จำ: support security culture → STAKEHOLDER INVOLVEMENT"),

(1023,"A new type of ransomware infected an org's network. Which would have BEST enabled detection?",
["Periodic IS training for end users","Use of integrated patch deployment tools","Regular review of the threat landscape","Monitoring of anomalies in system behavior"],"D",
"จำ: detect new ransomware type → MONITORING ANOMALIES IN SYSTEM BEHAVIOR"),

(1024,"What should an IS manager do FIRST upon notification of a potential security risk with a 3rd party provider?",
["Determine risk treatment options.","Conduct a vulnerability analysis.","Escalate to the third-party provider.","Conduct a risk analysis."],"D",
"จำ: potential 3rd party security risk → FIRST = CONDUCT RISK ANALYSIS"),

(1025,"When should an IS manager contact the information owner after a security incident is reported?",
["After the potential incident has been logged","After the incident has been contained","After the incident has been confirmed","After the incident has been mitigated"],"C",
"จำ: contact information owner → AFTER INCIDENT HAS BEEN CONFIRMED"),

(1026,"After recovery from a cyberattack is announced, what should be done NEXT?",
["Secure and preserve digital evidence for analysis.","Gather feedback on business impact.","Conduct a meeting to capture lessons learned.","Prepare an executive summary for senior management."],"C",
"จำ: after cyberattack recovery announced → NEXT = LESSONS LEARNED meeting"),

(1027,"Which defines the MOST comprehensive set of security requirements for a newly developed IS?",
["Baseline controls","Audit findings","Risk assessment results","Key risk indicators (KRIs)"],"C",
"จำ: comprehensive security requirements for new system → RISK ASSESSMENT RESULTS"),

(1028,"Which IS practice would BEST prevent a SQL injection attack?",
["Adopting agile development","Enhancing the patching program","Training developers on secure coding practices to reduce vulnerabilities","Performing vulnerability testing before each version release"],"C",
"จำ: prevent SQL injection → TRAIN DEVELOPERS ON SECURE CODING"),

(1029,"Which is a viable containment strategy for a DDoS attack?",
["Block IP addresses used by the attacker.","Disable firewall ports exploited by the attacker.","Power off affected servers.","Redirect the attacker's traffic."],"D",
"จำ: DDoS containment → REDIRECT ATTACKER'S TRAFFIC"),

(1030,"A data discovery project uncovers an unclassified process document. Who is BEST suited to determine the classification?",
["Creator of the document","Data custodian","IS manager","Security policy author"],"A",
"จำ: unclassified document classification → CREATOR OF THE DOCUMENT"),

(1031,"Which is MOST important to include in a post-incident report?",
["Forensic analysis results","List of potentially compromised assets","Root cause analysis","SLAs"],"C",
"จำ: post-incident report MOST important → ROOT CAUSE ANALYSIS"),

(1032,"When creating an IR plan, the triggers for the BCP MUST be based on:",
["a threat assessment.","RTOs.","a BIA.","a risk assessment."],"C",
"จำ: BCP triggers in IR plan → MUST based on BIA"),

(1033,"An org's IS strategy should be the PRIMARY input to which of the following?",
["Security governance framework design","Enterprise risk scenario development","Security program metrics","Organizational risk appetite"],"A",
"จำ: IS strategy PRIMARY input to → SECURITY GOVERNANCE FRAMEWORK DESIGN"),

(1034,"Which BEST enables an org to enhance its IR plan processes and procedures?",
["IS audits","Security risk assessments","Lessons learned analysis","KPIs"],"C",
"จำ: enhance IR plan → LESSONS LEARNED ANALYSIS"),

(1035,"Which is BEST used to determine the maturity of an IS program?",
["Organizational risk appetite","Risk assessment results","Security metrics","Security budget allocation"],"C",
"จำ: determine IS program maturity → SECURITY METRICS"),

(1036,"Which should be done FIRST when developing an IS strategy aligned with org goals?",
["Establish a security risk framework with KRIs.","Determine IS's impact on achievement of org goals.","Assess IS risk associated with the org goals.","Select IS projects related to org goals."],"C",
"จำ: IS strategy aligned with org goals FIRST → ASSESS IS RISK associated with org goals"),

(1037,"A BIA BEST enables an org to establish:",
["annualized loss expectancy (ALE).","recovery methods.","restoration priorities.","total cost of ownership (TCO)."],"C",
"จำ: BIA BEST enables → RESTORATION PRIORITIES"),

(1038,"Which is the PRIMARY objective of developing an IS program aligned with IS strategy?",
["To define resources required to achieve IS goals","To define a bottom-up approach for implementing IS policies","To define standards to be implemented","To define risk mitigation plans for security technologies"],"A",
"จำ: IS program aligned with IS strategy PRIMARY objective → DEFINE RESOURCES REQUIRED to achieve IS goals"),

(1039,"Which is MOST important to include in an IS framework?",
["Guidance for designing IS controls","IS organizational structure","Industry benchmarks of IS metrics","IS risk assessment"],"D",
"จำ: IS framework MOST important → IS RISK ASSESSMENT"),

(1040,"An org learns a service provider had a breach last month and did not notify. What should be the IS manager's FIRST action?",
["Terminate the provider contract.","Conduct a BIA.","Inform senior management.","Review the provider contract."],"D",
"จำ: provider breach not notified → FIRST = REVIEW THE PROVIDER CONTRACT"),

(1041,"Which communication approach BEST enables an IS manager to maximize IS program effectiveness?",
["Reporting on industry threats with potential business impact","Conducting periodic one-on-one meetings to align security with business","Participating in operational review meetings to discuss daily operations","Providing regular status of updates to security policies"],"B",
"จำ: maximize IS program effectiveness → PERIODIC ONE-ON-ONE MEETINGS to align security with business"),

(1042,"Which control type should be considered FIRST for aligning employee behavior with IS objectives?",
["Administrative security controls","Access security controls","Technical security controls","Physical security controls"],"A",
"จำ: align employee behavior with IS objectives → ADMINISTRATIVE SECURITY CONTROLS"),

(1043,"IS team presented risk register at steering committee. Which should be of MOST concern?",
["No owners were identified for some risks.","Business apps had the highest number of risks.","Risk mitigation action plans had no timelines.","Risk mitigation milestones were delayed."],"A",
"จำ: risk register MOST concern → NO OWNERS IDENTIFIED for some risks"),

(1044,"Which BEST enables an org to determine activities/changes on a system during a cybersecurity incident?",
["Penetration testing","Root cause analysis","Continuous log monitoring","Computer forensics"],"D",
"จำ: determine activities during cybersecurity incident → COMPUTER FORENSICS"),

(1045,"What should the IS manager do FIRST when a business dept wants to use blockchain for a new payment process?",
["Include new requirements in the SDLC pipeline.","Update business case to include security budget for new process.","Perform a risk assessment to identify emerging risks.","Benchmark blockchain solutions to determine most secure."],"C",
"จำ: new blockchain payment process → FIRST = RISK ASSESSMENT for emerging risks"),

(1046,"Which BEST facilitates development of IS procedures that support IS policy?",
["Aligning procedures with industry best practices","Classifying the information assets to be protected","Considering the impact of systemic risk events","Conducting external benchmarking"],"B",
"จำ: IS procedures support IS policy → CLASSIFYING INFORMATION ASSETS to be protected"),

(1047,"Which provides the BEST input to a business case for a technical solution to address system vulnerabilities?",
["BIA","Vulnerability scan results","Risk assessment","Penetration test results"],"C",
"จำ: business case for technical solution vs vulnerabilities → RISK ASSESSMENT"),

(1048,"Which is MOST helpful for determining priorities when creating a long-term IS roadmap?",
["The org's IS framework","IS steering committee input","Enterprise architecture (EA)","Industry best practices"],"B",
"จำ: long-term IS roadmap priorities → IS STEERING COMMITTEE INPUT"),

(1049,"A KEY consideration in use of quantitative risk analysis is that it:",
["applies commonly used labels to information assets.","assigns numeric values to exposures of information assets.","is based on criticality analysis of information assets.","aligns with best practice for risk analysis."],"B",
"จำ: quantitative risk analysis KEY → ASSIGNS NUMERIC VALUES to exposures"),

(1050,"An org has unpatched IT systems in violation of patching policy. This should be treated as:",
["an increased threat profile.","a vulnerability management failure.","an increased risk profile.","a security control failure."],"D",
"จำ: unpatched systems violating policy = SECURITY CONTROL FAILURE"),
]

# ── Q1051-1100 ────────────────────────────────────────────────────────────────
QUESTIONS += [
(1051,"How does data discovery assist with data classification?",
["It provides assurance of data integrity.","It shows where specific data is stored.","It automatically classifies data by keywords.","It helps to identify the data owner."],"B",
"จำ: data discovery assists classification → SHOWS WHERE SPECIFIC DATA IS STORED"),

(1052,"Which is the MOST effective control to prevent proliferation of shadow IT?",
["Implement a software allow list.","Conduct periodic vulnerability scanning.","Install a solution to detect unlicensed software.","Conduct software audits."],"A",
"จำ: prevent shadow IT → IMPLEMENT SOFTWARE ALLOW LIST"),

(1053,"Which is the MOST important driver when developing an effective IS strategy?",
["Benchmarking reports","IS standards","Business requirements","Security audit reports"],"C",
"จำ: effective IS strategy MOST important driver → BUSINESS REQUIREMENTS"),

(1054,"Which is MOST important for improvement of a BCP?",
["Implementing an IT resilience solution","Implementing management reviews","Documenting critical business processes","Incorporating lessons learned"],"D",
"จำ: BCP improvement MOST important → INCORPORATING LESSONS LEARNED"),

(1055,"Which is MOST important when choosing a shared alternate location for computing facilities?",
["IR team training","The org's risk tolerance","The org's mission","Resource availability"],"D",
"จำ: shared alternate computing location → RESOURCE AVAILABILITY"),

(1056,"A financial institution identified high fraud risk in credit dept. Which IS control will BEST reduce fraud risk?",
["Mandatory time off","Segregation of duties","Acceptable use policy","Periodic risk assessments"],"B",
"จำ: reduce fraud risk → SEGREGATION OF DUTIES"),

(1057,"An employee clicked a malicious link compromising company data. What is the BEST way to mitigate this future risk?",
["Assess and update spam filtering rules.","Establish an acceptable use policy.","Implement disciplinary procedures.","Conduct phishing awareness training."],"D",
"จำ: employee clicked malicious link → PHISHING AWARENESS TRAINING"),

(1058,"The business value of an information asset is derived from:",
["its replacement cost.","its criticality.","the threat profile.","the risk assessment."],"B",
"จำ: business value of information asset → ITS CRITICALITY"),

(1059,"Which is the BEST indicator of the maturity level of a vendor risk management process?",
["Number of vendors rejected due to security review","% of vendors regularly reviewed against defined criteria","% of vendors that have gone through vendor onboarding","Average time to complete vendor risk management process"],"B",
"จำ: vendor risk management maturity → % VENDORS REGULARLY REVIEWED against criteria"),

(1060,"An international org is implementing a corporate security policy for PII. Which should be the IS manager's MAIN concern?",
["Data backup strategy","Organizational reporting structure","Local regulations","Consistency in awareness programs"],"C",
"จำ: international PII policy → MAIN concern = LOCAL REGULATIONS"),

(1061,"Which is the BEST reason for senior management to support a business case for monitoring system for critical app?",
["The system can be replicated for additional use cases.","An industry peer experienced a recent breach with similar app.","The cost of implementing is less than the impact of downtime.","The solution is within the org's risk tolerance."],"C",
"จำ: business case for monitoring system → COST OF IMPLEMENTING < IMPACT OF DOWNTIME"),

(1062,"Which is MOST important when developing an IS governance framework?",
["Ensuring alignment with the org's risk management framework","Integrating security within SDLC","Developing policies and procedures to support the framework","Developing security IR measures"],"A",
"จำ: IS governance framework → ALIGN WITH ORG'S RISK MANAGEMENT FRAMEWORK"),

(1063,"What should be an IS manager's GREATEST concern when HR outsources data processing to a cloud provider?",
["Security posture of the provider","Data loss protection insurance","Required provider service levels","The scope of the data"],"D",
"จำ: HR outsources to cloud → GREATEST concern = SCOPE OF THE DATA"),

(1064,"Which BEST enables org to sustain delivery of products within acceptable time frames during disruption?",
["Business continuity plan (BCP)","Disaster recovery plan (DRP)","Business impact analysis (BIA)","Service level agreement (SLA)"],"A",
"จำ: sustain delivery during disruption → BCP"),

(1065,"Which BEST determines an information asset's classification?",
["Criticality to a business process","Value of information asset in marketplace","Risk assessment from data owner","Cost of producing information asset"],"A",
"จำ: information asset classification → CRITICALITY TO A BUSINESS PROCESS"),

(1066,"Which is the PRIMARY objective of a cyber resilience strategy?",
["Business continuity","Employee awareness","Executive support","Regulatory compliance"],"A",
"จำ: cyber resilience strategy PRIMARY objective → BUSINESS CONTINUITY"),

(1067,"Which is the MOST important reason to communicate to affected parties that a security incident occurred?",
["To improve IS awareness","To disclose root cause of incident","To comply with regulations regarding notification","To increase goodwill toward org"],"C",
"จำ: communicate security incident to affected parties → COMPLY WITH NOTIFICATION REGULATIONS"),

(1068,"Which is the BEST indication that an IS control is no longer relevant?",
["The control is not cost efficient.","The control does not support a specific business function.","IT management does not support the control.","The technology related to the control is obsolete."],"B",
"จำ: IS control no longer relevant → DOES NOT SUPPORT A SPECIFIC BUSINESS FUNCTION"),

(1069,"Which is the PRIMARY advantage of using DRaaS to manage DR program?",
["Offers flexible deployment options using cloud infrastructure.","Allows the org to prioritize its core operations.","Is more secure than traditional data backup architecture.","Allows use of a professional response team at a lower cost."],"B",
"จำ: DRaaS PRIMARY advantage → ALLOWS ORG TO PRIORITIZE CORE OPERATIONS"),

(1070,"Which is the MOST important outcome of a post-incident review?",
["The system affected is restored to prior state.","The root cause of incident is determined.","The person responsible is identified.","Impact reported to senior management."],"B",
"จำ: post-incident review MOST important outcome → ROOT CAUSE DETERMINED"),

(1071,"Which is the BEST indicator of performance of a security program?",
["Changes in ROIs","Changes in maturity level","Changes in budget allocation","Changes in security training attendance"],"B",
"จำ: security program performance BEST indicator → CHANGES IN MATURITY LEVEL"),

(1072,"An org remediated a security flaw in a system. What should be done NEXT?",
["Allocate budget for pen testing.","Update system documentation.","Assess the residual risk.","Share lessons learned with the org."],"C",
"จำ: security flaw remediated → NEXT = ASSESS RESIDUAL RISK"),

(1073,"Which BEST facilitates development of a comprehensive IS policy?",
["Alignment with established IS framework","Security KPIs","A review of recent IS incidents","An established internal audit program"],"A",
"จำ: comprehensive IS policy → ALIGNMENT WITH ESTABLISHED IS FRAMEWORK"),

(1074,"Which is the MOST effective way to demonstrate improvement in security performance?",
["Report results of security control CSA.","Present trends in a validated metrics dashboard.","Provide a summary of security project ROIs.","Present vulnerability testing results."],"B",
"จำ: demonstrate security performance improvement → TRENDS IN VALIDATED METRICS DASHBOARD"),

(1075,"Which is MOST important to consider for org-wide support for an IS program?",
["Corporate risk framework","Corporate culture","Clarity of security roles and responsibilities","Maturity of security policy"],"B",
"จำ: org-wide support for IS program → CORPORATE CULTURE"),

(1076,"Which is the BEST way to ensure the BCP is current?",
["Manage business process changes.","Update BIAs on a regular basis.","Review and update emergency contact lists.","Conduct periodic testing."],"B",
"จำ: ensure BCP is current → UPDATE BIAs REGULARLY"),

(1077,"Which would be MOST useful when determining the BCP strategy for a large org's data center?",
["BIA","Incident root cause analysis","Stakeholder feedback analysis","Business continuity risk analysis"],"A",
"จำ: BCP strategy for data center → BIA"),

(1078,"A risk assessment for network reconfiguration reveals high likelihood of sensitive data being compromised. What is the IS manager's BEST course of action?",
["Seek an independent opinion to confirm findings.","Determine alignment with existing regulations.","Report findings to key stakeholders.","Recommend additional network segmentation."],"C",
"จำ: risk assessment shows high likelihood of compromise → REPORT FINDINGS TO KEY STAKEHOLDERS"),

(1079,"Who should be included in INITIAL discussions regarding a failed security control?",
["Penetration testers","The service provider","Senior management","The process owner"],"D",
"จำ: failed security control initial discussions → THE PROCESS OWNER"),

(1080,"A new CRM system was implemented. Who should be responsible for enforcing authorized access to CRM data?",
["The data custodian","The data owner","Internal IT audit","The IS manager"],"A",
"จำ: enforce access to CRM data → DATA CUSTODIAN (implements owner's decisions)"),

(1081,"What should an IS manager do FIRST upon learning of new ransomware targeting a particular line of business?",
["Ensure backups are stored offsite.","Conduct a DR test and address gaps.","Assess the potential impact to the organization.","Conduct a vulnerability scan and remediate."],"C",
"จำ: new ransomware targeting line of business → FIRST = ASSESS POTENTIAL IMPACT"),

(1082,"Which should be the PRIMARY objective when establishing a new IS program?",
["Facilitating operational security","Optimizing resources","Minimizing organizational risk","Executing the security strategy"],"C",
"จำ: new IS program PRIMARY objective → MINIMIZING ORGANIZATIONAL RISK"),

(1083,"An org implemented controls to mitigate ransomware risk. Which is MOST important to present to senior mgmt?",
["Number and severity of ransomware incidents","Total cost of investment","Benchmarks of industry peers impacted by ransomware","Cost and associated risk reduction"],"D",
"จำ: report ransomware control performance → COST AND ASSOCIATED RISK REDUCTION"),

(1084,"Which is the BEST defense against DDoS attacks?",
["Regular patching","Multiple and redundant paths","Intruder-detection lockout","Well-configured routers and firewalls"],"B",
"จำ: best defense against DDoS → MULTIPLE AND REDUNDANT PATHS"),

(1085,"Which scenario would MOST likely require a change to corporate security policies?",
["New security standards have been implemented.","Employees do not understand or adhere to policies.","The org has undergone a merger.","The org incurs an increased number of security incidents."],"C",
"จำ: require change to security policies → ORG UNDERGONE A MERGER"),

(1086,"During a BCP test, which is the MOST important consideration?",
["The test involves IT members.","The test simulates actual prime-time processing conditions.","The test is scheduled to reduce operational impact.","The test addresses the critical components."],"D",
"จำ: BCP test MOST important → TEST ADDRESSES CRITICAL COMPONENTS"),

(1087,"When testing IR plan for ransomware recovery, which is MOST important to verify?",
["An alternative network link is immediately available.","Data backups are recoverable from an offsite location.","Network access requires two-factor authentication.","Digital currency is immediately available."],"B",
"จำ: test IR plan for ransomware → DATA BACKUPS RECOVERABLE from offsite"),

(1088,"Which is the GREATEST benefit of incorporating IS governance into corporate governance?",
["Management accountability for IS","Improved process resiliency in event of attacks","Promotion of security-by-design to business","Heightened awareness of IS strategies"],"A",
"จำ: IS governance in corporate governance GREATEST benefit → MANAGEMENT ACCOUNTABILITY for IS"),

(1089,"What should an IS manager do FIRST when a vulnerability has been disclosed?",
["Perform a patch update.","Conduct a risk assessment.","Conduct an impact assessment.","Perform a penetration test."],"B",
"จำ: vulnerability disclosed → FIRST = CONDUCT RISK ASSESSMENT"),

(1090,"When org experiences a disruptive event, the BCP should be triggered PRIMARILY based on:",
["expected duration of outage.","the root cause of the event.","type of security incident.","management direction."],"A",
"จำ: BCP trigger → PRIMARILY based on EXPECTED DURATION OF OUTAGE"),

(1091,"Which control would BEST help detect a targeted attack exploiting a zero-day vulnerability?",
["Intrusion prevention system (IPS)","Vulnerability scanning","Endpoint detection and response (EDR)","Extended detection and response (XDR)"],"D",
"จำ: detect zero-day targeted attack → EXTENDED DETECTION AND RESPONSE (XDR)"),

(1092,"Which is the MOST relevant control to address the integrity of information?",
["Implementation of a redundant server system","Encryption of email","Implementation of an Internet security app","Assignment of appropriate access permissions"],"D",
"จำ: information integrity → ASSIGNMENT OF APPROPRIATE ACCESS PERMISSIONS"),

(1093,"What should be the PRIMARY objective of an information classification scheme?",
["To define data retention requirements","To develop an asset inventory","To meet legislative and regulatory requirements","To implement controls proportionate to risk"],"D",
"จำ: information classification scheme PRIMARY objective → CONTROLS PROPORTIONATE TO RISK"),

(1094,"Which is MOST important when prioritizing threats during risk assessment?",
["Regulatory requirements on the org","The severity of exploited vulnerabilities","The threat landscape within the industry","The potential impact on operations"],"D",
"จำ: prioritize threats in risk assessment → POTENTIAL IMPACT ON OPERATIONS"),

(1095,"Which would BEST fulfill a board's request for concise overview of IS risk facing the business?",
["BIA","Balanced scorecard","Risk heat map","Risk scenario summary"],"C",
"จำ: board concise IS risk overview → RISK HEAT MAP"),

(1096,"Which is the PRIMARY purpose of a BIA?",
["To define security roles and responsibilities","To determine the criticality of information assets","To establish incident severity levels","To determine ROI"],"B",
"จำ: BIA PRIMARY purpose → DETERMINE CRITICALITY OF INFORMATION ASSETS"),

(1097,"An org wants to integrate IS into HR management processes. What should be the FIRST step?",
["Calculate the ROI.","Provide security awareness training to HR.","Assess the business objectives of the processes.","Benchmark processes with best practice to identify gaps."],"C",
"จำ: integrate IS into HR → FIRST = ASSESS BUSINESS OBJECTIVES of processes"),

(1098,"Following a breach where risk isolated and forensics done, what should be done NEXT?",
["Place the web server in quarantine.","Rebuild server from last verified backup.","Shut down server in organized manner.","Rebuild server with relevant patches from original media."],"D",
"จำ: after breach forensics → NEXT = REBUILD FROM ORIGINAL MEDIA with patches"),

(1099,"Which is MOST important for effective cybersecurity incident management?",
["Early detection and response","Regular tabletop exercises","Root cause analysis","Investigation and forensics"],"A",
"จำ: effective cybersecurity incident management → EARLY DETECTION AND RESPONSE"),

(1100,"An org's security standard has a major revision; old version no longer valid for certification. What should be the FIRST action?",
["Modify policies to ensure new requirements are covered.","Review the new standard for applicability to the business.","Evaluate the cost of maintaining the certification.","Communicate the new standard to senior leadership."],"B",
"จำ: security standard major revision → FIRST = REVIEW NEW STANDARD FOR APPLICABILITY"),
]

# ── Q1101-1150 ────────────────────────────────────────────────────────────────
QUESTIONS += [
(1101,"Which is the MOST appropriate metric to demonstrate effectiveness of IS controls to senior management?",
["Number of security vulnerabilities uncovered with network scans","Percentage of servers patched","Downtime due to malware infections","Annualized loss resulting from security incidents"],"D",
"จำ: demonstrate IS controls effectiveness to senior → ANNUALIZED LOSS from security incidents"),

(1102,"Which BEST indicates an org has integrated IS governance with corporate governance?",
["Impact is measured according to business loss when assessing IT risk.","Service levels for security vendors are defined according to business needs.","Security policies are reviewed whenever business objectives change.","Security performance metrics are measured against business objectives."],"D",
"จำ: IS + corporate governance integrated → SECURITY METRICS measured against BUSINESS OBJECTIVES"),

(1103,"The MOST effective way to present IS risk to senior management is to highlight:",
["business impact.","countermeasures.","threat intelligence.","risk mitigation over time."],"A",
"จำ: present IS risk to senior mgmt → BUSINESS IMPACT"),

(1104,"Within CIA triad, which activity BEST supports confidentiality?",
["Ensuring encryption for data in transit","Enforcing SLAs","Utilizing a formal change management process","Ensuring hashing of administrator credentials"],"A",
"จำ: CIA confidentiality → ENCRYPTION FOR DATA IN TRANSIT"),

(1105,"Which should be the PRIMARY objective for creating a culture of security within an org?",
["To obtain resources for IS initiatives","To reduce risk to acceptable levels","To prioritize security within the org","To demonstrate control effectiveness to senior mgmt"],"B",
"จำ: culture of security PRIMARY objective → REDUCE RISK TO ACCEPTABLE LEVELS"),

(1106,"Which should be updated FIRST when aligning IR plan with corporate strategy?",
["Security procedures","Disaster recovery plan (DRP)","Incident notification plan","Risk response scenarios"],"D",
"จำ: align IR plan with corporate strategy → FIRST = UPDATE RISK RESPONSE SCENARIOS"),

(1107,"Which is the MOST effective way to ensure security of services from 3rd party vendors?",
["Review 3rd party contracts as part of vendor management.","Perform an audit on vendors' security controls.","Integrate risk management into vendor management process.","Conduct security reviews on services and solutions."],"C",
"จำ: ensure 3rd party vendor security → INTEGRATE RISK MANAGEMENT into vendor management"),

(1108,"Which eradication method is MOST appropriate when responding to malware on an app server?",
["Disconnect the system from the network.","Change passwords on the compromised system.","Restore the system from a known good backup.","Perform OS hardening."],"C",
"จำ: eradicate malware on app server → RESTORE FROM KNOWN GOOD BACKUP"),

(1109,"Which is MOST important for guiding development and management of a comprehensive IS program?",
["Adopting IS program management best practices","Aligning org's business objectives with IT objectives","Establishing and maintaining an IS governance framework","Implementing policies and procedures to address IS strategy"],"C",
"จำ: guide comprehensive IS program → ESTABLISHING IS GOVERNANCE FRAMEWORK"),

(1110,"Which is the BEST way to ensure data is not co-mingled or exposed when using a cloud provider?",
["Require provider to follow stringent data classification procedures.","Obtain an independent audit report.","Review the provider's IS policies.","Include high penalties for security breaches in contract."],"B",
"จำ: data not co-mingled with cloud → OBTAIN INDEPENDENT AUDIT REPORT"),

(1111,"Before approving a new security solution, senior mgmt requires a business case. Which BEST supports justification?",
["The solution contributes to business strategy.","The solution improves business risk tolerance levels.","The solution reduces the cost of noncompliance.","The solution improves business resiliency."],"A",
"จำ: business case for security solution → CONTRIBUTES TO BUSINESS STRATEGY"),

(1112,"When implementing IS governance, it is MOST important for exec leadership to have direct role in:",
["reviewing the IS policy directing the organization.","developing technical KRIs for IS.","implementing IS metrics for the org.","approving IS standards and procedures."],"A",
"จำ: exec leadership direct role in IS governance → REVIEWING IS POLICY"),

(1113,"Which should have the MOST influence on org's response to a new industry regulation?",
["The org's risk control baselines","The org's control objectives","The org's risk management framework","The org's risk appetite"],"D",
"จำ: response to new regulation → ORG'S RISK APPETITE"),

(1114,"Biometrics are BEST used for:",
["authorization.","authentication.","auditing.","accounting."],"B",
"จำ: biometrics BEST used for → AUTHENTICATION"),

(1115,"Predetermined containment methods in cybersecurity IR should be based PRIMARILY on the:",
["capability of incident handlers.","type of confirmed incident.","predicted incident duration.","number of impacted users."],"B",
"จำ: containment methods based on → TYPE OF CONFIRMED INCIDENT"),

(1116,"Communicating which would be MOST helpful to gain senior mgmt support for risk treatment?",
["Threat analysis","Root cause analysis","Quantitative loss","Industry benchmarks"],"C",
"จำ: senior mgmt support for risk treatment → QUANTITATIVE LOSS"),

(1117,"Which is the PRIMARY objective of information asset classification?",
["Threat minimization","Vulnerability reduction","Risk management","Compliance management"],"C",
"จำ: information asset classification PRIMARY objective → RISK MANAGEMENT"),

(1118,"Which IDS trend would be of GREATEST concern when reviewing performance?",
["Increase in false negatives","Increase in false positives","Decrease in false positives","Decrease in false negatives"],"A",
"จำ: IDS GREATEST concern → INCREASE IN FALSE NEGATIVES (missing real attacks)"),

(1119,"Management wants to compare IaaS risk vs hosting internally. Which provides BEST method?",
["Reviewing mitigating and compensating controls for each risk scenario","Mapping risk scenarios by likelihood and impact on a chart","Performing a risk assessment on the IaaS provider","Mapping risk scenarios by sensitivity of data"],"B",
"จำ: compare IaaS risk vs internal → MAP by LIKELIHOOD AND IMPACT on a chart"),

(1120,"Which is the PRIMARY reason to regularly update BCP and DRP documents?",
["To ensure audit and compliance requirements are met","To enforce security policy requirements","To maintain business asset inventories","To ensure the availability of business operations"],"D",
"จำ: update BCP/DRP regularly → ENSURE AVAILABILITY OF BUSINESS OPERATIONS"),

(1121,"Which will have the GREATEST impact on development of information classification scheme?",
["Value of the information","Data format","Owners of the information","Organizational structure"],"A",
"จำ: information classification scheme GREATEST impact → VALUE OF THE INFORMATION"),

(1122,"To prepare for 3rd party forensics investigation after malware incident, IR team should:",
["clean the malware.","isolate the infected systems.","image the infected systems.","preserve the evidence."],"D",
"จำ: prepare for 3rd party forensics → PRESERVE THE EVIDENCE"),

(1123,"Who should own the risk associated with unauthorized access to application data?",
["Data custodian","Application developer","Application owner","Access administrator"],"C",
"จำ: own risk of unauthorized access to app data → APPLICATION OWNER"),

(1124,"The categorization of incidents is MOST important for evaluating which of the following?",
["Appropriate communication channels","Risk severity and incident priority","Allocation of needed resources","Response and containment requirements"],"B",
"จำ: incident categorization MOST important for → RISK SEVERITY AND INCIDENT PRIORITY"),

(1125,"An org learns a 3rd party outsourced critical functions to another external provider. What is MOST important?",
["Engage independent audit of the 3rd party's external provider.","Conduct external audit of contracted 3rd party.","Recommend canceling contract with 3rd party.","Evaluate the 3rd party's agreements with its external provider."],"D",
"จำ: 3rd party outsourced to another provider → EVALUATE 3RD PARTY'S AGREEMENTS with provider"),

(1126,"An org acquired a new system with strict maintenance instructions and schedules. Where should this be documented?",
["Standards","Procedures","Guidelines","Policies"],"B",
"จำ: maintenance instructions and schedules → PROCEDURES"),

(1127,"The PRIMARY benefit of using HTTPS is that it provides:",
["confidentiality of data transmitted.","integrity for data at rest.","authentication.","better session traceability."],"A",
"จำ: HTTPS PRIMARY benefit → CONFIDENTIALITY OF DATA TRANSMITTED"),

(1128,"Remote employees have notebooks, cable locks, smartphones, and VPN. What is MOST important for IS manager to ensure?",
["Employees are trained on the acceptable use policy.","Employees use smartphone tethering when accessing remotely.","Employees use VPN when accessing org's online resources.","Employees physically lock PCs when leaving immediate area."],"A",
"จำ: remote employees → MOST important = TRAINED ON ACCEPTABLE USE POLICY"),

(1129,"To improve org's IS culture, it is MOST important for senior management to:",
["participate in security training.","review security budget and resources.","demonstrate good security practices.","approve security policies."],"C",
"จำ: improve IS culture → senior mgmt DEMONSTRATE GOOD SECURITY PRACTICES"),

(1130,"Which BEST illustrates residual risk within an organization?",
["Balanced scorecard","Risk management framework","BIA","Heat map"],"D",
"จำ: illustrate residual risk → HEAT MAP"),

(1131,"Which is the MOST effective way to determine alignment of IS program with business strategy?",
["Evaluate results of BCP testing.","Evaluate business impact of incidents.","Review KPIs.","Engage business process owners."],"D",
"จำ: IS program alignment with business strategy → ENGAGE BUSINESS PROCESS OWNERS"),

(1132,"An org experienced loss of revenue during a disaster. Which would BEST prepare for recovery?",
["BIA","IR plan","DRP","BCP"],"D",
"จำ: prepare for recovery from disaster (revenue loss) → BCP"),

(1133,"Which is the MOST important success factor when developing an IS strategy?",
["The strategy delivery is adequately funded.","The strategy is aligned with industry-recognized security control framework.","The strategy is based on proven technologies.","The strategy is approved by board and executive management."],"D",
"จำ: IS strategy success factor → APPROVED BY BOARD AND EXECUTIVE MANAGEMENT"),

(1134,"Which BEST demonstrates a security-conscious organizational culture?",
["Security incidents reported directly to senior management.","Security awareness metrics established and tracked.","Phishing simulations are part of IS training.","Employees identify potential incidents and report them."],"D",
"จำ: security-conscious culture → EMPLOYEES IDENTIFY AND REPORT potential incidents"),

(1135,"Which is the MOST effective data loss control when connecting personal mobile to corporate email?",
["Email stored in encrypted format on the mobile device.","Users must agree to biometric MFA.","Senior manager must approve each new connection.","Email sync prevented when connected to public Wi-Fi."],"A",
"จำ: personal mobile + corporate email → EMAIL STORED ENCRYPTED on device"),

(1136,"Which should be the FIRST step when performing triage of a malware incident?",
["Preserving the forensic image","Containing the affected system","Comparing backup against production","Removing the malware"],"B",
"จำ: malware incident triage FIRST → CONTAINING THE AFFECTED SYSTEM"),

(1137,"Which BEST helps enable the desired IS culture within an org?",
["IS awareness training and campaigns","Incentives for appropriate IS-related behavior","Effective IS policies and procedures","Delegation of IS roles and responsibilities"],"A",
"จำ: enable IS culture → IS AWARENESS TRAINING AND CAMPAIGNS"),

(1138,"What should be the GREATEST concern when annual audit reveals BCP not reviewed in more than a year?",
["Org may suffer reputational damage for not following best practices.","Audit finding may impact overall risk rating.","Outdated BCP may result in less efficient recovery.","Lack of updates may result in noncompliance with internal policies."],"C",
"จำ: BCP not updated in over a year → GREATEST concern = LESS EFFICIENT RECOVERY"),

(1139,"Which is the MOST important goal of an IS program?",
["Optimizing resources","Reducing risk factors","Managing controls","Enhancing business decision making"],"B",
"จำ: IS program MOST important goal → REDUCING RISK FACTORS"),

(1140,"Which BEST helps ensure effective execution of an org's DRP?",
["The plan is based on industry best practices.","The plan is reviewed by senior and IT operational management.","Procedures are available at primary and failover location.","Process steps are documented by the DR team."],"C",
"จำ: effective DRP execution → PROCEDURES AVAILABLE AT PRIMARY AND FAILOVER LOCATION"),

(1141,"Which would be MOST effective in reducing impact of a DDoS attack?",
["Impose state limits on servers.","Spread a site across multiple ISPs.","Harden network security.","Block the attack at the source."],"B",
"จำ: reduce DDoS impact → SPREAD SITE ACROSS MULTIPLE ISPs"),

(1142,"The PRIMARY reason for senior management to monitor IS metrics is to ensure:",
["alignment of IS budget to corporate funding.","alignment of IS with corporate governance.","alignment of security and IT objectives.","alignment with risk mitigation efforts."],"B",
"จำ: senior mgmt monitor IS metrics → ALIGN IS WITH CORPORATE GOVERNANCE"),

(1143,"Which is the MOST important reason to perform a privacy impact assessment?",
["To provide assurance to senior management","To ensure business data processing assessed for risk","To ensure compensating controls are in place","To reduce threats associated with data processing"],"B",
"จำ: perform PIA → ENSURE BUSINESS DATA PROCESSING ASSESSED FOR RISK"),

(1144,"When reporting IS risk to senior management, it is MOST important to include:",
["control risk.","inherent risk.","detection risk.","residual risk."],"D",
"จำ: report IS risk to senior → RESIDUAL RISK"),

(1145,"Which is MOST likely to improve an org's security culture?",
["Involving stakeholders in security planning","Enforcing penalties for security incidents","Communicating security incidents within the industry","Incentivizing managers based on security metrics"],"A",
"จำ: improve security culture → INVOLVING STAKEHOLDERS in security planning"),

(1146,"Which is MOST important to complete during recovery phase before bringing affected systems back online?",
["Test and verify that compromised systems are clean.","Document recovery steps for senior management.","Record and close security incident tickets.","Capture and preserve forensic images."],"A",
"จำ: recovery phase before bringing back online → VERIFY SYSTEMS ARE CLEAN"),

(1147,"Which is the BEST way to improve risk management in org that manages risk at departmental level?",
["Deploy security risk management software in all departments.","Determine whether org has defined risk tolerance and appetite.","Subscribe to external risk reports relevant to each dept.","Propose that security risk be integrated under a common risk register."],"D",
"จำ: improve departmental risk management → INTEGRATE UNDER COMMON RISK REGISTER"),

(1148,"Which is MOST helpful when determining service level requirements for an outsourced app?",
["Supplier BCP","IS policy","Application capabilities","Data classification"],"D",
"จำ: service level requirements for outsourced app → DATA CLASSIFICATION"),

(1149,"Which is MOST important when planning eradication of a cyberattack?",
["Skills and competencies of the eradication team","Cost of tools and efforts required","Obtain a clean backup of the OS","Knowledge about the type and source of the threat"],"D",
"จำ: plan eradication of cyberattack → KNOWLEDGE ABOUT TYPE AND SOURCE OF THREAT"),

(1150,"Which BEST enables an IS manager to identify changes in threat landscape due to emerging technologies?",
["Input from external experts","Annual security assessments","Periodic risk assessments","Benchmarking against industry peers"],"A",
"จำ: identify threat landscape changes from emerging tech → INPUT FROM EXTERNAL EXPERTS"),
]

# ── Q1151-1200 ────────────────────────────────────────────────────────────────
QUESTIONS += [
(1151,"An enterprise decided to procure security services from a 3rd party vendor. Which is MOST important to include in vendor selection criteria?",
["The maturity of the vendor's internal control environment","Feedback from the vendor's previous clients","Alignment of the vendor's business objectives with enterprise security goals","Pen testing against the vendor's network"],"C",
"จำ: vendor selection for security services → ALIGNMENT OF VENDOR'S BUSINESS OBJECTIVES with enterprise security goals"),

(1152,"The resilience requirements of an application are BEST determined by:",
["a cost-benefit analysis.","a threat assessment.","a BIA.","a risk assessment."],"C",
"จำ: application resilience requirements → BIA"),

(1153,"Which BEST facilitates recovery of data lost as a result of a cybersecurity incident?",
["DRP","Offsite data backups","Encrypted data drives","Removable storage media"],"B",
"จำ: recover lost data from cybersecurity incident → OFFSITE DATA BACKUPS"),

(1154,"Which is MOST important to successful implementation of a new IS program?",
["Evaluating current IS processes","Gaining commitment from senior management","Conducting regular external benchmarking","Monitoring KPIs"],"B",
"จำ: new IS program success → SENIOR MANAGEMENT COMMITMENT"),

(1155,"IS team confirmed threat actors are exploiting a newly announced critical vulnerability. What should be done FIRST?",
["Notify senior management.","Prevent access to the application.","Invoke the IR plan.","Install additional application controls."],"C",
"จำ: threat actors exploiting critical vuln → FIRST = INVOKE THE IR PLAN"),

(1156,"Which is the MOST important consideration when evaluating performance of existing security controls?",
["Interviewing control owners to collect metrics data","Establishing testing scenarios based on international standards","Selecting testing methods that match the purpose of testing","Obtaining senior management support to facilitate testing"],"C",
"จำ: evaluate security control performance → TESTING METHODS MATCH THE PURPOSE"),

(1157,"Which metric BEST demonstrates effectiveness of org's security awareness program?",
["% employee computers infected with malware","% employees who regularly attend security training","Number of security incidents reported to help desk","Number of phishing emails viewed by end users"],"C",
"จำ: security awareness program effectiveness → # SECURITY INCIDENTS REPORTED TO HELP DESK"),

(1158,"Who should decide whether a specific control should be changed once risk is approved for mitigation?",
["Risk owner","Data owner","Control owner","Process owner"],"A",
"จำ: decide on control change after risk approved → RISK OWNER"),

(1159,"When determining KRIs for an IS program it is MOST important to select:",
["KRIs that track both short-term and long-term performance.","KRIs that align with business processes.","KRIs that are quantifiable.","as many KRIs as possible."],"B",
"จำ: determining KRIs for IS program → KRIs ALIGNED WITH BUSINESS PROCESSES"),

(1160,"Senior management requested a budget cut for IS program. What should be the IS manager's FIRST action?",
["Analyze the impact to the IS program.","Advise business unit heads of potential changes.","Evaluate cost savings within existing implementations.","Re-prioritize IS implementation and operations."],"A",
"จำ: IS budget cut requested → FIRST = ANALYZE IMPACT TO IS PROGRAM"),

(1161,"What is MOST important when establishing metrics for reporting to IS strategy committee?",
["Benchmarking expected value against industry standards","Aligning metrics with organizational culture","Agreeing on baseline values for metrics","Developing a dashboard for communicating metrics"],"B",
"จำ: metrics for IS strategy committee → ALIGN WITH ORGANIZATIONAL CULTURE"),

(1162,"Which presents the GREATEST challenge when assessing impact of emerging risk?",
["Outdated risk management strategy","Insufficient data related to the emerging risk","Complexity of the emerging risk","Lack of resources to perform risk assessments"],"B",
"จำ: assess emerging risk GREATEST challenge → INSUFFICIENT DATA about emerging risk"),

(1163,"To effectively manage org's IS risk, it is MOST important to:",
["establish and communicate risk tolerance.","benchmark risk scenarios against peer orgs.","assign risk management to an experienced consultant.","periodically identify and correct new system vulnerabilities."],"A",
"จำ: manage IS risk effectively → ESTABLISH AND COMMUNICATE RISK TOLERANCE"),

(1164,"Which is the MOST useful input for an IS manager when updating org's security policy?",
["Security team capabilities","Risk appetite","Vulnerability scan","Industry best practices"],"B",
"จำ: update security policy MOST useful input → RISK APPETITE"),

(1165,"The MOST effective way for IS manager to secure senior mgmt support for IS strategy is by:",
["presenting industry-specific IS best practices.","determining cost effective IS controls.","educating management on IS program needs.","developing reports showing current threats."],"C",
"จำ: secure senior mgmt support for IS strategy → EDUCATE MANAGEMENT ON IS PROGRAM NEEDS"),

(1166,"When engaging external party to perform pen test, it is MOST important to:",
["provide an updated asset inventory.","notify employees of the testing.","define the project scope.","provide network documentation."],"C",
"จำ: external pen test → MOST important = DEFINE PROJECT SCOPE"),

(1167,"Which is the MOST effective way to convey IS responsibilities across an org?",
["Implementing security awareness programs","Defining IS responsibilities in security policy","Developing a skills matrix","Documenting IS responsibilities within job descriptions"],"D",
"จำ: convey IS responsibilities across org → IS RESPONSIBILITIES IN JOB DESCRIPTIONS"),

(1168,"A financial institution is expanding to international jurisdictions. Which should be of GREATEST concern for protecting customer info?",
["Ability to monitor and enforce controls in multiple jurisdictions","Global payment card industry regulations","Privacy laws and regulations for each country","IS resources available in each country"],"C",
"จำ: expand internationally + protect customer info → PRIVACY LAWS AND REGULATIONS per country"),

(1169,"When evaluating cloud storage solutions, the FIRST consideration should be:",
["how sensitive data will be transferred.","SLA for encryption keys.","volume of data to be stored.","alignment with org's data classification policy."],"D",
"จำ: cloud storage FIRST consideration → ALIGNMENT WITH DATA CLASSIFICATION POLICY"),

(1170,"Which is the GREATEST benefit from introduction of data security standards for payment cards?",
["Helps achieve holistic protection of information assets in the industry.","Deters hackers from committing crimes related to card payments.","Enables wider range of more sophisticated payment methods.","Optimizes budget allocation for cybersecurity."],"A",
"จำ: payment card data security standards GREATEST benefit → HOLISTIC PROTECTION of information assets"),

(1171,"Which should an IS manager establish FIRST to ensure security-related activities are adequately monitored?",
["Regular reviews of system logs","Accountability for security functions","Procedures for security assessments","Schedules for internal audits"],"B",
"จำ: ensure security activities monitored → FIRST = ACCOUNTABILITY FOR SECURITY FUNCTIONS"),

(1172,"Which is the BEST approach for data owners to use when defining access privileges for users?",
["Implement an IAM tool.","Adopt user account settings recommended by vendor.","Perform a risk assessment of users' access privileges.","Define access privileges based on user roles."],"D",
"จำ: define user access privileges → BASED ON USER ROLES"),

(1173,"Which is the BEST control to protect customer personal info stored in the cloud?",
["Strong encryption methods","Appropriate data anonymization","Strong physical access controls","Timely deletion of digital records"],"A",
"จำ: protect customer personal info in cloud → STRONG ENCRYPTION METHODS"),

(1174,"Which is MOST important to include in an enterprise IS policy?",
["Acceptable use","Security objectives","Security metrics","Audit trail review requirements"],"B",
"จำ: enterprise IS policy MOST important → SECURITY OBJECTIVES"),

(1175,"IS manager wants to upgrade workstations to new OS. What would BEST help gain senior mgmt support?",
["Results of user surveys about issues with current OS","List of latest security features in new OS","Summary of performance improvements in new OS","Assessment of current OS based on risk"],"D",
"จำ: gain support for OS upgrade → RISK-BASED ASSESSMENT of current OS"),

(1176,"Which is MOST important to define when creating IS management metrics?",
["Budget","Objectives","Policy","Benchmarks"],"B",
"จำ: creating IS metrics MOST important to define → OBJECTIVES"),

(1177,"A PRIMARY benefit of adopting an IS framework is that it provides:",
["standardized security controls.","common exploitability indices.","credible emerging threat intelligence.","security and vulnerability reporting guidelines."],"A",
"จำ: IS framework PRIMARY benefit → STANDARDIZED SECURITY CONTROLS"),

(1178,"It is MOST important that risk owners understand they are accountable for:",
["collaborating with stakeholders to evaluate control effectiveness.","reporting risk metrics and control compliance to IS manager.","escalating control deficiencies to steering committee.","overseeing and monitoring the effectiveness of controls associated with the risk."],"D",
"จำ: risk owner accountability → OVERSEEING AND MONITORING CONTROL EFFECTIVENESS"),

(1179,"Which is MOST important to include in security incident escalation procedures?",
["Recovery procedures","Containment procedures","Key objectives of security program","Notification criteria"],"D",
"จำ: security incident escalation procedures → NOTIFICATION CRITERIA"),

(1180,"An org implemented a new email filter to mitigate email risk. Who is BEST suited to be the control owner?",
["Head of IT department","Head of compliance","Head of corporate communications","Head of IS"],"D",
"จำ: email filter control owner → HEAD OF INFORMATION SECURITY"),

(1181,"When introducing a new information asset, what is the MOST important responsibility of the asset owner?",
["Information backup","Information access administration","Information disposal","Information classification"],"D",
"จำ: new information asset → asset owner MOST important = INFORMATION CLASSIFICATION"),

(1182,"When establishing an IS governance framework, it is MOST important for an IS manager to understand:",
["IS best practices.","the corporate culture.","risk management techniques.","the threat environment."],"B",
"จำ: establish IS governance framework → MOST important to understand = CORPORATE CULTURE"),

(1183,"When updating IS policy to accommodate a new regulation, the IS manager should FIRST:",
["review KRIs.","consult process owners.","update KPIs.","perform a gap analysis."],"D",
"จำ: update IS policy for new regulation → FIRST = PERFORM GAP ANALYSIS"),

(1184,"Which is the BEST way to align security and business strategies?",
["Establish KPIs for the business.","Integrate IS governance into corporate governance.","Ensure IS program conforms to industry standards.","Include security risk in ongoing metrics reporting."],"B",
"จำ: align security and business strategies → INTEGRATE IS GOVERNANCE INTO CORPORATE GOVERNANCE"),

(1185,"What should an IS manager do FIRST when developing a security framework?",
["Document security procedures","Conduct an asset inventory","Update the security policy","Perform a gap analysis"],"B",
"จำ: developing security framework FIRST → CONDUCT ASSET INVENTORY"),

(1186,"A SaaS app supports critical business process. What is MOST important to include in SLA for timely incident response?",
["Vendor declarations and warranties","Enhanced monitoring of in-scope systems","Defined incident response roles and responsibilities","Established IR procedures"],"C",
"จำ: SaaS critical app SLA for timely IR → DEFINED IR ROLES AND RESPONSIBILITIES"),

(1187,"Who is BEST positioned to perform a BIA?",
["The IS team","Process owners","The IT team","Business continuity management auditors"],"B",
"จำ: perform BIA → PROCESS OWNERS"),

(1188,"Which is the BEST indication of an effective DR planning process?",
["RTOs are shorter than RPOs","Hot sites are required for any declared disaster","Post-incident reviews are conducted after each event","Chain of custody maintained throughout DR"],"C",
"จำ: effective DR planning → POST-INCIDENT REVIEWS after each event"),

(1189,"Which provides the BEST input to determine level of protection needed for an IT system?",
["Vulnerability assessment","Asset classification","Threat analysis","Internal audit findings"],"B",
"จำ: level of protection for IT system → ASSET CLASSIFICATION"),

(1190,"Which should be the FIRST consideration for an IS manager after a security incident is confirmed?",
["Developing incident reporting criteria","Executing containment procedures","Restoring business operations","Determining the root cause"],"B",
"จำ: security incident confirmed → FIRST = EXECUTING CONTAINMENT PROCEDURES"),

(1191,"Which action will BEST resolve root cause of cyber incident involving unauthorized network access via critical web server vuln?",
["Improving the patching process","Locking accounts with unauthorized access","Isolating affected systems","Terminating malicious network connections"],"A",
"จำ: root cause = critical vuln → resolve by IMPROVING THE PATCHING PROCESS"),

(1192,"Following an unsuccessful DoS attack, identified weaknesses should be:",
["noted and re-examined later if similar weaknesses are found","tracked and reported on until their final resolution","quickly resolved regardless of cost","documented in security awareness programs"],"B",
"จำ: DoS attack weaknesses identified → TRACKED AND REPORTED until final resolution"),

(1193,"Which is an IS manager's MOST important action during 3rd party provider selection?",
["Determining if the 3rd party is sufficiently staffed","Performing a network pen test","Analyzing the 3rd party's existing control environment","Consulting with the 3rd party's clients"],"C",
"จำ: 3rd party selection → ANALYZE EXISTING CONTROL ENVIRONMENT"),

(1194,"Which risk assessment finding for online-only business should be given HIGHEST priority for availability?",
["Back office payment system has slowed.","Web server vulnerable to DDoS attacks.","Email auth via SSO has history of failure.","Visitor WiFi access point has unpatched vulns."],"B",
"จำ: online business availability HIGHEST priority → WEB SERVER VULNERABLE TO DDoS"),

(1195,"At which stage of BCP planning is risk identification performed?",
["Impact analysis","Stakeholder meeting","Development","Project planning"],"D",
"จำ: BCP risk identification stage → PROJECT PLANNING"),

(1196,"IS team plans stronger auth for customer site but concerns about UX. What is IS manager's BEST course of action?",
["Refer to industry best practices.","Quantify the security risk to the business.","Provide security awareness training to customers.","Assess business impact against security risk."],"D",
"จำ: stronger auth vs UX concern → ASSESS BUSINESS IMPACT against security risk"),

(1197,"Which is the PRIMARY reason for executive management to be involved in establishing security management framework?",
["To determine the desired state of enterprise security","To satisfy auditors' recommendations","To ensure industry best practices are followed","To establish the minimum level of controls needed"],"A",
"จำ: exec mgmt in security framework → DETERMINE DESIRED STATE of enterprise security"),

(1198,"Which is MOST important for IS manager to consider when determining whether data should be stored?",
["Type and nature of data","Business requirements","Data storage limitations","Data protection regulations"],"B",
"จำ: determine whether to store data → BUSINESS REQUIREMENTS"),

(1199,"Strong password policy requires reset every 30 days; help desk flooded with resets. What is IS manager's BEST action?",
["Conduct a BIA","Provide end-user training","Escalate to senior management","Continue to enforce the policy"],"B",
"จำ: password policy → help desk flooded = PROVIDE END-USER TRAINING"),

(1200,"Which is the MOST important objective when planning an IR program?",
["Minimizing business impact","Managing resources","Recovering from a disaster","Ensuring IT resiliency"],"A",
"จำ: IR program MOST important objective → MINIMIZING BUSINESS IMPACT"),
]

# ── Q1201-1250 ────────────────────────────────────────────────────────────────
QUESTIONS += [
(1201,"Which is MOST important when selecting a 3rd party IDS vendor?",
["The vendor's proposal aligns with objectives of the org","The vendor's proposal allows for contract modification during tech refresh","The vendor's proposal requires provider to have a BCP","The vendor's proposal allows for escrow if 3rd party goes out of business"],"A",
"จำ: select IDS vendor → ALIGNS WITH OBJECTIVES OF THE ORG"),

(1202,"A financial institution is developing a new mobile app. Which is the BEST time to begin security compliance assessments?",
["During user acceptance testing (UAT)","During regulatory review","During the design phase","During static code analysis"],"C",
"จำ: security compliance for new mobile app → DURING THE DESIGN PHASE"),

(1203,"When considering a new security initiative, which should be done PRIOR to developing a business case?",
["Conduct a risk assessment","Conduct a benchmarking exercise","Perform a cost-benefit analysis","Identify resource requirements"],"A",
"จำ: before business case for security initiative → CONDUCT RISK ASSESSMENT"),

(1204,"Which BEST demonstrates potential for successful BC in event of a disaster?",
["Tabletop exercises","Awareness training assessments","Disaster recovery tests","Checklist reviews"],"C",
"จำ: demonstrate successful BC potential → DISASTER RECOVERY TESTS"),

(1205,"Which is an essential practice for workstations used in forensic investigations?",
["Documented chain of custody log kept for workstations","Workstations only accessed by members of forensics team","Only forensics-related software installed on workstations","Workstations backed up and hardened regularly"],"B",
"จำ: forensic investigation workstations → ONLY ACCESSED BY FORENSICS TEAM"),

(1206,"Which component of risk assessment should be reviewed FIRST to understand scope of emerging risk?",
["Risk categorization","Asset identification","Control evaluation","Risk treatment"],"B",
"จำ: understand scope of emerging risk → FIRST = ASSET IDENTIFICATION"),

(1207,"IS manager tasked to implement solution providing insight into potential security incidents. Which BEST supports this?",
["IDS","SIEM","DLP","User behavior analytics"],"B",
"จำ: insight into potential security incidents → SIEM"),

(1208,"Which is MOST important for IS manager to confirm when reviewing an IR plan?",
["Plan includes requirement for post-incident review","Plan is based on a BIA","Plan is stored at backup recovery locations","Plan is readily available for auditors"],"B",
"จำ: review IR plan → MOST important confirm = PLAN BASED ON BIA"),

(1209,"Unintentional employee behavior caused major data loss. BEST way to prevent recurrence?",
["Improve security awareness training program","Communicate consequences for future instances","Implement compensating controls","Enhance DLP solution"],"A",
"จำ: unintentional data loss by employee → IMPROVE SECURITY AWARENESS TRAINING"),

(1210,"Exceptions to a security policy should be approved PRIMARILY based on:",
["results of cost-benefit analysis.","risk appetite.","security incident classification.","industry best practices."],"B",
"จำ: approve policy exceptions → RISK APPETITE"),

(1211,"When developing a business case for new security initiative, IS manager should FIRST:",
["conduct a feasibility study.","calculate TCO.","perform cost-benefit analysis.","define the issues to be addressed."],"D",
"จำ: business case for security initiative FIRST → DEFINE THE ISSUES TO BE ADDRESSED"),

(1212,"A proposal to gain senior mgmt buy-in for a new security project will be MOST effective if it includes:",
["historical data of reported incidents.","analysis of current threat landscape.","industry benchmarking gap analysis.","projected return on investment (ROI)."],"D",
"จำ: gain senior mgmt buy-in for security project → PROJECTED ROI"),

(1213,"Which is MOST important for an IS steering committee to ensure?",
["Funding is available for IS projects.","IS is managed as a business critical issue.","Periodic IS audits are conducted.","Resources for IS projects are minimized."],"B",
"จำ: IS steering committee MOST important → IS MANAGED AS BUSINESS CRITICAL ISSUE"),

(1214,"Breach contained and remediated. Industry regs require external notification. What should IS manager do NEXT?",
["Refer to the privacy policy.","Refer to the IR plan.","Send out breach notification to all parties.","Contact board of directors."],"B",
"จำ: breach requires external notification → REFER TO IR PLAN"),

(1215,"Which is the BEST defense against a brute force attack?",
["Discretionary access control","Multi-factor authentication (MFA)","Mandatory access control","Time-of-day restrictions"],"B",
"จำ: brute force attack defense → MFA"),

(1216,"Which is MOST important to verify during a test of an org's IR process?",
["Whether IR team members know their responsibilities","Whether senior management endorses IR process","Whether users know which numbers to call in call tree","Whether IR team members are cross-trained"],"A",
"จำ: test IR process → MOST important verify = IR TEAM KNOW THEIR RESPONSIBILITIES"),

(1217,"IPS reported significant increase in hacking attempts; no systems compromised. What should IS manager do FIRST?",
["Tune the IPS to address false positives.","Report the increase to senior management.","Validate the events identified by the IPS.","Update security awareness training."],"C",
"จำ: IPS reports increased hacking attempts → FIRST = VALIDATE THE EVENTS"),

(1218,"The likelihood of a successful intrusion is a function of:",
["threat and vulnerability levels.","design and redundancy of network perimeter controls.","configuration and maintenance of log monitoring system.","opportunity and asset value."],"A",
"จำ: likelihood of successful intrusion = THREAT AND VULNERABILITY LEVELS"),

(1219,"Which is the BEST evidence that senior management supports the IS program?",
["IS manager reports to CRO","A reduction in IS costs","Consistent enforcement of IS policies","A high level of IS risk acceptance"],"C",
"จำ: senior mgmt supports IS program BEST evidence → CONSISTENT ENFORCEMENT of IS policies"),

(1220,"During incident recovery, which is the BEST approach to ensure eradication of traces hidden by attacker?",
["Reinstall the system from the original source.","Perform continuous monitoring until validation achieved.","Prohibit use of the compromised account.","Conduct a forensic investigation."],"A",
"จำ: eradicate attacker traces → REINSTALL SYSTEM FROM ORIGINAL SOURCE"),

(1221,"Which BEST enables effectiveness of IS training for new employees?",
["New employees required to acknowledge IS policy.","New employees must complete security assessment after training.","IS training precedes all other onboarding training.","Training is specific to new employees' job functions."],"D",
"จำ: IS training effectiveness for new employees → SPECIFIC TO JOB FUNCTIONS"),

(1222,"Increasing trend in CEO phishing attacks for wire transfer fraud. Which is the BEST way to reduce risk?",
["Temporarily suspend wire transfers.","Provide awareness training to staff responsible for wire transfers.","Disable emails for wire transfer staff.","Provide awareness training to CEO."],"B",
"จำ: CEO phishing wire transfer fraud → AWARENESS TRAINING TO WIRE TRANSFER STAFF"),

(1223,"Which is the BEST indication of effective IS governance?",
["Comprehensive security policies reflect organizational objectives.","IS is integrated into organizational processes.","IS program follows industry best practices.","IS risk register is maintained."],"B",
"จำ: effective IS governance → IS INTEGRATED INTO ORGANIZATIONAL PROCESSES"),

(1224,"DLP flagged PII during transmission. What should IS manager do FIRST?",
["Validate scope and impact with business process owner.","Escalate to senior management.","Review and validate rules within DLP system.","Initiate the IR plan."],"A",
"จำ: DLP flags PII → FIRST = VALIDATE SCOPE AND IMPACT with business process owner"),

(1225,"Which is MOST likely to require an org to update its BCP?",
["Successful BCP testing results","Increases in IS risk trends","Multiple changes in organizational leadership","Major changes in business operating environment"],"D",
"จำ: update BCP → MAJOR CHANGES IN BUSINESS OPERATING ENVIRONMENT"),

(1226,"Which is the GREATEST benefit of tabletop exercise of BCP?",
["Assesses availability of compatible backup hardware.","Identifies follow-up work to address shortcomings.","Provides low-cost method of assessing BCP completeness.","Allows for greater participation from business side."],"B",
"จำ: BCP tabletop exercise GREATEST benefit → IDENTIFIES FOLLOW-UP WORK to address shortcomings"),

(1227,"Which is the BEST approach for encouraging business units to assume IS roles and responsibilities?",
["Engage an independent security audit.","Perform a risk assessment.","Conduct awareness program for senior management.","Develop controls and countermeasures."],"C",
"จำ: encourage BU to assume IS roles → AWARENESS PROGRAM FOR SENIOR MANAGEMENT"),

(1228,"Which is MOST influential in driving effectiveness of an IS program?",
["Policies and standards","Organizational risk appetite","IS metrics","Organizational culture"],"D",
"จำ: IS program effectiveness MOST influential → ORGANIZATIONAL CULTURE"),

(1229,"The MAIN reason for senior management to review and approve IS strategic plan is to ensure:",
["compliance with legal and regulatory requirements.","the plan aligns with corporate governance.","staff participation in IS efforts.","org has required funds to implement plan."],"B",
"จำ: senior mgmt approve IS strategic plan → ALIGN WITH CORPORATE GOVERNANCE"),

(1230,"Which is the GREATEST risk from a poorly trained IR team responding to a major incident?",
["Separation of duty violations","Loss of confidential information","Evidence contamination","Failure to escalate to senior management"],"C",
"จำ: poorly trained IR team GREATEST risk → EVIDENCE CONTAMINATION"),

(1231,"Which is the PRIMARY preventive method to mitigate risks from privileged accounts?",
["Eliminate privileged accounts.","Perform periodic certification of access.","Provide privileged access only to users who need it.","Frequently monitor activities on privileged accounts."],"C",
"จำ: mitigate privileged account risks PRIMARY → PROVIDE ACCESS ONLY TO THOSE WHO NEED IT"),

(1232,"Which BEST enables IR team to determine appropriate actions during initial investigation?",
["Technical capabilities of the team","Feedback from affected departments","Historical data from past incidents","Procedures for incident triage"],"D",
"จำ: appropriate IR actions during initial investigation → PROCEDURES FOR INCIDENT TRIAGE"),

(1233,"Service desk reports PC displaying 'your personal files are encrypted.' What should be done FIRST?",
["Analyze the compromised PC to determine root cause.","Isolate the compromised PC from the network.","Meet with security team to identify related assets.","Update all security endpoints."],"B",
"จำ: files encrypted (ransomware) reported → FIRST = ISOLATE FROM NETWORK"),

(1234,"When multiple Internet intrusions on a server are detected, PRIMARY concern should be to ensure:",
["incident is reported to senior management.","integrity of evidence is preserved.","server is unplugged from power.","forensic investigation software is loaded."],"B",
"จำ: multiple server intrusions detected → PRESERVE INTEGRITY OF EVIDENCE"),

(1235,"Which group is MOST important to involve in development of IS procedures?",
["Audit management","Senior management","End users","Operational units"],"D",
"จำ: develop IS procedures → INVOLVE OPERATIONAL UNITS"),

(1236,"Which would be MOST useful to determine current status of IS program maturity level?",
["BIA","Cost-benefit analysis","Benchmark analysis","Risk assessment"],"C",
"จำ: IS program maturity level → BENCHMARK ANALYSIS"),

(1237,"The MOST significant outcome from conducting a BIA is improved:",
["employee awareness.","disaster recovery planning.","IT capacity planning.","budgeting."],"B",
"จำ: BIA MOST significant outcome → IMPROVED DISASTER RECOVERY PLANNING"),

(1238,"Which BEST indicates ongoing senior management commitment to org's IS strategy?",
["An efficient IR program","Established KPIs","A comprehensive security awareness training program","Adequate funding for the IS program"],"D",
"จำ: senior mgmt commitment to IS strategy → ADEQUATE FUNDING for IS program"),

(1239,"When presenting changes in security risk profile to senior management, which is MOST important to include?",
["Performance measures for existing controls","Number of false positives","Security training test results","Industry benchmarks"],"A",
"จำ: present security risk profile changes → PERFORMANCE MEASURES FOR EXISTING CONTROLS"),

(1240,"Which is the MOST important objective when recommending controls?",
["Ensuring implementation costs are approved","Identifying business processes the controls can support","Reducing the risk to an acceptable level","Minimizing the impact to business processes"],"C",
"จำ: recommending controls → REDUCING RISK TO ACCEPTABLE LEVEL"),

(1241,"Org learned subsidiary is in country where civil unrest just began. What should org do FIRST?",
["Invoke the IR plan.","Assess changes in the risk profile.","Conduct security awareness training.","Activate the DRP."],"B",
"จำ: civil unrest at subsidiary → FIRST = ASSESS CHANGES IN RISK PROFILE"),

(1242,"After updating password standards, apps can't enforce them. IS manager's FIRST action should be to:",
["evaluate cost of replacing the apps.","reevaluate the standards.","determine the potential impact.","implement compensating controls."],"C",
"จำ: apps can't enforce new password standards → FIRST = DETERMINE POTENTIAL IMPACT"),

(1243,"Which is a PRIMARY responsibility of a data owner?",
["Data backup","Data classification","Data quality","Data storage"],"B",
"จำ: data owner PRIMARY responsibility → DATA CLASSIFICATION"),

(1244,"Which is MOST helpful for retaining exec management support for an IS program?",
["Forming IS steering committee for oversight","Providing regular performance reports on program effectiveness","Including IS satisfaction in employee engagement surveys","Developing business cases for security awareness expenses"],"B",
"จำ: retain exec support for IS program → REGULAR PERFORMANCE REPORTS on effectiveness"),

(1245,"When performing a BIA, which is the MOST important reason to determine the MTD?",
["To determine data needed for timely recovery","To assist in developing recovery strategies","To facilitate selection of technologies needed","To establish resources needed for successful recovery"],"B",
"จำ: determine MTD in BIA → ASSIST IN DEVELOPING RECOVERY STRATEGIES"),

(1246,"Which process should remain internal when outsourcing IT operations?",
["Authorization management","Data encryption","Log monitoring","Incident management"],"A",
"จำ: outsource IT ops → keep AUTHORIZATION MANAGEMENT internal"),

(1247,"Org plans DevOps approach. What is IS manager's MOST important consideration for IS strategy?",
["Risk profile may change with new approach.","The identified framework may not be appropriate.","Security policies may need to be revised.","Security staff may lack software coding skills."],"A",
"จำ: DevOps approach → IS strategy = RISK PROFILE MAY CHANGE"),

(1248,"Which is the MOST important reason to integrate nonrepudiation into user authentication design?",
["To ensure no conflicts when changing database records","To ensure users cannot escalate their own access privileges","To ensure users cannot alter log records","To ensure actions can be traced to specific users"],"D",
"จำ: nonrepudiation in authentication → ACTIONS TRACED TO SPECIFIC USERS"),

(1249,"Significant risk in core business function; budget constraints prevent effective remediation. Who should be accountable for selecting risk treatment?",
["Data custodian","Data owner","Security officer","Senior management"],"D",
"จำ: significant risk + budget constraints → SENIOR MANAGEMENT accountable for risk treatment"),

(1250,"IS manager building business case for next-gen firewall. Which would BEST maximize effectiveness?",
["Comparing inherent risk to residual risk","Aligning proof-of-concept with IS strategy","Ensuring ROI is included","Comparing costs between new and current firewall"],"A",
"จำ: business case for firewall → COMPARING INHERENT RISK TO RESIDUAL RISK"),
]


LABELS      = ["A", "B", "C", "D"]
PAGE_SIZE   = 50
TOTAL       = len(QUESTIONS)
TOTAL_PAGES = (TOTAL + PAGE_SIZE - 1) // PAGE_SIZE

DOMAIN_RANGES = [
    (range(1,   51), "D1 Governance",       "#1565C0"),
    (range(51,  101),"D2 Risk Mgmt",        "#2E7D32"),
    (range(101, 151),"D3 Security Program", "#E65100"),
    (range(151, 201),"D4 Incident Mgmt",    "#6A1B9A"),
]

def get_domain(qnum):
    for r, label, color in DOMAIN_RANGES:
        if qnum in r:
            return label, color
    return "Mixed", "#37474F"

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [("page", 0), ("answers", {}), ("revealed", set())]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## CISM 500Q Practice")
    st.markdown("---")

    answered = len(st.session_state.answers)
    correct  = sum(1 for qnum, ch in st.session_state.answers.items()
                   if ch == QUESTIONS[qnum-1][3])
    pct      = int(answered / TOTAL * 100) if answered else 0

    st.markdown(f"**Overall Progress:** {answered}/{TOTAL} ({pct}%)")
    st.progress(answered / TOTAL)

    if answered:
        sc = int(correct / answered * 100)
        color = "#2E7D32" if sc >= 75 else "#E65100" if sc >= 60 else "#C62828"
        st.markdown(
            f"**Score:** <span style='color:{color};font-weight:700'>"
            f"{correct}/{answered} ({sc}%)</span>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("**Jump to page:**")

    page_labels = []
    for p in range(TOTAL_PAGES):
        s = p * PAGE_SIZE + 1
        e = min((p+1) * PAGE_SIZE, TOTAL)
        done = sum(1 for q in range(s, e+1) if q in st.session_state.answers)
        page_labels.append(f"Q{s}-{e}  ({done}/{e-s+1})")

    sel = st.radio("", page_labels,
                   index=st.session_state.page,
                   label_visibility="collapsed")
    st.session_state.page = page_labels.index(sel)

    st.markdown("---")
    if st.button("Reset All", use_container_width=True):
        st.session_state.answers  = {}
        st.session_state.revealed = set()
        st.session_state.page     = 0
        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
page      = st.session_state.page
start_idx = page * PAGE_SIZE
end_idx   = min(start_idx + PAGE_SIZE, TOTAL)
page_qs   = QUESTIONS[start_idx:end_idx]

p_start = page_qs[0][0]
p_end   = page_qs[-1][0]
p_done  = sum(1 for q in page_qs if q[0] in st.session_state.answers)
p_right = sum(1 for q in page_qs
              if q[0] in st.session_state.answers
              and st.session_state.answers[q[0]] == q[3])
p_wrong = p_done - p_right

st.markdown(f"## Questions {p_start} - {p_end}")

c1, c2, c3 = st.columns(3)
c1.metric("Answered", f"{p_done}/{len(page_qs)}")
c2.metric("Correct",  p_right)
c3.metric("Wrong",    p_wrong)

fill_pct   = int(p_done / len(page_qs) * 100)
fill_color = "#2E7D32" if fill_pct == 100 else "#E85D26"
st.markdown(
    f'''<div class="progress-wrap">
    <div class="progress-fill" style="width:{fill_pct}%;background:{fill_color}"></div>
    </div>''',
    unsafe_allow_html=True
)

if p_done == len(page_qs) and p_done > 0:
    sc = int(p_right / p_done * 100)
    gc = "#2E7D32" if sc >= 75 else "#E65100" if sc >= 60 else "#C62828"
    st.markdown(
        f'''<div class="score-card">
        <div style="font-size:14px;color:#aab;margin-bottom:4px">Page Score</div>
        <div class="score-big" style="color:{gc}">{sc}%</div>
        <div style="color:#ccc;margin-top:6px">{p_right} correct out of {p_done}</div>
        </div>''',
        unsafe_allow_html=True
    )

st.markdown("---")

# ── Each question ─────────────────────────────────────────────────────────────
for q in page_qs:
    qnum, qtext, opts, correct_ans, mem = q
    dom_label, dom_color = get_domain(qnum)
    answered_q = qnum in st.session_state.answers
    chosen     = st.session_state.answers.get(qnum)

    st.markdown(
        f'''<div class="q-card">
        <span class="domain-badge" style="background:{dom_color}20;color:{dom_color}">{dom_label}</span>
        <div class="q-number">Question #{qnum}</div>
        <div class="q-text">{qtext}</div>
        </div>''',
        unsafe_allow_html=True
    )

    if not answered_q:
        options = [f"{LABELS[i]}.  {opts[i]}" for i in range(4)]
        choice  = st.radio(
            label=f"q_{qnum}",
            options=options,
            index=None,
            label_visibility="collapsed",
            key=f"radio_{qnum}"
        )
        col_ans, col_skip = st.columns([3, 1])
        with col_ans:
            if st.button("Submit Answer", key=f"btn_{qnum}",
                         use_container_width=True, type="primary"):
                if choice is not None:
                    st.session_state.answers[qnum] = choice[0]
                    st.rerun()
                else:
                    st.warning("Please select an option first.")
        with col_skip:
            if st.button("Skip", key=f"skip_{qnum}", use_container_width=True):
                st.session_state.answers[qnum] = "SKIP"
                st.rerun()

    else:
        is_skip  = chosen == "SKIP"
        is_right = (chosen == correct_ans) and not is_skip

        for i, opt in enumerate(opts):
            lbl            = LABELS[i]
            is_correct_opt = (lbl == correct_ans)
            is_chosen_opt  = (lbl == chosen)

            if is_correct_opt:
                css    = "opt-correct"
                prefix = f"✅ {lbl}."
            elif is_chosen_opt and not is_right:
                css    = "opt-wrong"
                prefix = f"❌ {lbl}."
            else:
                css    = "opt-neutral"
                prefix = f"   {lbl}."

            st.markdown(
                f'''<div class="{css}">{prefix}&nbsp;&nbsp;{opt}</div>''',
                unsafe_allow_html=True
            )

        if is_skip:
            st.info(f"Skipped — Correct Answer: **{correct_ans}**")
        elif is_right:
            st.success("Correct!")
        else:
            st.error(f"Wrong — Correct Answer: **{correct_ans}**")

        st.markdown(
            f'''<div class="mem-box">💡 {mem}</div>''',
            unsafe_allow_html=True
        )

        if st.button("Undo", key=f"undo_{qnum}"):
            del st.session_state.answers[qnum]
            st.session_state.revealed.discard(qnum)
            st.rerun()

    st.markdown(
        "<div style='margin:28px 0 24px;border-top:3px solid #E85D26;opacity:.25;'></div>",
        unsafe_allow_html=True
    )

# ── Page navigation ───────────────────────────────────────────────────────────
col_prev, col_mid, col_next = st.columns([1, 2, 1])
with col_prev:
    if page > 0:
        if st.button("Previous", use_container_width=True):
            st.session_state.page -= 1
            st.rerun()
with col_mid:
    st.markdown(
        f"<p style='text-align:center;color:#888;font-size:14px'>"
        f"Page {page+1} / {TOTAL_PAGES}</p>",
        unsafe_allow_html=True
    )
with col_next:
    if page < TOTAL_PAGES - 1:
        if st.button("Next", use_container_width=True, type="primary"):
            st.session_state.page += 1
            st.rerun()
