"""Pydantic models for permissible purpose codes used in Clear API requests."""

from typing import Literal
from pydantic import BaseModel, Field


GLBCode = Literal["C", "A", "I", "J", "B", "L", "Q", "H", "K"]
DPPACode = Literal[1, 3, 4, 6, 0, "1", "3", "4", "6", "0"]
VoterCode = Literal[2, 5, 7, "2", "5", "7"]


class PermissiblePurpose(BaseModel):
    """Permissible purpose codes."""

    glb: GLBCode = Field(
        default="I",
        description=(
            "GLB code: C=Legal interest, A=Legal compliance, I=Transaction, "
            "J=Investigation, B=Fraud prevention, L=Law enforcement, "
            "Q=Consumer consent, H=Fiduciary, K=Risk control"
        ),
    )
    dppa: DPPACode = Field(
        default=3,
        description=(
            "DPPA code: 1=Official use, 3=Skip tracing, "
            "4=Legal proceeding, 6=Insurance, 0=No permitted use"
        ),
    )
    voter: VoterCode = Field(
        default=7,
        description="Voter code: 2=Election, 5=Non-commercial, 7=No permitted use",
    )
