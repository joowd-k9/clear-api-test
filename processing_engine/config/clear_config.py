"""Configuration management for Thomson Reuters CLEAR API integration."""

import os
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ClearAPIConfig(BaseModel):
    """Configuration model for CLEAR API integration."""

    # API Credentials
    client_key: str = Field(..., description="CLEAR API client key")
    client_secret: str = Field(..., description="CLEAR API client secret")

    # API Endpoints
    api_base_url: str = Field(
        default="https://api.thomsonreuters.com/",
        description="Base URL for CLEAR API authentication",
    )
    s2s_base_url: str = Field(
        default="https://s2ssandbox.thomsonreuters.com/",
        description="Base URL for CLEAR S2S services",
    )

    # Request Configuration
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    rate_limit_interval: float = Field(
        default=0.1, description="Minimum interval between requests in seconds"
    )

    # Cache Configuration
    token_cache_ttl: int = Field(default=3600, description="Token cache TTL in seconds")
    cache_directory: str = Field(
        default="~/.clear_api_cache", description="Directory for token caching"
    )

    # Processing Configuration
    enable_business_checks: bool = Field(
        default=True, description="Enable business background checks"
    )
    enable_person_checks: bool = Field(
        default=True, description="Enable person/owner background checks"
    )

    # Data Sources Configuration
    enable_ucc_records: bool = Field(default=True, description="Include UCC filings")
    enable_lien_records: bool = Field(
        default=True, description="Include liens and judgments"
    )
    enable_criminal_records: bool = Field(
        default=True, description="Include criminal history"
    )
    enable_lawsuit_records: bool = Field(
        default=True, description="Include lawsuit records"
    )
    enable_docket_records: bool = Field(
        default=True, description="Include docket records"
    )

    @classmethod
    def from_environment(cls) -> "ClearAPIConfig":
        """Create configuration from environment variables."""
        return cls(
            client_key=os.getenv("CLEAR_CLIENT_KEY", ""),
            client_secret=os.getenv("CLEAR_CLIENT_SECRET", ""),
            api_base_url=os.getenv("CLEAR_API_URL", "https://api.thomsonreuters.com/"),
            s2s_base_url=os.getenv(
                "CLEAR_S2S_URL", "https://s2ssandbox.thomsonreuters.com/"
            ),
            request_timeout=int(os.getenv("CLEAR_REQUEST_TIMEOUT", "30")),
            max_retries=int(os.getenv("CLEAR_MAX_RETRIES", "3")),
            rate_limit_interval=float(os.getenv("CLEAR_RATE_LIMIT_INTERVAL", "0.1")),
            token_cache_ttl=int(os.getenv("CLEAR_TOKEN_CACHE_TTL", "3600")),
            cache_directory=os.getenv("CLEAR_CACHE_DIR", "~/.clear_api_cache"),
            enable_business_checks=os.getenv(
                "CLEAR_ENABLE_BUSINESS_CHECKS", "true"
            ).lower()
            == "true",
            enable_person_checks=os.getenv("CLEAR_ENABLE_PERSON_CHECKS", "true").lower()
            == "true",
            enable_ucc_records=os.getenv("CLEAR_ENABLE_UCC", "true").lower() == "true",
            enable_lien_records=os.getenv("CLEAR_ENABLE_LIENS", "true").lower()
            == "true",
            enable_criminal_records=os.getenv("CLEAR_ENABLE_CRIMINAL", "true").lower()
            == "true",
            enable_lawsuit_records=os.getenv("CLEAR_ENABLE_LAWSUITS", "true").lower()
            == "true",
            enable_docket_records=os.getenv("CLEAR_ENABLE_DOCKETS", "true").lower()
            == "true",
        )

    def get_endpoints(self) -> Dict[str, str]:
        """Get API endpoint URLs."""
        api_base = str(self.api_base_url).rstrip("/")
        s2s_base = str(self.s2s_base_url).rstrip("/")
        return {
            "auth": f"{api_base}/tr-oauth/v1/token",
            "business-search": f"{s2s_base}/v2/business/searchResults",
            "person-search": f"{s2s_base}/v3/person/searchResults",
            "business-report": f"{s2s_base}/v2/businessReport/reportResults",
            "person-report": f"{s2s_base}/v3/personReport/reportResults",
        }

    def validate_credentials(self) -> None:
        """Validate that required credentials are present."""
        if not self.client_key or not self.client_secret:
            raise ValueError(
                "CLEAR API credentials are required. Set CLEAR_CLIENT_KEY and "
                "CLEAR_CLIENT_SECRET environment variables or provide them explicitly."
            )

    def get_datasources_config(self) -> Dict[str, bool]:
        """Get data sources configuration for API requests."""
        return {
            "PublicRecordBusiness": self.enable_business_checks,
            "NPIRecord": self.enable_business_checks,
            "PublicRecordUCCFilings": self.enable_ucc_records,
            "PublicRecordPerson": self.enable_person_checks,
            "CriminalAndTrafficRecord": self.enable_criminal_records,
            "LienJudgmentRecord": self.enable_lien_records,
            "UCCRecord": self.enable_ucc_records,
            "WorldCheckRiskIntelligence": True,  # Always enabled for risk intelligence
        }


# Global configuration instance
_config_instance: Optional[ClearAPIConfig] = None


def get_clear_config() -> ClearAPIConfig:
    """Get the global CLEAR API configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ClearAPIConfig.from_environment()
        _config_instance.validate_credentials()
    return _config_instance


def set_clear_config(config: ClearAPIConfig) -> None:
    """Set the global CLEAR API configuration instance."""
    global _config_instance
    config.validate_credentials()
    _config_instance = config
