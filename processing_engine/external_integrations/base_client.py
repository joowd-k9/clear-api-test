"""Base client module for external integrations."""

from abc import ABC, abstractmethod


class BaseExternalAPIClient(ABC):
    """Base client class for external integrations."""

    def __init__(self, credentials: dict):
        """Initialize the client."""
        self.credentials = credentials

    @abstractmethod
    def authenticate(self, credentials: dict) -> dict:
        """Authenticate with the external integration."""

    def headers(self) -> dict:
        """Get the headers for the external integration."""

        return {
            "Authorization": f"Bearer {self.authenticate(self.credentials)}",
        }
