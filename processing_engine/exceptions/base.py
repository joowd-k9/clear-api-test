"""
Base exceptions for the processing engine module that may happen during run time.
"""


class ProcessingEngineError(Exception):
    """
    Base exception for processing engine errors.
    """


class DependencyNotFoundError(ProcessingEngineError):
    """
    Raised when a required dependency is not found.
    """

    def __init__(
        self,
        run_id: str,
        processor_name: str,
        underwriting_id: str,
        dependency_name: str,
    ):
        self.run_id = run_id
        self.underwriting_id = underwriting_id
        self.processor_name = processor_name
        self.dependency_name = dependency_name
        message = (
            f"Dependency {dependency_name} not found for run_id: {run_id}, "
            f"processor_name: {processor_name}, and underwriting_id: {underwriting_id}"
        )
        super().__init__(message)


class DependencyUnderwritingMismatchError(ProcessingEngineError):
    """
    Raised when the dependency received mismatches with the underwriting_id.
    """

    def __init__(
        self,
        run_id: str,
        processor_name: str,
        underwriting_id: str,
        dependency_name: str,
    ):
        self.run_id = run_id
        self.underwriting_id = underwriting_id
        self.processor_name = processor_name
        self.dependency_name = dependency_name
        message = (
            f"Dependency {dependency_name} received mismatches with the run_id: {run_id}, "
            f"processor_name: {processor_name}, and underwriting_id: {underwriting_id}"
        )
        super().__init__(message)
