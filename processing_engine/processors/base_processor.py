"""
Base processor module providing abstract base class for document processing.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, final
import logging
from datetime import datetime
import uuid

from processing_engine.models.execution import (
    ExecutionContext,
    ProcessorInput,
    ProcessingResult,
    CostEntry,
)
from processing_engine.exceptions.execution import PrevalidationError
from processing_engine.processors.runners import (
    Runner,
    DefaultRunner,
)


class SubclassImplementationError(AttributeError, TypeError):
    """
    Exception raised when a subclass is not implemented correctly.
    """


class BaseProcessor(ABC):
    """
    Abstract base class for document processing implementations.

    Provides a common interface for all document processors with standardized
    error handling, validation, and configurable execution strategies.

    Attributes:
        PROCESSOR_NAME: The name of the processor, must be non-empty

        runner: The technique to use for the processor execution (sequential, threaded, process)

        execution_id: The id of the current run
        account_id: The id of the account the processor is running for
        underwriting_id: The id of the underwriting the processor is running for
        context: The context of the current run
        logger: The logger for the processor
    """

    PROCESSOR_NAME: str
    PROCESSOR_PREREQUISITES: tuple[str, ...] = ()
    runner: Runner

    execution_id: str
    account_id: str
    underwriting_id: str
    _cost_tracker: list[CostEntry]

    def __init__(
        self,
        account_id: str,
        underwriting_id: str,
        runner: Runner = DefaultRunner(),
    ):
        """
        Initialize the processor with underwriting ID
        and processor name which is defined in the subclass.
        """
        if not getattr(self, "PROCESSOR_NAME", "").strip():
            raise SubclassImplementationError("PROCESSOR_NAME must be non-empty")

        self.account_id = account_id
        self.underwriting_id = underwriting_id
        self.runner = runner
        self.context = ExecutionContext()
        self.logger = logging.getLogger(self.PROCESSOR_NAME)
        self._cost_tracker: list[CostEntry] = []

    @property
    def processor_name(self) -> str:
        """
        Get the processor name.
        """
        return f"p_{self.PROCESSOR_NAME}"


    @final
    def execute(
        self,
        data: list[ProcessorInput],
        context: ExecutionContext | None = None,
    ) -> ProcessingResult:
        """
        Execute the main processing logic for the given underwriting id and data.

        Args:
            data: The input data to process according to the processor requirements

        Returns:
            ProcessingResult: The result of the processing operation

        Raises:
            ProcessorExecutionError: If the processor execution fails
        """
        exceptions: tuple[Exception, ...] = (Exception,)
        self.execution_id: str = str(uuid.uuid4())
        if context is not None:
            for key, value in context.__dict__.items():
                setattr(self.context, key, value)

        preprocessing = [
            ("prevalidation", self._prevalidate_inputs),
            ("transformation", self._transform_input),
            ("validation", self._validate_input),
        ]

        processing = [
            ("extraction", self._extract_factors),
        ]

        postprocessing = [
            ("aggregation", self._aggregate_results),
            ("postvalidation", self._validate_result),
        ]

        init = datetime.now()

        def run(data: Any, pipeline: list[tuple[str, Callable]]) -> dict[str, Any]:
            """
            Run a pipeline for the given data.

            Args:
                data: The input data
                pipeline: List of (step_name, function) tuples to execute

            Returns:
                A dict containing success, step, exception, message or error details
            """
            current = data

            for step, function in pipeline:
                try:
                    current = function(current)
                except exceptions as error:
                    message = self._handle_error(error, step)
                    return {
                        "success": False,
                        "step": step,
                        "exception": error.__class__.__name__,
                        "message": message,
                    }
            return {
                "success": True,
                "output": current,
            }

        pre_result = run(data, preprocessing)
        if not pre_result["success"]:
            return ProcessingResult(
                execution_id=self.execution_id,
                account_id=self.account_id,
                underwriting_id=self.underwriting_id,
                success=False,
                output=None,
                error=pre_result,
                context=self.context,
                timestamp=datetime.now(),
                duration=(datetime.now() - init).total_seconds(),
            )

        results = self.runner.run(lambda data: run(data, processing), pre_result["output"])
        if not all(r["success"] for r in results):
            return ProcessingResult(
                execution_id=self.execution_id,
                account_id=self.account_id,
                underwriting_id=self.underwriting_id,
                success=False,
                output=None,
                error=next(r for r in results if not r["success"]),
                context=self.context,
                timestamp=init,
                duration=int((datetime.now() - init).total_seconds() * 1000),
            )

        post_result = run(results, postprocessing)
        if not post_result["success"]:
            return ProcessingResult(
                execution_id=self.execution_id,
                account_id=self.account_id,
                underwriting_id=self.underwriting_id,
                success=False,
                output=None,
                error=post_result,
                context=self.context,
                timestamp=init,
                duration=int((datetime.now() - init).total_seconds() * 1000),
            )

        return ProcessingResult(
            execution_id=self.execution_id,
            account_id=self.account_id,
            underwriting_id=self.underwriting_id,
            success=True,
            output=post_result["output"],
            context=self.context,
            timestamp=init,
            duration=int((datetime.now() - init).total_seconds() * 1000),
        )

    def _validate_input(self, data: Any) -> Any:
        """
        Validate the input data.

        This method is used to validate the input data before processing.

        Args:
            data: The input data to validate

        Returns:
            The validated data

        Raises:
            ValidationError: If the input data is not valid
        """
        return data

    def _validate_result(self, data: Any) -> Any:
        """
        Validate the result data.

        This method is used to validate the result data after processing.

        Args:
            data: The result data to validate

        Returns:
            The validated result data

        Raises:
            ValidationError: If the result data is not valid
        """
        return data

    def _transform_input(self, data: Any) -> Any:
        """
        Transform the input data.

        This method is used to transform the input data for processing.

        Args:
            data: The input data to transform

        Returns:
            The transformed data
        """
        return data

    @abstractmethod
    def _extract_factors(self, data: Any) -> dict[str, str | list | dict]:
        """
        Extract the factors from the processed data.

        Args:
            data: The processed data to extract from

        Returns:
            The extracted data in the example format:
            ```json
            {
                "risk_factor_key_1": "risk_factor_value_1",
                "risk_factor_key_2": [
                    "risk_factor_value_2_1",
                    "risk_factor_value_2_2",
                ],
                "risk_factor_key_3": {
                    "risk_factor_value_3_1": "risk_factor_value_3_1_1",
                    "risk_factor_value_3_2": [
                        "risk_factor_value_3_2_1",
                        "risk_factor_value_3_2_2",
                    ],
                },
                ...
            }
            ```
        """

    def _prevalidate_inputs(
        self, data: list[ProcessorInput]
    ) -> list[Any]:
        """
        Prevalidate the input data to ensure it is for the same account and underwriting.

        Args:
            data: The input data to prevalidate

        Returns:
            List of prevalidated data values

        Raises:
            PrevalidationError: If the input data is not for the same account or underwriting
        """
        if any(input.account_id != self.account_id for input in data):
            raise PrevalidationError(
                message="Input data is not for the same account",
                execution_id=getattr(self, "execution_id", None),
                account_id=self.account_id,
                underwriting_id=self.underwriting_id,
                processor_name=self.PROCESSOR_NAME,
            )

        if any(
            input.underwriting_id != self.underwriting_id
            for input in data
        ):
            raise PrevalidationError(
                message="Input data is not for the same underwriting",
                execution_id=getattr(self, "execution_id", None),
                account_id=self.account_id,
                underwriting_id=self.underwriting_id,
                processor_name=self.PROCESSOR_NAME,
            )

        return [item.data for item in data]


    def _calculate_cost(self, result: ProcessingResult) -> dict[str, float|dict]:
        """
        Calculate the cost of the run.

        Args:
            result: The result to calculate the cost of the run

        Returns:
            The cost of the run with detailed breakdown
        """
        return self.get_cost_breakdown()

    def _aggregate_results(self, results: list[dict[str, str]]) -> dict[str, str]:
        """
        Aggregate the results from the pipeline. Only executed when all steps are successful.

        Args:
            results: The results from the pipeline

        Returns:
            The aggregated results
        """
        return {k: v for r in results for k, v in r["output"].items()}



    def _handle_error(
        self, error: Exception, action: str
    ) -> str:
        """
        Handle an error.
        """
        self.logger.error(
            "Processor failed",
            extra={
                "execution_id": self.execution_id,
                "account_id": self.account_id,
                "underwriting_id": self.underwriting_id,
                "processor": self.PROCESSOR_NAME,
                "step": action,
                "error": str(error),
                "exception": error.__class__.__name__,
            },
            exc_info=True,
        )

        return (
            f"Error in {self.PROCESSOR_NAME} processor "
            f"(execution_id: {self.execution_id}, account_id: {self.account_id}, "
            f"underwriting_id: {self.underwriting_id}, step: {action}): \n {error}"
        )
