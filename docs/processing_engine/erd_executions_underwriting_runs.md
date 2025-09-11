# Processing Engine ERD: Underwriting Runs and Executions

## Scope
Sample, non-comprehensive ERD for underwriting runs and processor executions.

## Diagram
```mermaid
erDiagram
    UNDERWRITING ||--o{ UNDERWRITING_RUN : has
    UNDERWRITING_RUN ||--o{ EXECUTION : includes
    PROCESSOR ||--o{ EXECUTION : configured_for
    DOCUMENT ||--o{ EXECUTION_DOCUMENT : referenced_by
    EXECUTION ||--o{ EXECUTION_DOCUMENT : consumes
    EXECUTION ||--o{ EXECUTION_ERROR : records
    FACTOR ||--o{ EXECUTION_FACTOR : defined_as
    EXECUTION ||--o{ EXECUTION_FACTOR : produces

    UNDERWRITING {
        uuid id PK
        string external_reference
        string status
        datetime created_at
        datetime updated_at
    }

    UNDERWRITING_RUN {
        uuid id PK
        uuid underwriting_id FK
        int run_number
        string trigger_source
        string status
        datetime started_at
        datetime completed_at
    }

    EXECUTION {
        uuid id PK
        uuid run_id FK
        uuid processor_id FK
        string status
        datetime started_at
        datetime ended_at
        string error_code
    }

    PROCESSOR {
        uuid id PK
        string code
        string name
        string version
        int timeout_seconds
    }

    DOCUMENT {
        uuid id PK
        uuid underwriting_id FK
        string category
        string fingerprint
        datetime uploaded_at
    }

    EXECUTION_DOCUMENT {
        uuid id PK
        uuid execution_id FK
        uuid document_id FK
        string role
    }

    EXECUTION_ERROR {
        uuid id PK
        uuid execution_id FK
        string type
        text message
        datetime occurred_at
    }

    FACTOR {
        uuid id PK
        string key
        string description
        string unit
    }

    EXECUTION_FACTOR {
        uuid id PK
        uuid execution_id FK
        uuid factor_id FK
        string value
        float quality_score
    }
```

## Notes
- Relationships and attributes are illustrative and may be incomplete.
- Aligns to processing engine terminology for underwriting runs and executions.
