# Processor Execution Logic: v1 to v2 Changes

This document outlines the comprehensive changes made between v1 and v2 of the processor execution system.

---

## Overview of Changes

The v2 system represents a significant evolution from v1, introducing configurable execution strategies, improved retry logic, and enhanced error handling capabilities.

**Note:** This v2 implementation does not yet tackle manual triggers of processes - it focuses on the core execution engine improvements.

---

## 1) Architecture Changes

### v1 Architecture
- **Single-threaded execution only**
- **Single input processing** (one ProcessorInput at a time, but accepts both single input and list)
- **Basic retry logic** with limited step skipping - treats entire input list as single unit
- **Simple error handling** with basic error responses
- **Manual context management** for retry scenarios
- **No partial processing** - if any input fails, entire batch fails and retries

### v2 Architecture
- **Configurable execution strategies** via Runner system
- **Multiple input processing** (list of ProcessorInput objects)
- **Intelligent retry logic** with smart step skipping per individual input
- **Comprehensive error handling** with detailed error tracking
- **Automatic context merging** for retry scenarios
- **Partial processing support** - individual inputs can succeed/fail independently

---

## 2) Core Component Changes

### BaseProcessor Changes

| Aspect | v1 | v2 |
|--------|----|----|
| **Constructor** | `__init__(underwriting_id: str)` | `__init__(account_id: str, underwriting_id: str, runner: Runner)` |
| **Input Processing** | Single `ProcessorInput` or List (treated as one batch) | List of `ProcessorInput` objects |
| **Execution Strategy** | Sequential only | Configurable via Runner |
| **Pipeline Steps** | 4 steps (dependency, validation, processing, extraction) | 3-step pipeline + pre/post processing (input prevalidation → [validation, processing, extraction] → result aggregation) |
| **Error Handling** | Basic error responses | Detailed error tracking with payloads |
| **Hash Checking** | Hash-based change detection | Removed hash checking - No input change detection |
| **Result Aggregation** | Always aggregates results | Conditional aggregation - only when all inputs succeed |

### New Components in v2

#### Runner System
```python
# v2 introduces configurable execution strategies
class Runner(ABC):
    @abstractmethod
    def run(self, func: Callable, inputs: Iterable[Any]) -> list[dict[str, Any]]

class SequentialRunner(Runner):  # Sequential execution
class ThreadRunner(Runner):      # Multi-threaded execution
class ProcessRunner(Runner):     # Multi-process execution
```

#### Enhanced ProcessingResult
```python
# v2 ProcessingResult with additional fields
@dataclass
class ProcessingResult:
    run_id: str
    account_id: str  # New in v2
    underwriting_id: str
    output: list[dict[str, str]]  # Changed from dict to list
    success: bool
    context: ExecutionContext
    timestamp: datetime
    duration: int
    error: dict[str, str] | None
     payloads: dict[str, ProcessorInput] | None  # New in v2 - dict with input_id as key, ProcessorInput as value
```

---

## 3) Retry Logic Changes

### v1 Retry Logic
- **Batch-level retry**: Treats entire input list as single unit
- **All-or-nothing**: If any input fails, entire batch fails and retries
- **No partial success**: Cannot have some inputs succeed while others fail
- **Limited step skipping**: Basic resume from last error step for entire batch
- **Input hash comparison**: Uses single hash for entire input list

### v2 Retry Logic
- **Input-level retry**: Each input processed independently with its own retry logic
- **Partial processing**: Individual inputs can succeed/fail independently
- **Smart step skipping**: Each input resumes from its own failure point
- **Payload preservation**: Each input maintains its own retry payload
- **Granular error tracking**: Per-input error tracking and recovery

### Example: Retry Behavior Difference

**v1 Behavior:**
```
Input List: [doc1, doc2, doc3]
First run: doc1 → SUCCESS, doc2 → FAIL, doc3 → NOT PROCESSED (pipeline stops at doc2 failure)
Result: ENTIRE BATCH FAILS (all inputs retry together)
Retry: doc1 → validation → processing → extraction (reprocessed)
       doc2 → validation → processing → extraction (reprocessed)
       doc3 → validation → processing → extraction (first time processed)
```

**v2 Behavior:**
```
Input List: [doc1, doc2, doc3]
First run: doc1 → SUCCESS, doc2 → FAIL, doc3 → SUCCESS
Result: PARTIAL SUCCESS (only doc2 needs retry)
Retry: doc1 → SKIP (already successful)
       doc2 → validation → processing → extraction (resume from failure)
       doc3 → SKIP (already successful)
```

---

## 4) Execution Flow Changes

### v1 Execution Flow
```
Start → Dependency Check → Validation → Processing → Extraction → Result
```

### v2 Execution Flow
```
Start → Prevalidate Input List → Setup Fixed Pipeline → Use Configured Runner →
Process Each Input → Collect Results → Return Result
```

### Key Differences

| Aspect | v1 | v2 |
|--------|----|----|
| **Input Handling** | Single input or list (treated as batch) | List of inputs (individual processing) |
| **Dependency Check** | Built into pipeline | Removed (handled separately) |
| **Execution Strategy** | Sequential only | Configurable via Runner |
| **Parallel Processing** | Not supported | Supported via ThreadRunner/ProcessRunner |
| **Error Isolation** | Single failure stops all | Each input processed independently |

---

## 4) Retry Logic Changes

### v1 Retry Logic
- **Context-based retry** using ExecutionContext
- **Limited step skipping** (basic resume from last error step)
- **Manual context management** required
- **Hash-based input change detection**

### v2 Retry Logic
- **Payload-based retry** using ProcessorInput.payload
- **Intelligent step skipping** based on failed step
- **Automatic context merging** during execution
- **Individual input retry** (each input can have different resume points)
- **ExecutionContext.previous_run_id** indicates if this is a retry attempt

### Retry Behavior Comparison

| Scenario | v1 Behavior | v2 Behavior |
|----------|-------------|-------------|
| **Validation Failure** | Retry from validation | Retry from validation |
| **Processing Failure** | Retry from validation | Retry from processing (skip validation) |
| **Extraction Failure** | Retry from validation | Retry from extraction (skip validation & processing) |
| **Multiple Inputs** | All inputs retry together | Each input retries independently |
| **Context Management** | Manual context passing | Automatic context merging |

---

## 5) Error Handling Changes

### v1 Error Handling
```python
# Basic error response
{
    "step": "validation",
    "exception": "ValidationError",
    "message": "Invalid input",
    "payload": "current_state"
}
```

### v2 Error Handling
```python
# Enhanced error response with input tracking
{
    "input_id": "doc_123",
    "success": false,
    "step": "validation",
    "exception": "ValidationError",
    "message": "Invalid input",
    "payload": {
        "step": "validation",
        "exception": "ValidationError",
        "message": "Invalid input",
        "data": "current_state"
    }
}
```

### Error Handling Improvements

| Aspect | v1 | v2 |
|--------|----|----|
| **Error Tracking** | Basic step tracking | Detailed input-level tracking |
| **Error Isolation** | Single error stops execution | Individual input errors tracked |
| **Payload Preservation** | Basic payload storage | Enhanced payload with metadata |
| **Retry Information** | Limited retry context | Comprehensive retry metadata |

---

## 6) API Changes

### Constructor Changes
```python
# v1
processor = MyProcessor(underwriting_id="uw_123")

# v2
processor = MyProcessor(
    account_id="acc_123",
    underwriting_id="uw_123",
    runner=SequentialRunner()  # or ThreadRunner(), ProcessRunner()
)
```

### Execute Method Changes
```python
# v1 - accepts single ProcessorInput or list (treated as one batch)
result = processor.execute(data=ProcessorInput(...), context=ExecutionContext(...))
result = processor.execute(data=[ProcessorInput(...), ProcessorInput(...)], context=ExecutionContext(...))

# v2 - specifically expects list of ProcessorInput objects
result = processor.execute(data=[ProcessorInput(...), ProcessorInput(...)], context=ExecutionContext(...))
```

### Result Structure Changes
```python
# v1 ProcessingResult
{
    "underwriting_id": "uw_123",
    "run_id": "run_456",
    "processor_name": "p_my_processor",
    "extraction_output": {...},
    "success": true,
    "context": {...},
    "timestamp": "2025-01-01T00:00:00",
    "duration": 1000
}

# v2 ProcessingResult
{
    "run_id": "run_456",
    "account_id": "acc_123",      # New
    "underwriting_id": "uw_123",
    "output": [...],              # Changed from dict to list
    "success": true,
    "context": {...},
    "timestamp": "2025-01-01T00:00:00",
    "duration": 1000,
    "error": null,
    "payloads": null              # New
}
```

---

## 7) Performance Improvements

### v1 Performance Characteristics
- **Single-threaded execution** only
- **Sequential processing** of all operations
- **No parallel processing** capabilities
- **Limited scalability** for large datasets

### v2 Performance Improvements
- **Configurable execution strategies** (Sequential, Thread, Process)
- **Parallel processing** support via ThreadRunner and ProcessRunner
- **Better resource utilization** for I/O-bound and CPU-bound tasks
- **Improved scalability** for large datasets

### Performance Comparison

| Workload Type | v1 Performance | v2 Performance |
|---------------|----------------|----------------|
| **I/O-bound tasks** | Poor (sequential) | Good (ThreadRunner) |
| **CPU-bound tasks** | Poor (sequential) | Excellent (ProcessRunner) |
| **Small datasets** | Good | Good (SequentialRunner) |
| **Large datasets** | Poor | Excellent (ProcessRunner) |
| **Mixed workloads** | Poor | Good (configurable runners) |

---

## 8) Benefits of v2

### Developer Benefits
- **Configurable execution strategies** for different workload types
- **Better error handling** with detailed input-level tracking
- **Improved debugging** with comprehensive error metadata
- **Parallel processing** capabilities for better performance

### System Benefits
- **Better resource utilization** through configurable runners
- **Improved scalability** for large datasets
- **Enhanced reliability** with intelligent retry logic
- **Better observability** with detailed execution tracking

### Operational Benefits
- **Reduced processing time** for I/O-bound and CPU-bound tasks
- **Better error recovery** with smart step skipping
- **Improved monitoring** with detailed execution metrics
- **Enhanced maintainability** with cleaner separation of concerns

---

## 9) Summary

The v2 processor execution system represents a significant improvement over v1, providing:

- **Configurable execution strategies** via the Runner system
- **Multiple input processing** with individual error tracking
- **Intelligent retry logic** with smart step skipping
- **Enhanced error handling** with comprehensive metadata
- **Better performance** through parallel processing capabilities
- **Improved developer experience** with cleaner APIs and better debugging

While v2 requires migration from v1, the benefits in terms of performance, reliability, and maintainability make it a worthwhile upgrade for any processor implementation.
