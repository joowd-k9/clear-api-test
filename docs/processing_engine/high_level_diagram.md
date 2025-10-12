## Processing Engine – High-Level Design

This document summarizes the core architecture and flows for the Processing Engine using the Processor Orchestrator and Processor Execution Logic (v5) as references.

### Core Components

- **Processor Orchestrator**: Subscribes to `underwriting.created` and `underwriting.updated`, normalizes payloads, evaluates `PROCESSOR_TRIGGERS`, and coordinates execution.
- **Processor Registry**: Maps processor names to concrete classes and resolves eligible/purchased processors.
- **BaseProcessor + Concrete Processors**: Implements v5 three‑phase execution (pre‑extraction → extraction → post‑extraction), event emission, cost tracking, and persistence.
- **Runners**: `DefaultRunner` (sequential) and `ThreadRunner` (parallel) for extraction concurrency.
- **Persistence Layer**: Stores `processing_execution` records and upserts `factors`.
- **Eventing**: Emits `{processor_id}.execution.started|completed|failed` to Pub/Sub.

### Architecture Overview

```mermaid
flowchart LR
    %% Layout: left-to-right for clarity

    subgraph PubSub["Pub/Sub"]
      UC["underwriting.created"]
      UU["underwriting.updated"]
    end

    subgraph Orchestrator["Processor Orchestrator"]
      N["Normalize payload<br/>- flatten application_form<br/>- dedupe documents_list"]
      F["Filter processors<br/>ANY-match against PROCESSOR_TRIGGERS"]
      X["Execute eligible processors<br/>in parallel"]
      AP["Aggregate results<br/>per processor"]
      C["Collect results<br/>status, factors, errors, timings"]
    end

    subgraph Registry["Processor Registry"]
      R["Resolve purchased/eligible<br/>processor classes"]
    end

    subgraph Runners["Runners"]
      DR["DefaultRunner (sequential)"]
      TR["ThreadRunner (parallel)"]
    end

    subgraph Processors["Processors"]
      PC1["Bank Statement Processor"]
      PC2["Driver's License Processor"]
      PC3["Business Credit Report Processor"]
      PC4["Other Processors..."]
    end

    subgraph Persistence["Operational DB"]
      PE[("processing_executions")]
      FA[("factors")]
    end

    %% Main flow
    PubSub --> N
    N --> F
    F -->|resolve| Registry
    Registry -->|classes| Processors
    F --> X
    X --> Runners
    X --> Processors
    Processors --> AP
    X --> AP
    AP --> C
    C --> PE
    C --> FA

    %% Feedback loop & eventing
    Processors -->|available| F
    C -->|publish *.execution.*| PubSub
```

### Orchestration Flow (Detailed)

```mermaid
sequenceDiagram
    participant PS as "Pub/Sub"
    participant OR as "Orchestrator"
    participant RG as "Registry"
    participant P as "Processor(s)"
    participant DB as "Operational DB"

    PS->>OR: Message (underwriting.created/updated)
    OR->>OR: Normalize payload (flatten fields, dedupe docs)
    OR->>RG: Get purchased processors
    RG-->>OR: Processor classes
    OR->>OR: Filter via PROCESSOR_TRIGGERS (ANY-match)
    OR->>P: Execute eligible processors (parallel where applicable)
    P-->>DB: Persist execution + factors (via BaseProcessor)
    P-->>OR: Return results (status, factors, errors, timings)
    OR-->>PS: Publish underwriting.processing.completed

```

### Processor Execution (v5) – Three‑Phase Pipeline

```mermaid
flowchart TB
    A["Start"] --> B["Pre-extraction<br/>- prevalidate inputs<br/>- transform<br/>- validate"]
    B --> C{"All inputs valid?"}
    C -- No --> F["FAIL"]
    C -- Yes --> D["Extraction (Runner)<br/>- per-input extraction<br/>- sequential or threaded"]
    D --> E{"All inputs success?"}
    E -- No --> F
    E -- Yes --> G["Post-extraction<br/>- aggregate results<br/>- validate"]
    G --> H{"Results valid?"}
    H -- No --> F
    H -- Yes --> I["Persist execution + factors<br/>include total cost"]
    I --> J["SUCCESS"]
    F --> K["Emit *.execution.failed"]
    J --> L["Emit *.execution.completed"]

```

### Concurrency Strategy

- **DefaultRunner**: Sequential processing for simple operations.
- **ThreadRunner**: Parallel per independent input unit (e.g., owners, monthly chunks).

#### Runners – Execution Examples

```mermaid
flowchart LR
    subgraph "Bank Statement Processor"
      E1["Execution 1 (Doc 1)"]
      E2["Execution 2 (Doc 2)"]
      E3["Execution 3 (Doc 3)"]
      E4["Execution 4 (Doc 4)"]
      E5["Execution 5 (Doc 5)"]
    end

    subgraph "Driver's License Processor"
      EX["Execution 1"]
      subgraph "ThreadRunner (concurrent per document)"
        D1["Doc A"]:::par
        D2["Doc B"]:::par
      end
      EX --> D1
      EX --> D2
    end

    classDef par fill:#e8f4ff,stroke:#66a3ff,stroke-width:1px;
```

### Eventing & Cost

- **Events**: `.execution.started`, `.execution.completed`, `.execution.failed` published to Pub/Sub.
- **Cost Tracking**: Accumulate per-operation costs during extraction; persist as `run_cost_cents` in execution record.

### Persistence Summary

- Insert into `processing_executions` with status, timings, duration, processor name, run cost.
- Upsert `factors`: mark previous as not current, insert new values linked to execution.
