"""FastAPI application for Clear API"""

import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, Response
from api.config import ENDPOINTS
from api.token import Token
from api.builder import build_business_search_xml, build_business_report_xml

load_dotenv()

app = FastAPI(debug=True)


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


@app.get("/search")
def search_business():
    """Search for a business."""
    business_data = {
        "reference": "S2S Business Search",
        "company_entity_id": "",
        "business_name": "Thomson Reuters",
        "corporation_info": {
            "corporation_id": "C1586596",
            "filing_number": "",
            "filing_date": "",
            "fein": "133320829",
            "duns_number": "147833446",
        },
        "npi_number": "",
        "name_info": {
            "last_name": "Bello",
            "first_name": "Stephane",
            "middle_initial": "",
            "secondary_last_name": "",
        },
        "address_info": {
            "street": "3 Times Square",
            "city": "New York",
            "state": "NY",
            "county": "New York",
            "zip_code": "10036",
            "province": "",
            "country": "",
        },
        "phone_number": "646-223-4000",
    }

    search_response = requests.post(
        ENDPOINTS["business-search"],
        headers=get_headers(),
        data=build_business_search_xml(business_data),
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

    return Response(final_response, media_type="application/xml")
