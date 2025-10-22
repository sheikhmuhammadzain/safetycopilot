# Excel Data Analysis Report

Generated on: 2025-10-21 20:06:46

This document contains the structure and sample data from all sheets in the Excel file.

## Table of Contents

1. [Incident](#incident)
2. [Hazard ID](#hazard-id)
3. [Audit](#audit)
4. [Audit Findings](#audit-findings)
5. [Inspection](#inspection)
6. [Inspection Findings](#inspection-findings)

---

## Incident

**Total Columns:** 169
**Total Rows:** 2596
**Sample Rows:** 5

### Data Types and Sample Values

| Column | Data Type | Non-Null Count | Sample Values |
|--------|-----------|----------------|---------------|
| Incident Number | object | 866/2596 | IN-20220405-001, IN-20230102-001, IN-20230211-003 |
| Date of Occurrence | datetime64[ns] | 866/2596 | 2022-04-05 00:00:00, 2023-01-02 00:00:00, 2023-02-11 00:00:00 |
| Incident Type(s) | object | 866/2596 | Other; No Loss / No Injury, Site HSE Rules; No Loss / No Injury, Transport Safety; Property/Asset Damage |
| Section | object | 862/2596 | Technical, Production, Commercial |
| Title | object | 866/2596 | OVR catalyst loss, Agitator moved and hit the ladder while Poly-A ves..., Minor Car Accident |
| Status | object | 866/2596 | Closed |
| Category | object | 866/2596 | Incident |
| Description | object | 866/2596 | High catalyst loss has been observed from OVR for ..., Agitator of Poly-A at PVC-1 moved and hit the ladd..., On the congested 10th commercial street of DHA Pha... |
| Group Company | object | 866/2596 | Engro Polymer and Chemicals |
| Location | object | 866/2596 | Karachi, Lahore |
| Sub-Location | object | 866/2596 | Manufacturing Facility, Non Manufacturing, Projects and BD |
| Department | object | 861/2596 | Process - EDC / VCM, PVC, Chlor Alkali and Allied Chemicals |
| Sub-department | object | 798/2596 | EDC / VCM, PVC I, Chlor Alkali and Allied Chemicals |
| Location (EPCL) | object | 866/2596 | EVCM 200, PVC I Front End, Head Office |
| Injury Potential | float64 | 0/2596 |  |
| Location Tag | float64 | 0/2596 |  |
| Specific Location of Occurrence | float64 | 0/2596 |  |
| Repeated Incident | object | 866/2596 | Yes, No |
| D-Level Committee Number (EPCL) | object | 866/2596 | 22, Process Engineering, Not Applicable, 123, Maintenance Stationary VCM |
| Incident Time | object | 866/2596 | 14:00:00, 16:00:00, 17:00:00 |
| Repeated Event | object | 15/2596 | No |
| Person Involved | object | 364/2596 | Waseem Haider - EPCL Plant, Muhammad Rafae Haq - EPCL KHI NM, Contractor |
| Relationship of Person Involved | object | 863/2596 | Employee, 3rd Party Contractor, Other |
| Contracting Company | object | 166/2596 | GASCO, Etimaad Engineering, DESCON |
| Supervisor of Person Involved | object | 151/2596 | Amer Ahmed - EPCL Plant, Junaid Rafey - EPCL Plant, Fahad Hussain - EPCL KHI NM |
| Date Shift Began | object | 293/2596 | 2023-01-02 00:00:00, 2023-03-18 00:00:00, 2023-03-20 00:00:00 |
| Time Shift Began | object | 293/2596 | 07:00:00, 19:00:00, 18:00:00 |
| Reported By | object | 866/2596 | Kaiwan Shahzad - EPCL Plant, Syed Zia Abbas Naqvi - EPCL Plant, Muhammad Rafae Haq - EPCL KHI NM |
| Date Reported | datetime64[ns] | 866/2596 | 2023-10-03 00:00:00, 2023-04-27 00:00:00, 2023-03-22 00:00:00 |
| Date Entered | datetime64[ns] | 866/2596 | 2023-10-03 00:00:00, 2023-04-27 00:00:00, 2023-03-22 00:00:00 |
| Responsible For HSE Quality Check | object | 866/2596 | Safeer Hussain - ECORP KHI HO, Faraz Haris - EPCL P&BD, Yasir Ali - EPCL Plant |
| Responsible for Investigation | object | 866/2596 | Kaiwan Shahzad - EPCL Plant, Syed Zia Abbas Naqvi - EPCL Plant, Muhammad Zain Siddiqui - EPCL KHI NM |
| Task or Activity at Time of Incident | float64 | 0/2596 |  |
| Object/Substance That Directly Injured or Made Person Ill | object | 73/2596 | Horseplay at PM&S, Stones on ground, Bee Sting |
| Physical or Immediate Causes of Incident | float64 | 0/2596 |  |
| First Aid Responder | object | 73/2596 | Syed Nadeem Ashhad - EPCL Plant, External, Expansion Medic |
| Description of Treatment Provided | object | 73/2596 | Wound washing and Saniplst was applied. , Wound cleaned with antiseptic solution and dressin..., First aid supportive treatment done and patient re... |
| Reportable/Recordable? | object | 165/2596 | No, No (Environment), Yes |
| Regulatory Authority | object | 6/2596 | OSHA, State/Prov Environmental, VelocityEHS |
| Agency Contact Information | object | 1/2596 | SEPA |
| Date Reported (to agency) | datetime64[ns] | 1/2596 | 2023-10-25 00:00:00 |
| External Report Number | object | 1/2596 | SEPA, NPC |
| Injury Classification | object | 73/2596 | First Aid, Medical Treatment, Restricted Work |
| # Restricted Days | float64 | 1/2596 | 1.0 |
| # Lost Days | float64 | 0/2596 |  |
| Name of Physician or Health Care Professional | object | 1/2596 | Doctor to add comment |
| Healthcare Facility Name and Address | object | 1/2596 | Doctor to add comment |
| Name of Physician or Health Care Professional.1 | float64 | 0/2596 |  |
| Healthcare Facility Name and Address.1 | float64 | 0/2596 |  |
| Details of Treatment | float64 | 0/2596 |  |
| Point of Release Size | object | 14/2596 | <=5 mm |
| Material Class | object | 17/2596 | Corrosive, Flammable , Carcinogen  |
| Mode of Operation | object | 18/2596 | Normal Operation |
| Release Source | object | 11/2596 | Pipeline , Centrifugal Pump , Seal Oil Pot  |
| Investigation Team Leader | object | 27/2596 | Tauqir Nasir - EPCL Plant, Syed Zia Abbas Naqvi - EPCL Plant, Muhammad Shahid Karim - EPCL Plant |
| Target Completion Date | datetime64[ns] | 866/2596 | 2023-07-20 00:00:00, 2023-05-01 00:00:00, 2023-03-31 00:00:00 |
| Health Professional: I concur with the Injury/Illness Classification | object | 74/2596 | Yes, No |
| Sequence of Events | object | 862/2596 | Cu (ppm) recorded increasing from AS-201B bottom. , 0900hrs MX-1301A PM job handed over by SIC to mach..., On the congested 10th commercial street of DHA Pha... |
| Quantity Contaminated | object | 866/2596 | SCF, tn |
| Why #1 | object | 396/2596 | Q-1: Why did the agitator move during vessel entry..., Why choking occurred in the spool? , Why VE-8202 was opened in TA-2022 |
| Answer #1 | object | 388/2596 | Ans: The said agitator was not physically secured ..., Idle state of PVC-3 plant with VCM present in RVCM..., Vessel was opened as per planned TA job and inspec... |
| Why #2 | object | 352/2596 | Q-2: Why was agitator not secured during vessel en..., Why inspection/cleaning was not done previously?, Why vessel was not repaired in TA-2022 |
| Answer #2 | object | 351/2596 | Although VE permit asks for physical securing of m..., Choking potential in the circuit was not anticipat..., Due to extended work scope and plant start up was ... |
| Why #3 | object | 277/2596 | Q-3: Why was agitator manually rotated during vess..., Why oxygen content was higher post TA? , Why bypass line was installed. |
| Answer #3 | object | 276/2596 | Because agitator PM job was in-progress and vessel..., Oxygen content is present normally post TA which g..., It was decided to repair vessel by post TA so bypa... |
| Why #4 | object | 139/2596 | Q-4: Why AE did not pick simultaneous job handover..., Why moisture was higher in VCM ? , Why MOC was not approved in system. |
| Answer #4 | object | 138/2596 | Both jobs (Agitator PM and VE for cleaning) were h..., Multiple transfers were carried out at the start a..., Due to busy schedule in TA and unplanned activity ... |
| Why #5 | object | 77/2596 | Why bearings issue was not timely picked or overha..., Why HE-1403 tubes are leaking?, Why cat approaches the CCR |
| Answer #5 | object | 76/2596 | Due to gaps in preventive maintenance practices. , A separate investigation has been carried out for ..., CCR have 02 pantry and serving area.  |
| Management System Non-Compliance | object | 866/2596 | PSM, OHIH, EMS |
| PSM | object | 840/2596 | Mechanical Integrity, Procedure & Performance Standards, Contractor Safety Management |
| EMS | object | 14/2596 | Environmental Policies & Principles, Audits & Observations, Environmental Management System |
| OHIH | object | 14/2596 | Return to work after Illness Injury, Hazardous Chemical Exposure & Prevention Measures, Ergonomics Procedure |
| Conclusion | object | 866/2596 | High catalyst loss has been observed from OVR, the..., Root cause is non-compliance of work permit system..., Despite of little space, the truck forced its way ... |
| Completion Date | object | 866/2596 | 2023-10-05 00:00:00, 2023-05-26 00:00:00, 2024-04-08 00:00:00 |
| Injury/Illness Type | object | 73/2596 | Cuts, Other, Bruise |
| Body Part | object | 73/2596 | Face, Leg, Hand/Wrist |
| Accident Type | object | 73/2596 | Physically assaulted by a person, Drowned or asphyxiated, Injured by an animal |
| Accident Agent | object | 73/2596 | Other, Floor, Animal/Insect |
| Date of Birth | float64 | 0/2596 |  |
| Job Title | object | 1/2596 | Assistant Operations Engineer I |
| Hire Date | float64 | 0/2596 |  |
| Years in Present Job | float64 | 0/2596 |  |
| Total Years Experience | float64 | 0/2596 |  |
| PPE Worn | float64 | 0/2596 |  |
| Chemical(s) Released | object | 71/2596 | Lube Oil, 33 % HCl, EDC,VCM,HCL |
| CAS Number | object | 2/2596 | EDC/VCM/HCL; , edc |
| Chemical(s) Class | object | 64/2596 | Other, Corrosive, Flammable |
| Release Source.1 | object | 91/2596 | Spillage/Leakage, Air Emission - Regulatory Non-Compliance, Hazardous Waste - Regulatory Non-Compliance |
| Released To | object | 70/2596 | Land, Air, Land; Drain Channels |
| Quantity Released | object | 16/2596 | 0.5 L, 100 mL, 51.25 L |
| Quantity Recovered | object | 4/2596 | 0 mL, 0 L, 100 mL |
| Onsite Area Affected | float64 | 0/2596 |  |
| Offsite Area Affected | float64 | 0/2596 |  |
| Time To Contain | object | 6/2596 | 10 min, 12 h, 30 min |
| Fire Type | object | 20/2596 | Electrical Fire, General Fire, Process Fire |
| Ignition Source | object | 16/2596 | Electrical Equipment, Exposed Incandescent Material, Hot Surface |
| Extinguish Method | object | 4/2596 | Portable Fire Extinguisher, Fire Hose |
| Operational Upset Category | object | 33/2596 | Chocking; Runaway Reaction, Equipment Unavailability, Equipment Malfunction/Tripping |
| Motor Vehicle Accident | object | 26/2596 | Yes, No |
| Transportation Mode | object | 28/2596 | Road |
| Vehicle Type | object | 28/2596 | Company Car, Shahzore , Dumper |
| Vehicle Ownership | object | 28/2596 | Company, Contractor, 3rd Party |
| (Type of) Equipment Failure | object | 429/2596 | Pipeline, Mechanical Failure, Instrumentation |
| Equipment | object | 434/2596 | Valve, Pipe Line, Pressure Vacuum Relief Valve |
| Is the equipment safety critical? | object | 430/2596 | Yes, No |
| Equipment ID | object | 428/2596 | HV-3101 A, VGS, PSV-3113 |
| Product Contaminated | object | 5/2596 | PVC Production, RVCM, Nitrogen |
| Contaminant | object | 5/2596 | High FP / VCM / YID, Low pH, Oxygen |
| Equipment ID.1 | object | 5/2596 | PVC-2 Screen Sample, VE3301/VE3302, PSA Unit B |
| Exposure type | object | 4/2596 | Food Contamination, Poor Indoor Air Quality, Unacceptable Drinking Water Quality |
| Asset Damage Type | object | 51/2596 | Vehicle Damage, Plant Equipment, 3rd Party Asset |
| PSE Category | object | 368/2596 | Tier 1, Tier 3 - Challenges to Safety System, Tier 3 |
| Tier 3 Description | object | 367/2596 | SCD System Malfunction, LOPC (Body Leakage), LOPC |
| Material involved | object | 337/2596 | Catalyst , VCM, Waste Water |
| Description.1 | object | 97/2596 | Reliability Event, Incomplete documentation of changes, Pipeline Reliability |
| HSE Site Rules Category | object | 216/2596 | Safe Work Practices Violation, Management System Violation, Cardinal Rule Violation |
| Cardinal Rule Violation | object | 9/2596 | Sleeping on the job, Lighting Flame without Authorization, Horseplay or Fighting |
| Emergency Role Statement Violation | object | 9/2596 | Emergency Role Statement Not Followed, Resistance in following role statement |
| Policy Violation | object | 3/2596 | Smoking in non-designated area, Concealing the reportable incident, Willful damage to company data |
| PPEs Violation | object | 13/2596 | Mandatory PPEs Violation, Violation of special required PPEs, Use of sub-standard PPEs |
| Safe Work Practices Violation | object | 184/2596 | Work Permit procedure violation, Work at height, safety rules not followed, Failing to maintain appropriate license / certific... |
| Management System Violation | object | 20/2596 | MOC Protocol violation, Neglect of duty and / or lack of due care or dilig..., Safety Critical Device defeat protocol not followe... |
| Housing/Colony Related Violations | float64 | 0/2596 |  |
| Other Violations | object | 1/2596 | Miss use of company’s asset/service |
| Security Concern | object | 4/2596 | Other, Break and Enter, Theft |
| Insurance Group Notified | float64 | 0/2596 |  |
| Community Concern | float64 | 0/2596 |  |
| Relevant Consequence (Incident) | object | 866/2596 | Asset, People, Environment |
| Worst Case Consequence (Incident) | object | 866/2596 | C3 - Severe, C4 - Major, C2 - Serious |
| Actual Consequence (Incident) | object | 866/2596 | C0 - No Ill Effect, C1 - Minor, C2 - Serious |
| Relevant Consequence (Hazard ID) | object | 10/2596 | Environment, People, Asset |
| Worst Case Consequence Potential (Hazard ID) | object | 10/2596 | C2 - Serious, C4 - Major, C1 - Minor |
| Violation Type (Hazard ID) | object | 8/2596 | Safety Rule Violation, Unsafe Act, Unsafe Condition |
| Root Cause | object | 866/2596 | Inadequate preventive/corrective maintenance pract..., Changes to task situation not recognized; inadequa..., Personal Factors |
| Cost Type | object | 142/2596 | Production Loss, Equipment Loss, Other |
| Total Cost | float64 | 142/2596 | 516852.0, 100.0, 50.0 |
| Responsible for Approval (Hazard ID) | object | 18/2596 | Muhammad Rehan Khan - EPCL Plant, Syed Ali Majid Shah - EPCL Plant, Muhammad Obaid Qureshi - EPCL P&BD |
| Responsible For Investigation Approval | object | 866/2596 | Tauqir Nasir - EPCL Plant, Syed Zia Abbas Naqvi - EPCL Plant, Muhammad Zain Siddiqui - EPCL KHI NM |
| Investigation Type | object | 866/2596 | Team Investigation, RGL Level Investigation, Department Level Investigation |
| PSE Category Selection Criteria | object | 363/2596 | PRD release, Breaching threshold quantity limits, Fire/Explosion leading to Asset damage |
| Actual Leakage Quantity | object | 866/2596 | SCF, 0.5 L, 0.05 L |
| Corrective Actions | object | 2558/2596 | AC-INC-20231005-019, OVR Dip pipe metallurgy.Status:CompletionDue:2025-..., ; AC-INC-20231005-007 |
| Entered Investigation | object | 866/2596 | 2023-10-04 00:00:00, 2023-04-27 00:00:00, 2023-03-24 00:00:00 |
| Entered Review | object | 18/2596 | 2023-03-27 00:00:00, 2023-03-21; 2023-05-14, 2023-03-22; 2023-05-14 |
| Entered Pending Closure | object | 866/2596 | 2023-10-05 00:00:00, 2023-05-26 00:00:00, 2024-06-05 00:00:00 |
| Entered Closed | object | 866/2596 | 2023-10-09 00:00:00, 2023-08-08 00:00:00, 2024-06-05 00:00:00 |
| Task or Activity at Time of Incident.1 | object | 866/2596 | Others, Maintenance, Plant Shutdown |
| Regulatory Non-Compliance | object | 92/2596 | No, Yes |
| Surface Condition | object | 20/2596 | Under Construction, Smooth, Slippery Road  |
| Driving Conditions | object | 20/2596 | Proper Light, Others, Rain |
| Driver's Name + License Information | object | 24/2596 | Private Driver - Dial a Car, Mazda Driver, Abdul Hakeem KHan  |
| Behavioral Violation at the Time of Incident | object | 15/2596 | Failure to Maintain the Safe Distance, Others, Overtaking |
| Driver Speed | object | 24/2596 | Less than 25 Km/hr, 25-40 Km/hr, 40-60 Km/hr |
| Issues with Vehicle at the Time of Incident | object | 13/2596 | Others, Damaged Mirrors, Tire Rupture |
| Violation Type (Incident) | object | 12/2596 | Driving without Authorization , Vehicle/Crane Accident (due to human error) [10], Unsafe Driving |
| Loss of Containment | object | 24/2596 | No, Yes |
| Vehicle Fitness Certificate Available? | object | 24/2596 | Yes, No |
| Inhalation | object | 1/2596 | Carbon Dioxide |
| Ingestion | object | 1/2596 | Others |
| Noise | float64 | 0/2596 |  |
| Heat Stress | float64 | 0/2596 |  |
| Sharps | float64 | 0/2596 |  |
| Ergonomics | float64 | 0/2596 |  |
| Lighting | float64 | 0/2596 |  |
| Radiation | float64 | 0/2596 |  |
| OHIH Advisor Remarks | float64 | 0/2596 |  |
| Key Factor | object | 866/2596 | Repeat failure of facility equipment, Lack of control on work in confined spaces , Worker fatigue/distraction |
| Contributing Factor | object | 866/2596 | Repeat failure of facility equipment, Changes to task situation not recognized; inadequa..., Worker fatigue/distraction |

### Numeric Column Statistics

| Column | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| # Restricted Days | 1.00 | 1.00 | 1.00 | 1.00 | nan |

### Categorical Columns Summary

**Section** (11 unique values):

- Maintenance: 218
- Instruments & Electrical: 166
- Asset Integrity: 165
- Projects: 157
- Production: 61
- Technical: 29
- Administration: 28
- Supply Chain: 26
- Human Resources: 5
- Health, Safety and Environment: 4

**Location** (2 unique values):

- Karachi: 864
- Lahore: 2

**Sub-Location** (3 unique values):

- Manufacturing Facility: 673
- Projects and BD: 157
- Non Manufacturing: 36

### Sample Data (First 5 Rows)

| Incident Number   | Date of Occurrence   | Incident Type(s)           | Section   | Title             | Status   | Category   | Description                                                                                             | Group Company               | Location   | Sub-Location           | Department          | Sub-department   | Location (EPCL)   |   Injury Potential |   Location Tag |   Specific Location of Occurrence | Repeated Incident   | D-Level Committee Number (EPCL)   | Incident Time   |   Repeated Event |   Person Involved | Relationship of Person Involved   |   Contracting Company |   Supervisor of Person Involved |   Date Shift Began |   Time Shift Began | Reported By                 | Date Reported       | Date Entered        | Responsible For HSE Quality Check   | Responsible for Investigation   |   Task or Activity at Time of Incident |   Object/Substance That Directly Injured or Made Person Ill |   Physical or Immediate Causes of Incident |   First Aid Responder |   Description of Treatment Provided |   Reportable/Recordable? |   Regulatory Authority |   Agency Contact Information | Date Reported (to agency)   |   External Report Number |   Injury Classification |   # Restricted Days |   # Lost Days |   Name of Physician or Health Care Professional |   Healthcare Facility Name and Address |   Name of Physician or Health Care Professional.1 |   Healthcare Facility Name and Address.1 |   Details of Treatment |   Point of Release Size |   Material Class |   Mode of Operation |   Release Source | Investigation Team Leader   | Target Completion Date   |   Health Professional: I concur with the Injury/Illness Classification | Sequence of Events                                | Quantity Contaminated   |   Why #1 |   Answer #1 |   Why #2 |   Answer #2 |   Why #3 |   Answer #3 |   Why #4 |   Answer #4 |   Why #5 |   Answer #5 | Management System Non-Compliance   | PSM                  |   EMS |   OHIH | Conclusion                                                                                              | Completion Date     |   Injury/Illness Type |   Body Part |   Accident Type |   Accident Agent |   Date of Birth |   Job Title |   Hire Date |   Years in Present Job |   Total Years Experience |   PPE Worn |   Chemical(s) Released |   CAS Number |   Chemical(s) Class |   Release Source.1 |   Released To |   Quantity Released |   Quantity Recovered |   Onsite Area Affected |   Offsite Area Affected |   Time To Contain |   Fire Type |   Ignition Source |   Extinguish Method |   Operational Upset Category |   Motor Vehicle Accident |   Transportation Mode |   Vehicle Type |   Vehicle Ownership |   (Type of) Equipment Failure |   Equipment |   Is the equipment safety critical? |   Equipment ID |   Product Contaminated |   Contaminant |   Equipment ID.1 |   Exposure type |   Asset Damage Type | PSE Category   |   Tier 3 Description | Material involved   | Description.1     |   HSE Site Rules Category |   Cardinal Rule Violation |   Emergency Role Statement Violation |   Policy Violation |   PPEs Violation |   Safe Work Practices Violation |   Management System Violation |   Housing/Colony Related Violations |   Other Violations |   Security Concern |   Insurance Group Notified |   Community Concern | Relevant Consequence (Incident)   | Worst Case Consequence (Incident)   | Actual Consequence (Incident)   |   Relevant Consequence (Hazard ID) |   Worst Case Consequence Potential (Hazard ID) |   Violation Type (Hazard ID) | Root Cause                                                                                              |   Cost Type |   Total Cost |   Responsible for Approval (Hazard ID) | Responsible For Investigation Approval   | Investigation Type   |   PSE Category Selection Criteria | Actual Leakage Quantity   | Corrective Actions                                      | Entered Investigation   |   Entered Review | Entered Pending Closure   | Entered Closed      | Task or Activity at Time of Incident.1   |   Regulatory Non-Compliance |   Surface Condition |   Driving Conditions |   Driver's Name + License Information |   Behavioral Violation at the Time of Incident |   Driver Speed |   Issues with Vehicle at the Time of Incident |   Violation Type (Incident) |   Loss of Containment |   Vehicle Fitness Certificate Available? |   Inhalation |   Ingestion |   Noise |   Heat Stress |   Sharps |   Ergonomics |   Lighting |   Radiation |   OHIH Advisor Remarks | Key Factor                           | Contributing Factor                  |
|:------------------|:---------------------|:---------------------------|:----------|:------------------|:---------|:-----------|:--------------------------------------------------------------------------------------------------------|:----------------------------|:-----------|:-----------------------|:--------------------|:-----------------|:------------------|-------------------:|---------------:|----------------------------------:|:--------------------|:----------------------------------|:----------------|-----------------:|------------------:|:----------------------------------|----------------------:|--------------------------------:|-------------------:|-------------------:|:----------------------------|:--------------------|:--------------------|:------------------------------------|:--------------------------------|---------------------------------------:|------------------------------------------------------------:|-------------------------------------------:|----------------------:|------------------------------------:|-------------------------:|-----------------------:|-----------------------------:|:----------------------------|-------------------------:|------------------------:|--------------------:|--------------:|------------------------------------------------:|---------------------------------------:|--------------------------------------------------:|-----------------------------------------:|-----------------------:|------------------------:|-----------------:|--------------------:|-----------------:|:----------------------------|:-------------------------|-----------------------------------------------------------------------:|:--------------------------------------------------|:------------------------|---------:|------------:|---------:|------------:|---------:|------------:|---------:|------------:|---------:|------------:|:-----------------------------------|:---------------------|------:|-------:|:--------------------------------------------------------------------------------------------------------|:--------------------|----------------------:|------------:|----------------:|-----------------:|----------------:|------------:|------------:|-----------------------:|-------------------------:|-----------:|-----------------------:|-------------:|--------------------:|-------------------:|--------------:|--------------------:|---------------------:|-----------------------:|------------------------:|------------------:|------------:|------------------:|--------------------:|-----------------------------:|-------------------------:|----------------------:|---------------:|--------------------:|------------------------------:|------------:|------------------------------------:|---------------:|-----------------------:|--------------:|-----------------:|----------------:|--------------------:|:---------------|---------------------:|:--------------------|:------------------|--------------------------:|--------------------------:|-------------------------------------:|-------------------:|-----------------:|--------------------------------:|------------------------------:|------------------------------------:|-------------------:|-------------------:|---------------------------:|--------------------:|:----------------------------------|:------------------------------------|:--------------------------------|-----------------------------------:|-----------------------------------------------:|-----------------------------:|:--------------------------------------------------------------------------------------------------------|------------:|-------------:|---------------------------------------:|:-----------------------------------------|:---------------------|----------------------------------:|:--------------------------|:--------------------------------------------------------|:------------------------|-----------------:|:--------------------------|:--------------------|:-----------------------------------------|----------------------------:|--------------------:|---------------------:|--------------------------------------:|-----------------------------------------------:|---------------:|----------------------------------------------:|----------------------------:|----------------------:|-----------------------------------------:|-------------:|------------:|--------:|--------------:|---------:|-------------:|-----------:|------------:|-----------------------:|:-------------------------------------|:-------------------------------------|
| IN-20220405-001   | 2022-04-05 00:00:00  | Other; No Loss / No Injury | Technical | OVR catalyst loss | Closed   | Incident   | High catalyst loss has been observed from OVR for the months of April and June for which OVR was shu... | Engro Polymer and Chemicals | Karachi    | Manufacturing Facility | Process - EDC / VCM | EDC / VCM        | EVCM 200          |                nan |            nan |                               nan | Yes                 | 22, Process Engineering           | 14:00:00        |              nan |               nan | Employee                          |                   nan |                             nan |                nan |                nan | Kaiwan Shahzad - EPCL Plant | 2023-10-03 00:00:00 | 2023-10-03 00:00:00 | Safeer Hussain - ECORP KHI HO       | Kaiwan Shahzad - EPCL Plant     |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan | NaT                         |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan | Tauqir Nasir - EPCL Plant   | 2023-07-20 00:00:00      |                                                                    nan | Cu (ppm) recorded increasing from AS-201B bottom. | SCF                     |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan | PSM                                | Mechanical Integrity |   nan |    nan | High catalyst loss has been observed from OVR, the contributing factor for this event was due to con... | 2023-10-05 00:00:00 |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan | Tier 1         |                  nan | Catalyst            | Reliability Event |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan | Asset                             | C3 - Severe                         | C0 - No Ill Effect              |                                nan |                                            nan |                          nan | Inadequate preventive/corrective maintenance practices; Incomplete planning process ; Working Condit... |         nan |          nan |                                    nan | Tauqir Nasir - EPCL Plant                | Team Investigation   |                               nan | SCF                       | AC-INC-20231005-019                                     | 2023-10-04 00:00:00     |              nan | 2023-10-05 00:00:00       | 2023-10-09 00:00:00 | Others                                   |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan | Repeat failure of facility equipment | Repeat failure of facility equipment |
| nan               | NaT                  | nan                        | nan       | nan               | nan      | nan        | nan                                                                                                     | nan                         | nan        | nan                    | nan                 | nan              | nan               |                nan |            nan |                               nan | nan                 | nan                               | nan             |              nan |               nan | nan                               |                   nan |                             nan |                nan |                nan | nan                         | NaT                 | NaT                 | nan                                 | nan                             |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan | NaT                         |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan | nan                         | NaT                      |                                                                    nan | nan                                               | nan                     |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan | nan                                | nan                  |   nan |    nan | nan                                                                                                     | nan                 |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan | nan            |                  nan | nan                 | nan               |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan | nan                               | nan                                 | nan                             |                                nan |                                            nan |                          nan | nan                                                                                                     |         nan |          nan |                                    nan | nan                                      | nan                  |                               nan | nan                       | OVR Dip pipe metallurgy.Status:CompletionDue:2025-12-31 | nan                     |              nan | nan                       | nan                 | nan                                      |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan | nan                                  | nan                                  |
| nan               | NaT                  | nan                        | nan       | nan               | nan      | nan        | nan                                                                                                     | nan                         | nan        | nan                    | nan                 | nan              | nan               |                nan |            nan |                               nan | nan                 | nan                               | nan             |              nan |               nan | nan                               |                   nan |                             nan |                nan |                nan | nan                         | NaT                 | NaT                 | nan                                 | nan                             |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan | NaT                         |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan | nan                         | NaT                      |                                                                    nan | nan                                               | nan                     |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan | nan                                | nan                  |   nan |    nan | nan                                                                                                     | nan                 |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan | nan            |                  nan | nan                 | nan               |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan | nan                               | nan                                 | nan                             |                                nan |                                            nan |                          nan | nan                                                                                                     |         nan |          nan |                                    nan | nan                                      | nan                  |                               nan | nan                       | ; AC-INC-20231005-007                                   | nan                     |              nan | nan                       | nan                 | nan                                      |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan | nan                                  | nan                                  |
| nan               | NaT                  | nan                        | nan       | nan               | nan      | nan        | nan                                                                                                     | nan                         | nan        | nan                    | nan                 | nan              | nan               |                nan |            nan |                               nan | nan                 | nan                               | nan             |              nan |               nan | nan                               |                   nan |                             nan |                nan |                nan | nan                         | NaT                 | NaT                 | nan                                 | nan                             |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan | NaT                         |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan | nan                         | NaT                      |                                                                    nan | nan                                               | nan                     |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan | nan                                | nan                  |   nan |    nan | nan                                                                                                     | nan                 |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan | nan            |                  nan | nan                 | nan               |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan | nan                               | nan                                 | nan                             |                                nan |                                            nan |                          nan | nan                                                                                                     |         nan |          nan |                                    nan | nan                                      | nan                  |                               nan | nan                       | OVR diffuser cup metallurgy upgradation.Status:Closed   | nan                     |              nan | nan                       | nan                 | nan                                      |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan | nan                                  | nan                                  |
| nan               | NaT                  | nan                        | nan       | nan               | nan      | nan        | nan                                                                                                     | nan                         | nan        | nan                    | nan                 | nan              | nan               |                nan |            nan |                               nan | nan                 | nan                               | nan             |              nan |               nan | nan                               |                   nan |                             nan |                nan |                nan | nan                         | NaT                 | NaT                 | nan                                 | nan                             |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan | NaT                         |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan | nan                         | NaT                      |                                                                    nan | nan                                               | nan                     |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan | nan                                | nan                  |   nan |    nan | nan                                                                                                     | nan                 |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan | nan            |                  nan | nan                 | nan               |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan | nan                               | nan                                 | nan                             |                                nan |                                            nan |                          nan | nan                                                                                                     |         nan |          nan |                                    nan | nan                                      | nan                  |                               nan | nan                       | ; AC-INC-20231005-020                                   | nan                     |              nan | nan                       | nan                 | nan                                      |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan | nan                                  | nan                                  |

---

## Hazard ID

**Total Columns:** 169
**Total Rows:** 1211
**Sample Rows:** 5

### Data Types and Sample Values

| Column | Data Type | Non-Null Count | Sample Values |
|--------|-----------|----------------|---------------|
| Incident Number | object | 994/1211 | HA-20230316-009, HA-20230318-004, HA-20230321-001 |
| Date of Occurrence | datetime64[ns] | 994/1211 | 2023-03-16 00:00:00, 2023-03-18 00:00:00, 2023-03-21 00:00:00 |
| Incident Type(s) | object | 994/1211 | No Loss / No Injury, Process Safety Event; No Loss / No Injury, Other |
| Section | object | 892/1211 | Projects, Production, Maintenance |
| Title | object | 994/1211 | One Desiccator fell down from the height of 10ft. ..., HP Jetting Pump PU-3105 recycle hose leakage , At pipe rack area EEL subcontractor was observed u... |
| Status | object | 994/1211 | Closed, Approval |
| Category | object | 994/1211 | Hazard ID |
| Description | object | 994/1211 | Around 1235 hrs. at Product tank southside PR, dur..., HP Jetting Pump PU-3105 recycle hose leakage obser..., On 3/21/2023, At pipe rack area EEL subcontractor ... |
| Group Company | object | 994/1211 | Engro Polymer and Chemicals |
| Location | object | 994/1211 | Karachi, Lahore |
| Sub-Location | object | 994/1211 | Projects and BD, Manufacturing Facility, Non Manufacturing |
| Department | object | 855/1211 | HPO, PVC, HTDC |
| Sub-department | object | 706/1211 | HPO Contstruction, PVC III, HTDC Contstruction |
| Location (EPCL) | object | 994/1211 | HPO, PVC III Feedstock, HPO Process Area |
| Injury Potential | float64 | 0/1211 |  |
| Location Tag | float64 | 0/1211 |  |
| Specific Location of Occurrence | float64 | 0/1211 |  |
| Repeated Incident | float64 | 0/1211 |  |
| D-Level Committee Number (EPCL) | object | 994/1211 | 190, Mechanical (Projects) & Civil, Not Applicable, 102, PVC I/II/III Stationary |
| Incident Time | object | 994/1211 | 12:00:00, 14:00:00, 10:00:00 |
| Repeated Event | object | 873/1211 | No, Yes |
| Person Involved | float64 | 0/1211 |  |
| Relationship of Person Involved | float64 | 0/1211 |  |
| Contracting Company | float64 | 0/1211 |  |
| Supervisor of Person Involved | float64 | 0/1211 |  |
| Date Shift Began | float64 | 0/1211 |  |
| Time Shift Began | float64 | 0/1211 |  |
| Reported By | object | 994/1211 | Majid Khan - EPCL P&BD, Yasir Ali - EPCL Plant, Akbar Ali - EPCL Plant |
| Date Reported | datetime64[ns] | 994/1211 | 2023-03-20 00:00:00, 2023-04-03 00:00:00, 2023-03-23 00:00:00 |
| Date Entered | datetime64[ns] | 994/1211 | 2023-03-20 00:00:00, 2023-04-03 00:00:00, 2023-03-23 00:00:00 |
| Responsible For HSE Quality Check | float64 | 0/1211 |  |
| Responsible for Investigation | float64 | 0/1211 |  |
| Task or Activity at Time of Incident | float64 | 0/1211 |  |
| Object/Substance That Directly Injured or Made Person Ill | float64 | 0/1211 |  |
| Physical or Immediate Causes of Incident | float64 | 0/1211 |  |
| First Aid Responder | float64 | 0/1211 |  |
| Description of Treatment Provided | float64 | 0/1211 |  |
| Reportable/Recordable? | float64 | 0/1211 |  |
| Regulatory Authority | float64 | 0/1211 |  |
| Agency Contact Information | float64 | 0/1211 |  |
| Date Reported (to agency) | float64 | 0/1211 |  |
| External Report Number | float64 | 0/1211 |  |
| Injury Classification | float64 | 0/1211 |  |
| # Restricted Days | float64 | 0/1211 |  |
| # Lost Days | float64 | 0/1211 |  |
| Name of Physician or Health Care Professional | float64 | 0/1211 |  |
| Healthcare Facility Name and Address | float64 | 0/1211 |  |
| Name of Physician or Health Care Professional.1 | float64 | 0/1211 |  |
| Healthcare Facility Name and Address.1 | float64 | 0/1211 |  |
| Details of Treatment | float64 | 0/1211 |  |
| Point of Release Size | float64 | 0/1211 |  |
| Material Class | float64 | 0/1211 |  |
| Mode of Operation | float64 | 0/1211 |  |
| Release Source | float64 | 0/1211 |  |
| Investigation Team Leader | float64 | 0/1211 |  |
| Target Completion Date | float64 | 0/1211 |  |
| Health Professional: I concur with the Injury/Illness Classification | float64 | 0/1211 |  |
| Sequence of Events | float64 | 0/1211 |  |
| Quantity Contaminated | float64 | 0/1211 |  |
| Why #1 | float64 | 0/1211 |  |
| Answer #1 | float64 | 0/1211 |  |
| Why #2 | float64 | 0/1211 |  |
| Answer #2 | float64 | 0/1211 |  |
| Why #3 | float64 | 0/1211 |  |
| Answer #3 | float64 | 0/1211 |  |
| Why #4 | float64 | 0/1211 |  |
| Answer #4 | float64 | 0/1211 |  |
| Why #5 | float64 | 0/1211 |  |
| Answer #5 | float64 | 0/1211 |  |
| Management System Non-Compliance | float64 | 0/1211 |  |
| PSM | float64 | 0/1211 |  |
| EMS | float64 | 0/1211 |  |
| OHIH | float64 | 0/1211 |  |
| Conclusion | float64 | 0/1211 |  |
| Completion Date | float64 | 0/1211 |  |
| Injury/Illness Type | float64 | 0/1211 |  |
| Body Part | float64 | 0/1211 |  |
| Accident Type | float64 | 0/1211 |  |
| Accident Agent | float64 | 0/1211 |  |
| Date of Birth | float64 | 0/1211 |  |
| Job Title | float64 | 0/1211 |  |
| Hire Date | float64 | 0/1211 |  |
| Years in Present Job | float64 | 0/1211 |  |
| Total Years Experience | float64 | 0/1211 |  |
| PPE Worn | float64 | 0/1211 |  |
| Chemical(s) Released | float64 | 0/1211 |  |
| CAS Number | float64 | 0/1211 |  |
| Chemical(s) Class | float64 | 0/1211 |  |
| Release Source.1 | float64 | 0/1211 |  |
| Released To | float64 | 0/1211 |  |
| Quantity Released | float64 | 0/1211 |  |
| Quantity Recovered | float64 | 0/1211 |  |
| Onsite Area Affected | float64 | 0/1211 |  |
| Offsite Area Affected | float64 | 0/1211 |  |
| Time To Contain | float64 | 0/1211 |  |
| Fire Type | float64 | 0/1211 |  |
| Ignition Source | float64 | 0/1211 |  |
| Extinguish Method | float64 | 0/1211 |  |
| Operational Upset Category | float64 | 0/1211 |  |
| Motor Vehicle Accident | float64 | 0/1211 |  |
| Transportation Mode | float64 | 0/1211 |  |
| Vehicle Type | float64 | 0/1211 |  |
| Vehicle Ownership | float64 | 0/1211 |  |
| (Type of) Equipment Failure | float64 | 0/1211 |  |
| Equipment | float64 | 0/1211 |  |
| Is the equipment safety critical? | float64 | 0/1211 |  |
| Equipment ID | float64 | 0/1211 |  |
| Product Contaminated | float64 | 0/1211 |  |
| Contaminant | float64 | 0/1211 |  |
| Equipment ID.1 | float64 | 0/1211 |  |
| Exposure type | float64 | 0/1211 |  |
| Asset Damage Type | float64 | 0/1211 |  |
| PSE Category | float64 | 0/1211 |  |
| Tier 3 Description | float64 | 0/1211 |  |
| Material involved | float64 | 0/1211 |  |
| Description.1 | float64 | 0/1211 |  |
| HSE Site Rules Category | float64 | 0/1211 |  |
| Cardinal Rule Violation | float64 | 0/1211 |  |
| Emergency Role Statement Violation | float64 | 0/1211 |  |
| Policy Violation | float64 | 0/1211 |  |
| PPEs Violation | float64 | 0/1211 |  |
| Safe Work Practices Violation | float64 | 0/1211 |  |
| Management System Violation | float64 | 0/1211 |  |
| Housing/Colony Related Violations | float64 | 0/1211 |  |
| Other Violations | float64 | 0/1211 |  |
| Security Concern | float64 | 0/1211 |  |
| Insurance Group Notified | float64 | 0/1211 |  |
| Community Concern | float64 | 0/1211 |  |
| Relevant Consequence (Incident) | float64 | 0/1211 |  |
| Worst Case Consequence (Incident) | float64 | 0/1211 |  |
| Actual Consequence (Incident) | float64 | 0/1211 |  |
| Relevant Consequence (Hazard ID) | object | 994/1211 | People, Asset, Environment |
| Worst Case Consequence Potential (Hazard ID) | object | 994/1211 | C1 - Minor, C2 - Serious, C0 - No Ill Effect |
| Violation Type (Hazard ID) | object | 927/1211 | Unsafe Act, Unsafe Condition, Safety Rule Violation |
| Root Cause | float64 | 0/1211 |  |
| Cost Type | float64 | 0/1211 |  |
| Total Cost | float64 | 0/1211 |  |
| Responsible for Approval (Hazard ID) | object | 994/1211 | Muhammad Umar Shafiq - EPCL P&BD, Amer Ahmed - EPCL Plant, Ammar Ahmad - EPCL P&BD |
| Responsible For Investigation Approval | float64 | 0/1211 |  |
| Investigation Type | float64 | 0/1211 |  |
| PSE Category Selection Criteria | float64 | 0/1211 |  |
| Actual Leakage Quantity | float64 | 0/1211 |  |
| Corrective Actions | object | 428/1211 | AC-INC-20230512-002, Counseling of the individual to be carried out. St..., AC-INC-20230512-001 |
| Entered Investigation | float64 | 0/1211 |  |
| Entered Review | object | 994/1211 | 2023-03-20 00:00:00, 2023-04-03 00:00:00, 2023-03-23 00:00:00 |
| Entered Pending Closure | float64 | 0/1211 |  |
| Entered Closed | object | 962/1211 | 2023-04-05 00:00:00, 2023-04-27 00:00:00, 2023-03-31 00:00:00 |
| Task or Activity at Time of Incident.1 | float64 | 0/1211 |  |
| Regulatory Non-Compliance | float64 | 0/1211 |  |
| Surface Condition | float64 | 0/1211 |  |
| Driving Conditions | float64 | 0/1211 |  |
| Driver's Name + License Information | float64 | 0/1211 |  |
| Behavioral Violation at the Time of Incident | float64 | 0/1211 |  |
| Driver Speed | float64 | 0/1211 |  |
| Issues with Vehicle at the Time of Incident | float64 | 0/1211 |  |
| Violation Type (Incident) | float64 | 0/1211 |  |
| Loss of Containment | float64 | 0/1211 |  |
| Vehicle Fitness Certificate Available? | float64 | 0/1211 |  |
| Inhalation | float64 | 0/1211 |  |
| Ingestion | float64 | 0/1211 |  |
| Noise | float64 | 0/1211 |  |
| Heat Stress | float64 | 0/1211 |  |
| Sharps | float64 | 0/1211 |  |
| Ergonomics | float64 | 0/1211 |  |
| Lighting | float64 | 0/1211 |  |
| Radiation | float64 | 0/1211 |  |
| OHIH Advisor Remarks | float64 | 0/1211 |  |
| Key Factor | float64 | 0/1211 |  |
| Contributing Factor | float64 | 0/1211 |  |

### Numeric Column Statistics

| Column | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|

### Categorical Columns Summary

**Section** (11 unique values):

- Projects: 264
- Maintenance: 257
- Production: 200
- Instruments & Electrical: 66
- Asset Integrity: 36
- Administration: 33
- Technical: 15
- Supply Chain: 8
- Health, Safety and Environment: 8
- Operational Disipline: 3

**Status** (2 unique values):

- Closed: 962
- Approval: 32

**Location** (2 unique values):

- Karachi: 993
- Lahore: 1

**Sub-Location** (3 unique values):

- Manufacturing Facility: 718
- Projects and BD: 264
- Non Manufacturing: 12

### Sample Data (First 5 Rows)

| Incident Number   | Date of Occurrence   | Incident Type(s)                          | Section    | Title                                                                                      | Status   | Category   | Description                                                                                             | Group Company               | Location   | Sub-Location           | Department   | Sub-department     | Location (EPCL)   |   Injury Potential |   Location Tag |   Specific Location of Occurrence |   Repeated Incident | D-Level Committee Number (EPCL)    | Incident Time   | Repeated Event   |   Person Involved |   Relationship of Person Involved |   Contracting Company |   Supervisor of Person Involved |   Date Shift Began |   Time Shift Began | Reported By            | Date Reported       | Date Entered        |   Responsible For HSE Quality Check |   Responsible for Investigation |   Task or Activity at Time of Incident |   Object/Substance That Directly Injured or Made Person Ill |   Physical or Immediate Causes of Incident |   First Aid Responder |   Description of Treatment Provided |   Reportable/Recordable? |   Regulatory Authority |   Agency Contact Information |   Date Reported (to agency) |   External Report Number |   Injury Classification |   # Restricted Days |   # Lost Days |   Name of Physician or Health Care Professional |   Healthcare Facility Name and Address |   Name of Physician or Health Care Professional.1 |   Healthcare Facility Name and Address.1 |   Details of Treatment |   Point of Release Size |   Material Class |   Mode of Operation |   Release Source |   Investigation Team Leader |   Target Completion Date |   Health Professional: I concur with the Injury/Illness Classification |   Sequence of Events |   Quantity Contaminated |   Why #1 |   Answer #1 |   Why #2 |   Answer #2 |   Why #3 |   Answer #3 |   Why #4 |   Answer #4 |   Why #5 |   Answer #5 |   Management System Non-Compliance |   PSM |   EMS |   OHIH |   Conclusion |   Completion Date |   Injury/Illness Type |   Body Part |   Accident Type |   Accident Agent |   Date of Birth |   Job Title |   Hire Date |   Years in Present Job |   Total Years Experience |   PPE Worn |   Chemical(s) Released |   CAS Number |   Chemical(s) Class |   Release Source.1 |   Released To |   Quantity Released |   Quantity Recovered |   Onsite Area Affected |   Offsite Area Affected |   Time To Contain |   Fire Type |   Ignition Source |   Extinguish Method |   Operational Upset Category |   Motor Vehicle Accident |   Transportation Mode |   Vehicle Type |   Vehicle Ownership |   (Type of) Equipment Failure |   Equipment |   Is the equipment safety critical? |   Equipment ID |   Product Contaminated |   Contaminant |   Equipment ID.1 |   Exposure type |   Asset Damage Type |   PSE Category |   Tier 3 Description |   Material involved |   Description.1 |   HSE Site Rules Category |   Cardinal Rule Violation |   Emergency Role Statement Violation |   Policy Violation |   PPEs Violation |   Safe Work Practices Violation |   Management System Violation |   Housing/Colony Related Violations |   Other Violations |   Security Concern |   Insurance Group Notified |   Community Concern |   Relevant Consequence (Incident) |   Worst Case Consequence (Incident) |   Actual Consequence (Incident) | Relevant Consequence (Hazard ID)   | Worst Case Consequence Potential (Hazard ID)   | Violation Type (Hazard ID)   |   Root Cause |   Cost Type |   Total Cost | Responsible for Approval (Hazard ID)   |   Responsible For Investigation Approval |   Investigation Type |   PSE Category Selection Criteria |   Actual Leakage Quantity |   Corrective Actions |   Entered Investigation | Entered Review      |   Entered Pending Closure | Entered Closed      |   Task or Activity at Time of Incident.1 |   Regulatory Non-Compliance |   Surface Condition |   Driving Conditions |   Driver's Name + License Information |   Behavioral Violation at the Time of Incident |   Driver Speed |   Issues with Vehicle at the Time of Incident |   Violation Type (Incident) |   Loss of Containment |   Vehicle Fitness Certificate Available? |   Inhalation |   Ingestion |   Noise |   Heat Stress |   Sharps |   Ergonomics |   Lighting |   Radiation |   OHIH Advisor Remarks |   Key Factor |   Contributing Factor |
|:------------------|:---------------------|:------------------------------------------|:-----------|:-------------------------------------------------------------------------------------------|:---------|:-----------|:--------------------------------------------------------------------------------------------------------|:----------------------------|:-----------|:-----------------------|:-------------|:-------------------|:------------------|-------------------:|---------------:|----------------------------------:|--------------------:|:-----------------------------------|:----------------|:-----------------|------------------:|----------------------------------:|----------------------:|--------------------------------:|-------------------:|-------------------:|:-----------------------|:--------------------|:--------------------|------------------------------------:|--------------------------------:|---------------------------------------:|------------------------------------------------------------:|-------------------------------------------:|----------------------:|------------------------------------:|-------------------------:|-----------------------:|-----------------------------:|----------------------------:|-------------------------:|------------------------:|--------------------:|--------------:|------------------------------------------------:|---------------------------------------:|--------------------------------------------------:|-----------------------------------------:|-----------------------:|------------------------:|-----------------:|--------------------:|-----------------:|----------------------------:|-------------------------:|-----------------------------------------------------------------------:|---------------------:|------------------------:|---------:|------------:|---------:|------------:|---------:|------------:|---------:|------------:|---------:|------------:|-----------------------------------:|------:|------:|-------:|-------------:|------------------:|----------------------:|------------:|----------------:|-----------------:|----------------:|------------:|------------:|-----------------------:|-------------------------:|-----------:|-----------------------:|-------------:|--------------------:|-------------------:|--------------:|--------------------:|---------------------:|-----------------------:|------------------------:|------------------:|------------:|------------------:|--------------------:|-----------------------------:|-------------------------:|----------------------:|---------------:|--------------------:|------------------------------:|------------:|------------------------------------:|---------------:|-----------------------:|--------------:|-----------------:|----------------:|--------------------:|---------------:|---------------------:|--------------------:|----------------:|--------------------------:|--------------------------:|-------------------------------------:|-------------------:|-----------------:|--------------------------------:|------------------------------:|------------------------------------:|-------------------:|-------------------:|---------------------------:|--------------------:|----------------------------------:|------------------------------------:|--------------------------------:|:-----------------------------------|:-----------------------------------------------|:-----------------------------|-------------:|------------:|-------------:|:---------------------------------------|-----------------------------------------:|---------------------:|----------------------------------:|--------------------------:|---------------------:|------------------------:|:--------------------|--------------------------:|:--------------------|-----------------------------------------:|----------------------------:|--------------------:|---------------------:|--------------------------------------:|-----------------------------------------------:|---------------:|----------------------------------------------:|----------------------------:|----------------------:|-----------------------------------------:|-------------:|------------:|--------:|--------------:|---------:|-------------:|-----------:|------------:|-----------------------:|-------------:|----------------------:|
| HA-20230316-009   | 2023-03-16 00:00:00  | No Loss / No Injury                       | Projects   | One Desiccator fell down from the height of 10ft. at HPO Product tankform south side area. | Closed   | Hazard ID  | Around 1235 hrs. at Product tank southside PR, during the shifting of electrode welding rod oven wit... | Engro Polymer and Chemicals | Karachi    | Projects and BD        | HPO          | HPO Contstruction  | HPO               |                nan |            nan |                               nan |                 nan | 190, Mechanical (Projects) & Civil | 12:00:00        | No               |               nan |                               nan |                   nan |                             nan |                nan |                nan | Majid Khan - EPCL P&BD | 2023-03-20 00:00:00 | 2023-03-20 00:00:00 |                                 nan |                             nan |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan |                         nan |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan |                         nan |                      nan |                                                                    nan |                  nan |                     nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |                                nan |   nan |   nan |    nan |          nan |               nan |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan |            nan |                  nan |                 nan |             nan |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan |                               nan |                                 nan |                             nan | People                             | C1 - Minor                                     | Unsafe Act                   |          nan |         nan |          nan | Muhammad Umar Shafiq - EPCL P&BD       |                                      nan |                  nan |                               nan |                       nan |                  nan |                     nan | 2023-03-20 00:00:00 |                       nan | 2023-04-05 00:00:00 |                                      nan |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan |          nan |                   nan |
| HA-20230318-004   | 2023-03-18 00:00:00  | Process Safety Event; No Loss / No Injury | Production | HP Jetting Pump PU-3105 recycle hose leakage                                               | Closed   | Hazard ID  | HP Jetting Pump PU-3105 recycle hose leakage observed.                                                  | Engro Polymer and Chemicals | Karachi    | Manufacturing Facility | PVC          | PVC III            | PVC III Feedstock |                nan |            nan |                               nan |                 nan | Not Applicable                     | 14:00:00        | No               |               nan |                               nan |                   nan |                             nan |                nan |                nan | Yasir Ali - EPCL Plant | 2023-04-03 00:00:00 | 2023-04-03 00:00:00 |                                 nan |                             nan |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan |                         nan |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan |                         nan |                      nan |                                                                    nan |                  nan |                     nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |                                nan |   nan |   nan |    nan |          nan |               nan |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan |            nan |                  nan |                 nan |             nan |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan |                               nan |                                 nan |                             nan | People                             | C2 - Serious                                   | Unsafe Condition             |          nan |         nan |          nan | Amer Ahmed - EPCL Plant                |                                      nan |                  nan |                               nan |                       nan |                  nan |                     nan | 2023-04-03 00:00:00 |                       nan | 2023-04-27 00:00:00 |                                      nan |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan |          nan |                   nan |
| HA-20230321-001   | 2023-03-21 00:00:00  | No Loss / No Injury                       | Projects   | At pipe rack area EEL subcontractor was observed using unapproved anti cut gloves at site  | Closed   | Hazard ID  | On 3/21/2023, At pipe rack area EEL subcontractor was observed using unapproved anti cut gloves at s... | Engro Polymer and Chemicals | Karachi    | Projects and BD        | HPO          | HPO Contstruction  | HPO Process Area  |                nan |            nan |                               nan |                 nan | 190, Mechanical (Projects) & Civil | 10:00:00        | No               |               nan |                               nan |                   nan |                             nan |                nan |                nan | Majid Khan - EPCL P&BD | 2023-03-23 00:00:00 | 2023-03-23 00:00:00 |                                 nan |                             nan |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan |                         nan |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan |                         nan |                      nan |                                                                    nan |                  nan |                     nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |                                nan |   nan |   nan |    nan |          nan |               nan |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan |            nan |                  nan |                 nan |             nan |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan |                               nan |                                 nan |                             nan | People                             | C1 - Minor                                     | Safety Rule Violation        |          nan |         nan |          nan | Muhammad Umar Shafiq - EPCL P&BD       |                                      nan |                  nan |                               nan |                       nan |                  nan |                     nan | 2023-03-23 00:00:00 |                       nan | 2023-03-31 00:00:00 |                                      nan |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan |          nan |                   nan |
| HA-20230321-002   | 2023-03-21 00:00:00  | No Loss / No Injury                       | Projects   | EPIC fabricator was using grinder at HTDC layout-II without obtaining hot permit           | Closed   | Hazard ID  | Self-reporting: On 21st Mar 2023, It was observed that during hot job arrangements EPIC fabricator (... | Engro Polymer and Chemicals | Karachi    | Projects and BD        | HTDC         | HTDC Contstruction | HTDC              |                nan |            nan |                               nan |                 nan | 190, Mechanical (Projects) & Civil | 10:00:00        | No               |               nan |                               nan |                   nan |                             nan |                nan |                nan | Majid Khan - EPCL P&BD | 2023-03-23 00:00:00 | 2023-03-23 00:00:00 |                                 nan |                             nan |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan |                         nan |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan |                         nan |                      nan |                                                                    nan |                  nan |                     nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |                                nan |   nan |   nan |    nan |          nan |               nan |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan |            nan |                  nan |                 nan |             nan |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan |                               nan |                                 nan |                             nan | People                             | C2 - Serious                                   | Unsafe Act                   |          nan |         nan |          nan | Ammar Ahmad - EPCL P&BD                |                                      nan |                  nan |                               nan |                       nan |                  nan |                     nan | 2023-03-23 00:00:00 |                       nan | 2023-04-04 00:00:00 |                                      nan |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan |          nan |                   nan |
| HA-20230322-003   | 2023-03-22 00:00:00  | Other                                     | Projects   | EEL admin team members were not having escape mask while sitting in the containers         | Closed   | Hazard ID  | On 22nd Mar 2023, At EEL office Area during audit it was observed that in EEL admin office there was... | Engro Polymer and Chemicals | Karachi    | Projects and BD        | HPO          | HPO Contstruction  | Container Offices |                nan |            nan |                               nan |                 nan | 190, Mechanical (Projects) & Civil | 11:00:00        | No               |               nan |                               nan |                   nan |                             nan |                nan |                nan | Majid Khan - EPCL P&BD | 2023-03-23 00:00:00 | 2023-03-23 00:00:00 |                                 nan |                             nan |                                    nan |                                                         nan |                                        nan |                   nan |                                 nan |                      nan |                    nan |                          nan |                         nan |                      nan |                     nan |                 nan |           nan |                                             nan |                                    nan |                                               nan |                                      nan |                    nan |                     nan |              nan |                 nan |              nan |                         nan |                      nan |                                                                    nan |                  nan |                     nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |      nan |         nan |                                nan |   nan |   nan |    nan |          nan |               nan |                   nan |         nan |             nan |              nan |             nan |         nan |         nan |                    nan |                      nan |        nan |                    nan |          nan |                 nan |                nan |           nan |                 nan |                  nan |                    nan |                     nan |               nan |         nan |               nan |                 nan |                          nan |                      nan |                   nan |            nan |                 nan |                           nan |         nan |                                 nan |            nan |                    nan |           nan |              nan |             nan |                 nan |            nan |                  nan |                 nan |             nan |                       nan |                       nan |                                  nan |                nan |              nan |                             nan |                           nan |                                 nan |                nan |                nan |                        nan |                 nan |                               nan |                                 nan |                             nan | People                             | C2 - Serious                                   | Safety Rule Violation        |          nan |         nan |          nan | Muhammad Umar Shafiq - EPCL P&BD       |                                      nan |                  nan |                               nan |                       nan |                  nan |                     nan | 2023-03-23 00:00:00 |                       nan | 2023-03-31 00:00:00 |                                      nan |                         nan |                 nan |                  nan |                                   nan |                                            nan |            nan |                                           nan |                         nan |                   nan |                                      nan |          nan |         nan |     nan |           nan |      nan |          nan |        nan |         nan |                    nan |          nan |                   nan |

---

## Audit

**Total Columns:** 50
**Total Rows:** 1522
**Sample Rows:** 5

### Data Types and Sample Values

| Column | Data Type | Non-Null Count | Sample Values |
|--------|-----------|----------------|---------------|
| Audit Number | object | 1522/1522 | AU-20230101-001, AU-20230130-001, AU-20230131-002 |
| Audit Location | object | 1522/1522 | CA, Manufacturing Facility, Asset Integrity |
| Audit Title | object | 1522/1522 | Hydrogen vent stack falme arrestor inspection RMA, Marsh Insurance Audit, Marsh Audit 2023 - Inspection Deep Dive (IDD) |
| Auditor | object | 1522/1522 | Ghulam Murtaza - EPCL Plant, Ahtisham Qadir Malik - EPCL Plant, Junaid Rafey - EPCL Plant |
| Start Date | datetime64[ns] | 1522/1522 | 2023-01-01 00:00:00, 2023-01-30 00:00:00, 2023-01-31 00:00:00 |
| Audit Status | object | 1522/1522 | Closed, Action Plan Review, Pending Action Plan |
| Location Tag | float64 | 0/1522 |  |
| Audit Category | object | 1522/1522 | Audit |
| Auditing Body | object | 1522/1522 | Self, 3rd Party, 1st Party |
| Audit Rating | object | 401/1522 | Satisfactory, Significant Improvement Required, Enhancement Required |
| Group Company | object | 1522/1522 | EPCL |
| Location (EPCL) | object | 1522/1522 | CA-1650 and HCL Loading, Admin Building, EVCM 300 |
| Audit Type (EPCL) | object | 1522/1522 | 119-Internal Audit, 16-Insurance Audit, 82-Piping, Piping supports and Equipment Condition... |
| Template | object | 1522/1522 | General Audit Check List, RMA - Scaffolding Checklist (HSE), Job Cycle Check (JCC) Evaluation Form [FORM # SAF-... |
| Template Version | object | 1522/1522 | Current Version |
| Created By | object | 1522/1522 | Ghulam Murtaza - EPCL Plant, Safeer Hussain - ECORP KHI HO, Ghulam Muzammil - EPCL Plant |
| Audit Team | object | 1514/1522 | Moin Nasir - EPCL Plant, Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq ..., Muhammad Shoquaib Farooq - EPCL Plant |
| Supervisor | float64 | 0/1522 |  |
| Responsible for Action Plan | object | 1511/1522 | Ahtisham Qadir Malik - EPCL Plant, Safeer Hussain - ECORP KHI HO, Ghulam Muzammil - EPCL Plant |
| Responsible for Action Plan Review | object | 1510/1522 | Ahtisham Qadir Malik - EPCL Plant, Safeer Hussain - ECORP KHI HO, Junaid Rafey - EPCL Plant |
| Entered Scheduled | datetime64[ns] | 1100/1522 | 2023-09-27 00:00:00, 2023-05-25 00:00:00, 2023-03-29 00:00:00 |
| Entered In Progress | datetime64[ns] | 1513/1522 | 2023-09-27 00:00:00, 2023-05-25 00:00:00, 2023-10-24 00:00:00 |
| Entered Review | datetime64[ns] | 1322/1522 | 2023-09-27 00:00:00, 2023-05-29 00:00:00, 2023-10-24 00:00:00 |
| Entered Pending Action Plan | object | 1484/1522 | 2023-09-27 00:00:00, 2023-12-31 00:00:00, 2023-10-24 00:00:00 |
| Entered Review Action Plan | object | 1457/1522 | 2023-09-29 00:00:00, 2024-04-08 00:00:00, 2023-10-24 00:00:00 |
| Entered Pending Closure | object | 1442/1522 | 2023-09-29 00:00:00, 2024-05-11 00:00:00, 2023-10-24 00:00:00 |
| Entered Closed | datetime64[ns] | 1350/1522 | 2023-09-30 00:00:00, 2025-05-31 00:00:00, 2023-12-30 00:00:00 |
| Checklist Category | object | 1154/1522 | General Audit Check List, RMA - Scaffolding Checklist (HSE); RMA - Scaffoldi..., Job Cycle Check (JCC) Evaluation Form [FORM # SAF-... |
| Question | object | 1154/1522 | Audit Type, Check scaffolding material transportation criteria..., Is there a written procedure available for this ta... |
| Regulatory Reference | object | 127/1522 | ; ; ; ; ; ; ; ; ; ..., ; ; ; ; ; ; ; ; , ;  |
| Help Text | object | 1153/1522 | Just add audit type here and attach soft copy of a..., Spot check any activity. If OK rating is 1.0; If n..., ; ; ; ; ; ; ; ;  |
| Answer | object | 650/1522 | Insurance Survey Audit, RMA, 0 - Lowest Score; 0 - Lowest Score; 0 - Lowest Sco... |
| Recommendation | object | 226/1522 | All trollies tyres, side railing, moving handle, b..., To conduct awareness session with shift engineers ..., Communicated to contractor supervisor for segregat... |
| Response | object | 128/1522 | ; ; ; ; ; ; ; ; ; ..., ; ; ; ; ; ; ; ; , in progress  |
| Finding | object | 767/1522 | It was observed that maintenance KPIs have improve..., 23.01 Management of piping reaching end of service..., Refer attached file  |
| Finding Location | object | 820/1522 | Maintenance; Health, Safety and Environment; Healt..., Asset Integrity; Asset Integrity, Engro Polymer and Chemicals |
| Worst Case Consequence | object | 222/1522 | C2 - Serious; C3 - Severe; C3 - Severe; C2 - Serio..., ; , C1 - Minor; C1 - Minor |
| Action Item Number | object | 63/1522 | AC-AUD-20230529-001; AC-AUD-20230529-002; AC-AUD-2..., AC-AUD-20231024-007; AC-AUD-20231024-008; AC-AUD-2..., AC-AUD-20230411-002 |
| Action Item Title | object | 63/1522 | Enhance Maintenance KPIs (Marsh Audit Recommendati..., Management piping reaching end of service life; Pi..., Quality Esurance Check list after cleaning. |
| Action Item Description | object | 63/1522 | It is recommended to: Enhance the Maintenance KPIs..., • During the transition phase towards a new data m..., please develop the quality insurance check list, t... |
| Action Item Responsible | object | 63/1522 | Qamar Jaleel - EPCL Plant; Safeer Hussain - ECORP ..., Safeer Hussain - ECORP KHI HO; Safeer Hussain - EC..., Mazhar Ali - EPCL Plant |
| Action Item Delegated | object | 43/1522 | Umair Aslam - EPCL Plant; Muhammad Ali Shah - EPCL..., ; ; ; , Shaukat Hussain - EPCL Plant |
| Action Item Responsible for Verification | object | 62/1522 | Qamar Jaleel - EPCL Plant; Muhammad Ali Shah - EPC..., Junaid Rafey - EPCL Plant; Sajjad Muneer Alvi - EP..., Zafar Ali - EPCL Plant |
| Action Item Effective? | object | 48/1522 | ; Yes; Yes; Yes; Yes, Yes; Yes; Yes; , Yes; Yes; Yes |
| Action Item Verification Details | object | 47/1522 | ; Yes; Training session to improve ICC compliance ..., Yes; Must appreciate Inspection for doing a great ..., All materials have been properly transportation; A... |
| Action Item Priority | object | 60/1522 | C2, C3 - Medium; C4 - High; C2, C3 - Medium; C2, C..., C4 - High; C4 - High; C4 - High; C4 - High, C0, C1 - Low |
| Action Item Due Date | object | 63/1522 | 2023-09-30; 2024-09-30; 2023-09-30; 2023-09-30; 20..., 2023-11-30; 2024-12-31; 2023-12-31; 2026-12-31, 2023-05-31 00:00:00 |
| Action Item Verification Due Date | object | 26/1522 | ; ; ; ; , ; ; ; , ; ;  |
| Action Item Status | object | 63/1522 | Closed; Closed; Closed; Closed; Closed, Closed; Closed; Closed; Completion, Closed |
| Action Item Progress Notes | object | 62/1522 | 1. Plant Maintenance KPIs have been enhanced, they..., Total lines having remaining life less than 02 yea..., Checklist has been developed for drinking water ta... |

### Numeric Column Statistics

| Column | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|

### Categorical Columns Summary

**Audit Status** (7 unique values):

- Closed: 1350
- Pending Closure: 91
- Pending Action Plan: 28
- In Progress: 18
- Action Plan Review: 15
- Review: 11
- Scheduled: 9

**Auditing Body** (4 unique values):

- 1st Party: 903
- Self: 523
- 3rd Party: 57
- 2nd Party: 39

**Audit Rating** (3 unique values):

- Satisfactory: 390
- Enhancement Required: 7
- Significant Improvement Required: 4

**Template** (3 unique values):

- General Audit Check List: 1392
- Job Cycle Check (JCC) Evaluation Form [FORM # SAF-...: 121
- RMA - Scaffolding Checklist (HSE): 9

### Sample Data (First 5 Rows)

| Audit Number    | Audit Location              | Audit Title                                                                                   | Auditor                           | Start Date          | Audit Status   |   Location Tag | Audit Category   | Auditing Body   | Audit Rating   | Group Company   | Location (EPCL)         | Audit Type (EPCL)                                                  | Template                 | Template Version   | Created By                    | Audit Team                                                                                         |   Supervisor | Responsible for Action Plan       | Responsible for Action Plan Review   | Entered Scheduled   | Entered In Progress   | Entered Review      | Entered Pending Action Plan   | Entered Review Action Plan   | Entered Pending Closure   | Entered Closed      | Checklist Category       | Question   |   Regulatory Reference | Help Text                                                                                               | Answer                 |   Recommendation |   Response | Finding                                                                                                 | Finding Location                                                                                        | Worst Case Consequence                                            | Action Item Number                                                                                      | Action Item Title                                                                                       | Action Item Description                                                                                 | Action Item Responsible                                                                                 | Action Item Delegated                                                                                   | Action Item Responsible for Verification                                                                | Action Item Effective?   | Action Item Verification Details                                                                        | Action Item Priority                                                    | Action Item Due Date                                       | Action Item Verification Due Date   | Action Item Status                     | Action Item Progress Notes                                                                              |
|:----------------|:----------------------------|:----------------------------------------------------------------------------------------------|:----------------------------------|:--------------------|:---------------|---------------:|:-----------------|:----------------|:---------------|:----------------|:------------------------|:-------------------------------------------------------------------|:-------------------------|:-------------------|:------------------------------|:---------------------------------------------------------------------------------------------------|-------------:|:----------------------------------|:-------------------------------------|:--------------------|:----------------------|:--------------------|:------------------------------|:-----------------------------|:--------------------------|:--------------------|:-------------------------|:-----------|-----------------------:|:--------------------------------------------------------------------------------------------------------|:-----------------------|-----------------:|-----------:|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:-------------------------|:--------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|:-----------------------------------------------------------|:------------------------------------|:---------------------------------------|:--------------------------------------------------------------------------------------------------------|
| AU-20230101-001 | CA                          | Hydrogen vent stack falme arrestor inspection RMA                                             | Ghulam Murtaza - EPCL Plant       | 2023-01-01 00:00:00 | Closed         |            nan | Audit            | Self            | nan            | EPCL            | CA-1650 and HCL Loading | 119-Internal Audit                                                 | General Audit Check List | Current Version    | Ghulam Murtaza - EPCL Plant   | Moin Nasir - EPCL Plant                                                                            |          nan | Ahtisham Qadir Malik - EPCL Plant | Ahtisham Qadir Malik - EPCL Plant    | 2023-09-27 00:00:00 | 2023-09-27 00:00:00   | 2023-09-27 00:00:00 | 2023-09-27 00:00:00           | 2023-09-29 00:00:00          | 2023-09-29 00:00:00       | 2023-09-30 00:00:00 | General Audit Check List | Audit Type |                    nan | Just add audit type here and attach soft copy of audit / checklist as attachment. Finding /Recommend... | nan                    |              nan |        nan | nan                                                                                                     | nan                                                                                                     | nan                                                               | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                      | nan                                                                                                     | nan                                                                     | nan                                                        | nan                                 | nan                                    | nan                                                                                                     |
| AU-20230130-001 | Manufacturing Facility      | Marsh Insurance Audit                                                                         | Ahtisham Qadir Malik - EPCL Plant | 2023-01-30 00:00:00 | Closed         |            nan | Audit            | 3rd Party       | nan            | EPCL            | Admin Building          | 16-Insurance Audit                                                 | General Audit Check List | Current Version    | Safeer Hussain - ECORP KHI HO | Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq - EPCL Plant; Muhammad Shahid Karim - EPCL Plant |          nan | Safeer Hussain - ECORP KHI HO     | Ahtisham Qadir Malik - EPCL Plant    | 2023-05-25 00:00:00 | 2023-05-25 00:00:00   | 2023-05-29 00:00:00 | 2023-12-31 00:00:00           | 2024-04-08 00:00:00          | 2024-05-11 00:00:00       | 2025-05-31 00:00:00 | General Audit Check List | Audit Type |                    nan | Just add audit type here and attach soft copy of audit / checklist as attachment. Finding /Recommend... | Insurance Survey Audit |              nan |        nan | It was observed that maintenance KPIs have improved since previous visit, but do not adequately show... | Maintenance; Health, Safety and Environment; Health, Safety and Environment; Process - UTY and PP; H... | C2 - Serious; C3 - Severe; C3 - Severe; C2 - Serious; C3 - Severe | AC-AUD-20230529-001; AC-AUD-20230529-002; AC-AUD-20230529-003; AC-AUD-20230529-004; AC-AUD-20230529-... | Enhance Maintenance KPIs (Marsh Audit Recommendation); Permit Accessibility and Cross-referencing ; ... | It is recommended to: Enhance the Maintenance KPIs to cover the following items. And consider additi... | Qamar Jaleel - EPCL Plant; Safeer Hussain - ECORP KHI HO; Safeer Hussain - ECORP KHI HO; Waqas Habib... | Umair Aslam - EPCL Plant; Muhammad Ali Shah - EPCL Plant; Muhammad Ali Shah - EPCL Plant; ; Muhammad... | Qamar Jaleel - EPCL Plant; Muhammad Ali Shah - EPCL Plant; Muhammad Shahid Karim - EPCL Plant; Muham... | ; Yes; Yes; Yes; Yes     | ; Yes; Training session to improve ICC compliance was done by AQM with production team. ; Hose pipe ... | C2, C3 - Medium; C4 - High; C2, C3 - Medium; C2, C3 - Medium; C4 - High | 2023-09-30; 2024-09-30; 2023-09-30; 2023-09-30; 2023-12-30 | ; ; ; ;                             | Closed; Closed; Closed; Closed; Closed | 1. Plant Maintenance KPIs have been enhanced, they were presented to management to include performan... |
| AU-20230131-002 | Asset Integrity             | Marsh Audit 2023 - Inspection Deep Dive (IDD)                                                 | Junaid Rafey - EPCL Plant         | 2023-01-31 00:00:00 | Closed         |            nan | Audit            | 3rd Party       | nan            | EPCL            | Admin Building          | 16-Insurance Audit                                                 | General Audit Check List | Current Version    | Ghulam Muzammil - EPCL Plant  | Muhammad Shoquaib Farooq - EPCL Plant                                                              |          nan | Ghulam Muzammil - EPCL Plant      | Safeer Hussain - ECORP KHI HO        | NaT                 | 2023-10-24 00:00:00   | 2023-10-24 00:00:00 | 2023-10-24 00:00:00           | 2023-10-24 00:00:00          | 2023-10-24 00:00:00       | 2023-12-30 00:00:00 | General Audit Check List | Audit Type |                    nan | Just add audit type here and attach soft copy of audit / checklist as attachment. Finding /Recommend... | nan                    |              nan |        nan | 23.01 Management of piping reaching end of service life 23.02 Piping lines that have not yet been in... | Asset Integrity; Asset Integrity                                                                        | ;                                                                 | AC-AUD-20231024-007; AC-AUD-20231024-008; AC-AUD-20231024-009; AC-AUD-20231024-010                      | Management piping reaching end of service life; Piping lines that have not yet been inspected; Devel... | • During the transition phase towards a new data management system the existing databases must be fu... | Safeer Hussain - ECORP KHI HO; Safeer Hussain - ECORP KHI HO; Safeer Hussain - ECORP KHI HO; Mohamma... | ; ; ;                                                                                                   | Junaid Rafey - EPCL Plant; Sajjad Muneer Alvi - EPCL Plant; Junaid Rafey - EPCL Plant;                  | Yes; Yes; Yes;           | Yes; Must appreciate Inspection for doing a great job! ; ;                                              | C4 - High; C4 - High; C4 - High; C4 - High                              | 2023-11-30; 2024-12-31; 2023-12-31; 2026-12-31             | ; ; ;                               | Closed; Closed; Closed; Completion     | Total lines having remaining life less than 02 years already have a temporary repair (TR) installed ... |
| AU-20230301-004 | Engro Polymer and Chemicals | RMA Audit: Piping, Piping supports and Equipment Conditions related audits (For EDC-VCM unit) | Syed Tauseef Ali - EPCL Plant     | 2023-03-01 00:00:00 | Closed         |            nan | Audit            | 1st Party       | Satisfactory   | EPCL            | EVCM 300                | 82-Piping, Piping supports and Equipment Conditions related audits | General Audit Check List | Current Version    | Syed Tauseef Ali - EPCL Plant | Junaid Rafey - EPCL Plant                                                                          |          nan | Junaid Rafey - EPCL Plant         | Junaid Rafey - EPCL Plant            | 2023-03-29 00:00:00 | 2023-03-29 00:00:00   | 2023-03-29 00:00:00 | 2023-03-29 00:00:00           | 2023-03-29 00:00:00          | 2023-03-29 00:00:00       | 2023-03-31 00:00:00 | General Audit Check List | Audit Type |                    nan | Just add audit type here and attach soft copy of audit / checklist as attachment. Finding /Recommend... | nan                    |              nan |        nan | Refer attached file                                                                                     | Engro Polymer and Chemicals                                                                             | nan                                                               | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                      | nan                                                                                                     | nan                                                                     | nan                                                        | nan                                 | nan                                    | nan                                                                                                     |
| AU-20230301-005 | Engro Polymer and Chemicals | RMA Audit: Temporary repair field health assessment (For EDC-VCM unit)                        | Syed Tauseef Ali - EPCL Plant     | 2023-03-01 00:00:00 | Closed         |            nan | Audit            | 1st Party       | Satisfactory   | EPCL            | EVCM 300                | 74-Temporary Repair Field Health Assessment                        | General Audit Check List | Current Version    | Syed Tauseef Ali - EPCL Plant | Junaid Rafey - EPCL Plant; Syed Tauseef Ali - EPCL Plant                                           |          nan | Junaid Rafey - EPCL Plant         | Junaid Rafey - EPCL Plant            | 2023-03-29 00:00:00 | 2023-03-29 00:00:00   | 2023-03-29 00:00:00 | 2023-03-29 00:00:00           | 2023-03-29 00:00:00          | 2023-03-29 00:00:00       | 2023-03-31 00:00:00 | General Audit Check List | Audit Type |                    nan | Just add audit type here and attach soft copy of audit / checklist as attachment. Finding /Recommend... | nan                    |              nan |        nan | Refer attached file; Refer attached file                                                                | Engro Polymer and Chemicals; Engro Polymer and Chemicals                                                | C1 - Minor; C1 - Minor                                            | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                                                                                                     | nan                      | nan                                                                                                     | nan                                                                     | nan                                                        | nan                                 | nan                                    | nan                                                                                                     |

---

## Audit Findings

**Total Columns:** 50
**Total Rows:** 1031
**Sample Rows:** 5

### Data Types and Sample Values

| Column | Data Type | Non-Null Count | Sample Values |
|--------|-----------|----------------|---------------|
| Audit Number | object | 1031/1031 | AU-20230130-001, AU-20230131-002, AU-20230301-004 |
| Audit Location | object | 1031/1031 | Manufacturing Facility, Asset Integrity, Engro Polymer and Chemicals |
| Audit Title | object | 1031/1031 | Marsh Insurance Audit, Marsh Audit 2023 - Inspection Deep Dive (IDD), RMA Audit: Piping, Piping supports and Equipment C... |
| Auditor | object | 1031/1031 | Ahtisham Qadir Malik - EPCL Plant, Junaid Rafey - EPCL Plant, Syed Tauseef Ali - EPCL Plant |
| Start Date | datetime64[ns] | 1031/1031 | 2023-01-30 00:00:00, 2023-01-31 00:00:00, 2023-03-01 00:00:00 |
| Audit Status | object | 1031/1031 | Closed, Action Plan Review, Pending Action Plan |
| Location Tag | float64 | 0/1031 |  |
| Audit Category | object | 1031/1031 | Audit |
| Auditing Body | object | 1031/1031 | 3rd Party, 1st Party, Self |
| Audit Rating | object | 319/1031 | Satisfactory, Significant Improvement Required, Enhancement Required |
| Group Company | object | 1031/1031 | EPCL |
| Location (EPCL) | object | 1031/1031 | Admin Building, EVCM 300, UTY Area 1 |
| Audit Type (EPCL) | object | 1031/1031 | 16-Insurance Audit, 82-Piping, Piping supports and Equipment Condition..., 74-Temporary Repair Field Health Assessment |
| Template | object | 1031/1031 | General Audit Check List, RMA - Scaffolding Checklist (HSE), Job Cycle Check (JCC) Evaluation Form [FORM # SAF-... |
| Template Version | object | 1031/1031 | Current Version |
| Created By | object | 1031/1031 | Safeer Hussain - ECORP KHI HO, Ghulam Muzammil - EPCL Plant, Syed Tauseef Ali - EPCL Plant |
| Audit Team | object | 1029/1031 | Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq ..., Muhammad Shoquaib Farooq - EPCL Plant, Junaid Rafey - EPCL Plant |
| Supervisor | float64 | 0/1031 |  |
| Responsible for Action Plan | object | 1025/1031 | Safeer Hussain - ECORP KHI HO, Ghulam Muzammil - EPCL Plant, Junaid Rafey - EPCL Plant |
| Responsible for Action Plan Review | object | 1025/1031 | Ahtisham Qadir Malik - EPCL Plant, Safeer Hussain - ECORP KHI HO, Junaid Rafey - EPCL Plant |
| Entered Scheduled | datetime64[ns] | 711/1031 | 2023-05-25 00:00:00, 2023-03-29 00:00:00, 2023-03-31 00:00:00 |
| Entered In Progress | datetime64[ns] | 1031/1031 | 2023-05-25 00:00:00, 2023-10-24 00:00:00, 2023-03-29 00:00:00 |
| Entered Review | datetime64[ns] | 886/1031 | 2023-05-29 00:00:00, 2023-10-24 00:00:00, 2023-03-29 00:00:00 |
| Entered Pending Action Plan | object | 1018/1031 | 2023-12-31 00:00:00, 2023-10-24 00:00:00, 2023-03-29 00:00:00 |
| Entered Review Action Plan | object | 994/1031 | 2024-04-08 00:00:00, 2023-10-24 00:00:00, 2023-03-29 00:00:00 |
| Entered Pending Closure | object | 986/1031 | 2024-05-11 00:00:00, 2023-10-24 00:00:00, 2023-03-29 00:00:00 |
| Entered Closed | datetime64[ns] | 904/1031 | 2025-05-31 00:00:00, 2023-12-30 00:00:00, 2023-03-31 00:00:00 |
| Checklist Category | object | 420/1031 | General Audit Check List, RMA - Scaffolding Checklist (HSE), Job Cycle Check (JCC) Evaluation Form [FORM # SAF-... |
| Question | object | 420/1031 | Audit Type, Check means of transportation of scaffolding mater..., Ensure Induction & refresher trainings of scaffold... |
| Regulatory Reference | float64 | 0/1031 |  |
| Help Text | object | 412/1031 | Just add audit type here and attach soft copy of a..., If OK rating is 1.0; If not rating is 0.0., Spot check any activity. If OK rating is 1.0; If n... |
| Answer | object | 150/1031 | RMA, 0 - Lowest Score, 1 - Highest Score |
| Recommendation | object | 114/1031 | Refresher training sessions are required for all c..., All trollies tyres, side railing, moving handle, b..., Proper storage mechanism to be devised and impleme... |
| Response | object | 2/1031 | ok, Hose handling and management guidelines issued at ... |
| Finding | object | 933/1031 | It was observed that permits: Are currently stored..., It was observed that on the A-300 Furnace isolatio..., It was observed that, the site permit audits did n... |
| Finding Location | object | 1031/1031 | Health, Safety and Environment, Maintenance, Process - UTY and PP |
| Worst Case Consequence | object | 160/1031 | C3 - Severe, C2 - Serious, C1 - Minor |
| Action Item Number | object | 10/1031 | AC-AUD-20230322-003, AC-AUD-20230322-001, AC-AUD-20230322-002 |
| Action Item Title | object | 10/1031 | Scaffolding trollies health were found unsatisfact..., Mentioning of load during transport of scaffold ma..., Scaffolding material storage provision |
| Action Item Description | object | 10/1031 | Scaffolding trolleys to be ensured in healthy cond..., All trollies tyres, side railing, moving handle, b..., Proper storage mechanism to be devised and impleme... |
| Action Item Responsible | object | 10/1031 | Akbar Ali - EPCL Plant, Umair Aslam - EPCL Plant, Khalid Shahzad Abid - EPCL Plant |
| Action Item Delegated | object | 4/1031 | Muhammad Saad - EPCL Plant, Muhammad Saim Khan - EPCL Plant |
| Action Item Responsible for Verification | object | 10/1031 | Akbar Ali - EPCL Plant, Umair Aslam - EPCL Plant, Zafar Ali - EPCL Plant |
| Action Item Effective? | object | 9/1031 | Yes |
| Action Item Verification Details | object | 9/1031 | All unhealthy trollyies replaced with new one, All materials have been properly transportation, All material properly managed |
| Action Item Priority | object | 9/1031 | C0, C1 - Low, C2, C3 - Medium |
| Action Item Due Date | datetime64[ns] | 10/1031 | 2023-12-31 00:00:00, 2023-05-31 00:00:00, 2023-06-30 00:00:00 |
| Action Item Verification Due Date | float64 | 0/1031 |  |
| Action Item Status | object | 10/1031 | Closed |
| Action Item Progress Notes | object | 10/1031 | All unhealthy trollies replaced with new one, All points have been closed., All trolleys' tires, side railings, moving handles... |

### Numeric Column Statistics

| Column | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|

### Categorical Columns Summary

**Audit Status** (6 unique values):

- Closed: 904
- Pending Closure: 82
- Pending Action Plan: 24
- Action Plan Review: 8
- In Progress: 8
- Review: 5

**Auditing Body** (4 unique values):

- 1st Party: 671
- Self: 266
- 3rd Party: 50
- 2nd Party: 44

**Audit Rating** (3 unique values):

- Satisfactory: 308
- Significant Improvement Required: 7
- Enhancement Required: 4

**Template** (3 unique values):

- General Audit Check List: 992
- Job Cycle Check (JCC) Evaluation Form [FORM # SAF-...: 32
- RMA - Scaffolding Checklist (HSE): 7

### Sample Data (First 5 Rows)

| Audit Number    | Audit Location         | Audit Title           | Auditor                           | Start Date          | Audit Status   |   Location Tag | Audit Category   | Auditing Body   |   Audit Rating | Group Company   | Location (EPCL)   | Audit Type (EPCL)   | Template                 | Template Version   | Created By                    | Audit Team                                                                                         |   Supervisor | Responsible for Action Plan   | Responsible for Action Plan Review   | Entered Scheduled   | Entered In Progress   | Entered Review      | Entered Pending Action Plan   | Entered Review Action Plan   | Entered Pending Closure   | Entered Closed      |   Checklist Category |   Question |   Regulatory Reference |   Help Text |   Answer |   Recommendation |   Response | Finding                                                                                                 | Finding Location               | Worst Case Consequence   |   Action Item Number |   Action Item Title |   Action Item Description |   Action Item Responsible |   Action Item Delegated |   Action Item Responsible for Verification |   Action Item Effective? |   Action Item Verification Details |   Action Item Priority | Action Item Due Date   |   Action Item Verification Due Date |   Action Item Status |   Action Item Progress Notes |
|:----------------|:-----------------------|:----------------------|:----------------------------------|:--------------------|:---------------|---------------:|:-----------------|:----------------|---------------:|:----------------|:------------------|:--------------------|:-------------------------|:-------------------|:------------------------------|:---------------------------------------------------------------------------------------------------|-------------:|:------------------------------|:-------------------------------------|:--------------------|:----------------------|:--------------------|:------------------------------|:-----------------------------|:--------------------------|:--------------------|---------------------:|-----------:|-----------------------:|------------:|---------:|-----------------:|-----------:|:--------------------------------------------------------------------------------------------------------|:-------------------------------|:-------------------------|---------------------:|--------------------:|--------------------------:|--------------------------:|------------------------:|-------------------------------------------:|-------------------------:|-----------------------------------:|-----------------------:|:-----------------------|------------------------------------:|---------------------:|-----------------------------:|
| AU-20230130-001 | Manufacturing Facility | Marsh Insurance Audit | Ahtisham Qadir Malik - EPCL Plant | 2023-01-30 00:00:00 | Closed         |            nan | Audit            | 3rd Party       |            nan | EPCL            | Admin Building    | 16-Insurance Audit  | General Audit Check List | Current Version    | Safeer Hussain - ECORP KHI HO | Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq - EPCL Plant; Muhammad Shahid Karim - EPCL Plant |          nan | Safeer Hussain - ECORP KHI HO | Ahtisham Qadir Malik - EPCL Plant    | 2023-05-25 00:00:00 | 2023-05-25 00:00:00   | 2023-05-29 00:00:00 | 2023-12-31 00:00:00           | 2024-04-08 00:00:00          | 2024-05-11 00:00:00       | 2025-05-31 00:00:00 |                  nan |        nan |                    nan |         nan |      nan |              nan |        nan | It was observed that permits: Are currently stored outside, not immediately accessible at the work-f... | Health, Safety and Environment | C3 - Severe              |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan | NaT                    |                                 nan |                  nan |                          nan |
| AU-20230130-001 | Manufacturing Facility | Marsh Insurance Audit | Ahtisham Qadir Malik - EPCL Plant | 2023-01-30 00:00:00 | Closed         |            nan | Audit            | 3rd Party       |            nan | EPCL            | Admin Building    | 16-Insurance Audit  | General Audit Check List | Current Version    | Safeer Hussain - ECORP KHI HO | Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq - EPCL Plant; Muhammad Shahid Karim - EPCL Plant |          nan | Safeer Hussain - ECORP KHI HO | Ahtisham Qadir Malik - EPCL Plant    | 2023-05-25 00:00:00 | 2023-05-25 00:00:00   | 2023-05-29 00:00:00 | 2023-12-31 00:00:00           | 2024-04-08 00:00:00          | 2024-05-11 00:00:00       | 2025-05-31 00:00:00 |                  nan |        nan |                    nan |         nan |      nan |              nan |        nan | It was observed that on the A-300 Furnace isolation plan, a spool removal was not captured on the is... | Health, Safety and Environment | C3 - Severe              |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan | NaT                    |                                 nan |                  nan |                          nan |
| AU-20230130-001 | Manufacturing Facility | Marsh Insurance Audit | Ahtisham Qadir Malik - EPCL Plant | 2023-01-30 00:00:00 | Closed         |            nan | Audit            | 3rd Party       |            nan | EPCL            | Admin Building    | 16-Insurance Audit  | General Audit Check List | Current Version    | Safeer Hussain - ECORP KHI HO | Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq - EPCL Plant; Muhammad Shahid Karim - EPCL Plant |          nan | Safeer Hussain - ECORP KHI HO | Ahtisham Qadir Malik - EPCL Plant    | 2023-05-25 00:00:00 | 2023-05-25 00:00:00   | 2023-05-29 00:00:00 | 2023-12-31 00:00:00           | 2024-04-08 00:00:00          | 2024-05-11 00:00:00       | 2025-05-31 00:00:00 |                  nan |        nan |                    nan |         nan |      nan |              nan |        nan | It was observed that, the site permit audits did not highlight items identified in 23.02 and 23.03. ... | Health, Safety and Environment | C3 - Severe              |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan | NaT                    |                                 nan |                  nan |                          nan |
| AU-20230130-001 | Manufacturing Facility | Marsh Insurance Audit | Ahtisham Qadir Malik - EPCL Plant | 2023-01-30 00:00:00 | Closed         |            nan | Audit            | 3rd Party       |            nan | EPCL            | Admin Building    | 16-Insurance Audit  | General Audit Check List | Current Version    | Safeer Hussain - ECORP KHI HO | Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq - EPCL Plant; Muhammad Shahid Karim - EPCL Plant |          nan | Safeer Hussain - ECORP KHI HO | Ahtisham Qadir Malik - EPCL Plant    | 2023-05-25 00:00:00 | 2023-05-25 00:00:00   | 2023-05-29 00:00:00 | 2023-12-31 00:00:00           | 2024-04-08 00:00:00          | 2024-05-11 00:00:00       | 2025-05-31 00:00:00 |                  nan |        nan |                    nan |         nan |      nan |              nan |        nan | It was observed that maintenance KPIs have improved since previous visit, but do not adequately show... | Maintenance                    | C2 - Serious             |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan | NaT                    |                                 nan |                  nan |                          nan |
| AU-20230130-001 | Manufacturing Facility | Marsh Insurance Audit | Ahtisham Qadir Malik - EPCL Plant | 2023-01-30 00:00:00 | Closed         |            nan | Audit            | 3rd Party       |            nan | EPCL            | Admin Building    | 16-Insurance Audit  | General Audit Check List | Current Version    | Safeer Hussain - ECORP KHI HO | Junaid Rafey - EPCL Plant; Muhammad Ashar Mushtaq - EPCL Plant; Muhammad Shahid Karim - EPCL Plant |          nan | Safeer Hussain - ECORP KHI HO | Ahtisham Qadir Malik - EPCL Plant    | 2023-05-25 00:00:00 | 2023-05-25 00:00:00   | 2023-05-29 00:00:00 | 2023-12-31 00:00:00           | 2024-04-08 00:00:00          | 2024-05-11 00:00:00       | 2025-05-31 00:00:00 |                  nan |        nan |                    nan |         nan |      nan |              nan |        nan | It was observed that there is currently a utility pump running, feeding into the firewater circuit f... | Process - UTY and PP           | C2 - Serious             |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan | NaT                    |                                 nan |                  nan |                          nan |

---

## Inspection

**Total Columns:** 50
**Total Rows:** 1773
**Sample Rows:** 5

### Data Types and Sample Values

| Column | Data Type | Non-Null Count | Sample Values |
|--------|-----------|----------------|---------------|
| Audit Number | object | 1773/1773 | IS-20230904-011, IS-20230904-013, IS-20230904-014 |
| Audit Location | object | 1773/1773 | HTDC Contstruction, Projects, Stationary - PVC |
| Audit Title | object | 1773/1773 | Management Safety Audit (MSA) |
| Auditor | object | 1773/1773 | Rafay Shahid - EPCL Plant, Arsslan Bhatti - EPCL P&BD, Ahrad Bin Riaz - EPCL Plant |
| Start Date | datetime64[ns] | 1773/1773 | 2023-09-04 00:00:00, 2023-09-05 00:00:00, 2023-09-06 00:00:00 |
| Audit Status | object | 1773/1773 | Closed, In Progress, Review |
| Location Tag | float64 | 0/1773 |  |
| Audit Category | object | 1773/1773 | Inspection |
| Auditing Body | object | 1772/1773 | Self, 1st Party, 2nd Party |
| Audit Rating | float64 | 0/1773 |  |
| Group Company | object | 1773/1773 | EPCL |
| Location (EPCL) | object | 1770/1773 | HTDC, PVC I Front End, HPO Product Tank farm Area |
| Audit Type (EPCL) | object | 1771/1773 | 6-MSA, 138-Executive MSA (EMSA), 28-JCC |
| Template | object | 1773/1773 | Management Safety Audit (MSA) |
| Template Version | object | 1773/1773 | Current Version |
| Created By | object | 1773/1773 | Rafay Shahid - EPCL Plant, Arsslan Bhatti - EPCL P&BD, Ahrad Bin Riaz - EPCL Plant |
| Audit Team | object | 422/1773 | Zafar Tariq - EPCL Plant, Muhammad Umer - EPCL Plant, Muhammad Irfan Alahi - EPCL Plant |
| Supervisor | float64 | 0/1773 |  |
| Responsible for Action Plan | float64 | 0/1773 |  |
| Responsible for Action Plan Review | float64 | 0/1773 |  |
| Entered Scheduled | datetime64[ns] | 580/1773 | 2023-09-27 00:00:00, 2023-10-01 00:00:00, 2023-10-02 00:00:00 |
| Entered In Progress | object | 1769/1773 | 2023-09-11 00:00:00, 2023-09-30 00:00:00, 2023-10-01 00:00:00 |
| Entered Review | object | 1722/1773 | 2023-09-11 00:00:00, 2023-09-30 00:00:00, 2023-10-01 00:00:00 |
| Entered Pending Action Plan | float64 | 0/1773 |  |
| Entered Review Action Plan | float64 | 0/1773 |  |
| Entered Pending Closure | float64 | 0/1773 |  |
| Entered Closed | datetime64[ns] | 1439/1773 | 2024-01-29 00:00:00, 2023-10-31 00:00:00, 2023-10-03 00:00:00 |
| Checklist Category | object | 1761/1773 | Conversation with Workforce / Personnel; Key Stren..., Conversation with Workforce / Personnel; Key Stren..., Conversation with Workforce / Personnel; Key Stren... |
| Question | object | 1761/1773 | The conversation took place with at least three (3..., The conversation took place with at least three (3..., The conversation took place with at least three (3... |
| Regulatory Reference | object | 1761/1773 | ; ; Unsafe Act is defined as Failure to Follow HSE..., ; ; Unsafe Act is defined as Failure to Follow HSE..., ; ; Unsafe Act is defined as Failure to Follow HSE... |
| Help Text | object | 1761/1773 | ; ; ; ; ; ; ; , ; ; ; , ; ; ; ; ; ;  |
| Answer | object | 1761/1773 | Yes; Yes; Yes; 8 - Position of People (Absorbing);..., Yes; PPE compliance; Yes; No; 2 - Tools & Equipmen..., Yes; PPE compliance; Yes; No; 2 - Tools & Equipmen... |
| Recommendation | object | 1761/1773 | ; ; ; ; ; ; ; , ; ; ; , ; ; ; ; ; ;  |
| Response | object | 1761/1773 | ; ; ; ; ; ; ; , ; ; ; , ; ; ; ; ; ;  |
| Finding | object | 1435/1773 | Cables were lying haphazardly in the area. Workers..., No any major damage / PPEs deficiency was observed..., Asif MW was working on cleaning of the nitrogen co... |
| Finding Location | object | 1438/1773 | HTDC Contstruction; HTDC Contstruction, Stationary - PVC, HPO; HPO |
| Worst Case Consequence | object | 854/1773 | ; , ; ; ; ; ; ; ; ; , ; ; ; ;  |
| Action Item Number | object | 168/1773 | AC-AUD-20230918-004, AC-AUD-20230919-023, AC-AUD-20230928-097 |
| Action Item Title | object | 166/1773 | Safety goggle was not wear by excavator driver., Door temporarily fixed as in close position to avo..., Communication with Relevant area |
| Action Item Description | object | 158/1773 | Counselling was done with driver about PPEs., CLO2 facility doors are broken from hinges, need t..., Immediately barricaded by the HFC team |
| Action Item Responsible | object | 168/1773 | Ahtisham Qadir Malik - EPCL Plant, Zafar Ali - EPCL Plant, Allah Dewaya Nasir - EPCL Plant |
| Action Item Delegated | object | 79/1773 | ; ; ; ; , ; ; , ;  |
| Action Item Responsible for Verification | object | 151/1773 | Ahtisham Qadir Malik - EPCL Plant, Habib Ullah Brohi - EPCL Plant, Allah Dewaya Nasir - EPCL Plant |
| Action Item Effective? | object | 150/1773 | Yes, Yes; Yes; Yes; Yes; Yes, Yes; Yes; Yes |
| Action Item Verification Details | object | 148/1773 | y, Counselling done, Housekeeping is necessary for all plant |
| Action Item Priority | object | 151/1773 | C2, C3 - Medium, C0, C1 - Low, C2, C3 - Medium; C2, C3 - Medium; C2, C3 - Medium;... |
| Action Item Due Date | object | 168/1773 | 2023-09-30 00:00:00, 2023-09-18 00:00:00, 2023-09-20 00:00:00 |
| Action Item Verification Due Date | object | 79/1773 | ; ; ; ; , ; ; , ;  |
| Action Item Status | object | 168/1773 | Closed, Dropped, Closed; Closed; Closed; Closed; Closed |
| Action Item Progress Notes | object | 151/1773 | Counselling was done, Door temporarily fixed as in close position to avo..., Done |

### Numeric Column Statistics

| Column | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|

### Categorical Columns Summary

**Audit Status** (4 unique values):

- Closed: 1439
- Review: 273
- In Progress: 57
- Scheduled: 4

**Auditing Body** (3 unique values):

- Self: 1672
- 1st Party: 98
- 2nd Party: 2

**Audit Type (EPCL)** (4 unique values):

- 6-MSA: 1766
- 22-Misc.: 3
- 138-Executive MSA (EMSA): 1
- 28-JCC: 1

### Sample Data (First 5 Rows)

| Audit Number    | Audit Location     | Audit Title                   | Auditor                     | Start Date          | Audit Status   |   Location Tag | Audit Category   | Auditing Body   |   Audit Rating | Group Company   | Location (EPCL)   | Audit Type (EPCL)   | Template                      | Template Version   | Created By                  | Audit Team               |   Supervisor |   Responsible for Action Plan |   Responsible for Action Plan Review | Entered Scheduled   | Entered In Progress   | Entered Review      |   Entered Pending Action Plan |   Entered Review Action Plan |   Entered Pending Closure | Entered Closed      | Checklist Category                                                                                      | Question                                                                                                | Regulatory Reference                                                                                    | Help Text     | Answer                                                                                                  | Recommendation   | Response      | Finding                                                                                                 | Finding Location                       | Worst Case Consequence   |   Action Item Number |   Action Item Title |   Action Item Description |   Action Item Responsible |   Action Item Delegated |   Action Item Responsible for Verification |   Action Item Effective? |   Action Item Verification Details |   Action Item Priority |   Action Item Due Date |   Action Item Verification Due Date |   Action Item Status |   Action Item Progress Notes |
|:----------------|:-------------------|:------------------------------|:----------------------------|:--------------------|:---------------|---------------:|:-----------------|:----------------|---------------:|:----------------|:------------------|:--------------------|:------------------------------|:-------------------|:----------------------------|:-------------------------|-------------:|------------------------------:|-------------------------------------:|:--------------------|:----------------------|:--------------------|------------------------------:|-----------------------------:|--------------------------:|:--------------------|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|:--------------|:--------------------------------------------------------------------------------------------------------|:-----------------|:--------------|:--------------------------------------------------------------------------------------------------------|:---------------------------------------|:-------------------------|---------------------:|--------------------:|--------------------------:|--------------------------:|------------------------:|-------------------------------------------:|-------------------------:|-----------------------------------:|-----------------------:|-----------------------:|------------------------------------:|---------------------:|-----------------------------:|
| IS-20230904-011 | HTDC Contstruction | Management Safety Audit (MSA) | Rafay Shahid - EPCL Plant   | 2023-09-04 00:00:00 | Closed         |            nan | Inspection       | Self            |            nan | EPCL            | HTDC              | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Rafay Shahid - EPCL Plant   | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-09-11 00:00:00   | 2023-09-11 00:00:00 |                           nan |                          nan |                       nan | 2024-01-29 00:00:00 | Conversation with Workforce / Personnel; Key Strengths ; Audit Findings; Audit Findings; Audit Findi... | The conversation took place with at least three (3) workforce/ personnel on site.; Key Strength(s); ... | ; ; Unsafe Act is defined as Failure to Follow HSE Standards and/or Company Policies; ; ; ; Unsafe C... | ; ; ; ; ; ; ; | Yes; Yes; Yes; 8 - Position of People (Absorbing); Yes; NA; N/A; N/A                                    | ; ; ; ; ; ; ;    | ; ; ; ; ; ; ; | Cables were lying haphazardly in the area. Workers were working & moving around that area, which cou... | HTDC Contstruction; HTDC Contstruction | ;                        |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-013 | Projects           | Management Safety Audit (MSA) | Arsslan Bhatti - EPCL P&BD  | 2023-09-04 00:00:00 | In Progress    |            nan | Inspection       | Self            |            nan | EPCL            | HTDC              | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Arsslan Bhatti - EPCL P&BD  | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-09-30 00:00:00   | nan                 |                           nan |                          nan |                       nan | NaT                 | Conversation with Workforce / Personnel; Key Strengths ; Audit Findings; Audit Findings; Audit Findi... | The conversation took place with at least three (3) workforce/ personnel on site.; Key Strength(s); ... | ; ; Unsafe Act is defined as Failure to Follow HSE Standards and/or Company Policies; Unsafe Conditi... | ; ; ; ; ; ; ; | Yes; PPE compliance; Yes; No; 2 - Tools & Equipment (Barrication / Warning Lights); Yes; 2 - Tools &... | ; ; ; ; ; ; ;    | ; ; ; ; ; ; ; | nan                                                                                                     | nan                                    | nan                      |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-014 | Projects           | Management Safety Audit (MSA) | Arsslan Bhatti - EPCL P&BD  | 2023-09-04 00:00:00 | In Progress    |            nan | Inspection       | Self            |            nan | EPCL            | HTDC              | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Arsslan Bhatti - EPCL P&BD  | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-09-30 00:00:00   | nan                 |                           nan |                          nan |                       nan | NaT                 | Conversation with Workforce / Personnel; Key Strengths ; Audit Findings; Audit Findings; Audit Findi... | The conversation took place with at least three (3) workforce/ personnel on site.; Key Strength(s); ... | ; ; Unsafe Act is defined as Failure to Follow HSE Standards and/or Company Policies; Unsafe Conditi... | ; ; ; ; ; ; ; | Yes; PPE compliance; Yes; No; 2 - Tools & Equipment (Barrication / Warning Lights); 6 - Procedures (... | ; ; ; ; ; ; ;    | ; ; ; ; ; ; ; | nan                                                                                                     | nan                                    | nan                      |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-015 | Projects           | Management Safety Audit (MSA) | Arsslan Bhatti - EPCL P&BD  | 2023-09-04 00:00:00 | Closed         |            nan | Inspection       | Self            |            nan | EPCL            | HTDC              | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Arsslan Bhatti - EPCL P&BD  | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-09-30 00:00:00   | 2023-09-30 00:00:00 |                           nan |                          nan |                       nan | 2024-01-29 00:00:00 | Conversation with Workforce / Personnel; Key Strengths ; Audit Findings; Audit Findings; Audit Findi... | The conversation took place with at least three (3) workforce/ personnel on site.; Key Strength(s); ... | ; ; Unsafe Act is defined as Failure to Follow HSE Standards and/or Company Policies; Unsafe Conditi... | ; ; ; ; ; ; ; | Yes; PPE compliance; Yes; No; 2 - Tools & Equipment (Barrication / Warning Lights); 6 - Procedures (... | ; ; ; ; ; ; ;    | ; ; ; ; ; ; ; | nan                                                                                                     | nan                                    | nan                      |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-016 | Stationary - PVC   | Management Safety Audit (MSA) | Ahrad Bin Riaz - EPCL Plant | 2023-09-04 00:00:00 | Closed         |            nan | Inspection       | Self            |            nan | EPCL            | PVC I Front End   | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Ahrad Bin Riaz - EPCL Plant | Zafar Tariq - EPCL Plant |          nan |                           nan |                                  nan | NaT                 | 2023-10-01 00:00:00   | 2023-10-01 00:00:00 |                           nan |                          nan |                       nan | 2023-10-31 00:00:00 | Conversation with Workforce / Personnel; Key Strengths ; Audit Findings; Audit Findings; Audit Findi... | The conversation took place with at least three (3) workforce/ personnel on site.; Key Strength(s); ... | ; ; Unsafe Act is defined as Failure to Follow HSE Standards and/or Company Policies; Unsafe Conditi... | ; ; ; ; ; ; ; | Yes; PPEs Compliance; No; No; 1 - PPE (Ears); N/A; Yes; N/A                                             | ; ; ; ; ; ; ;    | ; ; ; ; ; ; ; | No any major damage / PPEs deficiency was observed amongst the workers.                                 | Stationary - PVC                       | nan                      |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |

---

## Inspection Findings

**Total Columns:** 50
**Total Rows:** 3063
**Sample Rows:** 5

### Data Types and Sample Values

| Column | Data Type | Non-Null Count | Sample Values |
|--------|-----------|----------------|---------------|
| Audit Number | object | 3063/3063 | IS-20230904-011, IS-20230904-016, IS-20230904-017 |
| Audit Location | object | 3063/3063 | HTDC Contstruction, Stationary - PVC, HPO |
| Audit Title | object | 3063/3063 | Management Safety Audit (MSA) |
| Auditor | object | 3063/3063 | Rafay Shahid - EPCL Plant, Ahrad Bin Riaz - EPCL Plant, Hassan Masroor - EPCL Plant |
| Start Date | datetime64[ns] | 3063/3063 | 2023-09-04 00:00:00, 2023-09-05 00:00:00, 2023-09-06 00:00:00 |
| Audit Status | object | 3063/3063 | Closed, Review, In Progress |
| Location Tag | float64 | 0/3063 |  |
| Audit Category | object | 3063/3063 | Inspection |
| Auditing Body | object | 3063/3063 | Self, 1st Party, 2nd Party |
| Audit Rating | float64 | 0/3063 |  |
| Group Company | object | 3063/3063 | EPCL |
| Location (EPCL) | object | 3054/3063 | HTDC, PVC I Front End, HPO Product Tank farm Area |
| Audit Type (EPCL) | object | 3063/3063 | 6-MSA, 138-Executive MSA (EMSA), 22-Misc. |
| Template | object | 3063/3063 | Management Safety Audit (MSA) |
| Template Version | object | 3063/3063 | Current Version |
| Created By | object | 3063/3063 | Rafay Shahid - EPCL Plant, Ahrad Bin Riaz - EPCL Plant, Hassan Masroor - EPCL Plant |
| Audit Team | object | 910/3063 | Zafar Tariq - EPCL Plant, Muhammad Umer - EPCL Plant, Muhammad Irfan Alahi - EPCL Plant |
| Supervisor | float64 | 0/3063 |  |
| Responsible for Action Plan | float64 | 0/3063 |  |
| Responsible for Action Plan Review | float64 | 0/3063 |  |
| Entered Scheduled | datetime64[ns] | 1017/3063 | 2023-10-01 00:00:00, 2023-09-14 00:00:00, 2023-09-28 00:00:00 |
| Entered In Progress | object | 3063/3063 | 2023-09-11 00:00:00, 2023-10-01 00:00:00, 2023-10-02 00:00:00 |
| Entered Review | object | 3019/3063 | 2023-09-11 00:00:00, 2023-10-01 00:00:00, 2023-10-02 00:00:00 |
| Entered Pending Action Plan | float64 | 0/3063 |  |
| Entered Review Action Plan | float64 | 0/3063 |  |
| Entered Pending Closure | float64 | 0/3063 |  |
| Entered Closed | datetime64[ns] | 2640/3063 | 2024-01-29 00:00:00, 2023-10-31 00:00:00, 2023-10-03 00:00:00 |
| Checklist Category | object | 2965/3063 | Audit Findings, Key Strengths , Self Learnings / Conclusion / Remarks |
| Question | object | 2965/3063 | Was it an Unsafe Act? , Key Strength(s), Add if any, Self Learnings / Additional Comments /... |
| Regulatory Reference | object | 1653/3063 | Unsafe Act is defined as Failure to Follow HSE Sta..., Unsafe Condition is defined as a Dangerous Conditi... |
| Help Text | float64 | 0/3063 |  |
| Answer | object | 2883/3063 | Yes, PPEs Compliance, Good PPEs Compliance |
| Recommendation | float64 | 0/3063 |  |
| Response | float64 | 0/3063 |  |
| Finding | object | 3024/3063 | Cables were lying haphazardly in the area. Workers..., Area housekeeping was found to be satisfactory and..., No any major damage / PPEs deficiency was observed... |
| Finding Location | object | 3063/3063 | HTDC Contstruction, Stationary - PVC, HPO |
| Worst Case Consequence | float64 | 0/3063 |  |
| Action Item Number | object | 290/3063 | AC-AUD-20230918-004, AC-AUD-20230919-023, AC-AUD-20230928-097 |
| Action Item Title | object | 284/3063 | Safety goggle was not wear by excavator driver., Door temporarily fixed as in close position to avo..., Communication with Relevant area |
| Action Item Description | object | 267/3063 | Counselling was done with driver about PPEs., CLO2 facility doors are broken from hinges, need t..., Immediately barricaded by the HFC team |
| Action Item Responsible | object | 290/3063 | Ahtisham Qadir Malik - EPCL Plant, Zafar Ali - EPCL Plant, Allah Dewaya Nasir - EPCL Plant |
| Action Item Delegated | object | 51/3063 | ; , ; ; ; , ; ;  |
| Action Item Responsible for Verification | object | 232/3063 | Ahtisham Qadir Malik - EPCL Plant, Habib Ullah Brohi - EPCL Plant, Allah Dewaya Nasir - EPCL Plant |
| Action Item Effective? | object | 231/3063 | Yes, Yes; Yes, Yes; Yes; Yes; Yes |
| Action Item Verification Details | object | 228/3063 | y, Counselling done, Housekeeping is necessary for all plant |
| Action Item Priority | object | 232/3063 | C2, C3 - Medium, C0, C1 - Low, C2, C3 - Medium; C2, C3 - Medium |
| Action Item Due Date | object | 290/3063 | 2023-09-30 00:00:00, 2023-09-18 00:00:00, 2023-09-21 00:00:00 |
| Action Item Verification Due Date | object | 51/3063 | ; , ; ; ; , ; ;  |
| Action Item Status | object | 290/3063 | Closed, Dropped, Closed; Closed |
| Action Item Progress Notes | object | 232/3063 | Counselling was done, Door temporarily fixed as in close position to avo..., Done |

### Numeric Column Statistics

| Column | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|

### Categorical Columns Summary

**Audit Status** (3 unique values):

- Closed: 2640
- Review: 363
- In Progress: 60

**Auditing Body** (3 unique values):

- Self: 2824
- 1st Party: 233
- 2nd Party: 6

**Audit Type (EPCL)** (3 unique values):

- 6-MSA: 3054
- 22-Misc.: 6
- 138-Executive MSA (EMSA): 3

### Sample Data (First 5 Rows)

| Audit Number    | Audit Location     | Audit Title                   | Auditor                     | Start Date          | Audit Status   |   Location Tag | Audit Category   | Auditing Body   |   Audit Rating | Group Company   | Location (EPCL)            | Audit Type (EPCL)   | Template                      | Template Version   | Created By                  | Audit Team               |   Supervisor |   Responsible for Action Plan |   Responsible for Action Plan Review | Entered Scheduled   | Entered In Progress   | Entered Review      |   Entered Pending Action Plan |   Entered Review Action Plan |   Entered Pending Closure | Entered Closed      | Checklist Category                    | Question                                                                | Regulatory Reference                                                             |   Help Text | Answer               |   Recommendation |   Response | Finding                                                                                                 | Finding Location   |   Worst Case Consequence |   Action Item Number |   Action Item Title |   Action Item Description |   Action Item Responsible |   Action Item Delegated |   Action Item Responsible for Verification |   Action Item Effective? |   Action Item Verification Details |   Action Item Priority |   Action Item Due Date |   Action Item Verification Due Date |   Action Item Status |   Action Item Progress Notes |
|:----------------|:-------------------|:------------------------------|:----------------------------|:--------------------|:---------------|---------------:|:-----------------|:----------------|---------------:|:----------------|:---------------------------|:--------------------|:------------------------------|:-------------------|:----------------------------|:-------------------------|-------------:|------------------------------:|-------------------------------------:|:--------------------|:----------------------|:--------------------|------------------------------:|-----------------------------:|--------------------------:|:--------------------|:--------------------------------------|:------------------------------------------------------------------------|:---------------------------------------------------------------------------------|------------:|:---------------------|-----------------:|-----------:|:--------------------------------------------------------------------------------------------------------|:-------------------|-------------------------:|---------------------:|--------------------:|--------------------------:|--------------------------:|------------------------:|-------------------------------------------:|-------------------------:|-----------------------------------:|-----------------------:|-----------------------:|------------------------------------:|---------------------:|-----------------------------:|
| IS-20230904-011 | HTDC Contstruction | Management Safety Audit (MSA) | Rafay Shahid - EPCL Plant   | 2023-09-04 00:00:00 | Closed         |            nan | Inspection       | Self            |            nan | EPCL            | HTDC                       | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Rafay Shahid - EPCL Plant   | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-09-11 00:00:00   | 2023-09-11 00:00:00 |                           nan |                          nan |                       nan | 2024-01-29 00:00:00 | Audit Findings                        | Was it an Unsafe Act?                                                   | Unsafe Act is defined as Failure to Follow HSE Standards and/or Company Policies |         nan | Yes                  |              nan |        nan | Cables were lying haphazardly in the area. Workers were working & moving around that area, which cou... | HTDC Contstruction |                      nan |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-011 | HTDC Contstruction | Management Safety Audit (MSA) | Rafay Shahid - EPCL Plant   | 2023-09-04 00:00:00 | Closed         |            nan | Inspection       | Self            |            nan | EPCL            | HTDC                       | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Rafay Shahid - EPCL Plant   | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-09-11 00:00:00   | 2023-09-11 00:00:00 |                           nan |                          nan |                       nan | 2024-01-29 00:00:00 | Key Strengths                         | Key Strength(s)                                                         | nan                                                                              |         nan | Yes                  |              nan |        nan | Area housekeeping was found to be satisfactory and PPE compliance was also good. Routine safety talk... | HTDC Contstruction |                      nan |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-016 | Stationary - PVC   | Management Safety Audit (MSA) | Ahrad Bin Riaz - EPCL Plant | 2023-09-04 00:00:00 | Closed         |            nan | Inspection       | Self            |            nan | EPCL            | PVC I Front End            | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Ahrad Bin Riaz - EPCL Plant | Zafar Tariq - EPCL Plant |          nan |                           nan |                                  nan | NaT                 | 2023-10-01 00:00:00   | 2023-10-01 00:00:00 |                           nan |                          nan |                       nan | 2023-10-31 00:00:00 | Key Strengths                         | Key Strength(s)                                                         | nan                                                                              |         nan | PPEs Compliance      |              nan |        nan | No any major damage / PPEs deficiency was observed amongst the workers.                                 | Stationary - PVC   |                      nan |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-017 | HPO                | Management Safety Audit (MSA) | Hassan Masroor - EPCL Plant | 2023-09-04 00:00:00 | Review         |            nan | Inspection       | Self            |            nan | EPCL            | HPO Product Tank farm Area | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Hassan Masroor - EPCL Plant | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-10-02 00:00:00   | 2023-10-02 00:00:00 |                           nan |                          nan |                       nan | NaT                 | Audit Findings                        | Was it an Unsafe Act?                                                   | Unsafe Act is defined as Failure to Follow HSE Standards and/or Company Policies |         nan | Yes                  |              nan |        nan | Asif MW was working on cleaning of the nitrogen compressor unit so complete ERP was reviewed with te... | HPO                |                      nan |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |
| IS-20230904-017 | HPO                | Management Safety Audit (MSA) | Hassan Masroor - EPCL Plant | 2023-09-04 00:00:00 | Review         |            nan | Inspection       | Self            |            nan | EPCL            | HPO Product Tank farm Area | 6-MSA               | Management Safety Audit (MSA) | Current Version    | Hassan Masroor - EPCL Plant | nan                      |          nan |                           nan |                                  nan | NaT                 | 2023-10-02 00:00:00   | 2023-10-02 00:00:00 |                           nan |                          nan |                       nan | NaT                 | Self Learnings / Conclusion / Remarks | Add if any, Self Learnings / Additional Comments / Conclusion / Remarks | nan                                                                              |         nan | Good PPEs Compliance |              nan |        nan | Overall compliance was good and counselling of MW was done                                              | HPO                |                      nan |                  nan |                 nan |                       nan |                       nan |                     nan |                                        nan |                      nan |                                nan |                    nan |                    nan |                                 nan |                  nan |                          nan |

---

## Summary

**Total Sheets:** 6

**Sheet Details:**

- **Incident**: 2596 rows × 169 columns
- **Hazard ID**: 1211 rows × 169 columns
- **Audit**: 1522 rows × 50 columns
- **Audit Findings**: 1031 rows × 50 columns
- **Inspection**: 1773 rows × 50 columns
- **Inspection Findings**: 3063 rows × 50 columns

---

*This report was automatically generated to provide context about the Excel data structure.*