"""Pydantic models for address used in Clear API requests."""

from pydantic import BaseModel, Field


class Address(BaseModel):
    """Address information."""

    zip_code: str = Field(
        default="", description="ZIP code", format="5 or 6 digit ZIP code"
    )
    street: str = Field(default="", description="Street address")
    city: str = Field(description="City")
    state: str = Field(
        description="State", format="2-letter state code (e.g. CA, NY, etc.)"
    )
    county: str = Field(default="", description="County")
    province: str = Field(
        default="", description="Province", format="Full province name"
    )
    country: str = Field(default="USA", description="Country", format="ISO alpha-3")
