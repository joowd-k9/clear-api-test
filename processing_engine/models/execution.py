"""
Execution models for processing engine.

This module defines data structures related to the execution of processors.
It captures runtime outcomes such as results, validation states, errors,
and historical execution tracking.

Key responsibilities:
- Represent the result of processor execution (success, failure, payload).
- Standardize validation results for input documents or data.
- Capture errors in a structured format with context.
- Optionally log metadata such as timestamps, duration, and user info.

These models are dynamic in nature, describing *what happened during a run*
of a processor rather than the processor's static configuration.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProcessorInput:
    """
    Processing input.
    """

    underwriting_id: str


@dataclass
class DocumentStipulation(ProcessorInput):
    """
    Represents a document used in underwriting or processing.
    """

    stipulation_name: str
    document_title: str
    content: bytes | str
    mime_type: str
    uploaded_at: datetime = field(default_factory=datetime.now)
    source: str | None = None


@dataclass
class ProcessingResult(ProcessorInput):
    """
    Processor's execution output.
    """

    run_id: str
    processor_name: str
    extraction_output: dict[str, dict | str]
    success: bool
    timestamp: datetime = field(default_factory=datetime.now)
    duration: int = 0
    error: Exception | None = None
