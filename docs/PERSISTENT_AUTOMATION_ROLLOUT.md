# Persistent automation rollout (NOT production enabled)

## Decision
PostgreSQL is authoritative for identity, claims, retries and state. Google Sheets is a read-only operational projection; Google Drive stores private artifacts. Sheets read/append plus GitHub Actions concurrency cannot guarantee atomic uniqueness across different runs or services. Apps Script LockService only coordinates participating executions within its lock scope and cannot atomically fence external render/Drive side effects. Never use runner-local SQLite as durable production storage.

## Provisioning (not performed)
1. Provision managed PostgreSQL with backups, TLS, restricted network access and a least-privilege service identity. Store DATABASE_URL in a protected GitHub Actions environment secret, never source or logs. Install psycopg[binary] pinned after review. Apply Ledger.initialize() via a controlled migration, not on every worker invocation.
2. Provision a dedicated private Drive parent folder, service account/OIDC credentials, and per-tenant/per-employee folders with explicit restricted permissions. No 'anyone with link', inherited cross-tenant sharing or public artifact URLs. Do not create or share files before owner approval.
3. Configure Sheets with job_id as immutable primary reference and project only sanitized ledger rows. All edits to state must go through the database-backed service, not direct Sheet edits.
4. Configure notification destination privately. Event payloads must omit secrets, customer data and unrestricted Drive URLs.

## Safety and recovery
- Deterministic job_id = SHA256(account_id|YYYY-MM-DD|slot 1/2); UNIQUE job_id and UNIQUE artifact_key. DB atomic UPDATE status='queued' -> 'rendering' returns one lease token. Every render completion is fenced by token and unexpired lease.
- A crash after external rendering but before DB commit is ambiguous: expire() changes status to reconcile_required, NEVER automatically rerenders. Operator must check the deterministic Drive artifact key and SHA256 and confirm whether a complete original exists; only then explicitly reset or finalize in a future reconciliation implementation. Current code intentionally provides no unsafe reset method.
- Object creation must use conditional create / generation-match or equivalent provider precondition and verify digest; Drive's ordinary filename is NOT a uniqueness constraint. Drive idempotent upload and recovery are NOT implemented yet. Do not claim exactly-once rendering: database claims provide at-most-one active owner while lease is valid, but an unfenced external renderer can continue after lease expiry. Block retries pending reconciliation.
- `qa()` is an interim adapter: caller must validate PR #15's real report, require resolution_1080x1920, every mandatory check true, reject REJECT_TECHNICAL, verify report SHA256 equals stored MP4 and verify report provenance. Current method alone does NOT enforce all these requirements. `approve()` requires explicit human, rights and employee authorization flags; production authentication/authorization source not wired.
- Never treat mock_only as an artifact. No TikTok upload/publication. No production cron until all gates below pass.

## PR #21 / PR #15 contracts
Renderer input: approved plan_id, run_id, account_id, approved script, private manifest path with independently approved asset provenance, narration and timed caption paths, deterministic output key. Renderer output: real local MP4 path, sha256, render report, source commit SHA, rights assertions; reject mock or missing file. PR #21 config currently expects output/narration/captions/assets/scenes and runs build.py --config; its draft status does not prove execution success. QA input: actual MP4 and caption sidecar; PR #15 outputs status/checks/sha256/dimensions. Reject any failed check, missing report or hash mismatch. Human phone-size video, pronunciation, rights/privacy and editorial review remains mandatory. Both PRs stay unmerged pending their owners' validation.

## Daily schedule (disabled)
Two slots per account per Asia/Tokyo calendar day. A future dispatcher should submit deterministic IDs only after database connection and production gates are verified; GitHub Actions workflow_dispatch for isolated testing is permissible but must not deliver. No schedule has been enabled here.

## Release blockers
Real PostgreSQL provisioning and transaction/concurrency/crash tests; reconcile operator implementation; Drive conditional/idempotent storage and permissions integration tests; real PR #21 render and PR #15 QA integration; six-employee authorization tests; authenticated human approval; alert delivery and operational runbook; explicit production activation approval. Current CI tests only isolated logic, not live cloud resources or actual MP4. No secrets committed.
