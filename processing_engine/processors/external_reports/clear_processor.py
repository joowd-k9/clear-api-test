"""Clear processor module for Thompson Reuters Clear S2S data processing."""

from processing_engine.processors.base_processor import BaseProcessor


class ClearProcessor(BaseProcessor):
    """Processor for Thompson Reuters Clear S2S API."""

    PROCESSOR_NAME: str = "clear_processor"

    REQUIRED_DEPENDENCIES: tuple[str, ...] = (
        "p_business_registration",
        "p_application_form",
        "p_driver_license",
    )

    def _validate(self, data: list) -> list:
        return data

    def _process(self, data: dict) -> dict:
        return data

    def _extract(self, data: dict) -> dict[str, dict]:
        return {"payload": data}
