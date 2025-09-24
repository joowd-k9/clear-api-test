# AURA Processing Engine API Reference

## Overview

APIs for managing document processors, orchestrating execution workflows, and extracting underwriting factors.

## Table of Contents

1. [Processor Management](#1-processor-management)
2. [Execution Management](#2-execution-management)

---

## 1. Processor Management

### List All Available Processors

Retrieves a list of all available processors in the system.

```http
GET /api/v1/processors
```

### Get Processor Details

Retrieves detailed information about a specific processor including its capabilities.

```http
GET /api/v1/processors/{processor_id}
```

### List All Processor Runs

Retrieves a list of all processor runs across all executions and underwritings.

```http
GET /api/v1/processors/runs
```

### Get Processor Run Details

Retrieves detailed information about a specific processor run instance.

```http
GET /api/v1/processors/runs/{run_id}
```

---

## 2. Execution Management

### Execute All Processors

Manually runs all or multiple specific available processors for this underwriting. This is the main execution command that processes all the documents and extracts factors.

```http
POST /api/v1/underwritings/{id}/processors/execute
```

### Execute Specific Processor

Manually runs a single processor for the specified underwriting.

```http
POST /api/v1/underwritings/{id}/processors/{processor_id}/execute
```

### List Executions for Underwriting

Retrieves all executions for a specific underwriting.

```http
GET /api/v1/underwritings/{id}/executions
```

### Get Execution Status

Retrieves the current status and progress of a processor execution.

```http
GET /api/v1/underwritings/{id}/executions/{execution_id}
```

### List Processor Runs in Execution

Retrieves all processor runs within a specific execution.

```http
GET /api/v1/underwritings/{id}/executions/{execution_id}/runs
```

### Retry Failed Execution

Retries a failed execution, optionally only retrying failed processors.

```http
POST /api/v1/underwritings/{id}/executions/{execution_id}/retry
```

### Cancel Execution

Cancels a running execution and stops all processor operations.

```http
POST /api/v1/underwritings/{id}/executions/{execution_id}/cancel
```

### Get Execution Logs

Retrieves detailed logs for a specific execution.

```http
GET /api/v1/underwritings/{id}/executions/{execution_id}/logs
```
