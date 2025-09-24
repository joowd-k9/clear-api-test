### Processing Engine Analytics Q&A

#### Questions
1. What are your most frequent analytical queries? (similar case lookups, performance metrics, compliance reports)
2. Do you need complex joins across multiple fact tables or simpler aggregations?
3. Will you be doing time-series analysis on underwriting performance over months/years?
4. How often will you query historical data vs. recent data?

#### Answers
1. Most frequent analytical queries (processing engine only)
   - Orchestrations: DAG state distribution, blockers (waiting-on dependencies), skip/early-termination reasons, selective reprocessing triggers.
   - Executions: outcome counts by processor and terminal reason, retry lineage, input document fingerprints used, factor output completeness.
   - Runs: latest run per underwriting, run diffs vs previous (docs changed, processors added/removed), partial vs full success flags.
   - Compliance/audit (processing scope): cancellation events (user vs system), circuit breaker activations, dead-lettered retries, auditability of inputs/outputs per execution.
   - Note: similar case lookups are handled by the AI Decision module and are out of scope here.

2. Join complexity
   - Primarily simpler aggregations: group-bys on a single fact (e.g., `executions`, `underwriting_runs`) with light joins to small dimensions (`processor`, `status`, `trigger_source`).
   - Occasional complex joins: compliance views that stitch multiple facts (`executions` + `execution_errors` + `execution_documents` + `execution_factors`) or cross-run comparisons.

3. Time-series analysis over months/years (excluding performance)
   - Yes, moderate: daily/weekly/monthly counts and rates for orchestrations, runs, and execution outcomes; rolling windows for retry and reprocessing effectiveness.
   - Advanced analyses (seasonality/change-points) are optional for periodic reviews, not day-to-day.

4. Historical vs recent query mix
   - Recent (operational): ~70% for last 7–30 days (active underwritings, current runs/executions, blockers, retries).
   - Historical (analytical/compliance): ~30% for 3–24 months and snapshots (trend analyses, reprocessing yield, audit and policy reviews).

#### API Reference Alignment
- Executions listing: `GET /api/v1/underwritings/{id}/executions` → counts by status, latest-execution flags.
- Execution detail: `GET /api/v1/underwritings/{id}/executions/{execution_id}` → state progression, terminal reason, retryable classification.
- Processor runs in execution: `GET /api/v1/underwritings/{id}/executions/{execution_id}/runs` → per-processor outcomes, retries, inputs, factor completeness.
- Retry/cancel: `POST /api/v1/underwritings/{id}/executions/{execution_id}/retry|cancel` → retry frequency/success; cancellations by reason.
- Processor inventory: `GET /api/v1/processors` and `GET /api/v1/processors/{processor_id}` → coverage and version distribution.
- Run inventory: `GET /api/v1/processors/runs` and `GET /api/v1/processors/runs/{run_id}` → outcome distributions, lineage, error summaries.
