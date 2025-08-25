"""Builder module for converting JSON requests to XML format for Thomson Reuters Clear S2S API."""

from typing import Dict, Any
import os
import re

# Keep the validation constants and functions
GLB_CODES = {
    "C": "For use by a person holding a legal or beneficial interest relating to the consumer.",
    "A": "For use in complying with federal, state, or local laws, rules, and other "
    "applicable legal requirements.",
    "I": "For use as necessary to effect, administer or enforce a transaction that "
    "a consumer requests or authorizes.",
    "J": "For use in complying with a properly authorized civil, criminal or "
    "regulatory investigation, or subpoena or summons by Federal, State or "
    "local authority.",
    "B": "For use to protect against or prevent actual or potential fraud, "
    "unauthorized transactions, claims or other liability.",
    "L": "For use by a Law Enforcement Agency, self-regulatory organizations or for "
    "an investigation on a matter related to public safety.",
    "Q": "With the consent or at the direction of the consumer.",
    "H": "To persons acting in a fiduciary or representative capacity on behalf of "
    "the consumer.",
    "K": "For required institutional risk control or for resolving consumer disputes "
    "or inquiries.",
}

DPPA_CODES = {
    "1": "For official use by a Court, Law Enforcement Agency or other Government agency.",
    "3": "To verify or correct information provided to you by a person in order to "
    "prevent fraud, pursue legal remedies or recover a debt; skip tracing.",
    "4": "For use in connection with a civil, criminal or arbitral legal proceeding "
    "or legal research.",
    "6": "For use in connection with an insurance claims investigation or insurance "
    "antifraud activities.",
    "0": "No permitted use.",
}

VOTER_CODES = {
    "2": "Use in connection with a permissible election-related purpose.",
    "5": "Use in connection with a non-commercial purpose.",
    "7": "No permitted use.",
}


def validate_permissible_purpose(
    glb: str = "C", dppa: str = "1", voter: str = "2"
) -> Dict[str, str]:
    """
    Validate permissible purpose codes and return descriptions.

    Args:
        glb: GLB code (C, A, I, J, B, L, Q, H, K)
        dppa: DPPA code (1, 3, 4, 6, 0)
        voter: Voter code (2, 5, 7)

    Returns:
        Dict with validated codes and their descriptions

    Raises:
        ValueError: If any code is invalid
    """
    if glb not in GLB_CODES:
        raise ValueError(
            f"Invalid GLB code: {glb}. Valid codes: {list(GLB_CODES.keys())}"
        )

    if dppa not in DPPA_CODES:
        raise ValueError(
            f"Invalid DPPA code: {dppa}. Valid codes: {list(DPPA_CODES.keys())}"
        )

    if voter not in VOTER_CODES:
        raise ValueError(
            f"Invalid Voter code: {voter}. Valid codes: {list(VOTER_CODES.keys())}"
        )

    return {
        "glb": glb,
        "dppa": dppa,
        "voter": voter,
        "glb_description": GLB_CODES[glb],
        "dppa_description": DPPA_CODES[dppa],
        "voter_description": VOTER_CODES[voter],
    }


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
    # Validate permissible purpose if provided
    if "permissible_purpose" in json_data:
        validate_permissible_purpose(**json_data["permissible_purpose"])

    # Load template
    template = _load_template("person-search.xml")

    # Flatten nested data for template interpolation
    flat_data = _flatten_dict(json_data)

    # Add default permissible purpose if not provided
    if "glb" not in flat_data:
        flat_data["glb"] = "I"
    if "dppa" not in flat_data:
        flat_data["dppa"] = "6"
    if "voter" not in flat_data:
        flat_data["voter"] = "7"

    # Interpolate template
    return _safe_format_template(template, flat_data)


def build_business_search_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON business search request to XML format using template.

    Args:
        json_data: Dictionary containing business search parameters

    Returns:
        str: XML string for business search request
    """
    # Validate permissible purpose if provided
    if "permissible_purpose" in json_data:
        validate_permissible_purpose(**json_data["permissible_purpose"])

    # Load template
    template = _load_template("business-search.xml")

    # Flatten nested data for template interpolation
    flat_data = _flatten_dict(json_data)

    # Add default permissible purpose if not provided
    if "glb" not in flat_data:
        flat_data["glb"] = "I"
    if "dppa" not in flat_data:
        flat_data["dppa"] = "6"
    if "voter" not in flat_data:
        flat_data["voter"] = "7"

    # Interpolate template
    return _safe_format_template(template, flat_data)


def build_person_report_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON person report request to XML format using template.

    Args:
        json_data: Dictionary containing person report parameters

    Returns:
        str: XML string for person report request
    """
    # Validate permissible purpose if provided
    if "permissible_purpose" in json_data:
        validate_permissible_purpose(**json_data["permissible_purpose"])

    # Load template
    template = _load_template("person-report.xml")

    # Flatten nested data for template interpolation
    flat_data = _flatten_dict(json_data)

    # Add default permissible purpose if not provided
    if "glb" not in flat_data:
        flat_data["glb"] = "I"
    if "dppa" not in flat_data:
        flat_data["dppa"] = "6"
    if "voter" not in flat_data:
        flat_data["voter"] = "7"

    # Interpolate template
    return _safe_format_template(template, flat_data)


def build_business_report_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON business report request to XML format using template.

    Args:
        json_data: Dictionary containing business report parameters

    Returns:
        str: XML string for business report request
    """
    # Validate permissible purpose if provided
    if "permissible_purpose" in json_data:
        validate_permissible_purpose(**json_data["permissible_purpose"])

    # Load template
    template = _load_template("business-report.xml")

    # Flatten nested data for template interpolation
    flat_data = _flatten_dict(json_data)

    # Add default permissible purpose if not provided
    if "glb" not in flat_data:
        flat_data["glb"] = "I"
    if "dppa" not in flat_data:
        flat_data["dppa"] = "6"
    if "voter" not in flat_data:
        flat_data["voter"] = "7"

    # Interpolate template
    return _safe_format_template(template, flat_data)
