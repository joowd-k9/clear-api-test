"""XML template builder for Thomson Reuters CLEAR API requests."""

import os
import re
from typing import Dict, Any

from processing_engine.models.clear_models import (
    BusinessSearchRequest,
    PersonSearchRequest,
    BusinessReportRequest,
    PersonReportRequest,
)


class XMLTemplateBuilder:
    """Builder class for converting request models to XML format."""

    def __init__(self):
        """Initialize the XML template builder."""
        self.template_dir = os.path.join(os.path.dirname(__file__), "templates")
        os.makedirs(self.template_dir, exist_ok=True)
        self._create_templates()

    def _create_templates(self) -> None:
        """Create XML template files if they don't exist."""
        templates = {
            "business-search.xml": self._get_business_search_template(),
            "person-search.xml": self._get_person_search_template(),
            "business-report.xml": self._get_business_report_template(),
            "person-report.xml": self._get_person_report_template(),
        }

        for filename, content in templates.items():
            filepath = os.path.join(self.template_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

    def _load_template(self, template_name: str) -> str:
        """Load XML template from templates directory."""
        template_path = os.path.join(self.template_dir, template_name)
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def _flatten_model(self, model: Any) -> Dict[str, Any]:
        """Flatten Pydantic model for template interpolation."""
        flat_data = {}

        if hasattr(model, "model_dump"):
            data = model.model_dump()
        else:
            data = model.dict()

        def flatten_dict(d: Dict[str, Any], prefix: str = "") -> None:
            for key, value in d.items():
                if isinstance(value, dict):
                    flatten_dict(value, prefix)
                else:
                    flat_data[key] = str(value) if value is not None else ""

        flatten_dict(data)
        return flat_data

    def _safe_format_template(self, template: str, data: Dict[str, Any]) -> str:
        """Safely format template with data, providing empty string for missing keys."""

        def replace_placeholder(match):
            key = match.group(1)
            return str(data.get(key, ""))

        return re.sub(r"\\{(\\w+)\\}", replace_placeholder, template)

    def build_business_search_xml(self, request: BusinessSearchRequest) -> str:
        """Convert BusinessSearchRequest to XML format."""
        template = self._load_template("business-search.xml")
        flat_data = self._flatten_model(request)
        return self._safe_format_template(template, flat_data)

    def build_person_search_xml(self, request: PersonSearchRequest) -> str:
        """Convert PersonSearchRequest to XML format."""
        template = self._load_template("person-search.xml")
        flat_data = self._flatten_model(request)
        return self._safe_format_template(template, flat_data)

    def build_business_report_xml(self, request: BusinessReportRequest) -> str:
        """Convert BusinessReportRequest to XML format."""
        template = self._load_template("business-report.xml")
        flat_data = self._flatten_model(request)
        return self._safe_format_template(template, flat_data)

    def build_person_report_xml(self, request: PersonReportRequest) -> str:
        """Convert PersonReportRequest to XML format."""
        template = self._load_template("person-report.xml")
        flat_data = self._flatten_model(request)
        return self._safe_format_template(template, flat_data)

    def _get_business_search_template(self) -> str:
        """Get business search XML template."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<bs:BusinessSearchRequest xmlns:bs="http://clear.thomsonreuters.com/api/search/2.0">
    <PermissiblePurpose>
        <GLB>{glb}</GLB>
        <DPPA>{dppa}</DPPA>
        <VOTER>{voter}</VOTER>
    </PermissiblePurpose>
    <Reference>{reference}</Reference>
    <Criteria>
        <b1:BusinessCriteria xmlns:b1="com/thomsonreuters/schemas/search">
            <CompanyEntityId>{company_entity_id}</CompanyEntityId>
            <BusinessName>{business_name}</BusinessName>
            <CorporationInfo>
                <CorporationId>{corporation_id}</CorporationId>
                <FilingNumber>{filing_number}</FilingNumber>
                <FilingDate>{filing_date}</FilingDate>
                <FEIN>{fein}</FEIN>
                <DUNSNumber>{duns_number}</DUNSNumber>
            </CorporationInfo>
            <NPINumber>{npi_number}</NPINumber>
            <NameInfo>
                <AdvancedNameSearch>
                    <LastSecondaryNameSoundSimilarOption>false</LastSecondaryNameSoundSimilarOption>
                    <SecondaryLastNameOption>OR</SecondaryLastNameOption>
                    <FirstNameSoundSimilarOption>false</FirstNameSoundSimilarOption>
                    <FirstNameVariationsOption>false</FirstNameVariationsOption>
                </AdvancedNameSearch>
                <LastName>{last_name}</LastName>
                <FirstName>{first_name}</FirstName>
                <MiddleInitial>{middle_initial}</MiddleInitial>
                <SecondaryLastName>{secondary_last_name}</SecondaryLastName>
            </NameInfo>
            <AddressInfo>
                <StreetNamesSoundSimilarOption>false</StreetNamesSoundSimilarOption>
                <Street>{street}</Street>
                <City>{city}</City>
                <State>{state}</State>
                <County>{county}</County>
                <ZipCode>{zip_code}</ZipCode>
                <Province>{province}</Province>
                <Country>{country}</Country>
            </AddressInfo>
            <PhoneNumber>{phone_number}</PhoneNumber>
            <IndustryCodes>
                <NAICSCode>{naics_code}</NAICSCode>
                <SICCode>{sic_code}</SICCode>
            </IndustryCodes>
        </b1:BusinessCriteria>
    </Criteria>
    <Datasources>
        <PublicRecordBusiness>true</PublicRecordBusiness>
        <NPIRecord>true</NPIRecord>
        <PublicRecordUCCFilings>true</PublicRecordUCCFilings>
        <WorldCheckRiskIntelligence>true</WorldCheckRiskIntelligence>
    </Datasources>
</bs:BusinessSearchRequest>"""

    def _get_person_search_template(self) -> str:
        """Get person search XML template."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<ps:PersonSearchRequest xmlns:ps="http://clear.thomsonreuters.com/api/search/3.0">
    <PermissiblePurpose>
        <GLB>{glb}</GLB>
        <DPPA>{dppa}</DPPA>
        <VOTER>{voter}</VOTER>
    </PermissiblePurpose>
    <Reference>{reference}</Reference>
    <Criteria>
        <p1:PersonCriteria xmlns:p1="com/thomsonreuters/schemas/search">
            <NameInfo>
                <AdvancedNameSearch>
                    <LastSecondaryNameSoundSimilarOption>false</LastSecondaryNameSoundSimilarOption>
                    <SecondaryLastNameOption>OR</SecondaryLastNameOption>
                    <FirstNameSoundSimilarOption>false</FirstNameSoundSimilarOption>
                    <FirstNameVariationsOption>false</FirstNameVariationsOption>
                </AdvancedNameSearch>
                <LastName>{last_name}</LastName>
                <FirstName>{first_name}</FirstName>
                <MiddleInitial>{middle_initial}</MiddleInitial>
                <SecondaryLastName>{secondary_last_name}</SecondaryLastName>
            </NameInfo>
            <AddressInfo>
                <StreetNamesSoundSimilarOption>false</StreetNamesSoundSimilarOption>
                <Street>{street}</Street>
                <City>{city}</City>
                <State>{state}</State>
                <County>{county}</County>
                <ZipCode>{zip_code}</ZipCode>
                <Province>{province}</Province>
                <Country>{country}</Country>
            </AddressInfo>
        </p1:PersonCriteria>
    </Criteria>
    <Datasources>
        <PublicRecordPerson>true</PublicRecordPerson>
        <CriminalAndTrafficRecord>true</CriminalAndTrafficRecord>
        <LienJudgmentRecord>true</LienJudgmentRecord>
        <UCCRecord>true</UCCRecord>
        <WorldCheckRiskIntelligence>true</WorldCheckRiskIntelligence>
    </Datasources>
</ps:PersonSearchRequest>"""

    def _get_business_report_template(self) -> str:
        """Get business report XML template."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<br:BusinessReportRequest xmlns:br="http://clear.thomsonreuters.com/api/report/2.0">
    <PermissiblePurpose>
        <GLB>{glb}</GLB>
        <DPPA>{dppa}</DPPA>
        <VOTER>{voter}</VOTER>
    </PermissiblePurpose>
    <Reference>{reference}</Reference>
    <Criteria>
        <GroupId>{group_id}</GroupId>
    </Criteria>
</br:BusinessReportRequest>"""

    def _get_person_report_template(self) -> str:
        """Get person report XML template."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<pr:PersonReportRequest xmlns:pr="http://clear.thomsonreuters.com/api/report/3.0">
    <PermissiblePurpose>
        <GLB>{glb}</GLB>
        <DPPA>{dppa}</DPPA>
        <VOTER>{voter}</VOTER>
    </PermissiblePurpose>
    <Reference>{reference}</Reference>
    <Criteria>
        <GroupId>{group_id}</GroupId>
    </Criteria>
</pr:PersonReportRequest>"""
