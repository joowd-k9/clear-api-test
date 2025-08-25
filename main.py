"""FastAPI application for Clear API"""

import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import requests
from fastapi import FastAPI
from api.config import ENDPOINTS
from api.token import Token
from api.builder import build_business_search_xml, build_business_report_xml
from api.parser import parse_business_search_response

load_dotenv()

app = FastAPI(debug=True)

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
        ENDPOINTS["business-search"],
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

    # Check if search request was successful
    if response.status_code != 200:
        print(f"Search request failed with status {response.status_code}: {response.text}")
        return {"error": f"Search request failed with status {response.status_code}", "response": response.text}

    root = ET.fromstring(response.text)
    uri_element = root.find('.//Uri')

    # Check if search was successful
    if uri_element is None:
        # Log the response for debugging
        print(f"Search failed. Response: {response.text}")
        return {"error": "Search failed - no URI found in response", "response": response.text}

    results_response = requests.get(
        uri_element.text,
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

    results_response = parse_business_search_response(results_response.text)

    business_report_data = {
        "reference": "S2S Business Report",
        "group_id": results_response["ResultGroup"]["GroupId"]
    }

    report_xml = build_business_report_xml(business_report_data)

    report_response_obj = requests.post(ENDPOINTS["business-report"], headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/xml",
        "Content-Type": "application/xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }, data=report_xml, timeout=30)

    # Check if report request was successful
    if report_response_obj.status_code != 200:
        print(f"Report request failed with status {report_response_obj.status_code}: {report_response_obj.text}")
        return {"error": f"Report request failed with status {report_response_obj.status_code}", "response": report_response_obj.text}

    report_response = report_response_obj.text

    xml_root = ET.fromstring(report_response)
    uri_element = xml_root.find('.//Uri')

    # Check if report request was successful
    if uri_element is None:
        print(f"Report request failed. Response: {report_response}")
        return {"error": "Report request failed - no URI found in response", "response": report_response}

    final_response = requests.get(uri_element.text, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }, timeout=30).text

    return parse_business_search_response(final_response)
