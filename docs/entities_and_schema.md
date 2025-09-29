## 1) Identity, Tenancy, Auth & RBAC

### tenant (organization)

```sql
id UUID PRIMARY KEY,
name TEXT NOT NULL,
status TEXT NOT NULL CHECK (status IN ('active','suspended')),
created_at TIMESTAMP NOT NULL,
updated_at TIMESTAMP NOT NULL

```

### account (user)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
firebase_uid TEXT NOT NULL UNIQUE,        -- Firebase Auth user id
email TEXT NOT NULL,
first_name TEXT,
last_name TEXT,
status TEXT NOT NULL CHECK (status IN ('active','invited','disabled')),
created_at TIMESTAMP NOT NULL,
updated_at TIMESTAMP NOT NULL,
UNIQUE (tenant_id, email)

```

### role (seed: MANAGER, UNDERWRITER, VIEWER)

```sql
id UUID PRIMARY KEY,
name TEXT NOT NULL UNIQUE,            -- 'MANAGER'|'UNDERWRITER'|'VIEWER'
description TEXT,
created_at TIMESTAMP NOT NULL,
updated_at TIMESTAMP NOT NULL

```

### permission (granular capability catalog)

```sql
id UUID PRIMARY KEY,
name TEXT NOT NULL UNIQUE,            -- e.g., 'underwriting:write', 'rules:manage'
description TEXT

```

### role_permission (assign permissions to roles)

```sql
role_id UUID NOT NULL REFERENCES role(id),
permission_id UUID NOT NULL REFERENCES permission(id),
PRIMARY KEY (role_id, permission_id)

```

### account_role (assign roles to accounts)

```sql
account_id UUID NOT NULL REFERENCES account(id),
role_id UUID NOT NULL REFERENCES role(id),
PRIMARY KEY (account_id, role_id)

```

-- Password reset and email verification are handled by Firebase; no local tables required.

### tenant_invitation (invite-based onboarding)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
email TEXT NOT NULL,
role_name TEXT NOT NULL CHECK (role_name IN ('MANAGER','UNDERWRITER','VIEWER')),
token_hash TEXT NOT NULL,
status TEXT NOT NULL CHECK (status IN ('pending','accepted','expired','revoked')),
invited_by UUID NOT NULL REFERENCES account(id),
expires_at TIMESTAMP NOT NULL,
accepted_at TIMESTAMP,
account_id UUID NULL REFERENCES account(id),
created_at TIMESTAMP NOT NULL

```

### idempotency_key (request-level)

```sql
tenant_id UUID NOT NULL REFERENCES tenant(id),
scope TEXT NOT NULL,
key TEXT NOT NULL,
response_hash TEXT,
created_at TIMESTAMP NOT NULL,
PRIMARY KEY (tenant_id, scope, key)

```

---

## 2) Core Underwriting & Application Data

### underwriting (root aggregate)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
created_by UUID NOT NULL REFERENCES account(id),
status TEXT NOT NULL CHECK (status IN ('created','processing','rejected','missing','passed','suggested','decided')),
application_type TEXT CHECK (application_type IN ('NEW','RENEWAL')),
application_ref_id TEXT,
request_amount NUMERIC(15,2),
request_date DATE,
purpose TEXT,
-- ISO details
iso_ref_id TEXT,
iso_name TEXT,
iso_email TEXT,
iso_phone TEXT,
-- Representative details
representative_ref_id TEXT,
representative_first_name TEXT,
representative_last_name TEXT,
representative_email TEXT,
representative_phone_mobile TEXT,
representative_phone_home TEXT,
representative_phone_work TEXT,
-- Merchant details
merchant_ref_id TEXT,
merchant_name TEXT,
merchant_dba_name TEXT,
merchant_email TEXT,
merchant_phone TEXT,
merchant_website TEXT,
merchant_industry TEXT,
merchant_ein TEXT,
merchant_entity_type TEXT,
merchant_incorporation_date DATE,
merchant_state_of_incorporation TEXT,
created_at TIMESTAMP NOT NULL,
updated_at TIMESTAMP NOT NULL

```

### merchant_address

```sql
id UUID PRIMARY KEY,
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
addr_1 TEXT,
addr_2 TEXT,
city TEXT,
state TEXT,
zip TEXT

```

### owner (beneficial owners)

```sql
id UUID PRIMARY KEY,
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
first_name TEXT,
last_name TEXT,
email TEXT,
phone_mobile TEXT,
phone_work TEXT,
phone_home TEXT,
birthday DATE,
fico_score INT,
ssn TEXT,
ownership_percent NUMERIC(5,2),
primary_owner BOOLEAN DEFAULT FALSE

```

### owner_address

```sql
id UUID PRIMARY KEY,
owner_id UUID NOT NULL REFERENCES owner(id) ON DELETE CASCADE,
addr_1 TEXT,
addr_2 TEXT,
city TEXT,
state TEXT,
zip TEXT

```

### stipulation_type (lookup)

```sql
key TEXT PRIMARY KEY,                 -- e.g., 'bank_statement','drivers_license'
label TEXT NOT NULL

```

### document (artifact pointer + classification)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
current_revision_id UUID NULL,
created_at TIMESTAMP NOT NULL,
updated_at TIMESTAMP NOT NULL

```

### document_revision (upload/replace history)

```sql
id UUID PRIMARY KEY,
document_id UUID NOT NULL REFERENCES document(id) ON DELETE CASCADE,
revision INT NOT NULL,
filename TEXT NOT NULL,
mime_type TEXT NOT NULL,
size_bytes BIGINT NOT NULL,
gcs_uri TEXT NOT NULL,
gcs_generation BIGINT,
crc32c TEXT,
md5 TEXT,
status TEXT NOT NULL CHECK (status IN ('created','rejected')),
stipulation_type TEXT NULL REFERENCES stipulation_type(key),
classification_confidence NUMERIC(5,2),
quality_score NUMERIC(5,2),
dpi_x INT,
dpi_y INT,
page_count INT,
rejection_code TEXT,
created_at TIMESTAMP NOT NULL,
created_by UUID NULL REFERENCES account(id),
UNIQUE (document_id, revision)

```

### ocr_result (pointer to OCR/parsed fields)

```sql
id UUID PRIMARY KEY,
document_revision_id UUID NOT NULL REFERENCES document_revision(id) ON DELETE CASCADE,
ocr_gcs_uri TEXT NOT NULL,
fields_json JSONB,
confidence NUMERIC(5,2),
created_at TIMESTAMP NOT NULL

```

---

## 3) Processing, Catalog, Executions, Costs

-- Processor catalog is code-managed (JSON in codebase). No DB table for processors.

### processor_purchase (per-tenant purchased processors)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
processor_key TEXT NOT NULL,               -- stable key from code catalog (no FK)
processor_name TEXT NOT NULL,              -- denormalized for reporting
purchased_by UUID NOT NULL REFERENCES account(id),
purchased_at TIMESTAMP NOT NULL,
status TEXT NOT NULL CHECK (status IN ('active','revoked','expired')),
plan TEXT,                                 -- plan/tier name
price_cents BIGINT,                        -- price at purchase time (immutable)
currency TEXT NOT NULL DEFAULT 'USD',
billing_cycle TEXT,                        -- monthly/annual/one_time
config JSONB,                              -- tenant-specific config snapshot at purchase
notes TEXT,
updated_at TIMESTAMP NOT NULL

```

-- Removed processor_subscription. All state tracked in processor_purchase (one or many records over time).

### processing_execution (single processor attempt per record)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
processor_purchase_id UUID NOT NULL REFERENCES processor_purchase(id),
processor_key TEXT NOT NULL,
processor_name TEXT NOT NULL,
status TEXT NOT NULL CHECK (status IN ('pending','running','completed','failed','cancelled')),
created_by UUID NULL REFERENCES account(id),
started_at TIMESTAMP,
completed_at TIMESTAMP,
factors_delta JSONB,                   -- factors written by this execution
run_cost_cents BIGINT,                 -- cost in cents at run time
currency TEXT NOT NULL DEFAULT 'USD',
created_at TIMESTAMP NOT NULL,
updated_at TIMESTAMP NOT NULL

```

## 4) Factors

### factor (atomic factors per underwriting)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
factor_key TEXT NOT NULL,                 -- e.g., 'f.avg_revenue', 'owners[0].credit_score.score'
value JSONB NOT NULL,                    -- typed value; store as JSONB to support number/string/bool/array
unit TEXT,                                -- optional units (e.g., 'USD/month')
source TEXT NOT NULL CHECK (source IN ('processor','manual')),
processor_purchase_id UUID NULL REFERENCES processor_purchase(id),
execution_id UUID NULL REFERENCES processing_execution(id) ON DELETE SET NULL,
document_revision_id UUID NULL REFERENCES document_revision(id) ON DELETE SET NULL,
is_current BOOLEAN NOT NULL DEFAULT TRUE, -- current effective value for this key
created_by UUID NULL REFERENCES account(id),
created_at TIMESTAMP NOT NULL,
updated_at TIMESTAMP NOT NULL,
supersedes_id UUID NULL REFERENCES factor(id)

```

Notes:

- Each processor execution can write multiple factor rows; link them via `execution_id` (one-to-many).
- Manual factor entries use `source = 'manual'` with `created_by` populated; `processor_purchase_id`/`execution_id` remain NULL.
- Update flows should set previous `is_current = FALSE` and insert a new row for the same `factor_key`.

### factor_snapshot

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
snapshot_hash TEXT NOT NULL,
data JSONB NOT NULL,
created_at TIMESTAMP NOT NULL,
UNIQUE (underwriting_id, snapshot_hash)

```

Snapshot guidance:

- `factor_snapshot.data` is a materialized, merged view of all `factor` rows where `is_current = TRUE` at that time.
- Compute `snapshot_hash` from the canonicalized `data`. Use snapshots for Pre‑Check/Score Card idempotency and audit.

---

## 5) Pre-Check Rules & Evaluations

### precheck_rule (versioned per row or via separate versions table)

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
name TEXT NOT NULL,
description TEXT,
priority INT NOT NULL DEFAULT 50,
enabled BOOLEAN NOT NULL DEFAULT TRUE,
criterion JSONB NOT NULL,              -- rule definition (paths, ops)
reason_code TEXT NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT now(),
effective_at TIMESTAMP,
expires_at TIMESTAMP,
version INT NOT NULL,
updated_by UUID REFERENCES account(id),
updated_at TIMESTAMP NOT NULL

```

### precheck_evaluation

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
factor_snapshot_id UUID NOT NULL REFERENCES factor_snapshot(id),
status TEXT NOT NULL CHECK (status IN ('Rejected','Passed','Missing')),
failures JSONB NOT NULL,
skipped JSONB NOT NULL,
rule_version TEXT NOT NULL,
evaluated_at TIMESTAMP NOT NULL,
UNIQUE (underwriting_id, factor_snapshot_id)

```

---

## 6) Score Card Config & Scores

### scorecard_config

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
version TEXT NOT NULL,                 -- immutable label
config JSONB NOT NULL,                 -- bins, weights, grading, reasons
created_at TIMESTAMP NOT NULL,
created_by UUID REFERENCES account(id),
UNIQUE (tenant_id, version)

```

### score

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
factor_snapshot_id UUID NOT NULL REFERENCES factor_snapshot(id),
scorecard_version TEXT NOT NULL,
score INT NOT NULL CHECK (score BETWEEN 0 AND 100),
grade TEXT NOT NULL CHECK (grade IN ('A','B','C','D','E')),
expected_loss NUMERIC(6,3) CHECK (expected_loss >= 0 AND expected_loss <= 1),
raw_points INT,
top_reasons JSONB,
missing_factors JSONB,
evaluated_at TIMESTAMP NOT NULL,
UNIQUE (underwriting_id, factor_snapshot_id)

```

---

## 7) Suggestions & Decisions

### suggestion

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
status TEXT NOT NULL CHECK (status IN ('queued','ready','failed')),
payload JSONB,                          -- generated suggestions
created_at TIMESTAMP NOT NULL

```

### decision

```sql
id UUID PRIMARY KEY,
tenant_id UUID NOT NULL REFERENCES tenant(id),
underwriting_id UUID NOT NULL REFERENCES underwriting(id) ON DELETE CASCADE,
decision TEXT NOT NULL CHECK (decision IN ('approve','reject','modify')),
amount_approved NUMERIC(15,2),
terms JSONB,                            -- interest, term_months, frequency
reasoning JSONB,
conditions JSONB,
decision_maker UUID NOT NULL REFERENCES account(id),
decided_at TIMESTAMP NOT NULL
```
