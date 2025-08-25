"""Business-related Pydantic models for Clear API."""

from typing import Union
from pydantic import BaseModel, Field


class BusinessSearchRequest(BaseModel):
    """Pydantic model for business search request."""

    reference: str = Field(
        default="S2S Business Search", description="Search reference"
    )
    business_name: str = Field(description="Business name")
    corporation_id: str = Field(default="", description="Corporation ID")
    filing_number: str = Field(default="", description="Filing Number")
    filing_date: str = Field(default="", description="Filing date", format="MM/DD/YYYY")
    fein: str = Field(default="", description="Federal Employer Identification Number")
    duns_number: Union[str, int] = Field(default="", description="DUNS number")
    npi_number: Union[str, int] = Field(
        default="", description="National Provider Identifier"
    )
    last_name: str = Field(description="Officer, Agent or Director Last Name")
    first_name: str = Field(description="Officer, Agent or Director First Name")
    middle_initial: str = Field(
        default="", description="Officer, Agent or Director Middle Initial"
    )
    secondary_last_name: str = Field(
        default="", description="Officer, Agent or Director Secondary Last Name"
    )
    street: str = Field(description="Street address")
    city: str = Field(description="City")
    state: str = Field(description="State")
    county: str = Field(default="", description="County")
    zip_code: Union[str, int] = Field(description="ZIP code")
    province: str = Field(default="", description="Province")
    country: str = Field(default="", description="Country")
    phone_number: Union[str, int] = Field(default="", description="Phone number")
