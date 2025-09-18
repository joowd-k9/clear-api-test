# Processor Run Cost Tracking Implementation

## Overview

The processing engine implements a cost tracking system that manages costs for processor execution, external API calls, and processing activities. This system is designed to handle dynamic cost calculation based on actual usage and supports caching to optimize costs.

## Definitions

### Execution
An **execution** is a single processing session for an underwriting request. A single underwriting can have multiple executions triggered by manual or automatic events (e.g., document updates, manual re-processing). Each execution represents one complete processing cycle and can contain multiple processor runs across different processor types. The execution is the container that tracks the cost and status of that specific processing session.

### Processor Run
A **processor run** is an individual attempt to execute a specific processor within an execution. Each processor run represents one attempt to process data using a particular processor (e.g., CLEAR processor, Experian processor, Bank Statement processor). Multiple runs of the same processor type can occur within a single execution due to retries, manual re-executions, or different processing requirements.

**Key Characteristics:**
- Each processor run has its own cost tracking
- Multiple runs of the same processor type can exist within one execution
- Processor base costs are charged only once per execution per processor type
- Each run tracks its own API calls, processing costs, and results

### Underwriting vs Execution Relationship
- **One Underwriting** can have **Multiple Executions**
- **One Execution** can have **Multiple Processor Runs**
- Executions are triggered by various events (manual, automatic, document updates, retries)
- Each execution maintains its own cost tracking and processing history

## Cost Structure

#### Processor Base Costs
Processors are stored in the database with their pricing information. Some configurations, including pricing, may also be stored in configuration files. Each processor may have a base cost or be free. Base costs are retrieved from the database or configuration files and can be updated without code changes.

Just for the sake of example, here are some possible charging patterns:

*Example 1 - Per Execution:* (used in examples below)
- Run 1: Test Processor - Base cost: $0.10 (charged)
- Run 2: Test Processor (manual re-process) - Base cost: $0.00 (already charged)

*Example 2 - Per Run:*
- Run 1: Test Processor - Base cost: $0.10 (charged)
- Run 2: Test Processor (manual re-process) - Base cost: $0.10 (charged again)

*Example 3 - Per Execution Per Run Per Input:*
- Run 1: Test Processor (input A) - Base cost: $0.10 (charged)
- Run 2: Test Processor (input A re-process) - Base cost: $0.00 (same execution, same input)
- Run 3: Test Processor (input B) - Base cost: $0.10 (charged - different input)

#### External API Costs
External APIs like CLEAR, Experian, and Equifax incur costs per API
call. Different services have different cost structures.

#### Processing Costs
Some processors might have processing costs (e.g., OCR, data transformation). These costs are determined by business rules implemented within each individual processor.

#### Caching Strategy
If results are from cached data, additional API or processing costs could be skipped. The system should track whether costs were avoided due to caching.

## Process Flow

### Single Processor Run Execution Flow

```
1. Processor Run Initialization
   ├── Load processor configuration
   ├── Check if base cost already charged for this processor type in execution
   ├── Initialize cost tracker for this run (empty list)
   └── Set up run context within execution

2. Input Prevalidation
   └── Pre-validate account/underwriting IDs

3. Processing Pipeline (called n times for each items in input list)
   ├── Validation Step
   │   ├── Validate business rules
   │   └── Check data completeness
   ├── Processing Step
   │   ├── Check cache for existing results        # if applicable
   │   ├── Make external API calls                 # if applicable
   │   ├── Do heavy processing                     # if applicable
   │   ├── Cache successful outputs                # if applicable
   │   └── Track costs for each operation          # if applicable
   └── Extraction Step
       ├── Extract factors from processed data
       └── Format output according to schema

4. Post Processing
   ├── Run custom business logic costs tracking (for this run if needed).
   ├── Result Aggregation Combine extracted factors from all inputs
   └── Prepare final output structure

5. Cost Calculation
   ├── Sum all tracked costs for this run
   ├── Add base cost according to configured business logic
   ├── Generate cost breakdown for this run
   └── Include in processing result

6. Result Return
   ├── Return ProcessingResult with cost breakdown
   └── Update execution history with run results
```

### External API Call Flow

```
1. Execution Start
   ├── New underwriting request
   └── Begin processing

2. Run 1: API Call Preparation
   ├── Generate cache key from parameters
   ├── Check cache for existing result
   └── If cached: return result with $0.00 cost (base cost may still apply per business logic)

3. Run 1: First API Attempt
   ├── Track cost: $0.50 (Processor Base Cost)
   ├── Make HTTP request to external API
   ├── Handle response
   ├── Track cost: $0.75 x 2 (if there are two external API calls)
   ├── Cache each successful result
   ├── Run 1 ends with success
   └── Return ProcessingResult with success status

4. Execution Cost Summary
   ├── Total runs: 1 (successful)
   ├── Total cost: $2 ($0.50 base + $0.75 API x 2)
   ├── Cache status: Cached (successful result)
   └── Execution status: Success
```

### Multi Processor Execution Flow

```
1. Execution Start
   ├── Execution could be automatic or manual
   └── Begin processing

2. Run 1: Clear Processor
   ├── Base cost: $0.10 (charged once per processor type per execution)
   ├── Check cache: Miss
   ├── API call: Success
   ├── Track cost: $0.75 x 2 (person search x 2)
   ├── Cache result
   ├── Run cost: $0.75 x 2
   └── Return ProcessingResult

3. Run 2: Bank Statement Processor
   ├── Base cost: $0.10 (charged once per processor type per execution)
   ├── Process document
   ├── Track cost: $2.50 (document processing - 5 pages @ $0.50/page)
   ├── Extract text
   ├── Run cost: $2.50
   └── Return ProcessingResult

4. Run 3: Manual Re-execution - Clear Processor
   ├── Base cost: $0.00 (already charged in Run 1 - per execution model)
   ├── Check cache: Hit (from Run 1)
   ├── Track cost: $0.00 (cached result)
   ├── Use cached data
   ├── Run cost: $0.00
   └── Return ProcessingResult

5. Execution Summary (per execution)
   ├── Total processor runs: 3
   ├── Successful processor runs: 3
   ├── Failed processor runs: 0
   ├── Total tracked cost: $4.00
   ├── Total base cost: $0.20 (2 unique processor types × $0.10 each)
   ├── Total execution cost: $4.20
   └── Execution status: Success
```

### Cache Hit Flow

```
1. Subsequent API Call
   ├── Generate cache key
   ├── Check cache: Hit
   ├── Track cost: $0.00 (cached)
   ├── Return cached result
   └── Skip external API call

2. Cost Optimization
   ├── Original cost: $0.50
   ├── Cached cost: $0.00
   ├── Savings: $0.50
   └── Cache hit rate: 100%

3. Performance Benefits
   ├── Response time: < 10ms (vs 500ms API call)
   ├── No external API load
   ├── Reduced rate limiting
   └── Improved user experience
```

## Cost Breakdown Structure

### Multi Processor Execution Cost Example

This example shows cost breakdown entries from the Multi Processor Execution Flow:

```json
{
    "execution_id": "exec_67890",
    "underwriting_id": "uw_12345",
    "execution_type": "automatic",
    "execution_history": [
        {
            "run_number": 1,
            "processor_name": "clear_processor",
            "base_cost": 0.10,
            "tracked_costs": {
                "person_search": {
                    "count": 2,
                    "total_cost": 1.50,
                    "entries": [
                        {
                            "cost": 0.75,
                            "timestamp": "2024-01-01T12:00:00",
                            "metadata": {
                                "person_name": "Example Person 1",
                                "cached": false,
                                "cache_hit": false,
                                "run_number": 1
                            }
                        },
                        {
                            "cost": 0.75,
                            "timestamp": "2024-01-01T12:00:05",
                            "metadata": {
                                "person_name": "Example Person 2",
                                "cached": false,
                                "cache_hit": false,
                                "run_number": 1
                            }
                        }
                    ]
                }
            },
            "total_tracked": 1.50
        },
        {
            "run_number": 4,
            "processor_name": "bank_statement_processor",
            "base_cost": 0.10,
            "tracked_costs": {
                "document_processing": {
                    "count": 1,
                    "total_cost": 2.50,
                    "entries": [
                        {
                            "cost": 2.50,
                            "timestamp": "2024-01-01T12:15:00",
                            "metadata": {
                                "pages_processed": 5,
                                "cost_per_page": 0.50,
                                "run_number": 4
                            }
                        }
                    ]
                }
            },
            "total_tracked": 2.50
        },
        {
            "run_number": 5,
            "processor_name": "clear_processor",
            "base_cost": 0.00,
            "tracked_costs": {
                "person_search": {
                    "count": 2,
                    "total_cost": 0.00,
                    "entries": [
                        {
                            "cost": 0.00,
                            "timestamp": "2024-01-01T12:20:00",
                            "metadata": {
                                "person_name": "Example Person 1",
                                "cached": true,
                                "cache_hit": true,
                                "run_number": 5
                            }
                        },
                        {
                            "cost": 0.00,
                            "timestamp": "2024-01-01T12:20:00",
                            "metadata": {
                                "person_name": "Example Person 2",
                                "cached": true,
                                "cache_hit": true,
                                "run_number": 5
                            }
                        }
                    ]
                }
            },
            "total_tracked": 0.00
        }
    ],
    "cumulative_costs": {
        "total_base_cost": 0.20,
        "total_tracked_cost": 4.00,
        "total_cost": 4.20
    }
}
```

## Best Practices

#### Cache-First Process
1. **Always Check Cache First**
   - Generate cache key from request parameters
   - Query cache before making external API calls
   - Return cached results with $0.00 cost tracking
   - Skip external API calls when cache hits

2. **Cache Miss Handling**
   - Track full cost for external API calls
   - Make API call to external service
   - Store successful results in cache
   - Include cache metadata in cost tracking

3. **Cache Key Strategy**
   - Use consistent key generation across processors
   - Include all relevant parameters in cache key
   - Consider TTL (Time To Live) for cache entries
   - Handle cache invalidation scenarios

#### Database and Configuration-Driven Cost Management
1. **Base Cost Retrieval**
   - Fetch processor pricing from database or configuration files on initialization
   - Cache pricing information for performance
   - Handle missing pricing gracefully (default to $0.00)
   - Support dynamic pricing updates without code changes
   - **Processor base costs follow configurable business logic patterns (per execution, per run, etc.)**

2. **Cost Configuration**
   - Store API costs in configuration files or database
   - Version control cost changes
   - Support environment-specific pricing
   - Configuration files can be overridden by database pricing

#### Cost Optimization Strategies
1. **Batch Processing**
   - Reduce number of external service requests
   - Implement request batching where supported
   - Optimize for bulk operations

2. **Smart Retry Logic**
   - Implement exponential backoff for retries
   - Track costs for each retry attempt
   - Set maximum retry limits to control costs

3. **Resource Management**
   - Monitor API rate limits
   - Implement circuit breakers for failing services
   - Use connection pooling for external APIs
   - Optimize memory usage for large datasets

## Monitoring and Analytics

#### Cost Metrics
- Total Cost per Run: Sum of base cost + tracked costs
- Cost per Service: Breakdown by external service
- Cache Hit Rate: Percentage of requests served from cache
- Cost Savings: Amount saved through caching
- Average Cost per Operation: Cost efficiency metrics

#### Cost Alerts
- Budget Thresholds: Alert when costs exceed limits
- Unusual Spending: Detect unexpected cost spikes
- Cache Performance: Monitor cache hit rates
- API Usage: Track external API consumption

## Error Handling

#### Failed API Call Process
1. **Initial API Call**
   - Track cost: $0.50 (first attempt)
   - Make HTTP request to external service
   - Handle timeout or connection error
   - Exception occurs: Processing execution ENDS

2. **Retry Execution (New Instance)**
   - New processor instance created
   - Track cost: $0.50 (retry attempt)
   - Make second HTTP request
   - Handle response or error

3. **Final Retry Execution**
   - New processor instance created
   - Track cost: $0.50 (final attempt)
   - Make third HTTP request
   - If still fails: raise exception

4. **Cost Accumulation**
   - Total cost: $1.50 (3 separate executions)
   - Each execution tracks its own costs
   - Metadata includes execution attempt number
   - Billing system receives cumulative costs

#### Cost Tracking Failure Process
1. **Tracking System Failure**
   - Cost tracking operation fails
   - Log error to monitoring system
   - Continue processor execution
   - Don't block main processing flow

2. **Fallback Behavior**
   - Use default cost values
   - Log missing cost information
   - Alert monitoring system
   - Maintain execution continuity

3. **Recovery Process**
   - Retry cost tracking operation
   - Update cost breakdown if successful
   - Maintain audit trail of failures
   - Ensure billing accuracy

This implementation provides a robust, database-driven cost tracking system that optimizes costs through caching while providing detailed cost breakdowns for monitoring and billing purposes.
This implementation provides a robust, database-driven cost tracking system that optimizes costs through caching while providing detailed cost breakdowns for monitoring and billing purposes.
