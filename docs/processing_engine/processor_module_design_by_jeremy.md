# Processor Module - High-Level Design

## What is the Processor Module?

The **Processor Module** is a coordinator that sits between the Orchestrator and individual processors. When the Orchestrator says "process this underwriting," the Processor Module figures out which processors to run and executes them.

```
Orchestrator → "Hey, process underwriting_123"
                      ↓
              Processor Module
              (figures everything out)
                      ↓
        Runs: [BankStatement, CreditCheck, BusinessVerification]
                      ↓
              Returns: factors extracted

```

---

## Core Responsibilities

1. **Receive event** from Orchestrator (CREATE/UPDATE/DELETE)
2. **Determine eligible processors** (purchased + triggered)
3. **Execute processors** (in parallel)
4. **Aggregate results** into factors
5. **Save factors** to database
6. **Return result** to Orchestrator

That's it. Keep it simple.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────┐
│         Processor Module                    │
│                                             │
│  ┌────────────────────────────────────┐   │
│  │  1. Event Handler                  │   │
│  │     - Receives CREATE/UPDATE/DELETE │   │
│  │     - Delegates to right handler    │   │
│  └─────────────┬──────────────────────┘   │
│                ↓                            │
│  ┌────────────────────────────────────┐   │
│  │  2. Processor Selector             │   │
│  │     - Check purchased processors    │   │
│  │     - Check triggers match          │   │
│  │     - Return list to execute        │   │
│  └─────────────┬──────────────────────┘   │
│                ↓                            │
│  ┌────────────────────────────────────┐   │
│  │  3. Execution Engine               │   │
│  │     - Run processors (parallel)     │   │
│  │     - Handle failures gracefully    │   │
│  │     - Save execution records        │   │
│  └─────────────┬──────────────────────┘   │
│                ↓                            │
│  ┌────────────────────────────────────┐   │
│  │  4. Factor Aggregator              │   │
│  │     - Combine processor outputs     │   │
│  │     - Resolve conflicts             │   │
│  │     - Create/update factors         │   │
│  └────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

```

---

## Component Breakdown

### 1. Event Handler

**Purpose:** Route incoming events to the right logic.

**Logic:**

```
handle_event(event):
    if event.type == "CREATE":
        return handle_create(event)
    elif event.type == "UPDATE":
        return handle_update(event)
    elif event.type == "DELETE":
        return handle_delete(event)

```

Simple if/else. No fancy patterns needed.

---

### 2. Processor Selector

**Purpose:** Decide which processors should run.

**Logic:**

```
select_processors(event):
    # Step 1: Get purchased processors
    purchased = query_database(
        "SELECT processor_id FROM user_processor_subscriptions
         WHERE tenant_id = ? AND enabled = true",
        event.tenant_id
    )

    # Step 2: Filter by triggers
    eligible = []
    for processor_id in purchased:
        triggers = get_processor_triggers(processor_id)
        if matches_any_trigger(triggers, event):
            eligible.append(processor_id)

    return eligible

matches_any_trigger(triggers, event):
    for trigger in triggers:
        if trigger starts with "s_":
            # Document trigger
            if trigger in event.documents_list:
                return true
        else:
            # Form field trigger (e.g., "merchant.ein")
            if has_form_field(trigger, event.application_form):
                return true
    return false

```

**Key Decision:** Use simple loop with if/else. No need for complex pattern matching.

---

### 3. Execution Engine

**Purpose:** Run processors and handle failures.

**Logic:**

```
execute_processors(processor_ids, event):
    results = []

    # Run in parallel using thread pool
    with ThreadPool(max_workers=10):
        for processor_id in processor_ids:
            processor = get_processor_instance(processor_id)
            result = thread_pool.submit(processor.execute, event)
            results.append(result)

    # Wait for all to complete
    completed_results = wait_for_all(results)

    # Save execution records
    for result in completed_results:
        save_execution_record(result)

    return completed_results

```

**Key Decisions:**

- Use thread pool for parallelism (processors are I/O-bound)
- Don't fail entire batch if one processor fails
- Save all execution records (success or failure)

---

### 4. Factor Aggregator

**Purpose:** Turn processor outputs into factors.

**Logic:**

```
aggregate_factors(execution_results, underwriting_id):
    # Get all active executions for this underwriting
    all_executions = get_active_executions(underwriting_id)

    # Merge with new results
    all_executions = merge(all_executions, execution_results)

    # Group by processor
    by_processor = group_by_processor_id(all_executions)

    # Extract factors from each processor's outputs
    factors = {}
    for processor_id, executions in by_processor:
        processor_factors = extract_factors(processor_id, executions)
        factors.update(processor_factors)

    # Save to database
    save_factors(underwriting_id, factors)

    return factors

extract_factors(processor_id, executions):
    # Example: Bank statement processor
    if processor_id == "bank_statement":
        all_revenues = [exec.output.monthly_revenue for exec in executions]
        return {
            "revenue_monthly_avg": average(all_revenues),
            "revenue_monthly_min": min(all_revenues),
            "revenue_monthly_max": max(all_revenues)
        }

    # Each processor defines how to aggregate its own outputs
    return processor.aggregate(executions)

```

**Key Decision:** Each processor knows how to aggregate its own outputs. No complex aggregation framework needed.

---

## Three Scenarios Explained

### Scenario 1: CREATE (New Application)

**What happens:**

```
1. Orchestrator → "New application created"
2. Processor Module:
   a. Query: Which processors did user purchase?
   b. Check: Which purchased processors have matching triggers?
   c. Execute: Run all eligible processors in parallel
   d. Aggregate: Combine outputs into factors
   e. Save: Write factors to database
3. Return → Status + list of executed processors

```

**Example:**

```
Input:
  - Business EIN: 12-3456789
  - Owner SSN: 123-45-6789
  - Documents: 3 bank statements, 1 driver's license

Processing:
  - Purchased: [bank_statement, credit_check, business_verification, drivers_license]
  - Triggered: All 4 (all have matching data)
  - Execute: All 4 run in parallel
  - Results: All succeed

Output:
  - Factors: revenue_monthly, credit_score, business_name, identity_verified
  - Status: SUCCESS

```

---

### Scenario 2: UPDATE (Application Changed)

**What happens:**

```
1. Orchestrator → "Application updated (SSN corrected, Month 4 added)"
2. Processor Module:
   a. Query: Which processors did user purchase?
   b. Check: Which are triggered by available data?
   c. Smart check: Did inputs actually change for each processor?
   d. Execute: Only re-run if inputs changed or previous failed
   e. Aggregate: Combine new + old execution results
   f. Save: Update factors
3. Return → Status + what was re-run + what was reused

```

**Example:**

```
Input (UPDATE):
  - Owner SSN changed: 123-45-6789 → 123-45-6788 (typo fix)
  - New document: Bank statement Month 4

Previous executions:
  - bank_statement (Months 1-3): SUCCESS
  - credit_check: SUCCESS
  - business_verification: SUCCESS

Processing:
  1. Check credit_check inputs:
     - Old: SSN = 123-45-6789
     - New: SSN = 123-45-6788
     - Decision: CHANGED → Re-run

  2. Check bank_statement inputs:
     - Old: Documents [doc_1, doc_2, doc_3]
     - New: Documents [doc_1, doc_2, doc_3, doc_4]
     - Decision: CHANGED → Re-run

  3. Check business_verification inputs:
     - Old: EIN = 12-3456789
     - New: EIN = 12-3456789
     - Decision: UNCHANGED → Reuse old execution

Output:
  - Re-run: credit_check, bank_statement
  - Reused: business_verification
  - Factors updated: credit_score, revenue_monthly

```

**How to detect "inputs changed"?**

```
compute_input_hash(processor_id, event):
    triggers = get_triggers(processor_id)
    inputs = []

    for trigger in triggers:
        if trigger is document type:
            # Hash: document IDs (or revision IDs)
            docs = event.documents_list[trigger]
            inputs.append(sorted(docs))
        else:
            # Hash: form field values
            value = get_form_field(trigger, event.application_form)
            inputs.append(value)

    return hash(inputs)

should_rerun(processor_id, event):
    new_hash = compute_input_hash(processor_id, event)
    old_execution = find_execution_by_hash(processor_id, new_hash)

    if old_execution exists and old_execution.status == "SUCCESS":
        return false  # Reuse old execution
    else:
        return true   # Re-run (inputs changed or previous failed)

```

---

### Scenario 3: DELETE (Document Removed)

**What happens:**

```
1. Orchestrator → "User deleted document doc_2"
2. Processor Module:
   a. Find: Which executions used doc_2?
   b. Invalidate: Mark those executions as invalid
   c. Check: Can processor still run with remaining documents?
   d. Execute: Re-run if minimum requirements met
   e. Aggregate: Recalculate factors without deleted data
   f. Save: Update factors
3. Return → Status + what was invalidated + new calculations

```

**Example:**

```
Input (DELETE):
  - Deleted: Bank statement Month 2 (doc_2)
  - Remaining: Months 1, 3, 4 (doc_1, doc_3, doc_4)

Previous execution:
  - bank_statement used documents: [doc_1, doc_2, doc_3]
  - Status: SUCCESS

Processing:
  1. Find executions using doc_2:
     - Found: bank_statement execution (exec_123)

  2. Mark exec_123 as invalid

  3. Check if can re-run:
     - Remaining documents: [doc_1, doc_3, doc_4] = 3 documents
     - Minimum requirement: 3 documents
     - Decision: YES, re-run

  4. Execute bank_statement with [doc_1, doc_3, doc_4]

  5. Recalculate factors

Output:
  - Invalidated: exec_123
  - Re-run: bank_statement (new execution)
  - Factors updated: revenue_monthly (recalculated with 3 months)

```

**What if remaining data doesn't meet minimum?**

```
check_can_rerun(processor_id, remaining_docs):
    min_required = get_minimum_documents(processor_id)

    if len(remaining_docs) >= min_required:
        return true  # Can re-run
    else:
        # Mark as incomplete, don't re-run
        mark_processor_incomplete(processor_id)
        return false

```

---

## Data Flow

### CREATE Flow

```
Event
  ↓
[Select Processors]
  - Query purchased processors
  - Filter by triggers
  ↓
[Execute]
  - Run all in parallel
  - Save execution records
  ↓
[Aggregate]
  - Extract factors from outputs
  - Save factors
  ↓
Result

```

### UPDATE Flow

```
Event
  ↓
[Select Processors]
  - Query purchased processors
  - Filter by triggers
  ↓
[Smart Check]
  - For each processor:
    - Compute input hash
    - Compare with previous execution
    - Decide: rerun or reuse
  ↓
[Execute]
  - Run only changed processors
  - Reactivate unchanged processors
  - Save execution records
  ↓
[Aggregate]
  - Combine new + old executions
  - Update factors
  ↓
Result

```

### DELETE Flow

```
Event
  ↓
[Find Affected]
  - Query executions using deleted documents
  ↓
[Invalidate]
  - Mark affected executions as invalid
  ↓
[Check Requirements]
  - For each affected processor:
    - Count remaining documents
    - Check if meets minimum
  ↓
[Execute]
  - Re-run if requirements met
  - Skip if not enough data
  - Save execution records
  ↓
[Aggregate]
  - Recalculate factors without deleted data
  ↓
Result

```

---

## Database Schema

### Tables Needed

**1. processing_executions**

```
id                  (primary key)
processor_id        (which processor)
underwriting_id     (which underwriting)
status              (SUCCESS, FAILED, PENDING)
input_hash          (hash of inputs used)
documents_used      (array of document IDs)
output              (JSON - processor-specific results)
error_message       (if failed)
created_at          (timestamp)
is_active           (boolean - false if superseded/invalidated)

```

**2. factors**

```
id                  (primary key)
underwriting_id     (which underwriting)
key                 (factor name, e.g., "revenue_monthly")
value               (JSON - factor value)
source_processor    (which processor created it)
created_at          (timestamp)
updated_at          (timestamp)

```

**3. user_processor_subscriptions**

```
id                  (primary key)
tenant_id           (which organization)
processor_id        (which processor)
enabled             (boolean)
custom_config       (JSON - optional customization)

```

**4. processor_config** (optional - can be in code)

```
processor_id        (primary key)
triggers            (array - what makes it eligible)
min_documents       (int - minimum docs required)
timeout_seconds     (int - execution timeout)

```

---

## Key Design Decisions

### 1. Parallel Execution

**Decision:** Use thread pool to run processors in parallel.

**Why:**

- Processors are I/O-bound (reading documents, calling APIs)
- Independent (no dependencies between processors)
- Faster overall processing time

**Implementation:**

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(run_processor, p) for p in processors]
    results = [f.result() for f in futures]

```

---

### 2. Partial Failure Tolerance

**Decision:** Don't fail entire underwriting if one processor fails.

**Why:**

- User might have uploaded valid data for most processors
- Can show partial results and clear feedback on what failed
- User can fix and retry only failed processor

**Example:**

```
5 processors run:
  ✅ bank_statement: SUCCESS
  ✅ business_verification: SUCCESS
  ❌ credit_check: FAILED (API timeout)
  ✅ drivers_license: SUCCESS
  ✅ tax_return: SUCCESS

Result: PARTIAL SUCCESS
  - 4 processors succeeded
  - 1 processor failed (retryable)
  - Factors extracted from 4 successful processors
  - Clear message: "Credit check failed due to API timeout. Please retry."

```

---

### 3. Smart Re-processing (Hash-Based)

**Decision:** Use input hashing to avoid redundant processing.

**Why:**

- Save API costs (don't re-call expensive credit bureau APIs)
- Save processing time
- Reuse valid results when inputs haven't changed

**How it works:**

```
UPDATE event arrives:
  1. For each eligible processor:
     - Compute hash of current inputs
     - Look up: Do we have a successful execution with this hash?

  2. If YES → Reuse old execution (mark as active)
  3. If NO → Run processor (inputs changed or no previous success)

```

**Hash includes:**

- Document IDs (or revision IDs) for document-based processors
- Form field values for form-based processors

---

### 4. Factor Aggregation Strategy

**Decision:** Each processor defines its own aggregation logic.

**Why:**

- Bank statements need averaging (revenue across months)
- Credit checks need latest value (most recent score)
- Different processors have different needs
- Keep it simple and flexible

**Example:**

```python
class BankStatementProcessor:
    def aggregate(self, executions):
        revenues = [e.output['monthly_revenue'] for e in executions]
        return {
            'revenue_monthly_avg': sum(revenues) / len(revenues),
            'revenue_monthly_min': min(revenues),
            'revenue_monthly_max': max(revenues)
        }

class CreditCheckProcessor:
    def aggregate(self, executions):
        # Just use the latest
        latest = max(executions, key=lambda e: e.created_at)
        return {
            'credit_score': latest.output['score']
        }

```

---

### 5. Execution History

**Decision:** Keep all execution records (never delete).

**Why:**

- Audit trail for compliance
- Can see what data was used for each decision
- Can reproduce results if needed
- Mark old executions as inactive rather than deleting

**Implementation:**

```
When UPDATE happens:
  1. Old execution stays in database
  2. Set is_active = false
  3. New execution created with is_active = true

When querying for factors:
  - Only use executions where is_active = true

```

---

## Error Handling

### Transient Errors (Retry)

```
execute_with_retry(processor, event):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return processor.execute(event)
        except APITimeout, NetworkError:
            if attempt < max_retries - 1:
                sleep(2^attempt)  # Exponential backoff
                continue
            else:
                return ExecutionResult(
                    status='FAILED',
                    error='API timeout after 3 retries',
                    retryable=true
                )

```

### Permanent Errors (No Retry)

```
execute_processor(processor, event):
    try:
        return processor.execute(event)
    except InvalidDocument, MissingData:
        return ExecutionResult(
            status='FAILED',
            error='PDF is corrupted',
            retryable=false
        )

```

### Result Structure

```
{
    "status": "PARTIAL",  // SUCCESS, PARTIAL, FAILED
    "executed_processors": ["bank_statement", "credit_check", "business_verification"],
    "successful": ["bank_statement", "business_verification"],
    "failed": [
        {
            "processor": "credit_check",
            "error": "API timeout",
            "retryable": true
        }
    ],
    "factors_updated": ["revenue_monthly", "business_name"],
    "execution_ids": {
        "bank_statement": "exec_123",
        "credit_check": "exec_124",
        "business_verification": "exec_125"
    }
}

```

---

## Configuration

### Processor Triggers (in code or config file)

```yaml
processors:
  bank_statement:
    triggers:
      - s_bank_statement
    min_documents: 3

  credit_check:
    triggers:
      - application_form.owners_list.ssn
    min_documents: 1

  business_verification:
    triggers:
      - application_form.merchant.ein
    min_documents: 1

```

### User Purchases (in database)

```sql
-- tenant_123 purchased these processors
INSERT INTO user_processor_subscriptions (tenant_id, processor_id, enabled)
VALUES
  ('tenant_123', 'bank_statement', true),
  ('tenant_123', 'credit_check', true),
  ('tenant_123', 'business_verification', false);  -- purchased but disabled

```

---

## Summary

The Processor Module is a simple coordinator with 4 main steps:

1. **Select** which processors to run (purchased + triggered)
2. **Execute** them in parallel (thread pool)
3. **Aggregate** outputs into factors (each processor defines how)
4. **Save** everything (execution records + factors)

**Three scenarios:**

- **CREATE**: Run all eligible processors
- **UPDATE**: Smart re-run (only if inputs changed)
- **DELETE**: Invalidate old executions, re-run with remaining data

**Key principles:**

- Keep it simple (no over-engineering)
- Partial failures OK (don't fail everything)
- Smart re-processing (save costs)
- Full audit trail (keep all executions)

**No fancy patterns needed.** Just straightforward logic with clear responsibilities.
