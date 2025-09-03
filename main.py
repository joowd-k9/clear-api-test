"""FastAPI application for Clear API"""

# Standard library imports
import hashlib
import os
import xml.etree.ElementTree as ET
from datetime import datetime

# Third-party imports
from dotenv import load_dotenv
import requests
from fastapi import FastAPI
from diskcache import Cache

# First-party imports
from api.config import ENDPOINTS
from api.token import Token
from api.builder import build_business_search_xml, build_business_report_xml
from api.parser import parse_business_report_xml
from models import BusinessSearchRequest
from processing_engine.processors.external_reports.clear_processor import ClearProcessor
from processing_engine.models.execution import ProcessingResult

load_dotenv()

app = FastAPI(debug=True)

# cache init
CACHE_DIR = os.getenv(
    "SEARCH_CACHE_DIR", os.path.join(os.path.expanduser("~"), ".clear_api_search_cache")
)
SEARCH_CACHE_TTL = int(os.getenv("SEARCH_CACHE_TTL", str(8 * 3600)))
_search_cache = Cache(CACHE_DIR)


def get_headers(content_type: str = "application/xml") -> dict:
    """Get standardized headers for Clear API requests."""

    token = Token().get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    if content_type:
        headers["Content-Type"] = content_type
        headers["Cache-Control"] = "no-cache"

    return headers


@app.get("/")
def read_root():
    """Return the root endpoint with API information."""
    return {"message": "Clear API Adapter", "version": "1.0.0"}


@app.get("/test")
def test_clear_processor():
    """Test endpoint to execute CLEAR processor with sample data."""
    exceptions = (Exception,)

    try:
        # Create sample underwriting ID
        underwriting_id = "test_underwriting_001"

        # Create mock ProcessingResult with application form data
        sample_extraction_output = {
            "stipulations": {
                "business_name": "Acme Corporation",
                "business_ein": "12-3456789",
                "business_phone": "555-123-4567",
                "business_address": "123 Main Street",
                "business_city": "New York",
                "business_state": "NY",
                "business_zip": "10001",
                "owner_first_name": "John",
                "owner_last_name": "Doe",
                "owner_middle_initial": "A",
            },
            "flags": {},
            "risk_factors": {},
        }

        # Create ProcessingResult mock data
        application_form_result = ProcessingResult(
            underwriting_id=underwriting_id,
            run_id="mock_run_001",
            processor_name="p_application_form",
            extraction_output=sample_extraction_output,
            success=True,
            timestamp=datetime.now(),
            duration=100,
            error=None,
        )

        # Initialize CLEAR processor
        clear_processor = ClearProcessor(underwriting_id)

        # Execute the processor
        return clear_processor.execute(application_form_result)

        return {
            "status": "success",
            "message": "CLEAR processor executed successfully",
            "underwriting_id": underwriting_id,
            "processor_result": {
                "run_id": result.run_id,
                "processor_name": result.processor_name,
                "success": result.success,
                "timestamp": result.timestamp.isoformat(),
                "duration": result.duration,
                "extraction_output": result.extraction_output,
                "error": str(result.error) if result.error else None,
            },
            "note": "Authentication errors are expected without valid CLEAR API credentials",
        }

    except exceptions as e:
        return {
            "status": "error",
            "message": f"Failed to execute CLEAR processor: {str(e)}",
            "error_type": type(e).__name__,
        }


@app.post("/search")
async def search(business_data: BusinessSearchRequest):
    """Search for a business using JSON body with Pydantic validation."""
    business_data_dict = business_data.model_dump()

    search_response = requests.post(
        ENDPOINTS["business-search"],
        headers=get_headers(),
        data=build_business_search_xml(business_data_dict),
        timeout=30,
    )

    if search_response.status_code != 200:
        print(
            "Search request failed with status "
            + str(search_response.status_code)
            + ": "
            + search_response.text
        )
        return {
            "error": f"Search request failed with status {search_response.status_code}",
            "response": search_response.text,
        }

    search_results_response = requests.get(
        ET.fromstring(search_response.text).find(".//Uri").text,
        headers=get_headers(content_type=None),
        timeout=30,
    )

    if search_results_response.status_code != 200:
        print(
            "Search results request failed with status "
            + str(search_results_response.status_code)
            + ": "
            + search_results_response.text
        )

        return {
            "error": "Search results request failed with status "
            + str(search_results_response.status_code)
            + ": "
            + search_results_response.text,
            "response": search_results_response.text,
        }

    # --- search results caching logic ---
    results_text = search_results_response.text
    results_key = (
        "search_res:" + hashlib.sha256(results_text.encode("utf-8")).hexdigest()
    )

    cached = _search_cache.get(results_key)
    if cached is not None:
        # return cached parsed result immediately
        return cached
    # --- search results caching logic end ---

    business_report_data = {
        "reference": "S2S Business Report",
        "group_id": ET.fromstring(search_results_response.text).find(".//GroupId").text,
    }

    report_response = requests.post(
        ENDPOINTS["business-report"],
        headers=get_headers(),
        data=build_business_report_xml(business_report_data),
        timeout=30,
    )

    if report_response.status_code != 200:
        print(
            "Report request failed with status "
            + str(report_response.status_code)
            + ": "
            + report_response.text
        )
        return {
            "error": f"Report request failed with status {report_response.status_code}",
            "response": report_response.text,
        }

    if ET.fromstring(report_response.text).find(".//Uri") is None:
        print(f"Report request failed. Response: {report_response}")

        return {
            "error": "Report request failed - no URI found in response",
            "response": report_response,
        }

    final_response = requests.get(
        ET.fromstring(report_response.text).find(".//Uri").text,
        headers=get_headers(content_type=None),
        timeout=30,
    ).text

    parsed = parse_business_report_xml(final_response)

    # store parsed result keyed by the search results content
    _search_cache.set(results_key, parsed, expire=SEARCH_CACHE_TTL)

    return parsed
