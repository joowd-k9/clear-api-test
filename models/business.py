"""Business-related Pydantic models for Clear API."""

from typing import Optional, Union
from pydantic import BaseModel, Field

from models.address import Address
from models.permissible_purpose import PermissiblePurpose
from models.person import Person


class IndustryCodes(BaseModel):
    """Industry codes."""

    naics_code: Optional[str] = Field(
        default="", description="NAICS code", format="6-digit"
    )
    sic_code: Optional[str] = Field(
        default="", description="SIC code", format="4-digit"
    )


class Business(BaseModel):
    """Business basic information."""

    company_entity_id: Optional[str] = Field(
        default="",
        description="Company entity ID. "
        "If this element is populated then no other criteria is required and "
        "will be ignored if populated.",
    )
    business_name: Optional[str] = Field(default="", description="Business name")
    corporation_id: Optional[str] = Field(default="", description="Corporation ID")
    filing_number: Optional[str] = Field(default="", description="Filing Number")
    filing_date: Optional[str] = Field(
        default="", description="Filing date", format="MM/DD/YYYY"
    )
    fein: Optional[str] = Field(
        default="",
        description="Federal Employer Identification Number",
        format="9 or 11 numeric characters",
    )
    duns_number: Optional[Union[str, int]] = Field(
        default="",
        description="DUNS number",
        format="9 numeric characters",
    )
    npi_number: Optional[Union[str, int]] = Field(
        default="",
        description="National Provider Identifier",
        format="10 numeric characters",
    )
    phone_number: Optional[Union[str, int]] = Field(
        default="", description="Phone number", format="###-###-#### or ###-####"
    )
    industry: Optional[IndustryCodes] = Field(
        default=None, description="Industry codes"
    )
    address: Optional[Address] = Field(default=None, description="Address information")
    principal: Optional[Person] = Field(
        default=None, description="Principal or owner information"
    )


class BusinessSearchRequest(BaseModel):
    """Search request for a business."""

    reference: str = Field(
        default="S2S Business Search", description="Search reference"
    )
    business: Business = Field(description="Business information")
    # industry: Optional[IndustryCodes] = Field(default=None, description="Industry codes")
    # principal: Optional[Person] = Field(
    #     default=None, description="Principal information"
    # )
    # address: Optional[Address] = Field(default=None, description="Address information")
    # permissible_purpose: PermissiblePurpose = Field(
    #     default=PermissiblePurpose(), description="Permissible purpose"
    # )
