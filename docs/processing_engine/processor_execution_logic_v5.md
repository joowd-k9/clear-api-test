# Processor Execution Logic

**Applies to:** `BaseProcessor` abstract class and all implementing processor subclasses.

**Purpose:** Define how a processor run is executed with configurable execution strategies and comprehensive error handling.

> ⚠️ NOTE: This document covers only the core execution engine for individual processors. It does NOT include orchestration, manual triggers, external API handling logic, or factor management systems.
>

---

# 1) Key Responsibilities

## Base Processor Class

- Emit lifecycle events (`prcessors.execution.started|completed|failed`) to Pub/Sub
- Determine eligibility to execute (check triggers against input; skip if not satisfied)
- Input prevalidation checking if document is of correct type and exists
- Execute the 3‑phase pipeline
    - pre‑extraction
    - extraction
    - post-extraction
- Coordinate the pipeline and enforce atomic success/failure semantics
- Summarize processing cost
- Error handling
- Data Persistence
    - inserting `processing_execution` record
    - inserting and overwriting `factors` records
    - optionally updating `application fields` when necessary

## Concrete Processor Subclass

- Define `PROCESSOR_NAME` and any `PROCESSOR_TRIGGERS`
- Transform input data when needed
    - document splicing
    - chunking large payloads
    - normalization
    - pulling supplementary data from db
- Validate transformed data and inputs for processor-specific requirements
- Implement extraction logic to produce factors from validated inputs
- Aggregate and validate outputs
    - map to canonical factor keys
    - optionally populate application fields
- Track processing costs as applicable
    - (per execution, per page, or per api call)
- Raise domain specific exceptions on failure
    - `InputValidationError`
    - `DataTransformationError`
    - `FactorExtractionError`
    - `ResultAggregationError`
    - `ResultValidationError`
    - `ApiError`
    - etcetera

---

# 2) Event Dispatching

## Overview

The `BaseProcessor` provides event dispatching capabilities to communicate processor execution status across different system layers.

## Event Dispatching Interface

The base class provides emit method for event communication:

```python
class BaseProcessor:
    def emit(
	    self,
	    data: dict[str, Any],
	    event: str,
	    target: list[str]|str = 'pubsub'
	  ) -> None:
        """
        Emit events to specified system layer.

        Args:
            data: Event payload
            event: Event name
            target: Target layer
        """

```

## Major Lifecycle Events

**Handled by the base class** - no implementation required. These events are automatically sent to `PubSub` layer:

| Event | Description | Trigger | Target |
| --- | --- | --- | --- |
| `{p_id}.execution.started` | Processor execution started | At the start of execution | `pubsub` |
| `{p_id}.execution.completed` | Processor execution succeeds | After successful completion of all phases | `pubsub` |
| `{p_id}.execution.failed` | Processor execution fails | On any phase failure | `pubsub` |

**Event Flow**:

- Publishes to `Google Cloud PubSub` topics for system integration
- Triggers downstream processors and workflows
- Enables system-wide event coordination

---

# 3) Cost Tracking

## Overview

The `BaseProcessor` provides cost tracking capabilities to monitor processing costs during execution.

## Cost Tracking Interface

The base class provides a cost tracking method:

```python
class BaseProcessor:
    def __init__(self):
        self._total_cost: float = 0.0  # Track accumulated costs

    def _add_cost(self, cost: float) -> None:
        """
        Add cost for an operation during processing.

        This method adds the cost to the internal _total_cost attribute.

        Args:
            cost: Cost amount to add to the total
        """
        self._total_cost += cost

```

## Cost Calculation Flow

- **During Processing**: Track individual operation costs using `_add_cost(cost)`
- **Cost Accumulation**: Each call to `_add_cost(cost)` adds the cost to `self._total_cost`
- **Access Total**: Use `self._total_cost` directly to get the accumulated total
- **Result Integration**: Total cost information is included in the `ProcessingResult`

---

# 4) Execution Pipeline

## Core Principle: Atomic Execution

The processor execution framework implements atomic transaction semantics:

- **Atomic Success**: Complete processing of all inputs constitutes a successful execution
- **Atomic Failure**: Any input processing failure results in complete execution termination
- **Consistent State**: The system maintains transactional integrity with no partial success states in the final output

## Execution Flow

The processor has a 3-phase execution structure with runners handling the extraction phase:

```
pre-extraction phase → [extraction phase] → post-extraction phase

```

## Execution Phases

| Phase | Description |
| --- | --- |
| **Pre-extraction Phase** | Input prevalidation, transformation, and input validation |
| **Extraction Phase** | Extraction step (executed by runners) |
| **Post-extraction Phase** | Result aggregation and result validation |

## Phase Responsibilities

## Pre-extraction Phase

- **Input Pre-validation**:
    - Checks if prerequisite document exists
    - Check if stipulation is of correct type
- **Input Transformation**: Transform and normalize input data before validation
- **Input Validation**: Input validation and structure verification

```mermaid
graph TD
    P0[Start Pre-extraction] --> P1[Prevalidate Input List]
    P1 --> P2[Transform Input Data]
    P2 --> P3[Validate All Inputs]
    P3 -->|All valid| P4[Proceed to Extraction]
    P3 -->|Any invalid| P5[FAIL - Return Error]
    P4 --> P6[End Pre-extraction]
    P5 --> P6

```

## Extraction Phase

- **Extraction**: Factor extraction and result formatting
- **Complete Processing**: All inputs must succeed or the entire execution fails
- **Runner Execution**: Parallel processing of validated inputs

```mermaid
graph TD
    E0[Start Extraction] --> E1[Runner Processes Each Input]
    E1 --> E2{All Inputs Success?}
    E2 -->|Yes| E3[Proceed to Post-extraction]
    E2 -->|No| E4[FAIL - Return Error]
    E3 --> E5[End Extraction]
    E4 --> E5

```

## Post-extraction Phase

- **Result Aggregation**: Merges the output factors from each input into a single result set
- **Result Validation**: Ensures all results are consistent and complete
- **Database Persistence**: Store execution record and factors in the operational DB
- **Complete Success**: Only returns success if all phases completed successfully

```mermaid
graph TD
    S0[Start Post-extraction] --> S1[Aggregate Results]
    S1 --> S2[Validate Aggregated Results]
    S2 --> S3{Results Valid?}
    S3 -->|Yes| S4[Persist to Database]
    S3 -->|No| S6[FAIL - Return Error]
    S4 --> S5[SUCCESS - Return Results]
    S5 --> S7[End Post-extraction]
    S6 --> S7

```

## Execution Flow

```mermaid
graph TD
    A[Start] --> B[Pre-extraction Phase]
    B --> C[Extraction Phase]
    C --> D[Post-extraction Phase]
    D --> E[End]

```

The processor execution follows these linear steps:

1. **Start** - Begin processing
2. **Execute** - Execute the processor
    1. **Pre-validate Input List** - Check prerequisite document existence and `underwriting_id` then return validated processor input's data
    2. **Transform Input Data** - Transform and normalize input data before validation
    3. **Validate All Inputs** - Input validation and structure verification
    4. **Check: All Inputs Valid?** - If any input fails input validation, entire execution fails
    5. **Runner Processes Each Input** - Execute factor extraction step on each input
    6. **Check: All Inputs Success?** - If any input fails, entire execution fails
    7. **Aggregate Results** - Merge output factors from all inputs
    8. **Result Validation** - Ensure aggregated results are consistent
    9. **Check: Results Valid?** - Result validation before success
    10. **Persist Results** - Save execution record and factors; optional application updates
    11. **Return Processing Result** - Return result with aggregated output or error
3. **End** - Processing complete

## Input Processing Strategy

The **3-Phase Execution** processes multiple input items as follows:

1. **Input List**: The processor receives a list of input items (documents, records)
2. **Pre-extraction Phase**: All inputs are pre-validated and input validated. **If any input fails, the entire execution fails immediately**
3. **Extraction Phase**: The runner takes each validated input and applies the factor extraction function. **If any input fails, the entire execution fails**
4. **Post-extraction Phase**: The `BaseProcessor` aggregates results and performs result validation. **If aggregation fails, the entire execution fails**

---

# 5) Database Persistence (Post-processing)

## Persistence steps

1. Insert `processing_execution` with `status`, timestamps (`started_at`/`completed_at`), `duration`, `processor_name`, and `run_cost_cents`.
2. Upsert factors: for each `factor_key`, set previous `is_current = FALSE` and insert a new `factor` row with `value`, optional `unit`, `source = 'processor'`, and `execution_id`.
3. Optionally update application fields (e.g., `merchant.industry`) when confidently derived.
4. Commit the transaction; on error, rollback and mark the execution as `failed`.

---

# 6) Concurrent Processing

The `BaseProcessor` provides configurable concurrent processing options for multiple inputs, allowing developers to choose between sequential and parallel execution strategies.

## Available Processing Strategies

### 1. `DefaultRunner`

- **Strategy**: Sequential processing (one input at a time)
- **Use Case**: Default for simple operations

### 2. `ThreadRunner`

- **Strategy**: Concurrent processing (multiple inputs in parallel)
- **Use Case**: When you want faster processing through thread based parallelism

## Example Use cases

The following are example use cases of running concurrency.

### CLEAR Person Search (Owner-level parallelism)

This example demonstrates concurrent processing where each owner is processed in a separate thread.

**High-level flow**

1. Transform application data from orchestration into an owners list of two items
2. Validate required fields (EIN format, ISO country code, name/DOB presence)
3. Extraction (runner): For each owner, call CLEAR Person Search API and extract factors in parallel
4. Aggregate the two result sets and validate the combined result
5. Persist execution and factors, then update the document/application fields

**Flowchart**

```mermaid
graph TD
    A[Start] --> T1["Transform application → owners list (2)"]
    T1 --> V1["Validate owner fields (EIN, country code, name, DOB)"]
    V1 -->|All valid| X1[Extraction - ThreadRunner]
    V1 -->|Invalid| F[FAIL]

    subgraph ThreadRunner
        direction LR
        X1 --> OA[Owner A: call CLEAR Person Search, extract factors]
        X1 --> OB[Owner B: call CLEAR Person Search, extract factors]
    end

    OA --> AGG[Aggregate owner results]
    OB --> AGG
    AGG --> RV[Validate aggregated results]
    RV -->|Valid| P[Persist execution + factors, update document]
    RV -->|Invalid| F
    P --> S[SUCCESS]
    S --> E[End]
    F --> E

```

**Why threads here?**

- Owner-level calls are independent I/O-bound API requests; `ThreadRunner` reduces wall-clock time by running them concurrently.

### Bank Statements (Monthly chunk parallelism)

This example demonstrates concurrent processing where each month-bucket of a bank statement is processed in parallel.

**High-level flow**

1. Transform the uploaded bank statement into monthly chunks (splice by statement period)
2. Validate each chunk (dates align, pages complete, no duplicate transactions)
3. Extraction (runner): Per month, compute credits/debits, NSF counts, average daily balance, volatility
4. Aggregate across months (3/6/12-month averages, trend, seasonality)
5. Persist execution and factors, then update document/application fields

**Flowchart**

```mermaid
graph TD
    A[Start] --> T1["Transform bank statement → split by month buckets"]
    T1 --> V1["Validate each month chunk (dates, completeness, duplicates)"]
    V1 -->|All valid| X1[Extraction - ThreadRunner]
    V1 -->|Invalid| F[FAIL]

    subgraph ThreadRunner
        direction LR
        X1 --> M1[Month 1: compute credits/debits, NSFs, avg daily balance]
        X1 --> M2[Month 2: compute credits/debits, NSFs, avg daily balance]
        X1 --> MN[Month N: compute credits/debits, NSFs, avg daily balance]
    end

    M1 --> AGG[Aggregate across months]
    M2 --> AGG
    MN --> AGG

    AGG --> RV["Validate aggregated results (3/6/12-mo avg, trend, volatility)"]
    RV -->|Valid| P[Persist execution + factors, update document]
    RV -->|Invalid| F
    P --> S[SUCCESS]
    S --> E[End]
    F --> E

```

**Why threads here?**

- Month-level calculations are independent and I/O/CPU-light per chunk; `ThreadRunner` speeds up wall-clock time while maintaining atomic success semantics.

---

# 7) Error Handling

## Processor Execution Exception Types

The system throws specific exceptions for different processor execution phases and error scenarios:

## Pre-extraction Phase Exceptions

- **`PrevalidationError`**: General pre-validation failures
- **`InputValidationError`**: Input validation failures (invalid format, missing required fields)
- **`TransformationError`**: Input transformation failures (data conversion, normalization errors)

## Extraction Phase Exceptions

- **`FactorExtractionError`**: General extraction failures
- **`ApiError`**: External API call failures (network, authentication, rate limiting)

## Post-extraction Phase Exceptions

- **`ResultAggregationError`**: Result collection and aggregation failures
- **`ResultValidationError`**: Result validation failures

## Error Handling

**Failure Behavior**

All failures result in complete execution failure will immediately the stop execution at first failure point.
