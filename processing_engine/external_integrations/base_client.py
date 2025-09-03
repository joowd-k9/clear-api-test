"""Base client module for external integrations."""

import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClientError(Exception):
    """Base exception for API client errors."""


class AuthenticationError(APIClientError):
    """Exception raised when authentication fails."""


class RateLimitError(APIClientError):
    """Exception raised when rate limit is exceeded."""


class BaseExternalAPIClient(ABC):
    """Base client class for external integrations with retry, rate limiting, and error handling."""

    def __init__(self, credentials: Dict[str, Any], timeout: int = 30):
        """Initialize the client with credentials and configuration."""
        self.credentials = credentials
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.1  # 100ms between requests

    @abstractmethod
    def authenticate(self) -> str:
        """Authenticate with the external service and return access token."""

    def _enforce_rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time

        if time_since_last_request < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last_request
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    def _get_headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        try:
            token = self.authenticate()
            return {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/xml",
                "Accept": "application/xml",
            }
        except Exception as e:
            raise AuthenticationError(f"Failed to authenticate: {str(e)}") from e

    def make_request(
        self,
        method: str,
        url: str,
        data: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Make an authenticated HTTP request with error handling."""
        self._enforce_rate_limit()

        request_headers = self._get_headers()
        if headers:
            request_headers.update(headers)

        try:
            self.logger.debug("Making %s request to %s", method, url)
            response = self.session.request(
                method=method,
                url=url,
                data=data,
                headers=request_headers,
                timeout=self.timeout,
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                self.logger.warning("Rate limited. Waiting %d seconds", retry_after)
                time.sleep(retry_after)
                return self.make_request(method, url, data, headers)

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            self.logger.error("Request failed: %s", str(e))
            raise APIClientError(f"Request failed: {str(e)}") from e

    def post(
        self, url: str, data: str, headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """Make a POST request."""
        return self.make_request("POST", url, data, headers)

    def get(
        self, url: str, headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """Make a GET request."""
        return self.make_request("GET", url, headers=headers)
