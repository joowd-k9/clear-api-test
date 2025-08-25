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
        "Flags": {},
        "UCCAnalysis": {},
        "CriminalHistoryAnalysis": {},
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
            result["Flags"] = _extract_risk_flags(section)

        # Analyze UCC filings for active/inactive status
        if section_name == "UCCSection":
            ucc_analysis = _analyze_ucc_filings(section)
            result["UCCAnalysis"] = ucc_analysis
            # Add UCC flag based on risk assessment
            if "Flags" not in result:
                result["Flags"] = {}
            result["Flags"]["UCCFilings"] = ucc_analysis["risk_assessment"]

        # Analyze criminal history
        if section_name == "CriminalSection":
            criminal_analysis = _analyze_criminal_history(section)
            result["CriminalHistoryAnalysis"] = criminal_analysis
            # Add criminal flag based on risk assessment
            if "Flags" not in result:
                result["Flags"] = {}
            result["Flags"]["CriminalHistory"] = criminal_analysis["risk_assessment"]

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
