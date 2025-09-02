"""Configuration module for external API endpoints and settings."""

import os


# Clear S2S API Credentials and Endpoints
CLEAR_CLIENT_KEY = os.getenv("CLEAR_CLIENT_KEY")
CLEAR_CLIENT_SECRET = os.getenv("CLEAR_CLIENT_SECRET")
CLEAR_API = os.getenv("CLEAR_API_URL") or "https://api.thomsonreuters.com/"
CLEAR_S2S = os.getenv("CLEAR_S2S_URL") or "https://s2ssandbox.thomsonreuters.com/"

# External API Endpoints
ENDPOINTS = {
    "clear_auth": f"{CLEAR_API}/tr-oauth/v1/token",
    "clear_business_search": f"{CLEAR_S2S}/v2/business/searchResults",
    "clear_person_search": f"{CLEAR_S2S}/v3/person/searchResults",
    "clear_business_report": f"{CLEAR_S2S}/v2/businessReport/reportResults",
    "clear_person_report": f"{CLEAR_S2S}/v3/personReport/reportResults",
}

# External API Credentials
CREDENTIALS = {
    "clear_client_key": CLEAR_CLIENT_KEY,
    "clear_client_secret": CLEAR_CLIENT_SECRET,
}

__all__ = ["ENDPOINTS", "CREDENTIALS"]
