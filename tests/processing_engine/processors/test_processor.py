"""
Concrete test processor implementation for testing BaseProcessor functionality.
"""

import sys
import os
from typing import Any

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.base_processor import BaseProcessor
from processing_engine.processors.runners import SequentialRunner


class ConcreteTestProcessor(BaseProcessor):
    """
    Concrete implementation of BaseProcessor for testing purposes.
    """

    PROCESSOR_NAME = "test_processor"

    def __init__(
        self, account_id: str, underwriting_id: str, should_fail: bool = False
    ):
        """
        Initialize the test processor.

        Args:
            account_id: The account ID
            underwriting_id: The underwriting ID
            should_fail: If True, the processor will fail during processing
        """
        super().__init__(account_id, underwriting_id, SequentialRunner())
        self.should_fail = should_fail

    def _validate(self, data: Any) -> Any:
        """
        Validate the input data.
        """
        if not isinstance(data, str):
            raise ValueError("Data must be a string")
        if len(data) < 3:
            raise ValueError("Data must be at least 3 characters long")
        return data

    def _process(self, data: Any) -> Any:
        """
        Process the validated data.
        """
        if self.should_fail:
            raise RuntimeError("Intentional failure for testing")
        return f"processed_{data}"

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """
        Extract factors from the processed data.
        """
        return {
            "original_data": data.replace("processed_", ""),
            "processed_data": data,
            "length": str(len(data)),
            "factors": {"is_processed": "true", "data_type": "string"},
        }


class FailingValidationProcessor(BaseProcessor):
    """
    Processor that fails during validation for testing error handling.
    """

    PROCESSOR_NAME = "failing_validation_processor"

    def _validate(self, data: Any) -> Any:
        """Always fail validation."""
        raise ValueError("Validation always fails")

    def _process(self, data: Any) -> Any:
        """This should never be called."""
        return data

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """This should never be called."""
        return {}


class FailingProcessingProcessor(BaseProcessor):
    """
    Processor that fails during processing for testing error handling.
    """

    PROCESSOR_NAME = "failing_processing_processor"

    def _validate(self, data: Any) -> Any:
        """Always pass validation."""
        return data

    def _process(self, data: Any) -> Any:
        """Always fail processing."""
        raise RuntimeError("Processing always fails")

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """This should never be called."""
        return {}


class FailingExtractionProcessor(BaseProcessor):
    """
    Processor that fails during extraction for testing error handling.
    """

    PROCESSOR_NAME = "failing_extraction_processor"

    def _validate(self, data: Any) -> Any:
        """Always pass validation."""
        return data

    def _process(self, data: Any) -> Any:
        """Always pass processing."""
        return f"processed_{data}"

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """Always fail extraction."""
        raise KeyError("Extraction always fails")
