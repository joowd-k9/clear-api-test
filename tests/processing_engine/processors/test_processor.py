"""
Concrete test processor implementation for testing BaseProcessor functionality.
"""

import sys
import os
from typing import Any

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.base_processor import BaseProcessor
from processing_engine.processors.runners import DefaultRunner


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
        super().__init__(account_id, underwriting_id, DefaultRunner())
        self.should_fail = should_fail

    def _validate_input(self, data: Any) -> Any:
        """
        Validate the input data.
        """
        if not isinstance(data, str):
            raise ValueError("Data must be a string")
        if len(data) < 3:
            raise ValueError("Data must be at least 3 characters long")
        return data

    def _validate_result(self, data: Any) -> Any:
        """
        Validate the result data.
        """
        return data

    def _aggregate_result(self, data: Any) -> dict[str, str | list | dict]:
        """
        Aggregate the result data.
        """
        return data

    def _transform_input(self, data: Any) -> Any:
        """
        Transform the input data.
        """
        if self.should_fail:
            raise RuntimeError("Intentional failure for testing")

        # Transform the data values in the list
        if isinstance(data, list):
            return [f"processed_{item}" for item in data]
        else:
            return f"processed_{data}"

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """
        Extract factors from the processed data.
        """
        # Since we removed the processing step, we need to handle the raw data
        # The data parameter is actually a ProcessorInput object
        if hasattr(data, 'data'):
            # Extract the actual data from ProcessorInput
            actual_data = data.data
        else:
            actual_data = data

        # Include validation logic here since validation step was removed
        if not isinstance(actual_data, str):
            raise ValueError("Data must be a string")
        if len(actual_data) < 3:
            raise ValueError("Data must be at least 3 characters long")

        processed_data = f"processed_{actual_data}"
        return {
            "original_data": actual_data,
            "processed_data": processed_data,
            "length": str(len(processed_data)),
            "factors": {"is_processed": "true", "data_type": "string"},
        }


class FailingValidationProcessor(BaseProcessor):
    """
    Processor that fails during extraction for testing error handling.
    """

    PROCESSOR_NAME = "failing_validation_processor"

    def _validate_input(self, data: Any) -> Any:
        """Always pass validation."""
        return data

    def _validate_result(self, data: Any) -> Any:
        """Always pass result validation."""
        return data

    def _aggregate_result(self, data: Any) -> dict[str, str | list | dict]:
        """Always pass aggregation."""
        return data

    def _transform_input(self, data: Any) -> Any:
        """Always pass transformation."""
        return data

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """Always fail extraction."""
        raise ValueError("Validation always fails")


class FailingProcessingProcessor(BaseProcessor):
    """
    Processor that fails during extraction for testing error handling.
    """

    PROCESSOR_NAME = "failing_processing_processor"

    def _validate_input(self, data: Any) -> Any:
        """Always pass validation."""
        return data

    def _validate_result(self, data: Any) -> Any:
        """Always pass result validation."""
        return data

    def _aggregate_result(self, data: Any) -> dict[str, str | list | dict]:
        """Always pass aggregation."""
        return data

    def _transform_input(self, data: Any) -> Any:
        """Always pass transformation."""
        return data

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """Always fail extraction."""
        raise RuntimeError("Processing always fails")


class FailingExtractionProcessor(BaseProcessor):
    """
    Processor that fails during extraction for testing error handling.
    """

    PROCESSOR_NAME = "failing_extraction_processor"

    def _validate_input(self, data: Any) -> Any:
        """Always pass validation."""
        return data

    def _validate_result(self, data: Any) -> Any:
        """Always pass result validation."""
        return data

    def _aggregate_result(self, data: Any) -> dict[str, str | list | dict]:
        """Always pass aggregation."""
        return data

    def _transform_input(self, data: Any) -> Any:
        """Always pass transformation."""
        return data

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """Always fail extraction."""
        raise KeyError("Extraction always fails")
