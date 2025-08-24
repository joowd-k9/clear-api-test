"""Configuration module for Clear API endpoints and settings."""

import os

from dotenv import load_dotenv

load_dotenv()

API = os.getenv("CLEAR_API_URL") or "https://api.thomsonreuters.com/"
S2S = os.getenv("CLEAR_S2S_URL") or "https://s2ssandbox.thomsonreuters.com/"

ENDPOINTS = {
    "auth": f"{API}/tr-oauth/v1/token",
    "business-search": f"{S2S}/v2/business/searchResults",
    "person-search": f"{S2S}/v3/person/searchResults",
    "business-report": f"{S2S}/v2/businessReport/reportResults",
    "person-report": f"{S2S}/v3/personReport/reportResults",
}
