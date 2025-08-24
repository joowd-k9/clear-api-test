"""Parser module for converting Thomson Reuters Clear S2S XML responses to JSON."""

import xml.etree.ElementTree as ET
from typing import Dict, Any


def parse_person_search_response(xml_string: str) -> Dict[str, Any]:
    """
    Parse Thomson Reuters Clear S2S person search XML response to JSON.

    Args:
        xml_string: XML response string from the API

    Returns:
        Dict containing parsed JSON data
    """
    root = ET.fromstring(xml_string)
    return _element_to_dict(root)


def parse_business_search_response(xml_string: str) -> Dict[str, Any]:
    """
    Parse Thomson Reuters Clear S2S business search XML response to JSON.

    Args:
        xml_string: XML response string from the API

    Returns:
        Dict containing parsed JSON data
    """
    root = ET.fromstring(xml_string)
    return _element_to_dict(root)


def _element_to_dict(element: ET.Element) -> Dict[str, Any]:
    """Convert XML element to dictionary."""
    result = {}

    # Add attributes
    if element.attrib:
        result['@attributes'] = element.attrib

    # Process child elements
    for child in element:
        tag = child.tag
        # Remove namespace prefix if present
        if '}' in tag:
            tag = tag.split('}', 1)[1]

        child_dict = _element_to_dict(child)

        # Handle multiple elements with same tag
        if tag in result:
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(child_dict)
        else:
            result[tag] = child_dict

    # Convert single item lists to single items for cleaner output
    for key, value in result.items():
        if isinstance(value, list) and len(value) == 1:
            result[key] = value[0]

    # If element has text content and no children, use text as value
    if element.text and element.text.strip() and not result:
        return element.text.strip()

    # If element has both text and children, add text as a special key
    elif element.text and element.text.strip():
        result['_text'] = element.text.strip()

    return result
