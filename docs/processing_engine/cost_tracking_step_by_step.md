# Cost Tracking Step-by-Step Explanation

## Overview
This document provides a detailed step-by-step explanation of how cost tracking works in the processing engine, combining the Single Processor Run Execution Flow with the External API Call Flow as a practical example.

## Complete Flow: Single Processor Run with External API Call

### Phase 1: Processor Run Initialization
**Step 1: Execution Start**
- A new processing execution begins for an underwriting request
- The system initializes the execution context and prepares for processor runs

**Step 2: Processor Run Initialization**
- Load processor configuration from database or config files
- Check if base cost has already been charged for this processor type in this execution
- Initialize an empty cost tracker list for this specific run
- Set up the run context within the execution

**Step 3: Input Prevalidation**
- Pre-validate account/underwriting IDs to ensure they exist and are valid
- Verify that required input data is present and properly formatted

### Phase 2: Processing Pipeline
**Step 4: Validation Step**
- Validate business rules specific to this processor type
- Check data completeness to ensure all required information is available
- Verify that the processor can handle the given input data

**Step 5: Processing Step - Cache Check**
- Generate a unique cache key based on request parameters (e.g., business name, address, etc.)
- Check cache for existing results with the same parameters
- If cached data is found: return result with $0.00 cost (base cost may still apply per business logic)
- If no cache hit: proceed to external API call

**Step 6: Processing Step - External API Call**
- **Base Cost Tracking**: $0.50 is tracked as the processor's base cost for this execution
- Make HTTP request to external service (e.g., CLEAR, Experian, Equifax)
- Handle the API response and process the returned data
- **API Cost Tracking**: $0.75 is tracked as the cost for the external API call
- Cache the successful result for future use

**Step 7: Processing Step - Heavy Processing (if applicable)**
- Perform any additional processing required (e.g., data transformation, analysis)
- Track costs for processing operations if applicable
- Cache successful outputs for future reference

**Step 8: Extraction Step**
- Extract relevant factors from the processed data
- Format the output according to the defined schema
- Ensure data quality and consistency

### Phase 3: Result Aggregation and Cost Calculation
**Step 9: Result Aggregation**
- Combine extracted factors from all inputs
- Prepare the final output structure according to the processor's requirements
- Validate the completeness of the aggregated results

**Step 10: Cost Calculation**
- Sum all tracked costs for this run (base cost + API costs + processing costs)
- Add base cost according to configured business logic (per execution, per run, etc.)
- Generate detailed cost breakdown for this run
- Include cost information in the processing result

**Step 11: Result Return**
- Return ProcessingResult with complete cost breakdown
- Update execution history with run results and cost information
- Mark the run as completed successfully

### Phase 4: Execution Summary
**Step 12: Execution Cost Summary**
- **Total Runs**: 1 successful run was executed
- **Cost Breakdown**: $1.25 total ($0.50 base cost + $0.75 API cost)
- **Cache Status**: The result was cached, so future identical requests will be served from cache
- **Execution Status**: The entire execution completed successfully

## Cost Tracking Details

### Base Cost Logic
- **Per Execution Pattern**: Base cost charged once per execution, regardless of retries
- **Per Run Pattern**: Base cost charged for every individual run attempt
- **Per Execution Per Run Pattern**: Base cost charged once per execution for each unique input combination

### External API Cost Tracking
- Each API call is tracked individually with its specific cost
- Failed API calls still incur costs (attempted calls are charged)
- Cached results avoid API costs but may still incur base costs

### Caching Strategy
- **Cache Key Generation**: Based on all relevant request parameters
- **Cache Hit**: Returns $0.00 API cost, base cost may still apply
- **Cache Miss**: Full API cost is tracked and result is cached
- **Error Caching**: 422/validation errors are cached, 500/server errors are not

## Key Benefits

### Cost Optimization
- **Caching**: Future identical requests use cached data, avoiding API costs
- **Smart Retry Logic**: Only retry on appropriate error types
- **Base Cost Management**: Flexible charging patterns based on business needs

### Performance
- **Fast Response**: Cached responses are much faster than API calls
- **Reduced Load**: Less external API traffic due to caching
- **Efficient Processing**: Parallel execution where possible

### Transparency
- **Detailed Tracking**: All costs are tracked and reported for billing
- **Audit Trail**: Complete history of all processing attempts and costs
- **Monitoring**: Real-time cost metrics and performance analytics

## Example Scenarios

### Scenario 1: Successful First Run
- Base Cost: $0.50 (charged)
- API Cost: $0.75 (charged)
- Total Cost: $1.25
- Result: Cached for future use

### Scenario 2: Cached Result
- Base Cost: $0.00 (already charged in same execution)
- API Cost: $0.00 (cached result)
- Total Cost: $0.00
- Result: Served from cache

### Scenario 3: Failed API Call with Retry
- Run 1: Base Cost: $0.50, API Cost: $0.75 (failed)
- Run 2: Base Cost: $0.00, API Cost: $0.75 (retry, success)
- Total Cost: $2.00
- Result: Cached after successful retry

This comprehensive flow ensures accurate cost tracking while optimizing performance through intelligent caching and retry mechanisms.
