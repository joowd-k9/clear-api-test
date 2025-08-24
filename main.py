"""FastAPI application for Clear API Token Manager."""

import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, Response
from api.config import ENDPOINTS
from api.token import Token
from api.builder import build_business_search_xml
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

    root = ET.fromstring(response.text)
    uri_element = root.find('.//Uri')


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

    xmlbody = """
<br:BusinessReportRequest xmlns:br="http://clear.thomsonreuters.com/api/report/2.0">
  <PermissiblePurpose>
    <GLB>See Appendix A: Permissible Use Definitions for acceptable values</GLB>
    <DPPA>See Appendix A: Permissible Use Definitions for acceptable values</DPPA>
    <VOTER>See Appendix A: Permissible Use Definitions for acceptable values</VOTER>
  </PermissiblePurpose>
  <Reference>S2S Business Report</Reference>
  <Criteria>
    <rc:ReportCriteria xmlns:rc="com/thomsonreuters/schemas/company-report">
      <GroupID>{results_response["ResultGroup"]["GroupId"]}</GroupID>
      <ReportChoice>Business</ReportChoice>
      <ReportSections>
        <BusinessOverviewSection>true</BusinessOverviewSection>
        <PhoneNumberSection>true</PhoneNumberSection>
        <BusinessSameAddressSection>true</BusinessSameAddressSection>
        <PeopleSameAddressSection>true</PeopleSameAddressSection>
        <PeopleSamePhoneSection>true</PeopleSamePhoneSection>
        <BusinessSamePhoneSection>true</BusinessSamePhoneSection>
        <FEINSection>true</FEINSection>
        <FictitiousBusinessNameSection>true</FictitiousBusinessNameSection>
        <ExecutiveAffiliationSection>true</ExecutiveAffiliationSection>
        <BusinessContactRecordsSection>true</BusinessContactRecordsSection>
        <ExecutiveProfileSection>true</ExecutiveProfileSection>
        <CompanyProfileSection>true</CompanyProfileSection>
        <AnnualFinancialsSection>true</AnnualFinancialsSection>
        <FundamentalRatiosSection>true</FundamentalRatiosSection>
        <MoneyServiceBusinessSection>true</MoneyServiceBusinessSection>
        <DunBradstreetSection>true</DunBradstreetSection>
        <DunBradstreetPCISection>true</DunBradstreetPCISection>
        <WorldbaseSection>true</WorldbaseSection>
        <CorporateSection>true</CorporateSection>
        <BusinessProfileSection>true</BusinessProfileSection>
        <GlobalSanctionSection>true</GlobalSanctionSection>
        <ArrestSection>true</ArrestSection>
        <CriminalSection>true</CriminalSection>
        <ProfessionalLicenseSection>true</ProfessionalLicenseSection>
        <WorldCheckSection>true</WorldCheckSection>
        <InfractionSection>true</InfractionSection>
        <LawsuitSection>true</LawsuitSection>
        <LienJudgmentSection>true</LienJudgmentSection>
        <DocketSection>true</DocketSection>
        <FederalCaseLawSection>true</FederalCaseLawSection>
        <StateCaseLawSection>true</StateCaseLawSection>
        <BankruptcySection>true</BankruptcySection>
        <RealPropertySection>true</RealPropertySection>
        <PreForeclosureSection>true</PreForeclosureSection>
        <BusinessContactSection>true</BusinessContactSection>
        <UCCSection>true</UCCSection>
        <SECFilingSection>true</SECFilingSection>
        <RelatedSECFilingRecordSection>true</RelatedSECFilingRecordSection>
        <OtherSecurityFilingRecordSection>true</OtherSecurityFilingRecordSection>
        <AircraftSection>true</AircraftSection>
        <VehicleSection>true</VehicleSection>
        <WatercraftSection>true</WatercraftSection>
        <NPISection>true</NPISection>
        <HealthcareSanctionSection>true</HealthcareSanctionSection>
        <ExcludedPartySection>true</ExcludedPartySection>
        <AssociateAnalyticsChartSection>true</AssociateAnalyticsChartSection>
        <QuickAnalysisFlagSection>true</QuickAnalysisFlagSection>
        <NewsSection>false</NewsSection>
        <WebAnalyticsSection>false</WebAnalyticsSection>
        <MarijuanaRelatedBusinessesSection>true</MarijuanaRelatedBusinessesSection>
        <NoMatchSections>true</NoMatchSections>
      </ReportSections>
      <IncludeArticles>
        <NewsRecord>
          <RecordId>Set NewsSection to true and use a RecordId from the same result as the GroupId.</RecordId>
        </NewsRecord>
        <WebAnalyticsRecord>
          <RecordId>Set WebAnalyticsSection to true and use a RecordId from the same result as the GroupId.</RecordId>
        </WebAnalyticsRecord>
      </IncludeArticles>
    </rc:ReportCriteria>
  </Criteria>
</br:BusinessReportRequest>
    """

    report_response = requests.post(ENDPOINTS["business-report"], headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/xml",
        "Content-Type": "application/xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }, data=xmlbody, timeout=30).text

    xml_root = ET.fromstring(report_response)
    uri_element = xml_root.find('.//Uri')

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
