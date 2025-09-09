"""
Tests for the resume from failure functionality.
"""

import pytest
import sys
import os
from typing import Any

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from processing_engine.processors.base_processor import BaseProcessor
from processing_engine.models.execution import ProcessorInput, ExecutionContext
from processing_engine.processors.runners import SequentialRunner


class ResumeFromFailureTestProcessor(BaseProcessor):
    """
    Test processor that can fail at different steps for testing resume functionality.
    """

    PROCESSOR_NAME = "resume_test_processor"

    def __init__(self, account_id: str, underwriting_id: str, fail_at_step: str = None):
        super().__init__(account_id, underwriting_id, SequentialRunner())
        self.fail_at_step = fail_at_step
        self.step_call_count = {"validation": 0, "processing": 0, "extraction": 0}

    def _validate(self, data: Any) -> Any:
        self.step_call_count["validation"] += 1
        if self.fail_at_step == "validation":
            raise ValueError("Validation failed")
        return data

    def _process(self, data: Any) -> Any:
        self.step_call_count["processing"] += 1
        if self.fail_at_step == "processing":
            raise RuntimeError("Processing failed")
        return f"processed_{data}"

    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        self.step_call_count["extraction"] += 1
        if self.fail_at_step == "extraction":
            raise KeyError("Extraction failed")
        return {
            "original_data": data.replace("processed_", ""),
            "processed_data": data,
            "length": str(len(data)),
        }


class TestResumeFromFailure:
    """Test the resume from failure functionality."""

    def test_normal_execution_no_retry(self):
        """Test normal execution without retry."""
        processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data"
            )
        ]

        result = processor.execute(inputs)

        assert result.success is True
        assert result.payloads is None

        # Check that all steps were called
        assert processor.step_call_count["validation"] == 1
        assert processor.step_call_count["processing"] == 1
        assert processor.step_call_count["extraction"] == 1

        # Check output
        assert result.output["original_data"] == "test_data"
        assert result.output["processed_data"] == "processed_test_data"

    def test_failure_at_validation_step(self):
        """Test failure at validation step and retry from validation."""
        processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456", fail_at_step="validation")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data"
            )
        ]

        # First execution - should fail at validation
        result = processor.execute(inputs)

        assert result.success is False
        assert result.payloads is not None
        assert len(result.payloads) == 1

        # Check that only validation was called
        assert processor.step_call_count["validation"] == 1
        assert processor.step_call_count["processing"] == 0
        assert processor.step_call_count["extraction"] == 0

        # Check error details
        error_result = result.output[0]
        assert error_result["success"] is False
        assert error_result["step"] == "validation"
        assert error_result["exception"] == "ValueError"

        # Now retry with the payload from the failed execution
        retry_inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data",
                payload=result.payloads[0].payload  # This contains the error info
            )
        ]

        # Create a new processor that won't fail this time
        retry_processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456")

        retry_result = retry_processor.execute(retry_inputs)

        assert retry_result.success is True

        # Check that it resumed from validation step (validation should be called again)
        assert retry_processor.step_call_count["validation"] == 1
        assert retry_processor.step_call_count["processing"] == 1
        assert retry_processor.step_call_count["extraction"] == 1

        # Check output
        assert retry_result.output["original_data"] == "test_data"
        assert retry_result.output["processed_data"] == "processed_test_data"

    def test_failure_at_processing_step(self):
        """Test failure at processing step and retry from processing."""
        processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456", fail_at_step="processing")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data"
            )
        ]

        # First execution - should fail at processing
        result = processor.execute(inputs)

        assert result.success is False

        # Check that validation and processing were called
        assert processor.step_call_count["validation"] == 1
        assert processor.step_call_count["processing"] == 1
        assert processor.step_call_count["extraction"] == 0

        # Check error details
        error_result = result.output[0]
        assert error_result["step"] == "processing"
        assert error_result["exception"] == "RuntimeError"

        # Now retry with the payload from the failed execution
        retry_inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data",
                payload=result.payloads[0].payload
            )
        ]

        # Create a new processor that won't fail this time
        retry_processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456")

        retry_result = retry_processor.execute(retry_inputs)

        assert retry_result.success is True

        # Check that it resumed from processing step (validation should be skipped)
        assert retry_processor.step_call_count["validation"] == 0  # Skipped
        assert retry_processor.step_call_count["processing"] == 1  # Resumed from here
        assert retry_processor.step_call_count["extraction"] == 1

        # Check output
        assert retry_result.output["original_data"] == "test_data"
        assert retry_result.output["processed_data"] == "processed_test_data"

    def test_failure_at_extraction_step(self):
        """Test failure at extraction step and retry from extraction."""
        processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456", fail_at_step="extraction")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data"
            )
        ]

        # First execution - should fail at extraction
        result = processor.execute(inputs)

        assert result.success is False

        # Check that all steps except extraction were called
        assert processor.step_call_count["validation"] == 1
        assert processor.step_call_count["processing"] == 1
        assert processor.step_call_count["extraction"] == 1

        # Check error details
        error_result = result.output[0]
        assert error_result["step"] == "extraction"
        assert error_result["exception"] == "KeyError"

        # Now retry with the payload from the failed execution
        retry_inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data",
                payload=result.payloads[0].payload
            )
        ]

        # Create a new processor that won't fail this time
        retry_processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456")

        retry_result = retry_processor.execute(retry_inputs)

        assert retry_result.success is True

        # Check that it resumed from extraction step (validation and processing should be skipped)
        assert retry_processor.step_call_count["validation"] == 0  # Skipped
        assert retry_processor.step_call_count["processing"] == 0  # Skipped
        assert retry_processor.step_call_count["extraction"] == 1  # Resumed from here

        # Check output
        assert retry_result.output["original_data"] == "test_data"
        assert retry_result.output["processed_data"] == "processed_test_data"

    def test_retry_without_payload_step_info(self):
        """Test retry when payload doesn't contain step information."""
        processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456", fail_at_step="validation")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data"
            )
        ]

        # First execution - should fail
        result = processor.execute(inputs)
        assert result.success is False

        # Create retry input with payload that doesn't contain step info
        retry_inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data",
                payload="some_old_payload"  # No step information
            )
        ]

        # Create a new processor that won't fail this time
        retry_processor = ResumeFromFailureTestProcessor("account_123", "underwriting_456")

        retry_result = retry_processor.execute(retry_inputs)

        assert retry_result.success is True

        # Should start from beginning since no step info in payload
        assert retry_processor.step_call_count["validation"] == 1
        assert retry_processor.step_call_count["processing"] == 1
        assert retry_processor.step_call_count["extraction"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
