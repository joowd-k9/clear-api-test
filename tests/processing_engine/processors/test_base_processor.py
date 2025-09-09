"""
Comprehensive tests for the BaseProcessor class.
"""

import pytest
import sys
import os
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.base_processor import (
    BaseProcessor,
    SubclassImplementationError,
)
from processing_engine.models.execution import ProcessorInput, ExecutionContext
from processing_engine.exceptions.execution import PrevalidationError
from processing_engine.processors.runners import SequentialRunner
from tests.processing_engine.processors.test_processor import (
    ConcreteTestProcessor,
    FailingValidationProcessor,
    FailingProcessingProcessor,
    FailingExtractionProcessor,
)


class TestBaseProcessorInitialization:
    """Test BaseProcessor initialization and basic functionality."""

    def test_processor_initialization_success(self):
        """Test successful processor initialization."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        assert processor.account_id == "account_123"
        assert processor.underwriting_id == "underwriting_456"
        assert processor.PROCESSOR_NAME == "test_processor"
        assert processor.processor_name == "p_test_processor"
        assert isinstance(processor.runner, SequentialRunner)
        assert isinstance(processor.context, ExecutionContext)
        assert processor.logger.name == "test_processor"

    def test_processor_initialization_without_processor_name_fails(self):
        """Test that processor initialization fails without PROCESSOR_NAME."""

        class InvalidProcessor(BaseProcessor):
            # Missing PROCESSOR_NAME
            def _validate(self, data):
                return data

            def _process(self, data):
                return data

            def _extract(self, data):
                return {}

        with pytest.raises(
            SubclassImplementationError, match="PROCESSOR_NAME must be non-empty"
        ):
            InvalidProcessor("account_123", "underwriting_456")

    def test_processor_initialization_with_empty_processor_name_fails(self):
        """Test that processor initialization fails with empty PROCESSOR_NAME."""

        class InvalidProcessor(BaseProcessor):
            PROCESSOR_NAME = ""

            def _validate(self, data):
                return data

            def _process(self, data):
                return data

            def _extract(self, data):
                return {}

        with pytest.raises(
            SubclassImplementationError, match="PROCESSOR_NAME must be non-empty"
        ):
            InvalidProcessor("account_123", "underwriting_456")

    def test_processor_initialization_with_whitespace_processor_name_fails(self):
        """Test that processor initialization fails with whitespace-only PROCESSOR_NAME."""

        class InvalidProcessor(BaseProcessor):
            PROCESSOR_NAME = "   "

            def _validate(self, data):
                return data

            def _process(self, data):
                return data

            def _extract(self, data):
                return {}

        with pytest.raises(
            SubclassImplementationError, match="PROCESSOR_NAME must be non-empty"
        ):
            InvalidProcessor("account_123", "underwriting_456")


class TestPrevalidateInputs:
    """Test the _prevalidate_inputs method with dictionary return."""

    def test_prevalidate_inputs_success(self):
        """Test successful prevalidation with valid inputs."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data_1",
            ),
            ProcessorInput(
                input_id="input_2",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data_2",
            ),
        ]

        result = processor._prevalidate_inputs(inputs)

        # Should return a dictionary with input_id as key
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "input_1" in result
        assert "input_2" in result
        assert result["input_1"].input_id == "input_1"
        assert result["input_2"].input_id == "input_2"

    def test_prevalidate_inputs_duplicate_input_ids(self):
        """Test that duplicate input_ids are deduplicated."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data_1",
            ),
            ProcessorInput(
                input_id="input_1",  # Duplicate
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data_2",
            ),
        ]

        result = processor._prevalidate_inputs(inputs)

        # Should only have one entry with the last value
        assert len(result) == 1
        assert "input_1" in result
        assert result["input_1"].data == "test_data_2"  # Last value wins

    def test_prevalidate_inputs_wrong_account_id_fails(self):
        """Test that prevalidation fails with wrong account_id."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="wrong_account",  # Wrong account
                underwriting_id="underwriting_456",
                data="test_data_1",
            )
        ]

        with pytest.raises(PrevalidationError, match="Processor execution failed"):
            processor._prevalidate_inputs(inputs)

    def test_prevalidate_inputs_wrong_underwriting_id_fails(self):
        """Test that prevalidation fails with wrong underwriting_id."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="wrong_underwriting",  # Wrong underwriting
                data="test_data_1",
            )
        ]

        with pytest.raises(PrevalidationError, match="Processor execution failed"):
            processor._prevalidate_inputs(inputs)

    def test_prevalidate_inputs_empty_list(self):
        """Test prevalidation with empty input list."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        result = processor._prevalidate_inputs([])

        assert isinstance(result, dict)
        assert len(result) == 0


class TestSuccessfulExecution:
    """Test successful execution flow."""

    def test_successful_execution_single_input(self):
        """Test successful execution with a single input."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="hello",
            )
        ]

        result = processor.execute(inputs)

        assert result.success is True
        assert result.account_id == "account_123"
        assert result.underwriting_id == "underwriting_456"
        assert result.run_id is not None
        assert result.duration >= 0  # Duration can be 0 for very fast operations
        assert result.payloads is None  # No payloads on success

        # Check the output structure
        assert isinstance(result.output, dict)
        assert result.output["original_data"] == "hello"
        assert result.output["processed_data"] == "processed_hello"
        assert result.output["length"] == "15"  # len("processed_hello")
        assert result.output["factors"]["is_processed"] == "true"

    def test_successful_execution_multiple_inputs(self):
        """Test successful execution with multiple inputs."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="hello",
            ),
            ProcessorInput(
                input_id="input_2",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="world",
            ),
        ]

        result = processor.execute(inputs)

        assert result.success is True
        assert result.payloads is None

        # Check aggregated output
        assert isinstance(result.output, dict)
        # Should contain factors from both inputs
        assert "original_data" in result.output
        assert "processed_data" in result.output
        assert "length" in result.output
        assert "factors" in result.output

    def test_execution_with_context(self):
        """Test execution with custom context."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test",
            )
        ]

        custom_context = ExecutionContext(
            trigger_type="manual", trigger_initiator="user:123", retry_count=1
        )

        result = processor.execute(inputs, custom_context)

        assert result.success is True
        assert result.context.trigger_type == "manual"
        assert result.context.trigger_initiator == "user:123"
        assert result.context.retry_count == 1


class TestErrorHandling:
    """Test error handling and failure scenarios."""

    def test_validation_failure(self):
        """Test handling of validation failures."""
        processor = FailingValidationProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test",
            )
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert result.payloads is not None
        assert len(result.payloads) == 1

        # Check error details
        error_result = result.output[0]  # Should be a list of error results
        assert error_result["success"] is False
        assert error_result["step"] == "validation"
        assert error_result["exception"] == "ValueError"
        assert "Validation always fails" in error_result["message"]
        assert error_result["input_id"] == "input_1"

    def test_processing_failure(self):
        """Test handling of processing failures."""
        processor = FailingProcessingProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test",
            )
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert result.payloads is not None
        assert len(result.payloads) == 1

        # Check error details
        error_result = result.output[0]
        assert error_result["success"] is False
        assert error_result["step"] == "processing"
        assert error_result["exception"] == "RuntimeError"
        assert "Processing always fails" in error_result["message"]

    def test_extraction_failure(self):
        """Test handling of extraction failures."""
        processor = FailingExtractionProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test",
            )
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert result.payloads is not None
        assert len(result.payloads) == 1

        # Check error details
        error_result = result.output[0]
        assert error_result["success"] is False
        assert error_result["step"] == "extraction"
        assert error_result["exception"] == "KeyError"
        assert "Extraction always fails" in error_result["message"]

    def test_mixed_success_failure(self):
        """Test handling of mixed success and failure scenarios."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="hello",  # Valid input
            ),
            ProcessorInput(
                input_id="input_2",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="hi",  # Too short, will fail validation
            ),
        ]

        result = processor.execute(inputs)

        assert result.success is False  # Any failure makes the whole execution fail
        assert result.payloads is not None
        assert len(result.payloads) == 2  # Both inputs should be in payloads

        # Check that we have both success and failure results
        assert len(result.output) == 2
        success_results = [r for r in result.output if r["success"]]
        failure_results = [r for r in result.output if not r["success"]]

        assert len(success_results) == 1
        assert len(failure_results) == 1
        assert failure_results[0]["step"] == "validation"


class TestPayloadReconstruction:
    """Test payload reconstruction on failure."""

    def test_payload_reconstruction_on_validation_failure(self):
        """Test that payloads are correctly reconstructed on validation failure."""
        processor = FailingValidationProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data",
            )
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert result.payloads is not None
        assert len(result.payloads) == 1

        payload = result.payloads[0]
        assert isinstance(payload, ProcessorInput)
        assert payload.input_id == "input_1"
        assert payload.account_id == "account_123"
        assert payload.underwriting_id == "underwriting_456"
        assert payload.data == "test_data"  # Original data preserved
        assert payload.payload is not None  # Failed payload should be set

    def test_payload_reconstruction_on_processing_failure(self):
        """Test that payloads are correctly reconstructed on processing failure."""
        processor = FailingProcessingProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data",
            )
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert result.payloads is not None
        assert len(result.payloads) == 1

        payload = result.payloads[0]
        assert payload.input_id == "input_1"
        assert payload.data == "test_data"  # Original data preserved
        assert payload.payload is not None  # Failed payload should be set

    def test_payload_reconstruction_with_multiple_failures(self):
        """Test payload reconstruction with multiple failed inputs."""
        processor = FailingValidationProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data_1",
            ),
            ProcessorInput(
                input_id="input_2",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="test_data_2",
            ),
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert result.payloads is not None
        assert len(result.payloads) == 2

        # Check both payloads
        payload_dict = {p.input_id: p for p in result.payloads}
        assert "input_1" in payload_dict
        assert "input_2" in payload_dict
        assert payload_dict["input_1"].data == "test_data_1"
        assert payload_dict["input_2"].data == "test_data_2"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_input_list(self):
        """Test execution with empty input list."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        result = processor.execute([])

        assert result.success is True
        assert result.output == {}
        assert result.payloads is None

    def test_very_short_input(self):
        """Test with input that's too short for validation."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="ab",  # Too short
            )
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert "Data must be at least 3 characters long" in result.output[0]["message"]

    def test_non_string_input(self):
        """Test with non-string input that fails validation."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data=123,  # Not a string
            )
        ]

        result = processor.execute(inputs)

        assert result.success is False
        assert "Data must be a string" in result.output[0]["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
