"""Person-related Pydantic models for Clear API."""

from typing import Optional
from pydantic import BaseModel, Field


class Person(BaseModel):
    """Person's name information."""

    last_name: str = Field(description="Last name")
    first_name: str = Field(description="First name")
    middle_initial: Optional[str] = Field(default="", description="Middle initial")
    secondary_last_name: Optional[str] = Field(
        default="", description="Secondary last name"
    )
