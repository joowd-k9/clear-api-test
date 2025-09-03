"""XML response parser for Thomson Reuters CLEAR API responses."""

import xml.etree.ElementTree as ET
from typing import Dict, Any

from processing_engine.models.clear_models import ClearSearchResult, ClearReportResult


class ClearXMLParser:
    """Parser for CLEAR API XML responses."""

    @staticmethod
    def parse_business_search_response(xml_content: str) -> ClearSearchResult:
        """Parse business search response XML and extract GroupId."""
        try:
            root = ET.fromstring(xml_content)

            # Extract GroupId from search results
            group_id_element = root.find(".//GroupId")
            group_id = group_id_element.text if group_id_element is not None else None

            if not group_id:
                return ClearSearchResult(
                    group_id=None,
                    xml_response=xml_content,
                    status_code=200,
                    success=False,
                    error="No GroupId found in search results",
                )

            return ClearSearchResult(
                group_id=group_id,
                xml_response=xml_content,
                status_code=200,
                success=True,
            )

        except ET.ParseError as e:
            return ClearSearchResult(
                group_id=None,
                xml_response=xml_content,
                status_code=200,
                success=False,
                error=f"Invalid XML: {str(e)}",
            )

    @staticmethod
    def parse_person_search_response(xml_content: str) -> ClearSearchResult:
        """Parse person search response XML and extract GroupId."""
        # Similar logic to business search
        return ClearXMLParser.parse_business_search_response(xml_content)

    @staticmethod
    def parse_business_report_response(xml_content: str) -> ClearReportResult:
        """Parse business report XML and convert to structured format."""
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            return ClearReportResult(
                xml_response=xml_content,
                status_code=200,
                success=False,
                error=f"Invalid XML: {str(e)}",
            )

        # Extract status information
        status = root.find(".//Status")
        if status is None:
            return ClearReportResult(
                xml_response=xml_content,
                status_code=200,
                success=False,
                error="No Status section found in XML",
            )

        result = ClearReportResult(
            reference=ClearXMLParser._get_text(status, "Reference"),
            report_type=ClearXMLParser._get_text(status, "ReportType"),
            subject=ClearXMLParser._get_text(status, "ReportSubject"),
            entity_id=ClearXMLParser._get_text(status, "EntityId"),
            timestamp=ClearXMLParser._get_text(status, "TimeStamp"),
            flags={
                "UCCFilings": "None",
                "LiensAndJudgements": "None",
                "CriminalHistory": "None",
                "Lawsuits": "None",
                "Dockets": "None",
            },
            xml_response=xml_content,
            status_code=200,
            success=True,
        )

        # Extract section results
        parsed_results = {}
        section_results = root.findall(".//SectionResults")

        for section in section_results:
            section_name = ClearXMLParser._get_text(section, "SectionName")
            clean_section_name = section_name.replace("Section", "")

            section_data = {
                "Description": ClearXMLParser._get_text(
                    section, "CLEARReportDescription"
                ),
                "Status": ClearXMLParser._get_text(section, "SectionStatus"),
                "RecordCount": ClearXMLParser._get_text(section, "SectionRecordCount"),
                "Details": ClearXMLParser._parse_section_details(section),
            }
            parsed_results[clean_section_name] = section_data

            # Handle special sections for analysis
            if section_name == "QuickAnalysisFlagSection":
                extracted_flags = ClearXMLParser._extract_risk_flags(section)
                result.flags = {**result.flags, **extracted_flags}
            elif section_name == "UCCSection":
                ucc_analysis = ClearXMLParser._analyze_ucc_filings(section)
                result.ucc_analysis = ucc_analysis
                result.flags["UCCFilings"] = ucc_analysis.get("risk_assessment", "None")
            elif section_name == "LienJudgmentSection":
                liens_analysis = ClearXMLParser._analyze_liens_and_judgments(section)
                result.liens_analysis = liens_analysis
                result.flags["LiensAndJudgements"] = liens_analysis.get(
                    "risk_assessment", "None"
                )
            elif section_name == "CriminalSection":
                criminal_analysis = ClearXMLParser._analyze_criminal_history(section)
                result.criminal_analysis = criminal_analysis
                result.flags["CriminalHistory"] = criminal_analysis.get(
                    "risk_assessment", "None"
                )
            elif section_name == "LawsuitSection":
                lawsuit_analysis = ClearXMLParser._analyze_lawsuits(section)
                result.lawsuit_analysis = lawsuit_analysis
                result.flags["Lawsuits"] = lawsuit_analysis.get(
                    "risk_assessment", "None"
                )
            elif section_name == "DocketSection":
                docket_analysis = ClearXMLParser._analyze_docket_records(section)
                result.docket_analysis = docket_analysis
                result.flags["Dockets"] = docket_analysis.get("risk_assessment", "None")

        result.parsed_results = parsed_results
        return result

    @staticmethod
    def parse_person_report_response(xml_content: str) -> ClearReportResult:
        """Parse person report XML and convert to structured format."""
        # Similar logic to business report with person-specific sections
        return ClearXMLParser.parse_business_report_response(xml_content)

    @staticmethod
    def _get_text(element: ET.Element, tag: str) -> str:
        """Get text content of a child element."""
        child = element.find(tag)
        return child.text if child is not None and child.text else ""

    @staticmethod
    def _parse_section_details(section: ET.Element) -> Dict[str, Any]:
        """Parse the SectionDetails content."""
        section_details = section.find(".//SectionDetails")
        if section_details is None:
            return {}

        # Get the first child element (the actual section content)
        for child in section_details:
            return ClearXMLParser._element_to_dict(child)

        return {}

    @staticmethod
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
                child_value = ClearXMLParser._element_to_dict(children[0])
                if child_value is not None:
                    result[tag_name] = child_value
            else:
                # Multiple children - convert to list and filter out None values
                child_values = [
                    ClearXMLParser._element_to_dict(child) for child in children
                ]
                filtered_values = [val for val in child_values if val is not None]
                if filtered_values:
                    result[tag_name] = filtered_values

        return result

    @staticmethod
    def _extract_risk_flags(section: ET.Element) -> Dict[str, str]:
        """Extract risk flags from QuickAnalysisFlagSection."""
        flags = {}

        # Find the RiskFlagsWithDocguids element
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

    @staticmethod
    def _analyze_ucc_filings(section: ET.Element) -> Dict[str, Any]:
        """Analyze UCC filings to determine active vs inactive status."""
        ucc_records = section.findall(".//UCCRecord")
        if not ucc_records:
            return {
                "active_count": 0,
                "inactive_count": 0,
                "risk_assessment": "None",
                "filings": [],
            }

        # Simplified UCC analysis
        active_count = 0
        inactive_count = 0

        for record in ucc_records:
            filing_info = record.find(".//UCCFilingInfo")
            if filing_info is not None:
                filing_type = ClearXMLParser._get_text(filing_info, "FilingType")
                if filing_type == "TERMINATION":
                    inactive_count += 1
                else:
                    active_count += 1

        # Risk assessment
        risk_level = "None"
        if active_count > 20:
            risk_level = "High"
        elif active_count > 10:
            risk_level = "Medium"
        elif active_count > 0:
            risk_level = "Low"

        return {
            "active_count": active_count,
            "inactive_count": inactive_count,
            "total_filings": len(ucc_records),
            "risk_assessment": risk_level,
        }

    @staticmethod
    def _analyze_liens_and_judgments(section: ET.Element) -> Dict[str, Any]:
        """Analyze liens and judgments for risk assessment."""
        lien_records = section.findall(".//LienJudgeRecord")
        if not lien_records:
            return {"total_count": 0, "risk_assessment": "None"}

        total_count = len(lien_records)
        active_liens = 0
        total_amount = 0

        for record in lien_records:
            filing_info = record.find(".//FilingInfo")
            if filing_info is not None:
                release_date = ClearXMLParser._get_text(filing_info, "ReleaseDate")
                if not release_date.strip():
                    active_liens += 1

                # Try to extract amount
                debtor_info = record.find(".//Debtor")
                if debtor_info is not None:
                    owed_amount = ClearXMLParser._get_text(
                        debtor_info, "DebtorOwedAmount"
                    )
                    try:
                        if owed_amount and owed_amount.startswith("$"):
                            amount = float(
                                owed_amount.replace("$", "").replace(",", "")
                            )
                            total_amount += amount
                    except (ValueError, AttributeError):
                        pass

        # Risk assessment
        risk_level = "None"
        if active_liens > 0 or total_amount > 10000:
            risk_level = "High"
        elif total_amount > 5000:
            risk_level = "Medium"
        elif total_count > 0:
            risk_level = "Low"

        return {
            "total_count": total_count,
            "active_liens": active_liens,
            "total_amount": total_amount,
            "risk_assessment": risk_level,
        }

    @staticmethod
    def _analyze_criminal_history(section: ET.Element) -> Dict[str, Any]:
        """Analyze criminal records for risk assessment."""
        criminal_records = section.findall(".//CriminalExpansionRecord")
        if not criminal_records:
            return {"total_count": 0, "risk_assessment": "None"}

        total_count = len(criminal_records)
        violent_crimes = 0
        financial_crimes = 0
        felony_charges = 0

        for record in criminal_records:
            offender_infos = record.findall(".//OffenderInfo")
            for offender_info in offender_infos:
                criminal_offense = ClearXMLParser._get_text(
                    offender_info, "CriminalOffense"
                ).upper()

                # Categorize crimes
                if any(
                    violent in criminal_offense
                    for violent in ["ASSAULT", "BATTERY", "MURDER", "ROBBERY"]
                ):
                    violent_crimes += 1
                if any(
                    financial in criminal_offense
                    for financial in ["FRAUD", "THEFT", "EMBEZZLEMENT"]
                ):
                    financial_crimes += 1
                if any(
                    felony in criminal_offense for felony in ["FELONY", "AGGRAVATED"]
                ):
                    felony_charges += 1

        # Risk assessment
        risk_level = "None"
        if violent_crimes > 0 or felony_charges > 0:
            risk_level = "High"
        elif financial_crimes > 0:
            risk_level = "Medium"
        elif total_count > 0:
            risk_level = "Low"

        return {
            "total_count": total_count,
            "violent_crimes": violent_crimes,
            "financial_crimes": financial_crimes,
            "felony_charges": felony_charges,
            "risk_assessment": risk_level,
        }

    @staticmethod
    def _analyze_lawsuits(section: ET.Element) -> Dict[str, Any]:
        """Analyze lawsuit records for risk assessment."""
        lawsuit_records = []
        for element in section.iter():
            tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag
            if tag.endswith("LawsuitRecord"):
                lawsuit_records.append(element)

        if not lawsuit_records:
            return {"total_count": 0, "risk_assessment": "None"}

        total_count = len(lawsuit_records)

        # Risk assessment based on count
        risk_level = "None"
        if total_count > 10:
            risk_level = "High"
        elif total_count > 5:
            risk_level = "Medium"
        elif total_count > 0:
            risk_level = "Low"

        return {"total_count": total_count, "risk_assessment": risk_level}

    @staticmethod
    def _analyze_docket_records(section: ET.Element) -> Dict[str, Any]:
        """Analyze docket records for risk assessment."""
        docket_records = section.findall(".//CompanyDocketRecord")
        if not docket_records:
            return {"total_count": 0, "risk_assessment": "None"}

        total_count = len(docket_records)
        federal_count = 0

        for record in docket_records:
            docket_info = record.find(".//DocketInfo")
            if docket_info is not None:
                source = ClearXMLParser._get_text(docket_info, "Source")
                if source == "Federal Docket Record":
                    federal_count += 1

        # Risk assessment
        risk_level = "None"
        if federal_count > 0:
            risk_level = "High"
        elif total_count > 5:
            risk_level = "Medium"
        elif total_count > 0:
            risk_level = "Low"

        return {
            "total_count": total_count,
            "federal_count": federal_count,
            "risk_assessment": risk_level,
        }
