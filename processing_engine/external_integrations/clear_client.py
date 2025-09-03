"""Thomson Reuters CLEAR API client implementation."""

import os
import time
from typing import Dict, Any, Optional
import requests
from diskcache import Cache

from .base_client import BaseExternalAPIClient, AuthenticationError, APIClientError


class ClearAPIClient(BaseExternalAPIClient):
    """Thomson Reuters CLEAR API client with authentication and caching."""

    def __init__(
        self, client_key: Optional[str] = None, client_secret: Optional[str] = None
    ):
        """Initialize CLEAR API client with credentials."""
        credentials = {
            "client_key": client_key or os.getenv("CLEAR_CLIENT_KEY"),
            "client_secret": client_secret or os.getenv("CLEAR_CLIENT_SECRET"),
        }

        if not credentials["client_key"] or not credentials["client_secret"]:
            raise AuthenticationError(
                "CLEAR_CLIENT_KEY and CLEAR_CLIENT_SECRET must be provided "
                "either as parameters or environment variables"
            )

        super().__init__(credentials)

        # API endpoints configuration
        self.api_base = (
            os.getenv("CLEAR_API_URL") or "https://api.thomsonreuters.com"
        ).rstrip("/")
        self.s2s_base = (
            os.getenv("CLEAR_S2S_URL") or "https://s2ssandbox.thomsonreuters.com"
        ).rstrip("/")

        self.endpoints = {
            "auth": f"{self.api_base}/tr-oauth/v1/token",
            "business-search": f"{self.s2s_base}/v2/business/searchResults",
            "person-search": f"{self.s2s_base}/v3/person/searchResults",
            "business-report": f"{self.s2s_base}/v2/businessReport/reportResults",
            "person-report": f"{self.s2s_base}/v3/personReport/reportResults",
        }

        # Token caching setup
        cache_dir = os.path.join(os.path.expanduser("~"), ".clear_api_cache")
        self._cache = Cache(cache_dir)
        self._cache_key = "clear_api_token"
        self._token_cache = None
        self._token_expires_at = 0

    def authenticate(self) -> str:
        """Authenticate with CLEAR API and return access token."""
        # Check cached token first
        current_time = time.time()

        if self._token_cache and current_time < self._token_expires_at - 60:
            return self._token_cache

        # Check disk cache
        cached_data = self._cache.get(self._cache_key)
        if cached_data:
            token, expires_at = cached_data
            if current_time < expires_at - 60:
                self._token_cache = token
                self._token_expires_at = expires_at
                return token

        # Get new token
        return self._refresh_token()

    def _refresh_token(self) -> str:
        """Request a new access token from CLEAR API."""
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "grant_type": "client_credentials",
            "client_id": self.credentials["client_key"],
            "client_secret": self.credentials["client_secret"],
        }

        try:
            response = requests.post(
                self.endpoints["auth"], headers=headers, data=data, timeout=self.timeout
            )
            response.raise_for_status()

            token_data = response.json()
            access_token = token_data["access_token"]
            expires_in = token_data["expires_in"]

            # Calculate absolute expiry time
            expires_at = time.time() + expires_in

            # Cache the token
            self._token_cache = access_token
            self._token_expires_at = expires_at
            self._cache.set(self._cache_key, (access_token, expires_at))

            self.logger.info("Successfully refreshed CLEAR API token")
            return access_token

        except requests.exceptions.RequestException as e:
            raise AuthenticationError(
                f"Failed to authenticate with CLEAR API: {str(e)}"
            ) from e
        except KeyError as e:
            raise AuthenticationError(f"Invalid token response format: {str(e)}") from e

    def business_search(self, xml_request: str) -> Dict[str, Any]:
        """Perform a business search request."""
        try:
            response = self.post(self.endpoints["business-search"], xml_request)
            return {"xml_response": response.text, "status_code": response.status_code}
        except Exception as e:
            self.logger.error(f"Business search failed: {str(e)}")
            raise APIClientError(f"Business search failed: {str(e)}") from e

    def person_search(self, xml_request: str) -> Dict[str, Any]:
        """Perform a person search request."""
        try:
            response = self.post(self.endpoints["person-search"], xml_request)
            return {"xml_response": response.text, "status_code": response.status_code}
        except Exception as e:
            self.logger.error(f"Person search failed: {str(e)}")
            raise APIClientError(f"Person search failed: {str(e)}") from e

    def business_report(self, xml_request: str) -> Dict[str, Any]:
        """Generate a business report."""
        try:
            response = self.post(self.endpoints["business-report"], xml_request)
            return {"xml_response": response.text, "status_code": response.status_code}
        except Exception as e:
            self.logger.error(f"Business report failed: {str(e)}")
            raise APIClientError(f"Business report failed: {str(e)}") from e

    def person_report(self, xml_request: str) -> Dict[str, Any]:
        """Generate a person report."""
        try:
            response = self.post(self.endpoints["person-report"], xml_request)
            return {"xml_response": response.text, "status_code": response.status_code}
        except Exception as e:
            self.logger.error(f"Person report failed: {str(e)}")
            raise APIClientError(f"Person report failed: {str(e)}") from e

    def clear_token_cache(self) -> None:
        """Clear the cached authentication token."""
        self._token_cache = None
        self._token_expires_at = 0
        self._cache.delete(self._cache_key)
        self.logger.info("Cleared CLEAR API token cache")

    def get_token_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the current cached token."""
        if not self._token_cache:
            cached_data = self._cache.get(self._cache_key)
            if cached_data:
                token, expires_at = cached_data
                self._token_cache = token
                self._token_expires_at = expires_at

        if not self._token_cache:
            return None

        current_time = time.time()
        expires_in = int(self._token_expires_at - current_time)

        return {
            "token_preview": (
                self._token_cache[:10] + "..."
                if len(self._token_cache) > 10
                else self._token_cache
            ),
            "expires_in": expires_in,
            "is_valid": current_time < self._token_expires_at - 60,
        }
