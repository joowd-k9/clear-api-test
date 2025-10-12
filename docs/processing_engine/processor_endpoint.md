# Overview

APIs for listing available processors, managing processor executions, and retrieving execution details.

# Table of Contents

1. System Processor Management
    - A. System Processor Attributes
    - B. List System Processors
2. Tenant Processor Management
    - A. Tenant Processor Attributes
    - B. List Tenant Processors
    - C. Show Tenant Processor
    - D. Create Tenant Processor
    - E. Update Tenant Processors
    - F. List Processor Executions
3. Underwriting Processor Management
    - A. Underwriting Processor Attributes
    - B. List All Processors of Single Underwriting
    - C. Add Processor to Single Underwriting
    - D. Update Processor of Single Underwriting
    - E. List All Executions of Single Processor of Single Underwriting
    - F. Show Processor Execution Details
    - G. Execute Single Processor
    - H. Force Consolidation
    - I. Activate Processor Execution
    - J. Deactivate Processor Execution

---

# 1. System Processor Management

This section covers the management of system-wide processors that can be purchased and configured by tenants. System processors define the core processing capabilities available in the AURA platform, including their pricing, requirements, and operational parameters.

***These information are hard-coded.***

## A. System Processor Attributes

This table shows all processor catalogue attributes. Field names align with platform-wide keys used by purchases and underwriting selections where applicable:

| **Attribute** | Type | **Description** | **Example** |
| --- | --- | --- | --- |
| processor | `str` | Unique processor identifier used across the platform | `"p_bank_statement_processor"` |
| title | `str` | Human readable name | `"Bank Statement Processor"` |
| description | `str` | Detailed information about what the processor does and its capabilities | `"Analyzes bank statements to extract revenue, cash flow patterns, and NSF occurrences"` |
| pricing | `dict` | Catalogue price preview | `{ "amount": 50, "unit": "page", "currency": "USD" }` |

## B. List System Processors

Retrieves a comprehensive list of all available processors in the system, including their configuration, pricing, and current status. This endpoint is typically used by administrators to view the complete processor catalogue and by tenants to see available processors for purchase.

> GET /api/v1/processors
>

**Response:**

```json
{
  "processors": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440012",
      "processor": "p_bank_statement_processor",
      "title": "Bank Statement Processor",
      "description": "Analyzes bank statements to extract revenue, cash flow patterns, and NSF occurrences",
      "pricing": {
        "amount": 50,
        "unit": "page",
        "currency": "USD"
      },
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440014",
      "processor": "p_clear_business_search_processor",
      "title": "CLEAR Business Search Processor",
      "description": "Searches Thomson Reuters CLEAR database for business information and risk assessment",
      "pricing": {
        "amount": 125,
        "unit": "search",
        "currency": "USD"
      },
    }
  ]
}

```

# 2. Tenant Processor Management

This section covers the management of processor subscriptions and configurations at the tenant level. Tenants can purchase processors, configure their execution settings, and monitor processor usage across their underwritings.

## A. Tenant Processor Attributes

This table shows purchased processor (tenant entitlement) attributes, aligned with `purchased_processors` schema:

| **Attribute** | Type | **Computed** | **Description** | **Example** |
| --- | --- | --- | --- | --- |
| id | `uuid` | No | Primary key of the purchased processor | `"550e8400-e29b-41d4-a716-446655440013"` |
| tenant_id | `uuid` | No | Tenant owning the purchase | `"550e8400-e29b-41d4-a716-446655440002"` |
| underwriting_id | `uuid` | No | Underwriting scope if underwriting-scoped | `null` |
| processor | `str` | No | Unique processor identifier | `"p_bank_statement_processor"` |
| name | `str` | No | Human-readable processor name | `"Bank Statement Processor"` |
| title | `str` | No | Tenant customized name | `"My Bank Statement Processor"` |
| plan | `str` | No | Plan/tier name | `"standard"` |
| priority | `int` | No | Consolidation priority (higher = consolidated later) | `100` |
| price_amount | `int` | No | Price at purchase time in cents | `50` |
| price_unit | `str` | No | Billing unit | `"page"` |
| price_currency | `str` | No | Currency code | `"USD"` |
| status | `str` | No | Status of entitlement | `"active"` |
| config | `object` | No | Config snapshot at purchase (can include `minimum_document`) | `{"minimum_document": 3}` |
| notes | `str` | No | Notes | `null` |
| disabled | `str` | Yes | If disabled_at is set will return true | `false` |
| purchased_at | `str` | No | ISO timestamp of purchase | `"2024-12-19T10:30:00Z"` |
| purchased_by | `uuid` | No | Account who purchased | `"550e8400-e29b-41d4-a716-446655440000"` |
| disabled_at | `str` | No | When disabled | `null` |
| disabled_by | `uuid` | No | Who disabled | `null` |
| updated_at | `str` | No | Last update time | `"2024-12-19T10:30:00Z"` |

## B. List Tenant Processors

Retrieves a list of all processors purchased and configured by the current tenant, including their execution settings and status.

**For system administrators:**

> GET /api/v1/tenants/{tenant_id}/processors
>

**For a tenant's authenticated account:**

> GET /api/v1/tenant-processors
>

**Response:**

```json
{
  "processors": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440016",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440016",
      "underwriting_id": null,
      "processor": "p_clear_business_search_processor",
      "name": "CLEAR Business Search Processor",
      "title": "CLEAR Business Search Processor",
      "plan": "standard",
      "price_amount": 125,
      "price_unit": "search",
      "price_currency": "USD",
      "status": "active",
      "disabled_at": null,
      "disabled_by": null,
      "purchased_by": "550e8400-e29b-41d4-a716-446655440000",
      "purchased_at": "2024-12-19T10:30:00Z",
      "updated_at": "2024-12-19T10:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440017",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440016",
      "underwriting_id": null,
      "processor": "p_bank_statement_processor",
      "name": "Bank Statement Processor",
      "title": "My Bank Statement Processor",
      "plan": "standard",
      "price_amount": 50,
      "price_unit": "page",
      "price_currency": "USD",
      "status": "active",
      "config": {},
      "notes": null,
      "disabled_at": null,
      "disabled_by": null,
      "purchased_by": "550e8400-e29b-41d4-a716-446655440000",
      "purchased_at": "2024-12-19T10:30:00Z",
      "updated_at": "2024-12-19T10:30:00Z"
    }
  ]
}

```

## C. Show Tenant Processor

Retrieves detailed information about a specific processor configuration for the current tenant, including its execution settings, computed attributes from the system processor, and audit information.

**For system administrators:**

> GET /api/v1/tenants/{tenant_id}/processors/{processor_id}
>

**For a tenant's authenticated account:**

> GET /api/v1/tenant-processors/{processor_id}
>

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440017",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440016",
  "underwriting_id": null,
  "processor": "p_bank_statement_processor",
  "name": "Bank Statement Processor",
  "title": "My Bank Statement Processor",
  "plan": "standard",
  "price_amount": 50,
  "price_unit": "page",
  "price_currency": "USD",
  "status": "active",
  "config": {},
  "notes": null,
  "disabled_at": null,
  "disabled_by": null,
  "purchased_by": "550e8400-e29b-41d4-a716-446655440000",
  "purchased_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}

```

## D. Create Tenant Processor

Purchases a processor entitlement for the tenant. Creates a new record in `purchased_processors`. Use 2.E to update purchase configuration or disable later.

**For system administrators:**

> POST /api/v1/tenants/{tenant_id}/processors
>

**For a tenant's authenticated account:**

> POST /api/v1/tenant-processors
>

**Request Body:**

```json
{
  "processor": "p_bank_statement_processor",
  "plan": "standard",
  "priority": 100,
  "title": "My Bank Statement Processor",
  "notes": "optional notes",
  "config": {
    "minimum_document": 3
  }
}

```

**Request Body Parameters:**

- **`processor`**
    - **Type**: `string`
    - **Required**: Yes
    - **Description**: Unique processor identifier from system catalog
    - **Example**: `"p_bank_statement_processor"`
- **`plan`**
    - **Type**: `string`
    - **Required**: Yes
    - **Description**: Plan/tier name for pricing
    - **Example**: `"standard"`
- **`priority`**
    - **Type**: `integer`
    - **Required**: No
    - **Description**: Consolidation priority - higher values are consolidated later, allowing them to overwrite factors from lower priority processors
    - **Default**: `0`
    - **Example**: `100`
- **`title`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Tenant-customized display name
    - **Example**: `"My Bank Statement Processor"`
- **`notes`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Free-form notes
    - **Example**: `"optional notes"`
- **`config`**
    - **Type**: `object`
    - **Required**: No
    - **Description**: Processor configuration options
    - **Common config fields**:
      - `minimum_document` (int): Minimum documents required for execution (used by `should_execute()`)
      - Other processor-specific settings
    - **Example**: `{"minimum_document": 3}`

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440018",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440016",
  "underwriting_id": null,
  "processor": "p_bank_statement_processor",
  "name": "Bank Statement Processor",
  "title": "My Bank Statement Processor",
  "plan": "standard",
  "priority": 100,
  "price_amount": 50,
  "price_unit": "page",
  "price_currency": "USD",
  "status": "active",
  "config": {
    "minimum_document": 3
  },
  "notes": null,
  "disabled": false,
  "disabled_at": null,
  "disabled_by": null,
  "purchased_by": "550e8400-e29b-41d4-a716-446655440000",
  "purchased_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}

```

## E. Update Tenant Processors

Updates an existing tenant processor purchase configuration. Does not create a new purchase (use 2.D to purchase). Supports updating metadata, config, and disabling the purchase.

**For system administrators:**

> PUT /api/v1/tenants/{tenant_id}/processors/{processor_id}
>

**For a tenant's authenticated account:**

> PUT /api/v1/tenant-processors/{processor_id}
>

**Request Body:**

```json
{
  "title": "My Bank Statement Processor",
  "notes": "optional notes",
  "config": {},
  "disabled": true
}

```

**Request Body Parameters:**

- **`title`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Tenant-customized display name for the purchased processor
    - **Example**: `"My Bank Statement Processor"`
- **`notes`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Free-form notes for this purchase
    - **Example**: `"Use for all renewals"`
- **`config`**
    - **Type**: `object`
    - **Required**: No
    - **Description**: Configuration overrides for the purchased processor
    - **Example**: `{}`
- **`disabled`**
    - **Type**: `boolean`
    - **Required**: No
    - **Description**: Disable or enable the purchased processor. When set true, `disabled_at`/`disabled_by` are populated.
    - **Example**: `true`

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440017",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440016",
  "underwriting_id": null,
  "processor": "p_bank_statement_processor",
  "name": "Bank Statement Processor",
  "title": "My Bank Statement Processor",
  "plan": "standard",
  "price_amount": 50,
  "price_unit": "page",
  "price_currency": "USD",
  "status": "active",
  "config": {},
  "notes": "optional notes",
  "disabled": true,
  "disabled_at": "2024-12-19T10:31:00Z",
  "disabled_by": "550e8400-e29b-41d4-a716-446655440000",
  "purchased_by": "550e8400-e29b-41d4-a716-446655440000",
  "purchased_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:31:00Z"
}

```

## F. List Processor Executions

Retrieves a paginated list of all processor executions for a specific processor across all underwritings within the current tenant's scope.

**For system administrators:**

> GET /api/v1/tenants/{tenant_id}/processors/{processor_id}/executions
>

**For a tenant's authenticated account:**

> GET /api/v1/tenant-processors/{processor_id}/executions
>

**Parameters:**

- **`page`**
    - **Type**: `number`
    - **Required**: No
    - **Description**: 1-based page index for pagination
    - **Default**: `1`
    - **Example**: `2`
- **`limit`**
    - **Type**: `number`
    - **Required**: No
    - **Description**: Page size with maximum of 200
    - **Default**: `50`
    - **Example**: `100`
- **`sort`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Sort field with optional direction. Prefix with for descending order
    - **Default**: `started_at`
    - **Available fields**: `started_at`, `completed_at`, `status`, `run_cost_cents`
    - **Example**: `started_at` (newest first)
- **`select`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Comma-separated list of fields to include in response
    - **Example**: `id,status,run_cost_cents`
- **`filters`**
    - **Type**: `object`
    - **Required**: No
    - **Description**: Field-value pairs for filtering results
    - **Example**: `started_from=2025-09-10&started_to=2025-09-11`

**Example:**

> GET /api/v1/tenants/{tenant_id}/processors/{processor_id}/executions?page=2&limit=50&sort=-started_at&started_from=2025-09-11
>

**Response:**

```json
{
  "processor_purchase": {
      "id": "550e8400-e29b-41d4-a716-446655440014",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
      "processor": "p_clear_business_search_processor",
      "name": "CLEAR Business Search Processor",
      "title": "CLEAR Business Search Processor",
      "price_amount": 125,
      "price_unit": "search",
      "price_currency": "USD",
      "status": "active",
      "purchased_by": "550e8400-e29b-41d4-a716-446655440000",
      "purchased_at": "2024-12-19T10:30:00Z",
      "updated_at": "2024-12-19T10:30:00Z"
    },
	"executions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440009",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
      "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
      "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440003",
      "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440014",
      "processor": "p_clear_business_search_processor",
      "name": "CLEAR Business Search Processor",
      "status": "completed",
      "started_at": "2024-12-19T10:30:00Z",
      "completed_at": "2024-12-19T10:30:15Z",
      "run_cost_cents": 25,
      "currency": "USD",
      "created_by": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2024-12-19T10:30:00Z",
      "updated_at": "2024-12-19T10:30:15Z",
      "factors_delta": {
          "f_business_name": "ABC Corp"
      }
    }
  ]
}

```

# 3. Underwriting Processor Management

## A. Underwriting Processor Attributes

This table shows underwriting processor attributes, aligned with `underwriting_processor` schema:

| **Attribute** | Type | **Computed** | **Description** | **Example** |
| --- | --- | --- | --- | --- |
| id | `uuid` | No | Primary key of underwriting processor selection | `"550e8400-e29b-41d4-a716-446655440011"` |
| tenant_id | `uuid` | No | Tenant owning the underwriting | `"550e8400-e29b-41d4-a716-446655440011"` |
| underwriting_id | `uuid` | No | Underwriting this processor is attached to | `"550e8400-e29b-41d4-a716-446655440011"` |
| purchased_processor_id | `uuid` | Yes | Linked purchase if present | `"550e8400-e29b-41d4-a716-446655440014"` |
| processor | `str` | No | Unique processor identifier | `"p_clear_business_search_processor"` |
| name | `str` | No | Human-readable processor name | `"CLEAR Business Search Processor"` |
| title | `str` | Yes | Tenant-customized display title | `"Custom CLEAR Title"` |
| auto | `bool` | No | Execute automatically when conditions are met | `true` |
| notes | `str` | Yes | Free-form notes for this underwriting processor | `null` |
| config_override | `object` | Yes | Overrides relative to purchase config (if configured) | `{}` |
| effective_config | `object` | Yes | Resolved configuration at selection time | `{}` |
| price_snapshot_amount | `int` | Yes | Optional price snapshot amount (cents) | `125` |
| price_snapshot_unit | `str` | Yes | Unit for price snapshot | `"search"` |
| price_snapshot_currency | `str` | Yes | Currency for price snapshot | `"USD"` |
| created_by | `uuid` | Yes | Account who created this selection | `"550e8400-e29b-41d4-a716-446655440000"` |
| created_at | `str` | No | timestamp when created | `"2024-12-19T10:30:00Z"` |
| updated_at | `str` | No | timestamp when updated | `"2024-12-19T10:30:00Z"` |

## B. List All Processors of Single Underwriting

Retrieves all processors configured for a specific underwriting, including their current settings and status. This endpoint provides a comprehensive view of which processors are available and how they are configured for the underwriting.

> GET /api/v1/underwritings/{underwriting_id}/processors
>

**Response:**

```json
{
  "processors": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440011",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440011",
      "underwriting_id": "550e8400-e29b-41d4-a716-446655440011",
      "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440011",
      "processor": "p_clear_business_search_processor",
      "name": "CLEAR Business Search Processor",
      "title": null,
      "enabled": true,
      "auto": true,
      "notes": null,
      "config_override": {},
      "effective_config": {},
      "price_snapshot_amount": 125,
      "price_snapshot_unit": "search",
      "price_snapshot_currency": "USD",
      "created_by": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2024-12-19T10:30:00Z",
      "updated_at": "2024-12-19T10:30:00Z"
    }
  ]
}

```

## C. Add Processors to Single Underwriting

Adds a processor to a specific underwriting with custom configuration settings. This allows fine-tuning processor behavior for individual underwritings while maintaining tenant-level defaults.

> POST /api/v1/underwritings/{underwriting_id}/processors
>

**Request Body:**

```json
{
  "processor": "p_clear_processor",
  "auto": true,
  "disabled": true,
  "title": "Custom CLEAR Title",
  "notes": "Optional notes"
}

```

**Request Body Parameters:**

- **`processor`**
    - **Type**: `string`
    - **Required**: Yes
    - **Description**: Unique processor identifier linking to system processor
    - **Example**: `"p_clear_processor"`
- **`auto`**
    - **Type**: `boolean`
    - **Required**: Yes
    - **Description**: Whether processor executes automatically when conditions are met
    - **Example**: `true`
- **`disabled`**
    - **Type**: `boolean`
    - **Required**: Yes
    - **Description**: Whether processor is disabled for this underwriting
    - **Example**: `true`
- **`title`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Tenant-customized display title for this underwriting processor
    - **Example**: `"Custom CLEAR Title"`
- **`notes`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Free-form notes for this underwriting processor
    - **Example**: `"Optional notes"`

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-4466554400300",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
  "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440014",
  "processor": "p_clear_business_search_processor",
  "name": "CLEAR Business Search Processor",
  "title": null,
  "auto": true,
  "notes": null,
  "config_override": {},
  "effective_config": {},
  "price_snapshot_amount": 125,
  "price_snapshot_unit": "search",
  "price_snapshot_currency": "USD",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-12-19T10:30:00Z",
  "disabled_by": "550e8400-e29b-41d4-a716-446655440000",
  "disabled_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}

```

## D. Update Processor of Single Underwriting

Modifies the configuration of an existing processor within a specific underwriting. This allows updating processor settings such as auto-execution and disabled status without affecting other underwritings or tenant-level configurations.

> PUT /api/v1/underwritings/{underwriting_id}/processors/{purchased_processor_id}
>

**Request Body:**

```json
{
  "auto": true,
  "enabled": true,
  "title": "Custom CLEAR Title",
  "notes": "Optional notes"
}

```

**Request Body Parameters:**

- **`auto`**
    - **Type**: `boolean`
    - **Required**: No
    - **Description**: Whether processor executes automatically when conditions are met
    - **Example**: `true`
- **`disabled`**
    - **Type**: `boolean`
    - **Required**: No
    - **Description**: Whether processor is disabled for this underwriting
    - **Example**: `true`
- **`title`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Tenant-customized display title for this underwriting processor
    - **Example**: `"Custom CLEAR Title"`
- **`notes`**
    - **Type**: `string`
    - **Required**: No
    - **Description**: Free-form notes for this underwriting processor
    - **Example**: `"Optional notes"`

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440033",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
  "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440014",
  "processor": "p_clear_business_search_processor",
  "name": "CLEAR Business Search Processor",
  "title": "Custom CLEAR Title",
  "auto": true,
  "notes": null,
  "config_override": {},
  "effective_config": {},
  "price_snapshot_amount": 125,
  "price_snapshot_unit": "search",
  "price_snapshot_currency": "USD",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-12-19T10:30:00Z",
  "disabled_by": "550e8400-e29b-41d4-a716-446655440000",
  "disabled_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z"
}

```

## E. List All Executions of Single Processor of Single Underwriting

Retrieves all execution history for a specific processor within a particular underwriting. This endpoint provides comprehensive execution tracking without pagination, showing the complete history of processor runs and their results.

> GET /api/v1/underwritings/{underwriting_id}/processors/{processor_id}/executions
>

**Response:**

```json
{
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
  "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440003",
  "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440003",
  "underwriting_processor": {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "processor": "p_clear_business_search_processor",
    "name": "CLEAR Business Search Processor",
    "title": "CLEAR Business Search Processor",
    "auto": true,
    "notes": null,
    "config_override": {},
    "effective_config": {},
    "price_snapshot_amount": 125,
    "price_snapshot_unit": "search",
    "price_snapshot_currency": "USD",
    "created_by": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-12-19T10:30:00Z",
    "updated_at": "2024-12-19T10:30:00Z"
  },
  "executions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440009",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
      "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
      "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440003",
      "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440003",
      "processor": "p_clear_business_search_processor",
      "status": "completed",
      "started_at": "2024-12-19T10:30:00Z",
      "completed_at": "2024-12-19T10:30:15Z",
      "run_cost_cents": 25,
      "currency": "USD",
      "factors_delta": {
        "f_business_name": "ABC Corp"
      }
    }
    ]
}

```

## F. Show Processor Execution Details

Retrieves detailed information about a specific processor execution instance, including all extracted factors, performance metrics, and execution metadata. This endpoint is useful for debugging failed executions or analyzing successful processing results.

> GET /api/v1/underwritings/{underwriting_id}/processors/{processor_id}/executions/{execution_id}
>

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440009",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
  "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440003",
  "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440003",
  "processor": "p_clear_business_search_processor",
  "status": "completed",
  "started_at": "2024-12-19T10:30:00Z",
  "completed_at": "2024-12-19T10:30:15Z",
  "run_cost_cents": 25,
  "currency": "USD",
  "factors_delta": {
    "f_business_name": "ABC Corp"
  }
}

```

## G. Execute Single Processor

Manually triggers execution of a specific processor for the underwriting. This is the primary execution command that processes documents and extracts factors. The execution can be scoped to specific documents or property.

> POST /api/v1/underwritings/{underwriting_id}/processors/{processor_id}/execute
>

**Request Body:**

```json
{
  "document_list": ["doc_123984", "doc_08923"],
  "application_property": {
    "merchant.ein": "123",
    "owners": {
      "owner_001": {
        "first_name": "Jane",
        "addresses": {
          "addr_001": {
            "city": "Austin",
            "state": "TX"
          }
        }
      }
    }
  }
}

```

**Request Body Parameters:**

- **`document_list`**
    - **Type**: `array<string>`
    - **Required**: No
    - **Description**: Optional array of document IDs to process (each item is a `document.id`).
    - **Example**: `["doc_123984", "doc_08923"]`
- **`application_property`**
    - **Type**: `object`
    - **Required**: No
    - **Description**: Partial application data to override/augment inputs for this execution.
        - Use dot-notation keys for scalar merchant fields (e.g., `"merchant.ein"`, `"merchant.industry"`).
        - For array-like entities (e.g., owners), pass an object keyed by the entity ID containing its attributes.
        - Nest owner addresses inside each owner under an `addresses` object keyed by address ID.
        - Owner example: `"owners": { "owner_001": { "first_name": "Jane", "addresses": { "addr_001": { "city": "Austin", "state": "TX" } } } }`.
    - **Example**:

        ```json
        {
          "merchant.ein": "123456789",
          "owners": {
            "owner_001": {
              "first_name": "Jane",
              "addresses": {
                "addr_001": { "city": "Austin", "state": "TX" }
              }
            }
          }
        }

        ```


**Response:**

```json
{
  "executions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440009",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440005",
      "underwriting_id": "550e8400-e29b-41d4-a716-446655440006",
      "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440007",
      "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440011",
      "processor": "p_clear_business_search_processor",
      "status": "running",
      "started_at": "2024-12-19T10:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440005",
      "underwriting_id": "550e8400-e29b-41d4-a716-446655440006",
      "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440007",
      "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440011",
      "processor": "p_clear_business_search_processor",
      "status": "running",
      "started_at": "2024-12-19T10:30:00Z"
    }
  ]
}

```

## H. Force Consolidation

Forces re-consolidation of factors for a specific processor without creating new executions. Uses existing active executions to recalculate factors. Typically called after processor configuration changes.

> POST /api/v1/underwritings/{underwriting_id}/processors/{purchased_processor_id}/consolidate
>

**Response:**

```json
{
  "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
  "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440033",
  "processor": "p_clear_business_search_processor",
  "consolidation_completed_at": "2024-12-19T10:31:00Z"
}
```

## I. Activate Processor Execution

Activates a previous processor execution, effectively rolling back to that execution's state. For application-based processors, this restores the application_property data from the execution. For document-based processors, this marks the execution as active and disables conflicting executions.

> POST /api/v1/underwritings/{underwriting_id}/processors/{processor_id}/executions/{execution_id}/activate
>

**Response:**

```json
{
  "execution": {
    "id": "550e8400-e29b-41d4-a716-446655440009",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
    "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
    "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440003",
    "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440014",
    "processor": "p_clear_business_search_processor",
    "status": "completed",
    "is_active": true,
    "started_at": "2024-12-19T10:30:00Z",
    "completed_at": "2024-12-19T10:30:15Z",
    "run_cost_cents": 25,
    "currency": "USD",
    "factors_delta": {
      "f_business_name": "ABC Corp"
    }
  }
}
```

## J. Deactivate Processor Execution

Deactivates an active processor execution, removing it from the current execution list. This triggers re-consolidation to update factors without the deactivated execution. Does not modify application form or documents.

> POST /api/v1/underwritings/{underwriting_id}/processors/{processor_id}/executions/{execution_id}/deactivate
>

**Response:**

```json
{
  "execution": {
    "id": "550e8400-e29b-41d4-a716-446655440009",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
    "underwriting_id": "550e8400-e29b-41d4-a716-446655440002",
    "underwriting_processor_id": "550e8400-e29b-41d4-a716-446655440003",
    "purchased_processor_id": "550e8400-e29b-41d4-a716-446655440014",
    "processor": "p_clear_business_search_processor",
    "status": "completed",
    "is_active": false,
    "started_at": "2024-12-19T10:30:00Z",
    "completed_at": "2024-12-19T10:30:15Z",
    "run_cost_cents": 25,
    "currency": "USD"
  },
}
```
