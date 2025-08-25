"""Parser module for converting XML responses to JSON format."""

import xml.etree.ElementTree as ET
from typing import Dict, Any


def parse_business_report_xml(xml_content: str) -> Dict[str, Any]:
    """
    Parse business report XML and convert to JSON format.

    Args:
        xml_content: XML string from business report response

    Returns:
        Dict with structure:
        {
            "Reference": str,
            "Type": str,
            "Subject": str,
            "Id": str,
            "Timestamp": str,
            "Flags": {
                "WorldCheck": str,
                "OFAC": str,
                "GlobalSanctions": str,
                ...
            },
            "Results": {
                "SectionName": {
                    "Description": str,
                    "Status": str,
                    "RecordCount": str,
                    "Details": dict
                }
            }
        }
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        return {"error": f"Invalid XML: {str(e)}"}

        # Extract status information
    status = root.find(".//Status")
    if status is None:
        return {"error": "No Status section found in XML"}

    result = {
        "Reference": _get_text(status, "Reference"),
        "Type": _get_text(status, "ReportType"),
        "Subject": _get_text(status, "ReportSubject"),
        "ID": _get_text(status, "EntityId"),
        "Timestamp": _get_text(status, "TimeStamp"),
        "Flags": {
            "UCCFilings": "None",
            "LiensAndJudgements": "None",
            "CriminalHistory": "None",
            "Lawsuits": "None",
            "Dockets": "None",
        },
        "UCCFilingsAnalysis": {},
        "LiensAndJudgementsAnalysis": {},
        "CriminalHistoryAnalysis": {},
        "DocketAnalysis": {},
        "LawsuitAnalysis": {},
        "Results": {},
    }

    # Extract section results
    section_results = root.findall(".//SectionResults")
    for section in section_results:
        section_name = _get_text(section, "SectionName")
        section_data = {
            "Description": _get_text(section, "CLEARReportDescription"),
            "Status": _get_text(section, "SectionStatus"),
            "RecordCount": _get_text(section, "SectionRecordCount"),
            "Details": _parse_section_details(section),
        }
        result["Results"][section_name] = section_data

        # Extract flags from QuickAnalysisFlagSection
        if section_name == "QuickAnalysisFlagSection":
            result["Flags"] = {**result.get("Flags", {}), **_extract_risk_flags(section)}

        # Analyze UCC filings for active/inactive status
        if section_name == "UCCSection":
            ucc_analysis = _analyze_ucc_filings(section)
            result["UCCFilingsAnalysis"] = ucc_analysis
            # Add UCC flag based on risk assessment
            if "Flags" not in result:
                result["Flags"] = {}
            result["Flags"]["UCCFilings"] = ucc_analysis["risk_assessment"]

        # Analyze liens and judgments
        if section_name == "LienJudgmentSection":
            liens_analysis = _analyze_liens_and_judgments(section)
            result["LiensAndJudgementsAnalysis"] = liens_analysis
            # Add liens flag based on risk assessment
            if "Flags" not in result:
                result["Flags"] = {}
            result["Flags"]["LiensAndJudgements"] = liens_analysis["risk_assessment"]

        # Analyze criminal history
        if section_name == "CriminalSection":
            criminal_analysis = _analyze_criminal_history(section)
            result["CriminalHistoryAnalysis"] = criminal_analysis
            # Add criminal flag based on risk assessment
            if "Flags" not in result:
                result["Flags"] = {}
            result["Flags"]["CriminalHistory"] = criminal_analysis["risk_assessment"]

        # Analyze lawsuits
        if section_name == "LawsuitSection":
            lawsuit_analysis = _analyze_lawsuits(section)
            result["LawsuitAnalysis"] = lawsuit_analysis
            # Add lawsuit flag based on risk assessment
            if "Flags" not in result:
                result["Flags"] = {}
            result["Flags"]["Lawsuits"] = lawsuit_analysis["risk_assessment"]

        # Analyze docket records
        if section_name == "DocketSection":
            docket_analysis = _analyze_docket_records(section)
            result["DocketAnalysis"] = docket_analysis
            # Add docket flag based on risk assessment
            if "Flags" not in result:
                result["Flags"] = {}
            result["Flags"]["Dockets"] = docket_analysis["risk_assessment"]

    return result


def _get_text(element: ET.Element, tag: str) -> str:
    """Get text content of a child element."""
    child = element.find(tag)
    return child.text if child is not None else ""


def _extract_risk_flags(section: ET.Element) -> Dict[str, str]:
    """Extract risk flags from QuickAnalysisFlagSection."""
    flags = {}

    # Find the RiskFlagsWithDocguids element (note: lowercase 'g')
    risk_flags = section.find(".//RiskFlagsWithDocguids")
    if risk_flags is None:
        return flags

    # Extract each risk flag
    for flag_element in risk_flags:
        flag_name = (
            flag_element.tag.split("}")[-1]
            if "}" in flag_element.tag
            else flag_element.tag
        )
        risk_flag = flag_element.find("RiskFlag")
        if risk_flag is not None and risk_flag.text:
            flags[flag_name] = risk_flag.text

    return flags


def _analyze_ucc_filings(section: ET.Element) -> Dict[str, Any]:
    """Analyze UCC filings to determine active vs inactive status."""
    ucc_records = section.findall(".//UCCRecord")
    if not ucc_records:
        return {"active_count": 0, "inactive_count": 0, "filings": []}

        # Group filings by reference number to track amendments
    filing_groups = {}

    for record in ucc_records:
        filing_info = record.find(".//UCCFilingInfo")
        if filing_info is None:
            continue

        filing_stmt = filing_info.find(".//FilingStmtInfo")
        if filing_stmt is None:
            continue

        business_info = filing_stmt.find(".//BusinessInfo")
        if business_info is None:
            continue

        filing_type = _get_text(business_info, "FilingType")
        filing_number = _get_text(business_info, "FilingNumber")
        filing_date = _get_text(business_info, "FilingDate")
        reference_number = _get_text(filing_stmt, "ReferenceFileNumber")

        # Clean reference number (remove spaces) and use as key, or filing number if no reference
        clean_reference = reference_number.replace(" ", "") if reference_number else ""
        key = clean_reference if clean_reference else filing_number

        if key not in filing_groups:
            filing_groups[key] = []

        filing_data = {
            "filing_type": filing_type,
            "filing_number": filing_number,
            "filing_date": filing_date,
            "reference_number": clean_reference,  # Use cleaned reference number
            "is_active": _is_active_ucc_filing(filing_type),
        }

        filing_groups[key].append(filing_data)

        # Determine final status for each filing group (unique security interest)
    active_security_interests = 0
    inactive_security_interests = 0
    all_filing_groups = []

    for key, filings in filing_groups.items():
        # Sort by filing date to get chronological order (convert MM/DD/YYYY to sortable format)
        filings.sort(
            key=lambda x: x["filing_date"].split("/")[2]
            + x["filing_date"].split("/")[0]
            + x["filing_date"].split("/")[1]
        )

        # Determine final status based on the most recent filing
        latest_filing = filings[-1]
        final_status = _determine_final_ucc_status(filings)

        # Find the original filing (first ORIGINAL filing, or first filing if no ORIGINAL)
        original_filing = None
        for filing in filings:
            if filing["filing_type"] == "ORIGINAL":
                original_filing = filing
                break
        if original_filing is None:
            original_filing = filings[0]  # Use first filing if no ORIGINAL found

        # Create a filing group summary
        filing_group = {
            "security_interest_id": key,
            "original_filing": original_filing,
            "latest_filing": latest_filing,
            "total_filings": len(filings),
            "filing_history": filings,
            "final_status": final_status,
            "is_active": final_status == "ACTIVE",
        }

        if final_status == "ACTIVE":
            active_security_interests += 1
        else:
            inactive_security_interests += 1

        all_filing_groups.append(filing_group)

    total_filings_count = sum(
        len(group["filing_history"]) for group in all_filing_groups
    )

    # Risk assessment logic for UCC filings
    risk_level = "None"
    if total_filings_count > 0:
        if active_security_interests > 20:  # High debt burden
            risk_level = "High"
        elif active_security_interests > 10:  # Moderate debt burden
            risk_level = "Medium"
        elif active_security_interests > 0:
            risk_level = "Low"

    return {
        "risk_assessment": risk_level,
        "total_ucc_filings": total_filings_count,
        "distinct_ucc_filings": len(all_filing_groups),
        "active_ucc_filings": active_security_interests,
        "inactive_ucc_filings": inactive_security_interests,
        "grouped_ucc_filings": all_filing_groups,
    }


def _analyze_criminal_history(section: ET.Element) -> Dict[str, Any]:
    """Analyze criminal records to provide summary statistics and risk assessment."""
    criminal_records = section.findall(".//CriminalExpansionRecord")
    if not criminal_records:
        return {
            "risk_assessment": "None",
            "total_criminal_records": 0,
            "unique_individuals": 0,
            "criminal_records": [],
        }

    total_records = len(criminal_records)
    individuals = set()
    all_criminal_records = []

    # Categories for risk assessment
    violent_crimes = 0
    financial_crimes = 0
    recent_crimes = 0  # Last 10 years
    felony_charges = 0
    active_cases = 0

    for record in criminal_records:
        # Extract defendant information
        defendant_info = record.find(".//DefendantInfo")
        if defendant_info is not None:
            person_info = defendant_info.find(".//PersonInfo")
            if person_info is not None:
                person_name = person_info.find(".//PersonName")
                if person_name is not None:
                    full_name = _get_text(person_name, "FullName")
                    individuals.add(full_name)

        # Extract offender information
        offender_infos = record.findall(".//OffenderInfo")
        for offender_info in offender_infos:
            criminal_offense = _get_text(offender_info, "CriminalOffense")
            crime_date = _get_text(offender_info, "CrimeDate")
            disposition = _get_text(
                offender_info, "CaseDispositionDecisionCategoryText"
            )
            docket_number = _get_text(offender_info, "DocketNumber")

            # Determine crime category
            is_violent = any(
                violent in criminal_offense.upper()
                for violent in [
                    "ASSAULT",
                    "BATTERY",
                    "MURDER",
                    "ROBBERY",
                    "BURGLARY",
                    "KIDNAP",
                ]
            )
            is_financial = any(
                financial in criminal_offense.upper()
                for financial in [
                    "FRAUD",
                    "THEFT",
                    "EMBEZZLEMENT",
                    "FORGERY",
                    "MONEY LAUNDERING",
                ]
            )
            is_felony = any(
                felony in criminal_offense.upper()
                for felony in ["FELONY", "AGGRAVATED", "FIRST DEGREE", "SECOND DEGREE"]
            )

            # Check if recent (last 10 years)
            try:
                if crime_date:
                    crime_year = int(crime_date.split("/")[2])
                    if crime_year >= 2014:  # Last 10 years
                        recent_crimes += 1
            except (ValueError, IndexError):
                pass

            # Check if case is active/pending
            is_active = disposition in ["PENDING", "ACTIVE", "OPEN"] or not disposition

            if is_violent:
                violent_crimes += 1
            if is_financial:
                financial_crimes += 1
            if is_felony:
                felony_charges += 1
            if is_active:
                active_cases += 1

            criminal_record = {
                "defendant_name": full_name if "full_name" in locals() else "",
                "criminal_offense": criminal_offense,
                "crime_date": crime_date,
                "disposition": disposition,
                "docket_number": docket_number,
                "is_violent": is_violent,
                "is_financial": is_financial,
                "is_felony": is_felony,
                "is_active": is_active,
                "is_recent": (
                    crime_date and crime_year >= 2014
                    if "crime_year" in locals()
                    else False
                ),
            }
            all_criminal_records.append(criminal_record)

    # Risk assessment logic
    risk_level = "None"
    if total_records > 0:
        # High risk: Violent crimes, felonies, or active cases
        if violent_crimes > 0 or felony_charges > 0 or active_cases > 0:
            risk_level = "High"
        # Medium risk: Financial crimes or recent crimes (last 10 years)
        elif financial_crimes > 0 or recent_crimes > 0:
            risk_level = "Medium"
        # Low risk: Old, minor, resolved crimes
        else:
            risk_level = "Low"

    return {
        "risk_assessment": risk_level,
        "total_criminal_records": total_records,
        "unique_individuals": len(individuals),
        "violent_crimes": violent_crimes,
        "financial_crimes": financial_crimes,
        "recent_crimes": recent_crimes,
        "felony_charges": felony_charges,
        "active_cases": active_cases,
        "criminal_records": all_criminal_records,
    }


def _analyze_liens_and_judgments(section: ET.Element) -> Dict[str, Any]:
    """Analyze liens and judgments to provide summary statistics and risk assessment."""
    lien_records = section.findall(".//LienJudgeRecord")
    if not lien_records:
        return {
            "risk_assessment": "None",
            "total_liens_and_judgments": 0,
            "total_amount": 0,
            "active_liens": 0,
            "released_liens": 0,
            "tax_liens": 0,
            "civil_judgments": 0,
            "recent_liens": 0,  # Last 5 years
            "high_value_liens": 0,  # Over $10,000
            "lien_records": [],
        }

    total_records = len(lien_records)
    total_amount = 0
    active_liens = 0
    released_liens = 0
    tax_liens = 0
    civil_judgments = 0
    recent_liens = 0
    high_value_liens = 0
    all_lien_records = []

    for record in lien_records:
        # Extract filing information
        filing_info = record.find(".//FilingInfo")
        if filing_info is None:
            continue

        filing_type = _get_text(filing_info, "TypeofFiling")
        file_date = _get_text(filing_info, "FileDate")
        release_date = _get_text(filing_info, "ReleaseDate")

        # Extract debtor information
        debtor_info = record.find(".//Debtor")
        if debtor_info is None:
            continue

        owed_amount = _get_text(debtor_info, "DebtorOwedAmount")

        # Extract creditor information
        creditor_info = record.find(".//Creditor")
        creditor_name = ""
        if creditor_info is not None:
            party_info = creditor_info.find(".//PartyInfo")
            if party_info is not None:
                person_name = party_info.find(".//PersonName")
                if person_name is not None:
                    creditor_name = _get_text(person_name, "FullName")

        # Parse amount
        amount = 0
        try:
            if owed_amount and owed_amount.startswith("$"):
                amount = float(owed_amount.replace("$", "").replace(",", ""))
                total_amount += amount
        except (ValueError, AttributeError):
            pass

        # Determine lien characteristics
        is_tax_lien = any(
            tax in filing_type.upper()
            for tax in ["TAX", "IRS", "STATE TAX", "FEDERAL TAX"]
        )
        is_civil_judgment = any(
            judgment in filing_type.upper() for judgment in ["JUDGMENT", "CIVIL"]
        )
        is_released = release_date is not None and release_date.strip() != ""
        is_recent = False
        is_high_value = amount > 10000

        # Check if recent (last 5 years)
        try:
            if file_date:
                file_year = int(file_date.split("/")[2])
                if file_year >= 2019:  # Last 5 years
                    recent_liens += 1
                    is_recent = True
        except (ValueError, IndexError):
            pass

        if is_tax_lien:
            tax_liens += 1
        if is_civil_judgment:
            civil_judgments += 1
        if is_released:
            released_liens += 1
        else:
            active_liens += 1
        if is_high_value:
            high_value_liens += 1

        lien_record = {
            "creditor_name": creditor_name,
            "filing_type": filing_type,
            "file_date": file_date,
            "release_date": release_date,
            "amount": amount,
            "is_tax_lien": is_tax_lien,
            "is_civil_judgment": is_civil_judgment,
            "is_released": is_released,
            "is_active": not is_released,
            "is_recent": is_recent,
            "is_high_value": is_high_value,
        }
        all_lien_records.append(lien_record)

    # Risk assessment logic for liens and judgments
    risk_level = "None"
    if total_records > 0:
        # High risk: Active liens, high value liens, or recent liens
        if (
            active_liens > 0
            or high_value_liens > 0
            or recent_liens > 0
            or tax_liens > 0
        ):
            risk_level = "High"
        # Medium risk: Released liens or moderate amounts
        elif total_amount > 5000:
            risk_level = "Medium"
        # Low risk: Old, released, low-value liens
        else:
            risk_level = "Low"

    return {
        "risk_assessment": risk_level,
        "total_liens_and_judgments": total_records,
        "total_amount": total_amount,
        "active_liens": active_liens,
        "released_liens": released_liens,
        "tax_liens": tax_liens,
        "civil_judgments": civil_judgments,
        "recent_liens": recent_liens,
        "high_value_liens": high_value_liens,
        "lien_records": all_lien_records,
    }


def _analyze_lawsuits(section: ET.Element) -> Dict[str, Any]:
    """Analyze lawsuits to provide summary statistics and risk assessment."""
    # Find all elements that end with "LawsuitRecord" (handle namespaces)
    lawsuit_records = []
    for element in section.iter():
        # Remove namespace prefix if present
        tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag
        if tag.endswith("LawsuitRecord"):
            lawsuit_records.append(element)

    if not lawsuit_records:
        return {
            "risk_assessment": "None",
            "total_lawsuits": 0,
            "active_lawsuits": 0,
            "resolved_lawsuits": 0,
            "recent_lawsuits": 0,  # Last 3 years
            "high_value_lawsuits": 0,  # Over $100,000
            "employment_lawsuits": 0,
            "contract_lawsuits": 0,
            "class_action_lawsuits": 0,
            "regulatory_lawsuits": 0,
            "lawsuit_records": [],
        }

    total_lawsuits = len(lawsuit_records)
    active_lawsuits = 0
    resolved_lawsuits = 0
    recent_lawsuits = 0
    high_value_lawsuits = 0
    employment_lawsuits = 0
    contract_lawsuits = 0
    class_action_lawsuits = 0
    regulatory_lawsuits = 0
    all_lawsuit_records = []

    for record in lawsuit_records:
        # Extract lawsuit information directly from record
        case_type = _get_text(record, "CaseType")
        case_category = _get_text(record, "CaseCategory")
        filing_date = _get_text(record, "FileDate")
        docket_number = _get_text(record, "FilingNumber")
        court = _get_text(record, "Court")
        venue_location = _get_text(record, "VenueLocation")

        # Check if company is defendant or plaintiff
        company_interest = ""
        defendants = record.findall(".//Defendant")
        plaintiffs = record.findall(".//Plaintiff")

        # Check if Thomson/company name appears in defendants or plaintiffs
        company_names = ["THOMSON", "REUTERS", "THOMSON REUTERS", "THOMSON CORPORATION"]
        for defendant in defendants:
            full_name = _get_text(defendant, "FullName")
            if any(name in full_name.upper() for name in company_names):
                company_interest = "DEFENDANT"
                break

        if not company_interest:
            for plaintiff in plaintiffs:
                full_name = _get_text(plaintiff, "FullName")
                if any(name in full_name.upper() for name in company_names):
                    company_interest = "PLAINTIFF"
                    break

        # Determine lawsuit characteristics based on actual case types
        # Handle empty or None case_type
        case_type_upper = case_type.upper() if case_type else ""

        is_employment = case_type in ["WRONGFUL TERMINATION"]

        is_contract = case_type in [
            "BREACH OF CONTRACT",
            "OTHER - CONTRACT ACTION",
            "OTHER - CONTRACTS",
            "ACCOUNT STATED"
        ]

        # Check for class action indicators
        # 1. Multiple plaintiffs (common in class actions)
        # 2. Specific case types that might indicate class actions
        multiple_plaintiffs = len(plaintiffs) > 1
        class_action_keywords = [
            "CLASS ACTION",
            "MASS TORT",
            "COLLECTIVE ACTION",
            "REPRESENTATIVE ACTION",
        ]
        class_action_case_types = ["FRAUD"]  # Based on actual data

        is_class_action = (
            multiple_plaintiffs
            or any(keyword in case_type_upper for keyword in class_action_keywords)
            or case_type in class_action_case_types
        )

        # Regulatory cases - based on actual data, these are rare
        # Most regulatory cases would be handled by federal agencies
        is_regulatory = case_type in [
            "MISC - FOREIGN CIVIL JUDGMENTS"  # Could involve regulatory compliance
        ]
        is_active = company_interest in ["DEFENDANT", "PLAINTIFF"] and filing_date
        is_recent = False
        is_high_value = False  # Would need amount field if available

        # Check if recent (last 3 years)
        try:
            if filing_date:
                filing_year = int(filing_date.split("/")[2])
                if filing_year >= 2021:  # Last 3 years
                    recent_lawsuits += 1
                    is_recent = True
        except (ValueError, IndexError):
            pass

        if is_employment:
            employment_lawsuits += 1
        if is_contract:
            contract_lawsuits += 1
        if is_class_action:
            class_action_lawsuits += 1
        if is_regulatory:
            regulatory_lawsuits += 1
        if is_active:
            active_lawsuits += 1
        else:
            resolved_lawsuits += 1

        lawsuit_record = {
            "case_type": case_type,
            "case_category": case_category,
            "filing_date": filing_date,
            "docket_number": docket_number,
            "court": court,
            "venue_location": venue_location,
            "company_interest": company_interest,
            "is_employment": is_employment,
            "is_contract": is_contract,
            "is_class_action": is_class_action,
            "is_regulatory": is_regulatory,
            "is_active": is_active,
            "is_recent": is_recent,
            "is_high_value": is_high_value,
        }
        all_lawsuit_records.append(lawsuit_record)

    # Risk assessment logic for lawsuits
    risk_level = "None"
    if total_lawsuits > 0:
        # High risk: Active lawsuits, class actions, or regulatory actions
        if (
            active_lawsuits > 0
            or class_action_lawsuits > 0
            or regulatory_lawsuits > 0
        ):
            risk_level = "High"
        # Medium risk: Recent lawsuits or employment/contract disputes
        elif (
            recent_lawsuits > 0
            or employment_lawsuits > 0
            or contract_lawsuits > 0
        ):
            risk_level = "Medium"
        # Low risk: Old, resolved lawsuits
        else:
            risk_level = "Low"

    return {
        "risk_assessment": risk_level,
        "total_lawsuits": total_lawsuits,
        "active_lawsuits": active_lawsuits,
        "resolved_lawsuits": resolved_lawsuits,
        "recent_lawsuits": recent_lawsuits,
        "high_value_lawsuits": high_value_lawsuits,
        "employment_lawsuits": employment_lawsuits,
        "contract_lawsuits": contract_lawsuits,
        "class_action_lawsuits": class_action_lawsuits,
        "regulatory_lawsuits": regulatory_lawsuits,
        "lawsuit_records": all_lawsuit_records,
    }


def _analyze_docket_records(section: ET.Element) -> Dict[str, Any]:
    """Analyze docket records to provide summary statistics and risk assessment."""
    docket_records = section.findall(".//CompanyDocketRecord")

    if not docket_records:
        return {
            "risk_assessment": "None",
            "total_docket_records": 0,
            "federal_docket_records": 0,
            "state_docket_records": 0,
            "recent_docket_records": 0,  # Last 3 years
            "company_as_defendant": 0,
            "company_as_plaintiff": 0,
            "active_docket_records": 0,
            "docket_records": [],
        }

    total_docket_records = len(docket_records)
    federal_docket_records = 0
    state_docket_records = 0
    recent_docket_records = 0
    company_as_defendant = 0
    company_as_plaintiff = 0
    active_docket_records = 0
    all_docket_records = []

    for record in docket_records:
        docket_info = record.find(".//DocketInfo")
        if docket_info is None:
            continue

        docket_title = _get_text(docket_info, "DocketTitle")
        docket_number = _get_text(docket_info, "DocketNumber")
        filing_date = _get_text(docket_info, "FilingDate")
        court = _get_text(docket_info, "Court")
        nature_of_suit = _get_text(docket_info, "NatureOfSuit")
        company_interest = _get_text(docket_info, "CompanyInterest")
        source = _get_text(docket_info, "Source")

        # Determine record type
        is_federal = source == "Federal Docket Record" or "FED" in court.upper() or "C.A." in court
        is_state = source == "State Docket Record" or not is_federal

        # Check if recent (last 3 years)
        is_recent = False
        try:
            if filing_date:
                filing_year = int(filing_date.split("/")[2])
                if filing_year >= 2021:  # Last 3 years
                    recent_docket_records += 1
                    is_recent = True
        except (ValueError, IndexError):
            pass

        # Check company role
        is_defendant = "DEFENDANT" in company_interest.upper()
        is_plaintiff = "PLAINTIFF" in company_interest.upper()

        # Assume active if recent (within last 3 years)
        is_active = is_recent

        if is_federal:
            federal_docket_records += 1
        else:
            state_docket_records += 1

        if is_defendant:
            company_as_defendant += 1
        elif is_plaintiff:
            company_as_plaintiff += 1

        if is_active:
            active_docket_records += 1

        docket_record = {
            "docket_title": docket_title,
            "docket_number": docket_number,
            "filing_date": filing_date,
            "court": court,
            "nature_of_suit": nature_of_suit,
            "company_interest": company_interest,
            "source": source,
            "is_federal": is_federal,
            "is_state": is_state,
            "is_recent": is_recent,
            "is_defendant": is_defendant,
            "is_plaintiff": is_plaintiff,
            "is_active": is_active,
        }
        all_docket_records.append(docket_record)

    # Risk assessment logic for docket records
    risk_level = "None"
    if total_docket_records > 0:
        # High risk: Recent federal cases, company as defendant, or multiple active cases
        if (recent_docket_records > 0 and federal_docket_records > 0) or company_as_defendant > 2:
            risk_level = "High"
        # Medium risk: Recent state cases or moderate number of cases
        elif recent_docket_records > 0 or total_docket_records > 5:
            risk_level = "Medium"
        # Low risk: Old cases or company as plaintiff
        else:
            risk_level = "Low"

    return {
        "risk_assessment": risk_level,
        "total_docket_records": total_docket_records,
        "federal_docket_records": federal_docket_records,
        "state_docket_records": state_docket_records,
        "recent_docket_records": recent_docket_records,
        "company_as_defendant": company_as_defendant,
        "company_as_plaintiff": company_as_plaintiff,
        "active_docket_records": active_docket_records,
        "docket_records": all_docket_records,
    }


def _is_active_ucc_filing(filing_type: str) -> bool:
    """Determine if a UCC filing type is generally active."""
    active_types = {"ORIGINAL", "AMENDMENT", "CONTINUATION"}
    inactive_types = {"TERMINATION"}

    if filing_type in active_types:
        return True
    if filing_type in inactive_types:
        return False
    return True  # Unknown types, assume active


def _determine_final_ucc_status(filings: list) -> str:
    """Determine the final status of a UCC filing group based on filing history."""
    if not filings:
        return "UNKNOWN"

    # Check the most recent filing type
    latest_filing = filings[-1]
    latest_type = latest_filing["filing_type"]

    if latest_type == "TERMINATION":
        return "INACTIVE"
    if latest_type == "ORIGINAL":
        return "ACTIVE"
    if latest_type == "AMENDMENT":
        # Amendments modify existing filings - check if they're recent
        # For simplicity, assume amendments keep filings active unless followed by termination
        return "ACTIVE"
    if latest_type == "CONTINUATION":
        return "ACTIVE"
    return "ACTIVE"  # Unknown types, assume active


def _parse_section_details(section: ET.Element) -> Dict[str, Any]:
    """Parse the SectionDetails content."""
    section_details = section.find(".//SectionDetails")
    if section_details is None:
        return {}

    # Get the first child element (the actual section content)
    for child in section_details:
        return _element_to_dict(child)

    return {}


def _element_to_dict(element: ET.Element) -> Any:
    """Convert XML element to dictionary/primitive value."""
    if element is None:
        return None

    # If element has no children, return text content or None if empty
    if len(element) == 0:
        return element.text if element.text and element.text.strip() else None

    # If element has children, create a dict
    result = {}

    # Handle multiple children with same tag name
    children_by_tag = {}
    for child in element:
        tag_name = child.tag.split("}")[-1] if "}" in child.tag else child.tag

        if tag_name not in children_by_tag:
            children_by_tag[tag_name] = []
        children_by_tag[tag_name].append(child)

    # Process each tag
    for tag_name, children in children_by_tag.items():
        if len(children) == 1:
            # Single child - convert to dict/value
            child_value = _element_to_dict(children[0])
            if child_value is not None:
                result[tag_name] = child_value
        else:
            # Multiple children - convert to list and filter out None values
            child_values = [_element_to_dict(child) for child in children]
            filtered_values = [val for val in child_values if val is not None]
            if filtered_values:
                result[tag_name] = filtered_values

    return result


def parse_business_search_response(xml_content: str) -> Dict[str, Any]:
    """
    Parse business search response XML and extract GroupId.

    Args:
        xml_content: XML string from business search response

    Returns:
        Dict with GroupId and other search result data
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        return {"error": f"Invalid XML: {str(e)}"}

    # Extract GroupId from search results
    group_id_element = root.find(".//GroupId")
    if group_id_element is None:
        return {"error": "No GroupId found in search results"}

    result = {"ResultGroup": {"GroupId": group_id_element.text}}

    return result
