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
from typing import Any, Literal


@dataclass
class CostEntry:
    """
    Represents a single cost entry for tracking API calls or processing activities.

    This class is used by processors to track costs incurred during execution,
    particularly for external API calls that have per-call charges.

    Attributes:
        service: The service name (e.g., 'experian', 'clear', 'ocr')
        operation: The operation performed (e.g., 'credit_report', 'business_search')
        cost: The cost of the operation
        metadata: Additional metadata about the operation
        timestamp: When the cost was incurred
    """
    service: str
    operation: str
    cost: float
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ProcessorInput:
    """
    Processor input data.

    Each input is given a unique `input_id` so it can be traced,
    retried, or correlated with outputs and errors.

    Attributes:
        input_id (str): Unique identifier for this input.
            - Useful for idempotency (detecting duplicate runs).
            - Allows partial retries in batch processing.
            - Enables fine-grained logging and auditing.
        account_id (str): Identifier of the account the input belongs to.
        underwriting_id (str): Identifier of the underwriting process
            this input is tied to.
        data (Any): The actual payload to be processed.
        payload (Any): If the processor fails, this is the payload that failed.
    """

    input_id: str
    account_id: str
    underwriting_id: str
    data: Any
    payload: Any | None = None


@dataclass
class ExecutionContext:
    """
    Execution context containing metadata about the current processing run.

    This provides a flexible container for execution-related information
    that can be extended as needed without changing method signatures.
    """

    trigger_type: Literal["manual", "automatic"] = "automatic"
    trigger_initiator: str | None = None  # user:id or system
    trigger_timestamp: datetime | None = None
    parent_run_id: str | None = None
    previous_run_id: str | None = None
    last_error_step: str | None = None
    retry_count: int = 0
    execution_metadata: dict[str, str] = field(default_factory=dict)
    payloads: list[ProcessorInput | dict[str, str]] = field(default_factory=list)

    def update(self, **kwargs):
        """
        Update the execution context with the given kwargs.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclass
class ProcessingResult:
    """
    Processor's execution output.

    Attributes:
        execution_id: The id of the current run
        account_id: The id of the account the processor is running for
        underwriting_id: The id of the underwriting the processor is running for
        output: The output of the processor
        success: Whether the processor execution was successful
        context: The context of the current run
        timestamp: The timestamp of the processor execution
        duration: The duration of the processor execution
        error: The error of the processor execution
        payloads: The payloads of the processor execution if the processor failed
        cost_breakdown: Detailed cost breakdown for the processor execution
    """

    execution_id: str
    account_id: str
    underwriting_id: str
    output: list[dict[str, str]]
    success: bool
    context: ExecutionContext = field(default_factory=ExecutionContext)
    timestamp: datetime = field(default_factory=datetime.now)
    duration: int = 0
    error: dict[str, str] | None = None
    payloads: list[ProcessorInput | dict[str, str]] | None = None
    cost_breakdown: dict[str, Any] | None = None
