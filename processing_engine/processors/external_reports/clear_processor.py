"""Thomson Reuters CLEAR API processor for comprehensive background checks."""

from typing import Any, Union

from processing_engine.external_integrations.clear_client import ClearAPIClient
from processing_engine.utils.xml_builder import XMLTemplateBuilder
from processing_engine.utils.xml_parser import ClearXMLParser
from processing_engine.models.clear_models import (
    BusinessSearchRequest,
    PersonSearchRequest,
    BusinessReportRequest,
    PersonReportRequest,
    Business,
    Person,
    Address,
)
from processing_engine.models.execution import ProcessorInput, DocumentStipulation

from ..base_processor import BaseProcessor


class ClearProcessor(BaseProcessor):
    """Processor for Thomson Reuters CLEAR API comprehensive background checks."""

    PROCESSOR_NAME: str = "clear_processor"

    REQUIRED_DEPENDENCIES: tuple[str, ...] = (
        "p_application_forms",  # For business and owner information
    )

    def __init__(self, underwriting_id: str):
        """Initialize the CLEAR processor."""
        super().__init__(underwriting_id)
        self.clear_client = ClearAPIClient()
        self.xml_builder = XMLTemplateBuilder()
        self.xml_parser = ClearXMLParser()

    def _validate(
        self, data: Union[ProcessorInput, list[ProcessorInput]]
    ) -> list[ProcessorInput]:
        """Validate input data for CLEAR processing."""
        inputs = [data] if not isinstance(data, list) else data

        # Ensure we have the required application form data
        application_form = None
        for input_item in inputs:
            if (
                isinstance(input_item, DocumentStipulation)
                and input_item.stipulation_name == "s_application_form"
            ):
                application_form = input_item
                break

        if not application_form:
            raise ValueError("Application form data is required for CLEAR processing")

        # Validate that we have minimum required information
        form_data = getattr(application_form, "data", {})
        if not form_data:
            raise ValueError("Application form data is empty")

        # Check for business name or owner information
        business_name = form_data.get("business_name", "").strip()
        owner_first_name = form_data.get("owner_first_name", "").strip()
        owner_last_name = form_data.get("owner_last_name", "").strip()

        if not business_name and not (owner_first_name and owner_last_name):
            raise ValueError(
                "Either business name or owner name information is required"
            )

        self.logger.info("Validation passed for underwriting %s", self.underwriting_id)
        return inputs

    def _process(self, data: list[ProcessorInput]) -> dict[str, Any]:
        """Process CLEAR API requests for business and person background checks."""
        # Extract application form data
        application_form = None
        for input_item in data:
            if (
                isinstance(input_item, DocumentStipulation)
                and input_item.stipulation_name == "s_application_form"
            ):
                application_form = input_item
                break

        if not application_form:
            raise ValueError("Application form not found in validated data")

        form_data = getattr(application_form, "data", {})
        results = {}

        # Process business background check if business information is available
        business_result = self._process_business_check(form_data)
        if business_result:
            results["business_report"] = business_result

        # Process owner/principal background check if owner information is available
        owner_result = self._process_owner_check(form_data)
        if owner_result:
            results["owner_report"] = owner_result

        if not results:
            raise ValueError(
                "No valid searches could be performed with the provided data"
            )

        self.logger.info(
            "CLEAR processing completed for underwriting %s", self.underwriting_id
        )
        return results

    def _process_business_check(self, form_data: dict[str, Any]) -> dict[str, Any]:
        """Process business background check via CLEAR API."""
        business_name = form_data.get("business_name", "").strip()
        if not business_name:
            return None

        # Create business search request
        business = Business(
            business_name=business_name,
            fein=form_data.get("business_ein", ""),
            phone_number=form_data.get("business_phone", ""),
            address=self._extract_business_address(form_data),
        )

        search_request = BusinessSearchRequest(
            reference=f"AURA Business Search - {self.underwriting_id}",
            business=business,
        )

        # Perform business search
        search_xml = self.xml_builder.build_business_search_xml(search_request)
        search_response = self.clear_client.business_search(search_xml)
        search_result = self.xml_parser.parse_business_search_response(
            search_response["xml_response"]
        )

        if not search_result.success or not search_result.group_id:
            self.logger.warning("Business search failed: %s", search_result.error)
            return {
                "search_result": search_result.model_dump(),
                "report_result": None,
                "success": False,
                "error": search_result.error,
            }

        # Generate business report
        report_request = BusinessReportRequest(
            reference=f"AURA Business Report - {self.underwriting_id}",
            group_id=search_result.group_id,
        )

        report_xml = self.xml_builder.build_business_report_xml(report_request)
        report_response = self.clear_client.business_report(report_xml)
        report_result = self.xml_parser.parse_business_report_response(
            report_response["xml_response"]
        )

        return {
            "search_result": search_result.model_dump(),
            "report_result": report_result.model_dump(),
            "success": report_result.success,
            "error": report_result.error,
        }

    def _process_owner_check(self, form_data: dict[str, Any]) -> dict[str, Any]:
        """Process owner/principal background check via CLEAR API."""
        first_name = form_data.get("owner_first_name", "").strip()
        last_name = form_data.get("owner_last_name", "").strip()

        if not first_name or not last_name:
            return None

        # Create person search request
        person = Person(
            first_name=first_name,
            last_name=last_name,
            middle_initial=form_data.get("owner_middle_initial", ""),
        )

        search_request = PersonSearchRequest(
            reference=f"AURA Owner Search - {self.underwriting_id}",
            person=person,
            address=self._extract_owner_address(form_data),
        )

        # Perform person search
        search_xml = self.xml_builder.build_person_search_xml(search_request)
        search_response = self.clear_client.person_search(search_xml)
        search_result = self.xml_parser.parse_person_search_response(
            search_response["xml_response"]
        )

        if not search_result.success or not search_result.group_id:
            self.logger.warning("Person search failed: %s", search_result.error)
            return {
                "search_result": search_result.model_dump(),
                "report_result": None,
                "success": False,
                "error": search_result.error,
            }

        # Generate person report
        report_request = PersonReportRequest(
            reference=f"AURA Owner Report - {self.underwriting_id}",
            group_id=search_result.group_id,
        )

        report_xml = self.xml_builder.build_person_report_xml(report_request)
        report_response = self.clear_client.person_report(report_xml)
        report_result = self.xml_parser.parse_person_report_response(
            report_response["xml_response"]
        )

        return {
            "search_result": search_result.model_dump(),
            "report_result": report_result.model_dump(),
            "success": report_result.success,
            "error": report_result.error,
        }

    def _extract_business_address(self, form_data: dict[str, Any]) -> Address:
        """Extract business address from form data."""
        return Address(
            street=form_data.get("business_address", ""),
            city=form_data.get("business_city", ""),
            state=form_data.get("business_state", ""),
            zip_code=form_data.get("business_zip", ""),
            country="US",  # Default to US
        )

    def _extract_owner_address(self, form_data: dict[str, Any]) -> Address:
        """Extract owner address from form data."""
        return Address(
            street=form_data.get(
                "owner_address", form_data.get("business_address", "")
            ),
            city=form_data.get("owner_city", form_data.get("business_city", "")),
            state=form_data.get("owner_state", form_data.get("business_state", "")),
            zip_code=form_data.get("owner_zip", form_data.get("business_zip", "")),
            country="US",  # Default to US
        )

    def _extract(self, data: dict[str, Any]) -> dict[str, dict]:
        """Extract factors and flags from CLEAR processing results."""
        extraction_output = {
            "payload": data,
            "stipulations": {},
            "flags": {},
            "risk_factors": {},
        }

        # Extract business risk factors
        if "business_report" in data and data["business_report"].get("success"):
            business_report = data["business_report"]["report_result"]
            if business_report:
                extraction_output["flags"]["business_clear_check"] = "Completed"
                extraction_output["risk_factors"]["business_risk_flags"] = (
                    business_report.get("flags", {})
                )

                # Extract specific risk indicators
                if business_report.get("ucc_analysis"):
                    ucc_data = business_report["ucc_analysis"]
                    extraction_output["risk_factors"]["active_ucc_filings"] = (
                        ucc_data.get("active_count", 0)
                    )
                    extraction_output["flags"]["ucc_filings_risk"] = ucc_data.get(
                        "risk_assessment", "None"
                    )

                if business_report.get("liens_analysis"):
                    liens_data = business_report["liens_analysis"]
                    extraction_output["risk_factors"]["active_liens"] = liens_data.get(
                        "active_liens", 0
                    )
                    extraction_output["risk_factors"]["total_lien_amount"] = (
                        liens_data.get("total_amount", 0)
                    )
                    extraction_output["flags"]["liens_risk"] = liens_data.get(
                        "risk_assessment", "None"
                    )
        else:
            extraction_output["flags"]["business_clear_check"] = "Failed"
            if "business_report" in data:
                extraction_output["flags"]["business_clear_error"] = data[
                    "business_report"
                ].get("error", "Unknown error")

        # Extract owner risk factors
        if "owner_report" in data and data["owner_report"].get("success"):
            owner_report = data["owner_report"]["report_result"]
            if owner_report:
                extraction_output["flags"]["owner_clear_check"] = "Completed"
                extraction_output["risk_factors"]["owner_risk_flags"] = (
                    owner_report.get("flags", {})
                )

                # Extract criminal history indicators
                if owner_report.get("criminal_analysis"):
                    criminal_data = owner_report["criminal_analysis"]
                    extraction_output["risk_factors"]["criminal_records"] = (
                        criminal_data.get("total_count", 0)
                    )
                    extraction_output["risk_factors"]["violent_crimes"] = (
                        criminal_data.get("violent_crimes", 0)
                    )
                    extraction_output["risk_factors"]["financial_crimes"] = (
                        criminal_data.get("financial_crimes", 0)
                    )
                    extraction_output["flags"]["criminal_history_risk"] = (
                        criminal_data.get("risk_assessment", "None")
                    )

                # Extract lawsuit indicators
                if owner_report.get("lawsuit_analysis"):
                    lawsuit_data = owner_report["lawsuit_analysis"]
                    extraction_output["risk_factors"]["total_lawsuits"] = (
                        lawsuit_data.get("total_count", 0)
                    )
                    extraction_output["flags"]["lawsuit_risk"] = lawsuit_data.get(
                        "risk_assessment", "None"
                    )
        else:
            extraction_output["flags"]["owner_clear_check"] = "Failed"
            if "owner_report" in data:
                extraction_output["flags"]["owner_clear_error"] = data[
                    "owner_report"
                ].get("error", "Unknown error")

        # Set overall CLEAR processing status
        business_success = data.get("business_report", {}).get("success", False)
        owner_success = data.get("owner_report", {}).get("success", False)

        if business_success or owner_success:
            extraction_output["flags"]["clear_processing_status"] = "Completed"
        else:
            extraction_output["flags"]["clear_processing_status"] = "Failed"

        self.logger.info(
            "Factor extraction completed for underwriting %s", self.underwriting_id
        )
        return extraction_output
