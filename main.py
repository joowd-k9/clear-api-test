"""FastAPI application for Clear API Token Manager."""

import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import requests
from fastapi import FastAPI
from api.config import ENDPOINTS
from api.token import Token
from api.builder import build_business_search_xml
from api.parser import parse_business_search_response

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    """Return the root endpoint with API information."""
    return {"message": "Clear API Adapter", "version": "1.0.0"}

@app.get("/search")
def search_business():
    """Search for a business."""
    token = Token().get_token()

    business_data = {
        "reference": "S2S Business Search",
        "company_entity_id": "",
        "business_name": "Thomson Reuters",
        "corporation_info": {
            "corporation_id": "C1586596",
            "filing_number": "",
            "filing_date": "",
            "fein": "133320829",
            "duns_number": "147833446"
        },
        "npi_number": "",
        "name_info": {
            "last_secondary_name_sound_similar_option": "false",
            "secondary_last_name_option": "OR",
            "first_name_sound_similar_option": "false",
            "first_name_variations_option": "false",
            "last_name": "Bello",
            "first_name": "Stephane",
            "middle_initial": "",
            "secondary_last_name": ""
        },
        "address_info": {
            "street_names_sound_similar_option": "false",
            "street": "3 Times Square",
            "city": "New York",
            "state": "NY",
            "county": "New York",
            "zip_code": "10036",
            "province": "",
            "country": ""
        },
        "phone_number": "646-223-4000",
        "datasources": {
            "public_record_business": "true",
            "npi_record": "true",
            "public_record_ucc_filings": "true",
            "world_check_risk_intelligence": "true"
        }
    }

    query = build_business_search_xml(business_data)

    response = requests.post(
        ENDPOINTS["business"],
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/xml",
            "Content-Type": "application/xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache"
        },
        data=query,
        timeout=30
    )

    root = ET.fromstring(response.text)
    uri_element = root.find('.//Uri')

    if uri_element is not None:
        results_uri = uri_element.text

        results_response = requests.get(
            results_uri,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/xml",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                              "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            },
            timeout=30
        )

        return parse_business_search_response(results_response.text)

    return parse_business_search_response(response.text)
