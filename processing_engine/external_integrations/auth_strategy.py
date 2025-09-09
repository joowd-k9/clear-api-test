"""Authentication strategies for external API clients."""

from abc import ABC, abstractmethod
from requests import Session


class AuthStrategy(ABC):
    """Base class for authentication strategies."""

    @abstractmethod
    def apply(self, session: Session) -> None:
        """Apply authentication to a requests session."""

    def __repr__(self) -> str:
        """
        Return a string representation of the authentication strategy.
        Hide the sensitive information like the API key or token.
        """


class ApiKeyAuth(AuthStrategy):
    """API key authentication strategy."""

    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self.api_key = api_key
        self.header_name = header_name

    def __repr__(self) -> str:
        return f"<ApiKeyAuth header={self.header_name}>"

    def apply(self, session: Session) -> None:
        """Add API key header to session."""
        session.headers[self.header_name] = self.api_key


class BasicAuth(AuthStrategy):
    """Basic authentication strategy."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f"<BasicAuth username={self.username}>"

    def apply(self, session: Session) -> None:
        """Add basic auth to session."""
        session.auth = (self.username, self.password)


class BearerTokenAuth(AuthStrategy):
    """Bearer token authentication strategy."""

    def __init__(self, token: str):
        self.token = token

    def __repr__(self) -> str:
        return f"<BearerTokenAuth token={self.token}>"

    def apply(self, session: Session) -> None:
        """Add Bearer token to session."""
        session.headers["Authorization"] = f"Bearer {self.token}"
