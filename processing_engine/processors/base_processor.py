"""
Base processor module providing abstract base class for document processing.
"""

from abc import ABC, abstractmethod
from typing import Any, final
import logging
from datetime import datetime
import uuid

from processing_engine.models.execution import (
    ExecutionContext,
    ProcessorInput,
    ProcessingResult,
)
from processing_engine.exceptions.execution import PrevalidationError
from processing_engine.processors.runners import (
    Runner,
    SequentialRunner,
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

        run_id: The id of the current run
        account_id: The id of the account the processor is running for
        underwriting_id: The id of the underwriting the processor is running for
        context: The context of the current run
        logger: The logger for the processor
    """

    PROCESSOR_NAME: str
    runner: Runner

    run_id: str
    account_id: str
    underwriting_id: str

    def __init__(
        self,
        account_id: str,
        underwriting_id: str,
        runner: Runner = SequentialRunner(),
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
        self.run_id: str = str(uuid.uuid4())
        if context is not None:
            # Update context with the provided context's attributes
            for key, value in context.__dict__.items():
                setattr(self.context, key, value)

        data = self._prevalidate_inputs(data)

        pipeline = [
            ("validation", self._validate),
            ("processing", self._process),
            ("extraction", self._extract),
        ]

        init = datetime.now()

        def run(input_id: str, input_data: Any) -> dict[str, Any]:
            """
            Run the pipeline for a single input.

            Args:
                input_id: The id of the input being processed
                input_data: The raw input data

            Returns:
                A dict containing success, step, exception, message, payload or error details
            """
            item = data[input_id]
            current = input_data
            start = 0

            if item.payload is not None and isinstance(item.payload, dict):
                current = item.payload.get("data", input_data)
                failed_step = item.payload.get("step")
                if failed_step:
                    for i, (step_name, _) in enumerate(pipeline):
                        if step_name == failed_step:
                            start = i
                            break

            for i, (step, function) in enumerate(pipeline):
                if i < start:
                    continue
                try:
                    current = function(current)
                except exceptions as error:
                    message = self._handle_error(error, step, input_id)
                    return {
                        "input_id": input_id,
                        "success": False,
                        "step": step,
                        "exception": error.__class__.__name__,
                        "message": message,
                        "payload": current,
                    }
            return {
                "input_id": input_id,
                "success": True,
                "output": current,
            }

        def payloads(results: list[dict[str, Any]]) -> list[ProcessorInput]:
            """
            Extract the payloads from the results, including step information for retry scenarios.
            """
            return [
                ProcessorInput(
                    input_id=result["input_id"],
                    account_id=self.account_id,
                    underwriting_id=self.underwriting_id,
                    data=data[result["input_id"]].data,
                    payload={
                        "step": result.get("step"),
                        "exception": result.get("exception"),
                        "message": result.get("message"),
                        "data": result.get("payload"),
                    } if not result["success"] else None,
                )
                for result in results
                if result["input_id"] in data
            ]

        results = self.runner.run(lambda i: run(i.input_id, i.data), data.values())
        success = all(r["success"] for r in results)

        return ProcessingResult(
            run_id=self.run_id,
            account_id=self.account_id,
            underwriting_id=self.underwriting_id,
            success=success,
            output=self._aggregate_results(results) if success else results,
            context=self.context,
            timestamp=init,
            duration=int((datetime.now() - init).total_seconds() * 1000),
            payloads=payloads(results) if not success else None,
        )

    @abstractmethod
    def _validate(self, data: Any) -> Any:
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

    @abstractmethod
    def _process(self, data: Any) -> Any:
        """
        Process the input data from the validated data.

        This is the step where the main processing logic is implemented transforming
        the validated raw data into a new processed form ready for extraction.

        Args:
            data: The validated data to process from

        Returns:
            The processed data
        """

    @abstractmethod
    def _extract(self, data: Any) -> dict[str, str | list | dict]:
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
    ) -> dict[str, ProcessorInput]:
        """
        Prevalidate the input data to ensure it is for the same account and underwriting.

        Args:
            data: The input data to prevalidate

        Returns:
            Dictionary of unique prevalidated data with input_id as key

        Raises:
            PrevalidationError: If the input data is not for the same account or underwriting
        """
        unique_data = {item.input_id: item for item in data}

        if any(input.account_id != self.account_id for input in unique_data.values()):
            raise PrevalidationError(
                message="Input data is not for the same account",
                run_id=getattr(self, "run_id", None),
                account_id=self.account_id,
                underwriting_id=self.underwriting_id,
                processor_name=self.PROCESSOR_NAME,
            )

        if any(
            input.underwriting_id != self.underwriting_id
            for input in unique_data.values()
        ):
            raise PrevalidationError(
                message="Input data is not for the same underwriting",
                run_id=getattr(self, "run_id", None),
                account_id=self.account_id,
                underwriting_id=self.underwriting_id,
                processor_name=self.PROCESSOR_NAME,
            )

        return unique_data

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
        self, error: Exception, action: str, input_id: str | None = None
    ) -> str:
        """
        Handle an error.
        """
        self.logger.error(
            "Processor failed",
            extra={
                "run_id": self.run_id,
                "account_id": self.account_id,
                "underwriting_id": self.underwriting_id,
                "input_id": input_id,
                "processor": self.PROCESSOR_NAME,
                "step": action,
                "error": str(error),
                "exception": error.__class__.__name__,
            },
            exc_info=True,
        )

        return (
            f"Error in {self.PROCESSOR_NAME} processor "
            f"(run_id: {self.run_id}, account_id: {self.account_id}, "
            f"underwriting_id: {self.underwriting_id}, step: {action}): \n {error}"
        )
