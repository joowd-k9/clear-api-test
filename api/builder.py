"""Builder module for converting JSON requests to XML format for Thomson Reuters Clear S2S API."""

from typing import Dict, Any
import xml.etree.ElementTree as ET

NS = {
    'ps': 'http://clear.thomsonreuters.com/api/search/2.0',
    'p1': 'com/thomsonreuters/schemas/search',
    'bs': 'http://clear.thomsonreuters.com/api/search/2.0',
    'b1': 'com/thomsonreuters/schemas/search'
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

GLB_CODES = {
    'C': 'For use by a person holding a legal or beneficial interest relating to the consumer.',
    'A': 'For use in complying with federal, state, or local laws, rules, and other ' \
         'applicable legal requirements.',
    'I': 'For use as necessary to effect, administer or enforce a transaction that ' \
         'a consumer requests or authorizes.',
    'J': 'For use in complying with a properly authorized civil, criminal or ' \
         'regulatory investigation, or subpoena or summons by Federal, State or ' \
         'local authority.',
    'B': 'For use to protect against or prevent actual or potential fraud, ' \
         'unauthorized transactions, claims or other liability.',
    'L': 'For use by a Law Enforcement Agency, self-regulatory organizations or for ' \
         'an investigation on a matter related to public safety.',
    'Q': 'With the consent or at the direction of the consumer.',
    'H': 'To persons acting in a fiduciary or representative capacity on behalf of ' \
         'the consumer.',
    'K': 'For required institutional risk control or for resolving consumer disputes ' \
         'or inquiries.'
}

DPPA_CODES = {
    '1': 'For official use by a Court, Law Enforcement Agency or other Government agency.',
    '3': 'To verify or correct information provided to you by a person in order to ' \
         'prevent fraud, pursue legal remedies or recover a debt; skip tracing.',
    '4': 'For use in connection with a civil, criminal or arbitral legal proceeding ' \
         'or legal research.',
    '6': 'For use in connection with an insurance claims investigation or insurance ' \
         'antifraud activities.',
    '0': 'No permitted use.'
}

VOTER_CODES = {
    '2': 'Use in connection with a permissible election-related purpose.',
    '5': 'Use in connection with a non-commercial purpose.',
    '7': 'No permitted use.'
}


def validate_permissible_purpose(
    glb: str = 'C',
    dppa: str = '1',
    voter: str = '2'
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
        raise ValueError(f"Invalid GLB code: {glb}. Valid codes: {list(GLB_CODES.keys())}")

    if dppa not in DPPA_CODES:
        raise ValueError(f"Invalid DPPA code: {dppa}. Valid codes: {list(DPPA_CODES.keys())}")

    if voter not in VOTER_CODES:
        raise ValueError(f"Invalid Voter code: {voter}. Valid codes: {list(VOTER_CODES.keys())}")

    return {
        'glb': glb,
        'dppa': dppa,
        'voter': voter,
        'glb_description': GLB_CODES[glb],
        'dppa_description': DPPA_CODES[dppa],
        'voter_description': VOTER_CODES[voter]
    }


def build_person_search_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON person search request to XML format.

    Args:
        json_data: Dictionary containing person search parameters

    Returns:
        str: XML string for person search request

    Example JSON format:
    {
        "permissible_purpose": {
            "glb": "C",
            "dppa": "1",
            "voter": "2"
        },
        "reference": "S2S Person Search",
        "name_info": {
            "last_name": "Sample-Document",
            "first_name": "Jane",
            "middle_initial": "",
            "secondary_last_name": "Document"
        },
        "address_info": {
            "street": "101 W 6th ST",
            "city": "TUCSON",
            "state": "AZ",
            "zip_code": "85701"
        },
        "npi_number": "9999999999",
        "ssn": "999-99-9990",
        "person_birth_date": "01/01/1951",
        "driver_license_number": "MI0022446688",
        "datasources": {
            "public_record_people": "true",
            "npi_record": "true",
            "world_check_risk_intelligence": "true"
        }
    }
    """
    root = ET.Element('{http://clear.thomsonreuters.com/api/search/2.0}PersonSearchRequestV3')

    _add_permissible_purpose(root, json_data.get('permissible_purpose', {}))

    reference = ET.SubElement(root, 'Reference')
    reference.text = json_data.get('reference', 'S2S Person Search')

    criteria = ET.SubElement(root, 'Criteria')
    person_criteria = ET.SubElement(criteria, '{com/thomsonreuters/schemas/search}PersonCriteria')

    _add_name_info(person_criteria, json_data.get('name_info', {}))

    _add_address_info(person_criteria, json_data.get('address_info', {}))

    _add_simple_fields(person_criteria, json_data)

    _add_datasources(root, json_data.get('datasources', {}))

    return _xml_to_string(root)


def build_business_search_xml(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON business search request to XML format.

    Args:
        json_data: Dictionary containing business search parameters

    Returns:
        str: XML string for business search request

    Example JSON format:
    {
        "permissible_purpose": {
            "glb": "C",
            "dppa": "1",
            "voter": "2"
        },
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
            "last_name": "Bello",
            "first_name": "Stephane"
        },
        "address_info": {
            "street": "3 Times Square",
            "city": "New York",
            "state": "NY",
            "zip_code": "10036"
        },
        "phone_number": "646-223-4000",
        "datasources": {
            "public_record_business": "true",
            "npi_record": "true",
            "public_record_ucc_filings": "true",
            "world_check_risk_intelligence": "true"
        }
    }
    """
    root = ET.Element('{http://clear.thomsonreuters.com/api/search/2.0}BusinessSearchRequest')

    _add_permissible_purpose(root, json_data.get('permissible_purpose', {}))

    reference = ET.SubElement(root, 'Reference')
    reference.text = json_data.get('reference', 'S2S Business Search')

    criteria = ET.SubElement(root, 'Criteria')
    business_criteria = ET.SubElement(criteria, '{com/thomsonreuters/schemas/search}BusinessCriteria')

    company_id = ET.SubElement(business_criteria, 'CompanyEntityId')
    company_id.text = json_data.get('company_entity_id', '')

    business_name = ET.SubElement(business_criteria, 'BusinessName')
    business_name.text = json_data.get('business_name', '')

    _add_corporation_info(business_criteria, json_data.get('corporation_info', {}))

    npi = ET.SubElement(business_criteria, 'NPINumber')
    npi.text = json_data.get('npi_number', '')

    _add_business_name_info(business_criteria, json_data.get('name_info', {}))

    _add_address_info(business_criteria, json_data.get('address_info', {}))

    phone = ET.SubElement(business_criteria, 'PhoneNumber')
    phone.text = json_data.get('phone_number', '')

    _add_business_datasources(root, json_data.get('datasources', {}))

    return _xml_to_string(root)


def _add_corporation_info(parent: ET.Element, corp_data: Dict[str, Any]) -> None:
    """Add CorporationInfo section."""
    corp_info = ET.SubElement(parent, 'CorporationInfo')

    corp_fields = ['CorporationId', 'FilingNumber', 'FilingDate', 'FEIN', 'DUNSNumber']
    for field in corp_fields:
        elem = ET.SubElement(corp_info, field)
        elem.text = corp_data.get(field.lower(), '')


def _add_business_datasources(root: ET.Element, datasources: Dict[str, Any]) -> None:
    """Add Datasources section for business search."""
    datasources_elem = ET.SubElement(root, 'Datasources')

    source_fields = [
        'PublicRecordBusiness',
        'NPIRecord',
        'PublicRecordUCCFilings',
        'WorldCheckRiskIntelligence'
    ]
    for field in source_fields:
        elem = ET.SubElement(datasources_elem, field)
        elem.text = str(datasources.get(field.lower(), 'true')).lower()


def _add_permissible_purpose(root: ET.Element, purpose_data: Dict[str, Any]) -> None:
    """Add PermissiblePurpose section."""
    purpose = ET.SubElement(root, 'PermissiblePurpose')

    glb = ET.SubElement(purpose, 'GLB')
    glb.text = purpose_data.get('glb', 'See Appendix A: Permissible Use Definitions for ' \
                                      'acceptable values')

    dppa = ET.SubElement(purpose, 'DPPA')
    dppa.text = purpose_data.get('dppa', 'See Appendix A: Permissible Use Definitions for ' \
                                        'acceptable values')

    voter = ET.SubElement(purpose, 'VOTER')
    voter.text = purpose_data.get('voter', 'See Appendix A: Permissible Use Definitions for ' \
                                          'acceptable values')


def _add_name_info(parent: ET.Element, name_data: Dict[str, Any]) -> None:
    """Add NameInfo section."""
    name_info = ET.SubElement(parent, 'NameInfo')

    advanced = ET.SubElement(name_info, 'AdvancedNameSearch')
    advanced_options = [
        'LastSecondaryNameSoundSimilarOption',
        'SecondaryLastNameOption',
        'FirstNameBeginsWithOption',
        'FirstNameSoundSimilarOption',
        'FirstNameExactMatchOption'
    ]

    for option in advanced_options:
        elem = ET.SubElement(advanced, option)
        if option == 'SecondaryLastNameOption':
            elem.text = name_data.get(option.lower(), 'OR')
        else:
            elem.text = str(name_data.get(option.lower(), 'false')).lower()

    name_fields = ['LastName', 'FirstName', 'MiddleInitial', 'SecondaryLastName']
    for field in name_fields:
        elem = ET.SubElement(name_info, field)
        elem.text = name_data.get(field.lower(), '')


def _add_business_name_info(parent: ET.Element, name_data: Dict[str, Any]) -> None:
    """Add NameInfo section for business search."""
    name_info = ET.SubElement(parent, 'NameInfo')

    advanced = ET.SubElement(name_info, 'AdvancedNameSearch')
    advanced_options = [
        'LastSecondaryNameSoundSimilarOption',
        'SecondaryLastNameOption',
        'FirstNameSoundSimilarOption',
        'FirstNameVariationsOption'
    ]

    for option in advanced_options:
        elem = ET.SubElement(advanced, option)
        if option == 'SecondaryLastNameOption':
            elem.text = name_data.get(option.lower(), 'OR')
        else:
            elem.text = str(name_data.get(option.lower(), 'false')).lower()

    name_fields = ['LastName', 'FirstName', 'MiddleInitial', 'SecondaryLastName']
    for field in name_fields:
        elem = ET.SubElement(name_info, field)
        elem.text = name_data.get(field.lower(), '')


def _add_address_info(parent: ET.Element, address_data: Dict[str, Any]) -> None:
    """Add AddressInfo section."""
    address_info = ET.SubElement(parent, 'AddressInfo')

    sound_option = ET.SubElement(address_info, 'StreetNamesSoundSimilarOption')
    sound_option.text = str(address_data.get('street_names_sound_similar_option', 'false')).lower()

    address_fields = ['Street', 'City', 'State', 'County', 'ZipCode', 'Province', 'Country']
    for field in address_fields:
        elem = ET.SubElement(address_info, field)
        elem.text = address_data.get(field.lower(), '')


def _add_simple_fields(parent: ET.Element, data: Dict[str, Any]) -> None:
    """Add simple fields like EmailAddress, NPINumber, SSN, etc."""
    simple_fields = [
        'EmailAddress',
        'NPINumber',
        'SSN',
        'PhoneNumber',
        'DriverLicenseNumber',
        'WorldCheckUniqueId'
    ]

    for field in simple_fields:
        elem = ET.SubElement(parent, field)
        elem.text = data.get(field.lower(), '')

    age_info = ET.SubElement(parent, 'AgeInfo')
    age_fields = ['PersonBirthDate', 'PersonAgeTo', 'PersonAgeFrom']
    for field in age_fields:
        elem = ET.SubElement(age_info, field)
        elem.text = data.get(field.lower(), '')

    person_entity_id = ET.SubElement(parent, 'PersonEntityId')
    person_entity_id.text = data.get('person_entity_id', '')


def _add_datasources(root: ET.Element, datasources: Dict[str, Any]) -> None:
    """Add Datasources section."""
    datasources_elem = ET.SubElement(root, 'Datasources')

    source_fields = ['PublicRecordPeople', 'NPIRecord', 'WorldCheckRiskIntelligence']
    for field in source_fields:
        elem = ET.SubElement(datasources_elem, field)
        elem.text = str(datasources.get(field.lower(), 'true')).lower()


def _xml_to_string(root: ET.Element) -> str:
    """Convert XML element to properly formatted string."""
    xml_str = ET.tostring(root, encoding='unicode', method='xml')

    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
