"""Builder module for converting JSON requests to XML format for Thomson Reuters Clear S2S API."""

from typing import Dict, Any
import os
import re


def _load_template(template_name: str) -> str:
    """Load XML template from templates directory."""
    template_path = os.path.join(
        os.path.dirname(__file__), "..", "templates", template_name
    )
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def _flatten_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten nested dictionary for template interpolation."""
    flat_data = {}

    for key, value in data.items():
        if isinstance(value, dict):
            # Handle nested dictionaries by extracting their values directly
            for nested_key, nested_value in value.items():
                flat_data[nested_key] = nested_value
        else:
            flat_data[key] = value

    return flat_data


def _safe_format_template(template: str, data: Dict[str, Any]) -> str:
    """Safely format template with data, providing empty string for missing keys."""

    def replace_placeholder(match):
        key = match.group(1)
        return str(data.get(key, ""))

    return re.sub(r"\{(\w+)\}", replace_placeholder, template)


def build_person_search_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON person search request to XML format using template.

    Args:
        json_data: Dictionary containing person search parameters

    Returns:
        str: XML string for person search request
    """

    # Interpolate template
    return _safe_format_template(
        _load_template("person-search.xml"), _flatten_dict(json_data)
    )


def build_business_search_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON business search request to XML format using template.

    Args:
        json_data: Dictionary containing business search parameters

    Returns:
        str: XML string for business search request
    """

    # Interpolate template
    return _safe_format_template(
        _load_template("business-search.xml"), _flatten_dict(json_data)
    )


def build_person_report_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON person report request to XML format using template.

    Args:
        json_data: Dictionary containing person report parameters

    Returns:
        str: XML string for person report request
    """
    return _safe_format_template(
        _load_template("person-report.xml"), _flatten_dict(json_data)
    )


def build_business_report_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON business report request to XML format using template.

    Args:
        json_data: Dictionary containing business report parameters

    Returns:
        str: XML string for business report request
    """
    return _safe_format_template(
        _load_template("business-report.xml"), _flatten_dict(json_data)
    )
