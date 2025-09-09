# AURA Processing Engine API Reference

## Overview

APIs for managing document processors, orchestrating execution workflows, and extracting underwriting factors.

## Table of Contents

1. [Processor Management](#1-processor-management)
2. [Execution Management](#2-execution-management)
3. [Re-Processing](#3-re-processing)
4. [Factor Management](#4-factor-management)

---

## 1. Processor Management

### List Available Processors for Account

```http
GET /api/v1/accounts/{account_id}/processors
```

**Response:**
```json
{
  "account_id": "acc_12345",
  "processors": [
    {
      "id": "p_bank_statement",
      "name": "Bank Statement Processor",
      "status": "active"
    }
  ],
  "total": 8
}
```

### Register/Update Processor for Account

Register a new processor or update an existing one for your account. This is where you configure credentials for external API processors.

```http
POST /api/v1/accounts/{account_id}/processors
PUT /api/v1/accounts/{account_id}/processors/{processor_id}
```

**Request Body:**
```json
{
  "processor_id": "p_clear_api",
  "name": "CLEAR Business Intelligence Processor",
  "credentials": {
    "api_key": "your_clear_api_key",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
  },
  "configuration": {
    "timeout": 300,
    "retry_count": 3,
    "rate_limit": 100
  }
}
```

**Explanation:**
- **credentials**: API keys and authentication details for external services
- **configuration**: Processor-specific settings like timeouts and retry counts


---

## 2. Execution Management

### Execute All Processors

Runs all available processors for this underwriting. This is the main execution command that processes all the documents and extracts factors.

```http
POST /api/v1/underwritings/{id}/processors/execute
```

**Request Body:**
```json
{
  "execution_mode": "parallel",
  "priority": "normal",
  "timeout": 1800
}
```

**Response:**
```json
{
  "execution_id": "exec_12345",
  "status": "started",
  "processors": [
    {
      "processor_id": "p_bank_statement",
      "status": "queued"
    }
  ],
  "estimated_duration": 300
}
```

**Explanation:**
- **execution_mode**: How to run processors (parallel or sequential)
- **priority**: Execution priority level
- **timeout**: Maximum time to wait for completion

### Execute Specific Processor

```http
POST /api/v1/underwritings/{id}/processors/{processor_id}/execute
```

### Get Execution Status

```http
GET /api/v1/executions/{execution_id}
```

**Response:**
```json
{
  "id": "exec_12345",
  "status": "completed",
  "started_at": "2024-01-20T14:30:00Z",
  "completed_at": "2024-01-20T14:35:00Z",
  "duration": 300,
  "processors": [
    {
      "processor_id": "p_bank_statement",
      "status": "completed",
      "duration": 120
    }
  ]
}
```

### Retry Failed Execution

```http
POST /api/v1/executions/{execution_id}/retry
```

**Request Body:**
```json
{
  "retry_failed_only": true,
  "max_retries": 3
}
```

---

## 3. Re-Processing

### Smart Re-process Based on Changes

```http
POST /api/v1/underwritings/{id}/reprocess
```

**Request Body:**
```json
{
  "trigger": "document_change",
  "changed_documents": ["doc_123", "doc_456"],
  "force_full_reprocess": false
}
```

**Response:**
```json
{
  "reprocess_id": "reprocess_789",
  "affected_processors": [
    {
      "processor_id": "p_bank_statement",
      "reason": "document_change",
      "estimated_duration": 120
    }
  ],
  "skipped_processors": [
    {
      "processor_id": "p_credit_report",
      "reason": "no_changes_detected"
    }
  ]
}
```

### Re-process Specific Processor

```http
POST /api/v1/underwritings/{id}/reprocess/{processor_id}
```

---

## 4. Factor Management

### Get All Extracted Factors

```http
GET /api/v1/underwritings/{id}/factors
```

**Response:**
```json
{
  "factors": {
    "financial": {
      "monthly_revenue": {
        "value": 50000,
        "source": "p_bank_statement",
        "confidence": 0.95
      }
    },
    "risk": {
      "nsf_count": {
        "value": 2,
        "source": "p_bank_statement",
        "confidence": 1.0
      }
    }
  },
  "completeness": 0.85
}
```

### Get Factors from Specific Processor

```http
GET /api/v1/underwritings/{id}/factors/{processor_id}
```

### Validate Extracted Factors

Checks if the extracted factors meet business rules and quality standards. This ensures the data is accurate and complete before making decisions.

```http
POST /api/v1/underwritings/{id}/factors/validate
```

**Request Body:**
```json
{
  "validation_rules": [
    "revenue_consistency",
    "credit_score_range",
    "business_age_validation"
  ]
}
```

**Response:**
```json
{
  "validation_status": "passed",
  "validated_factors": 15,
  "failed_validations": 0,
  "warnings": [
    {
      "factor": "monthly_revenue",
      "warning": "Revenue seems unusually high for business type"
    }
  ]
}
```


## Error Responses

Standardized error format:

```json
{
  "error": {
    "code": "PROCESSOR_NOT_FOUND",
    "message": "Processor with ID 'p_invalid' not found"
  },
  "timestamp": "2024-01-20T14:30:00Z"
}
```