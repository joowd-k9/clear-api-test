"""
Example external API processor demonstrating cost tracking implementation.

This example shows how to implement cost tracking for external API calls
in a processor that makes calls to external services.
"""

from typing import Any
import requests
from processing_engine.processors.base_processor import BaseProcessor
from processing_engine.models.execution import CostEntry


class ExternalAPIProcessor(BaseProcessor):
    """
    Example processor that demonstrates cost tracking for external API calls.
    
    This processor simulates making calls to external services and tracking
    the associated costs.
    """
    
    PROCESSOR_NAME = "external_api_example"
    
    def __init__(self, account_id: str, underwriting_id: str, **kwargs):
        super().__init__(account_id, underwriting_id, **kwargs)
        
        # Define cost structure for different API operations
        self.api_costs = {
            "experian": {
                "business_credit_report": 0.50,
                "personal_credit_report": 0.25,
                "trade_lines": 0.10,
            },
            "clear": {
                "business_search": 0.75,
                "principal_search": 0.50,
                "address_verification": 0.15,
            },
            "equifax": {
                "business_report": 0.45,
                "payment_history": 0.20,
            }
        }
    
    def base_cost(self) -> float:
        """
        Get the base cost of the processor from database.
        In a real implementation, this would fetch from the database.
        """
        # This would typically fetch from database
        # return self._get_processor_pricing("external_api_example").base_cost
        return 0.10  # Example base cost
    
    def _validate(self, data: Any) -> Any:
        """Validate input data."""
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")
        
        if "business_name" not in data:
            raise ValueError("business_name is required")
        
        return data
    
    def _process(self, data: Any) -> Any:
        """Process the data by making external API calls."""
        business_name = data["business_name"]
        
        # Simulate making API calls to different services
        results = {}
        
        # Call Experian API
        experian_result = self._call_experian_api(business_name)
        results["experian"] = experian_result
        
        # Call CLEAR API
        clear_result = self._call_clear_api(business_name)
        results["clear"] = clear_result
        
        # Call Equifax API
        equifax_result = self._call_equifax_api(business_name)
        results["equifax"] = equifax_result
        
        return results
    
    def _extract(self, data: Any) -> dict[str, str | list | dict]:
        """Extract factors from the processed data."""
        factors = {}
        
        # Extract credit scores
        if "experian" in data and "credit_score" in data["experian"]:
            factors["experian_credit_score"] = str(data["experian"]["credit_score"])
        
        if "equifax" in data and "credit_score" in data["equifax"]:
            factors["equifax_credit_score"] = str(data["equifax"]["credit_score"])
        
        # Extract business information
        if "clear" in data and "business_info" in data["clear"]:
            factors["business_verification"] = data["clear"]["business_info"]
        
        return factors
    
    def _call_experian_api(self, business_name: str) -> dict[str, Any]:
        """Simulate calling Experian API and track costs."""
        try:
            # Simulate API call
            # response = requests.get(f"https://api.experian.com/business/{business_name}")
            
            # Track the cost for business credit report
            self.track_cost(
                service="experian",
                operation="business_credit_report",
                cost=self.api_costs["experian"]["business_credit_report"],
                metadata={
                    "business_name": business_name,
                    "api_endpoint": "business_credit_report",
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            )
            
            # Simulate additional calls if needed
            if self._needs_personal_credit():
                self.track_cost(
                    service="experian",
                    operation="personal_credit_report",
                    cost=self.api_costs["experian"]["personal_credit_report"],
                    metadata={
                        "business_name": business_name,
                        "api_endpoint": "personal_credit_report"
                    }
                )
            
            # Return simulated response
            return {
                "credit_score": 750,
                "trade_lines": 12,
                "status": "active"
            }
            
        except Exception as e:
            # Even if the API call fails, we might still be charged
            self.track_cost(
                service="experian",
                operation="business_credit_report",
                cost=self.api_costs["experian"]["business_credit_report"],
                metadata={
                    "business_name": business_name,
                    "error": str(e),
                    "charged_despite_error": True
                }
            )
            raise
    
    def _call_clear_api(self, business_name: str) -> dict[str, Any]:
        """Simulate calling CLEAR API and track costs."""
        try:
            # Track the cost for business search
            self.track_cost(
                service="clear",
                operation="business_search",
                cost=self.api_costs["clear"]["business_search"],
                metadata={
                    "business_name": business_name,
                    "search_type": "business_entity"
                }
            )
            
            # Simulate additional address verification
            self.track_cost(
                service="clear",
                operation="address_verification",
                cost=self.api_costs["clear"]["address_verification"],
                metadata={
                    "business_name": business_name,
                    "verification_type": "address"
                }
            )
            
            return {
                "business_info": {
                    "entity_type": "LLC",
                    "registration_date": "2020-01-01",
                    "status": "active"
                },
                "address_verified": True
            }
            
        except Exception as e:
            self.track_cost(
                service="clear",
                operation="business_search",
                cost=self.api_costs["clear"]["business_search"],
                metadata={
                    "business_name": business_name,
                    "error": str(e)
                }
            )
            raise
    
    def _call_equifax_api(self, business_name: str) -> dict[str, Any]:
        """Simulate calling Equifax API and track costs."""
        try:
            # Track the cost for business report
            self.track_cost(
                service="equifax",
                operation="business_report",
                cost=self.api_costs["equifax"]["business_report"],
                metadata={
                    "business_name": business_name,
                    "report_type": "commercial"
                }
            )
            
            return {
                "credit_score": 720,
                "payment_history": "excellent",
                "delinquencies": 0
            }
            
        except Exception as e:
            self.track_cost(
                service="equifax",
                operation="business_report",
                cost=self.api_costs["equifax"]["business_report"],
                metadata={
                    "business_name": business_name,
                    "error": str(e)
                }
            )
            raise
    
    def _needs_personal_credit(self) -> bool:
        """Determine if personal credit check is needed."""
        # This would contain business logic to determine if personal credit is needed
        return True


# Example usage and cost tracking demonstration
if __name__ == "__main__":
    # Create processor instance
    processor = ExternalAPIProcessor(
        account_id="acc_123",
        underwriting_id="uw_456"
        # Base cost is now retrieved from database via base_cost() method
    )
    
    # Simulate processing
    from processing_engine.models.execution import ProcessorInput
    
    input_data = [
        ProcessorInput(
            input_id="input_1",
            account_id="acc_123",
            underwriting_id="uw_456",
            data={"business_name": "Example Corp"}
        )
    ]
    
    # Execute processor
    result = processor.execute(input_data)
    
    # Display cost breakdown
    print("Cost Breakdown:")
    print(f"Total Cost: ${result.cost_breakdown['total_cost']:.2f}")
    print(f"Base Cost: ${result.cost_breakdown['base_cost']:.2f}")
    print(f"Tracked Costs: ${result.cost_breakdown['total_tracked']:.2f}")
    
    print("\nDetailed Breakdown:")
    for service, operations in result.cost_breakdown['tracked_costs'].items():
        print(f"\n{service.upper()}:")
        for operation, details in operations.items():
            print(f"  {operation}: ${details['total_cost']:.2f} ({details['count']} calls)")
            for entry in details['entries']:
                print(f"    - ${entry['cost']:.2f} at {entry['timestamp']}")
                if entry['metadata']:
                    print(f"      Metadata: {entry['metadata']}")
