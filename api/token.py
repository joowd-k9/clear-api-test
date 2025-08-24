"""Token management module for Clear API authentication."""

import os
import time
from typing import Dict, Optional, Tuple
import requests
from diskcache import Cache
from .config import ENDPOINTS


class Token:
    """
    Singleton class for managing Clear API authentication tokens.

    This class provides persistent token caching using diskcache and handles
    token expiry automatically. It uses the authentication endpoint from config.py
    and reads client credentials from environment variables.
    """

    _instance: Optional['Token'] = None
    _cache: Optional[Cache] = None
    _cache_key = "clear_api_token"

    def __new__(cls) -> 'Token':
        """Ensure only one instance of Token class exists."""
        if cls._instance is None:
            cls._instance = super(Token, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the Token singleton if not already initialized."""
        if getattr(self, '_initialized', False):
            return

        # Initialize diskcache for persistent storage
        cache_dir = os.path.join(os.path.expanduser("~"), ".clear_api_cache")
        self._cache = Cache(cache_dir)

        # Get authentication endpoint from config
        self.auth_url = ENDPOINTS["auth"]

        # Get client credentials from environment
        self.client_key = os.getenv("CLEAR_CLIENT_KEY")
        self.client_secret = os.getenv("CLEAR_CLIENT_SECRET")

        if not self.client_key or not self.client_secret:
            raise ValueError(
                "CLEAR_CLIENT_KEY and CLEAR_CLIENT_SECRET environment variables " \
                "must be set"
            )

        self._initialized = True

    def get_token(self) -> str:
        """
        Get a valid access token.

        Returns:
            str: access_token

        Raises:
            requests.RequestException: If token request fails
            ValueError: If client credentials are missing
        """
        # Check if we have a cached token that's still valid
        cached_data = self._cache.get(self._cache_key)

        if cached_data:
            token, expires_at = cached_data
            current_time = time.time()

            # If token is still valid (with 60 second buffer), return it
            if current_time < expires_at - 60:
                return token

        # Token expired or doesn't exist, get a new one
        return self._refresh_token()

    def _refresh_token(self) -> str:
        """
        Request a new access token from the Clear API.

        Returns:
            str: access_token

        Raises:
            requests.RequestException: If token request fails
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_key,
            "client_secret": self.client_secret
        }

        response = requests.post(self.auth_url, headers=headers, data=data, timeout=30)
        response.raise_for_status()

        token_data = response.json()
        access_token = token_data["access_token"]
        expires_in = token_data["expires_in"]

        # Calculate absolute expiry time
        expires_at = time.time() + expires_in

        # Cache the token with its expiry time
        self._cache.set(self._cache_key, (access_token, expires_at))

        return access_token

    def clear_cache(self) -> None:
        """Clear the cached token."""
        self._cache.delete(self._cache_key)

    def get_cached_token_info(self) -> Optional[Dict]:
        """
        Get information about the currently cached token.

        Returns:
            Optional[Dict]: Token info or None if no cached token
        """
        cached_data = self._cache.get(self._cache_key)
        if not cached_data:
            return None

        token, expires_at = cached_data
        current_time = time.time()
        expires_in = int(expires_at - current_time)

        return {
            "token": token[:10] + "..." if len(token) > 10 else token,
            "expires_in": expires_in,
            "is_valid": current_time < expires_at - 60
        }
