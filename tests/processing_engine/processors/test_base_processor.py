"""
Comprehensive tests for the BaseProcessor class.
"""

import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.base_processor import (
    BaseProcessor,
    SubclassImplementationError,
)
from processing_engine.models.execution import ProcessorInput, ExecutionContext
from processing_engine.exceptions.execution import PrevalidationError
from processing_engine.processors.runners import DefaultRunner
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
        assert isinstance(processor.runner, DefaultRunner)
        assert isinstance(processor.context, ExecutionContext)
        assert processor.logger.name == "test_processor"

    def test_processor_initialization_without_processor_name_fails(self):
        """Test that processor initialization fails without PROCESSOR_NAME."""

        class InvalidProcessor(BaseProcessor):
            # Missing PROCESSOR_NAME
            def _validate_input(self, data):
                return data

            def _validate_result(self, data):
                return data

            def _aggregate_result(self, data):
                return {}

            def _transform_input(self, data):
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

            def _validate_input(self, data):
                return data

            def _validate_result(self, data):
                return data

            def _aggregate_result(self, data):
                return {}

            def _transform_input(self, data):
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

            def _validate_input(self, data):
                return data

            def _validate_result(self, data):
                return data

            def _aggregate_result(self, data):
                return {}

            def _transform_input(self, data):
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

        # Should return a list of data values
        assert isinstance(result, list)
        assert len(result) == 2
        assert "test_data_1" in result
        assert "test_data_2" in result

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

        # Should have both values (no deduplication for lists)
        assert len(result) == 2
        assert "test_data_1" in result
        assert "test_data_2" in result

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

        assert isinstance(result, list)
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
        assert result.execution_id is not None
        assert result.duration >= 0  # Duration can be 0 for very fast operations

        # Check the output structure
        assert isinstance(result.output, dict)
        output_dict = result.output  # Type hint for linter
        # With preprocessing pipeline, the _extract method receives the transformed data
        assert output_dict["original_data"] == "processed_hello"
        assert output_dict["processed_data"] == "processed_processed_hello"
        assert output_dict["length"] == "25"  # len("processed_processed_hello")
        assert output_dict["factors"]["is_processed"] == "true"

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

        # Check error details - with early termination, output is None and error is in error field
        assert result.output is None
        assert result.error is not None
        assert "Validation always fails" in result.error["message"]

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

        # Check error details - with early termination, output is None and error is in error field
        assert result.output is None
        assert result.error is not None
        assert "Processing always fails" in result.error["message"]

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

        # Check error details - with early termination, output is None and error is in error field
        assert result.output is None
        assert result.error is not None
        assert "Extraction always fails" in result.error["message"]

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
                data="hi",  # Too short, but gets transformed to "processed_hi" which passes validation
            ),
        ]

        result = processor.execute(inputs)

        # With preprocessing pipeline, both inputs should succeed because "hi" becomes "processed_hi"
        assert result.success is True
        assert isinstance(result.output, dict)
        # The output should be from the last successful input
        output_dict = result.output
        assert output_dict["original_data"] == "processed_hi"
        assert output_dict["processed_data"] == "processed_processed_hi"




class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_input_list(self):
        """Test execution with empty input list."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        result = processor.execute([])

        assert result.success is True
        assert result.output == {}

    def test_very_short_input(self):
        """Test with input that's too short for validation."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data="ab",  # Too short, but gets transformed to "processed_ab" which passes validation
            )
        ]

        result = processor.execute(inputs)

        # With preprocessing pipeline, this should succeed because "ab" becomes "processed_ab"
        assert result.success is True
        assert isinstance(result.output, dict)
        output_dict = result.output
        assert output_dict["original_data"] == "processed_ab"
        assert output_dict["processed_data"] == "processed_processed_ab"

    def test_non_string_input(self):
        """Test with non-string input that fails validation."""
        processor = ConcreteTestProcessor("account_123", "underwriting_456")

        inputs = [
            ProcessorInput(
                input_id="input_1",
                account_id="account_123",
                underwriting_id="underwriting_456",
                data=123,  # Not a string, but gets transformed to "processed_123" which passes validation
            )
        ]

        result = processor.execute(inputs)

        # With preprocessing pipeline, this should succeed because 123 becomes "processed_123"
        assert result.success is True
        assert isinstance(result.output, dict)
        output_dict = result.output
        assert output_dict["original_data"] == "processed_123"
        assert output_dict["processed_data"] == "processed_processed_123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
