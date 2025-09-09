"""Base API client with rate limiting and authentication support."""

from abc import ABC
import requests
from .auth_strategy import AuthStrategy
from .rate_limiter import RateLimiter


class BaseApiClient(ABC):
    """
    Base client for external APIs with pluggable authentication
    and optional rate limiting.
    """

    BASE_URL: str

    def __init__(
        self,
        auth_strategy: AuthStrategy | None = None,
        timeout: int = 30,
        rate_limiter: RateLimiter | None = None,
    ):
        self.base_url = self.BASE_URL.rstrip("/")
        self.auth_strategy = auth_strategy
        self.session = requests.Session()
        self.timeout = timeout
        self.rate_limiter = rate_limiter

        if self.auth_strategy:
            self.auth_strategy.apply(self.session)

    def _full_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs):
        if self.rate_limiter:
            self.rate_limiter.acquire()

        url = self._full_url(path)
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        return self._handle_response(response)

    def get(self, path: str, **kwargs):
        """Make a GET request."""
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        """Make a POST request."""
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        """Make a PUT request."""
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        """Make a DELETE request."""
        return self._request("DELETE", path, **kwargs)

    def _handle_response(self, response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(f"API request failed: {e}") from e
        try:
            return response.json()
        except ValueError:
            return response.text
