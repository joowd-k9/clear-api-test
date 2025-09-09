"""
Base exceptions for the processing engine module that may happen during run time.
"""


class ProcessingEngineError(Exception):
    """
    Base exception for processing engine errors.
    """

    def __init__(self, message: str = ""):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
