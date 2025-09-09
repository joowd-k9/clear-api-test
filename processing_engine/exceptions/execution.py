"""
Base exceptions for the processing engine module that may happen during run time.
"""

from processing_engine.exceptions.base import ProcessingEngineError


class ProcessorExecutionError(ProcessingEngineError):
    """
    Raised when the processor execution fails.
    """

    def __init__(
        self,
        run_id: str | None = None,
        account_id: str | None = None,
        underwriting_id: str | None = None,
        processor_name: str | None = None,
        message: str | None = None,
    ):
        self.run_id = run_id
        self.account_id = account_id
        self.underwriting_id = underwriting_id
        self.processor_name = processor_name
        self.message = (
            f"Processor execution failed:\n"
            f"run_id: `{run_id}`\n "
            f"account_id: `{account_id}`\n "
            f"underwriting_id: `{underwriting_id}`\n "
            f"processor_name: `{processor_name}`" + (f"\n{message}" if message else "")
        )
        super().__init__(self.message)


class ProcessorInputMismatchError(ProcessorExecutionError):
    """
    Raised when the processor received input with mismatches with
    the run_id, account_id, processor_name, and underwriting_id.
    """


class ValidationError(ProcessorExecutionError):
    """
    Raised when the input data is not valid.
    """


class PrevalidationError(ProcessorExecutionError):
    """
    Raised when the input data is not for the same account and underwriting.
    """
