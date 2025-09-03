"""External API integrations for processing engine."""

from .base_client import (
    BaseExternalAPIClient,
    APIClientError,
    AuthenticationError,
    RateLimitError,
)
from .clear_client import ClearAPIClient

__all__ = [
    "BaseExternalAPIClient",
    "APIClientError",
    "AuthenticationError",
    "RateLimitError",
    "ClearAPIClient",
]
