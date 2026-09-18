# Employee management isolated prototype (NOT deployed)

This module is an offline SQLite domain layer, not a web server, authentication provider, Google Form, or deployed GAS. Never expose `bootstrap_admin`, `decide`, or `set_generation_result` to untrusted requests. Production must derive actor identity from verified Google identity/session and enforce admin privileges server-side. The caller-supplied `actor_id` is safe ONLY for local trusted tests; it is not authentication.

## Interfaces
- Registration: `register(employee_id,email)` -> pending; unique case-insensitive email and unique ID. Production registration must validate verified email ownership and serialize writes in a transactional datastore.
- Admin: `decide(verified_admin_id,employee_id,approved|rejected|suspended)`; link account after verified ownership.
- Employee: `request(verified_employee_id,account_id)` -> job ID; engine reads approved job only via trusted server integration.
- Engine: `set_generation_result(verified_admin_id,job_id,generating|qa_failed|ready,artifact_ref)` is a temporary privileged adapter, not an engine credential mechanism. Replace with signed service identity and verified QA evidence; do not call ready merely because MP4 exists.
- Employee: `review(verified_employee_id,job_id,revision|posted,post_url)` records manually published TikTok URL only. No upload or publication API exists.
- History: `history(verified_actor_id,employee_id)` enforces owner or admin visibility.

## Security and production blockers
- Repository is public: NEVER commit names/emails from real forms, tokens, passwords, cookies, private assets, SQLite DB files, or employee records. This code contains test-only example.test identities.
- SQLite stores only IDs, email, status, handle, job references and audit metadata. No TikTok credentials are collected. Real deployment requires a private database, backup policy, retention policy and restricted access.
- Existing Google Form ID, published URL, Apps Script project/deployment, form responses and scopes have not been verified. Do not claim live registration or authorization.
- Employee configurations in `config/accounts/` are static generation settings, not authenticated employee identities. Do not equate `status:active` with manager approval.
- Production integration requires verified Google identity, owner-controlled initial admin provisioning, signed engine callbacks, CSRF protection where applicable, idempotent request keys, private artifact authorization, full audit retention, and end-to-end testing of six employees.
- Form must never request TikTok password or token. Employee manually posts after explicit approval and records URL; no TikTok API calls.

Run local tests: `python -m unittest discover -s tests -p 'test_employee_management.py' -v`.
