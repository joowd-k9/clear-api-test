"""Pydantic models for Thomson Reuters CLEAR API integration."""

from typing import Optional, Union, Dict, Any
from pydantic import BaseModel, Field


class Address(BaseModel):
    """Address information model."""

    street: Optional[str] = Field(default="", description="Street address")
    city: Optional[str] = Field(default="", description="City name")
    state: Optional[str] = Field(default="", description="State/Province")
    county: Optional[str] = Field(default="", description="County")
    zip_code: Optional[str] = Field(default="", description="ZIP/Postal code")
    province: Optional[str] = Field(default="", description="Province (for non-US)")
    country: Optional[str] = Field(default="", description="Country")


class Person(BaseModel):
    """Person information model."""

    last_name: str = Field(description="Last name")
    first_name: str = Field(description="First name")
    middle_initial: Optional[str] = Field(default="", description="Middle initial")
    secondary_last_name: Optional[str] = Field(
        default="", description="Secondary last name"
    )


class PermissiblePurpose(BaseModel):
    """Permissible purpose for data access."""

    glb: str = Field(default="Y", description="GLB compliance flag")
    dppa: str = Field(default="Y", description="DPPA compliance flag")
    voter: str = Field(default="Y", description="Voter record access flag")


class IndustryCodes(BaseModel):
    """Industry classification codes."""

    naics_code: Optional[str] = Field(default="", description="NAICS code (6-digit)")
    sic_code: Optional[str] = Field(default="", description="SIC code (4-digit)")


class Business(BaseModel):
    """Business entity information."""

    company_entity_id: Optional[str] = Field(
        default="",
        description="Company entity ID - if populated, other criteria ignored",
    )
    business_name: Optional[str] = Field(default="", description="Business name")
    corporation_id: Optional[str] = Field(default="", description="Corporation ID")
    filing_number: Optional[str] = Field(default="", description="Filing number")
    filing_date: Optional[str] = Field(
        default="", description="Filing date (MM/DD/YYYY)"
    )
    fein: Optional[str] = Field(
        default="",
        description="Federal Employer Identification Number (9 or 11 digits)",
    )
    duns_number: Optional[Union[str, int]] = Field(
        default="", description="DUNS number (9 digits)"
    )
    npi_number: Optional[Union[str, int]] = Field(
        default="", description="National Provider Identifier (10 digits)"
    )
    phone_number: Optional[Union[str, int]] = Field(
        default="", description="Phone number"
    )
    industry: Optional[IndustryCodes] = Field(
        default=None, description="Industry codes"
    )
    address: Optional[Address] = Field(default=None, description="Business address")
    principal: Optional[Person] = Field(
        default=None, description="Principal/owner info"
    )


class BusinessSearchRequest(BaseModel):
    """Business search request model."""

    reference: str = Field(
        default="AURA Business Search", description="Search reference"
    )
    business: Business = Field(description="Business search criteria")
    permissible_purpose: PermissiblePurpose = Field(
        default_factory=PermissiblePurpose,
        description="Permissible purpose for data access",
    )


class PersonSearchRequest(BaseModel):
    """Person search request model."""

    reference: str = Field(default="AURA Person Search", description="Search reference")
    person: Person = Field(description="Person search criteria")
    address: Optional[Address] = Field(default=None, description="Person address")
    permissible_purpose: PermissiblePurpose = Field(
        default_factory=PermissiblePurpose,
        description="Permissible purpose for data access",
    )


class BusinessReportRequest(BaseModel):
    """Business report generation request."""

    reference: str = Field(
        default="AURA Business Report", description="Report reference"
    )
    group_id: str = Field(description="Group ID from business search results")
    permissible_purpose: PermissiblePurpose = Field(
        default_factory=PermissiblePurpose,
        description="Permissible purpose for data access",
    )


class PersonReportRequest(BaseModel):
    """Person report generation request."""

    reference: str = Field(default="AURA Person Report", description="Report reference")
    group_id: str = Field(description="Group ID from person search results")
    permissible_purpose: PermissiblePurpose = Field(
        default_factory=PermissiblePurpose,
        description="Permissible purpose for data access",
    )


class ClearSearchResult(BaseModel):
    """CLEAR search result model."""

    group_id: Optional[str] = Field(
        default=None, description="Group ID for report generation"
    )
    xml_response: str = Field(description="Raw XML response from CLEAR API")
    status_code: int = Field(description="HTTP status code")
    success: bool = Field(description="Whether the search was successful")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class ClearReportResult(BaseModel):
    """CLEAR report result model."""

    reference: Optional[str] = Field(default=None, description="Report reference")
    report_type: Optional[str] = Field(default=None, description="Type of report")
    subject: Optional[str] = Field(default=None, description="Report subject")
    entity_id: Optional[str] = Field(default=None, description="Entity ID")
    timestamp: Optional[str] = Field(default=None, description="Report timestamp")

    # Risk flags and analysis
    flags: Dict[str, str] = Field(default_factory=dict, description="Risk flags")
    ucc_analysis: Dict[str, Any] = Field(
        default_factory=dict, description="UCC filings analysis"
    )
    liens_analysis: Dict[str, Any] = Field(
        default_factory=dict, description="Liens and judgments analysis"
    )
    criminal_analysis: Dict[str, Any] = Field(
        default_factory=dict, description="Criminal history analysis"
    )
    lawsuit_analysis: Dict[str, Any] = Field(
        default_factory=dict, description="Lawsuit analysis"
    )
    docket_analysis: Dict[str, Any] = Field(
        default_factory=dict, description="Docket records analysis"
    )

    # Raw data
    xml_response: str = Field(description="Raw XML response from CLEAR API")
    parsed_results: Dict[str, Any] = Field(
        default_factory=dict, description="Parsed report sections"
    )
    status_code: int = Field(description="HTTP status code")
    success: bool = Field(description="Whether the report was successful")
    error: Optional[str] = Field(default=None, description="Error message if failed")
