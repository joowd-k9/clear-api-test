"""
Base processor module providing abstract base class for document processing.
"""

from abc import ABC, abstractmethod
from typing import Any, final
import logging
from datetime import datetime
import uuid
from processing_engine.exceptions.base import (
    DependencyNotFoundError,
    DependencyUnderwritingMismatchError,
)
from processing_engine.models.execution import (
    DocumentStipulation,
    ProcessorInput,
    ProcessingResult,
)


class SubclassImplementationError(AttributeError, TypeError):
    """
    Exception raised when a subclass is not implemented correctly.
    """


class BaseProcessor(ABC):
    """
    Abstract base class for document processing implementations.

    Provides a common interface for all document processors with standardized
    error handling and validation methods.
    """

    PROCESSOR_NAME: str | None = None  # p_business_registration

    REQUIRED_DEPENDENCIES: tuple[
        str, ...
    ] = ()  # (s_application_form, p_bank_statement,)

    OPTIONAL_DEPENDENCIES: tuple[
        str, ...
    ] = ()  # (p_driver_license, p_secretary_of_state, p_voided_check)

    run_id: str
    underwriting_id: str

    def __init__(self, underwriting_id: str):
        """
        Initialize the processor with underwriting ID
        and processor name which is defined in the subclass.
        """
        if self.PROCESSOR_NAME is None or self.PROCESSOR_NAME.strip() == "":
            raise SubclassImplementationError(
                "Processor name is expected to be defined.",
            )

        if not self.REQUIRED_DEPENDENCIES:
            raise SubclassImplementationError(
                "Processor dependencies are expected to be defined.",
            )

        self.underwriting_id = underwriting_id
        self.logger = logging.getLogger(self.processor_name)

    @property
    def all_dependencies(self) -> tuple[str, ...]:
        """
        Get all the dependencies of the processor.
        """
        return self.required_dependencies + self.optional_dependencies

    @property
    def required_dependencies(self) -> tuple[str, ...]:
        """
        Get the required dependencies of the processor.
        """
        return tuple(
            {dep for dep in self.REQUIRED_DEPENDENCIES if dep.startswith(("p_", "s_"))}
        )

    @property
    def optional_dependencies(self) -> tuple[str, ...]:
        """
        Get the optional dependencies of the processor.
        """
        return tuple(
            {dep for dep in self.OPTIONAL_DEPENDENCIES if dep.startswith(("p_", "s_"))}
        )

    @property
    def processor_name(self) -> str:
        """
        Get the name of the processor.
        """
        return f"p_{self.PROCESSOR_NAME}"

    @final
    def execute(self, data: ProcessorInput | list[ProcessorInput]) -> ProcessingResult:
        """
        Execute the main processing logic for the given underwriting id and data.

        Args:
            data: The input data to process according to the processor requirements

        Returns:
            ProcessingResult: The result of the processing operation

        Raises:
            DependencyNotFoundError: If any of the dependencies are not found
            DependencyUnderwritingMismatchError: If any of the dependencies are mismatched
        """
        self.run_id = str(uuid.uuid4())
        exceptions: tuple[Exception, ...] = (Exception,)
        pipeline = [
            ("precheck", self._dependency_check),
            ("validation", self._validate),
            ("processing", self._process),
            ("extraction", self._extract),
        ]
        init = datetime.now()
        result = data

        for step, function in pipeline:
            try:
                result = function(result)
            except exceptions as error:
                self._handle_error(error, step)
                return ProcessingResult(
                    run_id=self.run_id,
                    underwriting_id=self.underwriting_id,
                    processor_name=self.processor_name,
                    extraction_output={},
                    success=False,
                    error=error,
                    timestamp=init,
                    duration=int((datetime.now() - init).total_seconds() * 1000),
                )

        return ProcessingResult(
            run_id=self.run_id,
            underwriting_id=self.underwriting_id,
            processor_name=self.processor_name,
            extraction_output=result,
            success=True,
            error=None,
            timestamp=init,
            duration=int((datetime.now() - init).total_seconds() * 1000),
        )

    @abstractmethod
    def _validate(self, data: ProcessorInput | list[ProcessorInput]) -> Any:
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
    def _extract(self, data: Any) -> dict[str, dict]:
        """
        Extract necessary data like stipulations, flags, etc. from the processed data.

        Args:
            data: The processed data to extract from

        Returns:
            The extracted data in the format:
            ```
            {
                "payload": {}, #(the raw processed data if needed)
                "stipulations": {}, #(the stipulations data)
                "flags": {}, #(the flags data)
                ... #(any other relevant data)
            }
            ```
        """

    def _handle_error(self, error: Exception, action: str) -> str:
        """
        Handle an error.

        # TODO: Implement proper error handling
        """

        self.logger.error("Error %s: %s", action, error, exc_info=True)

        return f"Error {self.underwriting_id} - {self.processor_name}: {error}"

    def _dependency_check(
        self,
        data: ProcessorInput | list[ProcessorInput],
    ) -> ProcessorInput | list[ProcessorInput]:
        """
        Check whether all the dependencies of the processor are available and
        are for the same underwriting id.

        Raises:
            DependencyNotFoundError: If any of the dependencies are not found
            DependencyUnderwritingMismatchError: If any of the dependencies are mismatched
        """
        inputs = [data] if not isinstance(data, list) else data

        def identify(item: ProcessorInput) -> tuple[str | None, str | None]:
            match item:
                case DocumentStipulation():
                    return (item.stipulation_name, item.underwriting_id)
                case ProcessingResult():
                    return (item.processor_name, item.underwriting_id)
                case _:
                    return (None, None)

        identifiers = list(map(identify, inputs))

        for dependency in self.required_dependencies:
            if not any(dependency == name for name, _ in identifiers):
                raise DependencyNotFoundError(
                    self.run_id,
                    self.processor_name,
                    self.underwriting_id,
                    dependency,
                )

        for dependency in self.all_dependencies:
            if any(
                dependency == name and underwriting_id != self.underwriting_id
                for name, underwriting_id in identifiers
            ):
                raise DependencyUnderwritingMismatchError(
                    self.run_id,
                    self.processor_name,
                    self.underwriting_id,
                    dependency,
                )

        return data
