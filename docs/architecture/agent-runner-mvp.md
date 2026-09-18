# AI development agent runner — MVP specification

Status: DESIGN ONLY. No autonomous coding agent, schedule, credentials, deployment or end-to-end test is enabled by this document.

## Source of truth
Read `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, Issues #6–#12 and open PRs before every task. v33 is the video quality reference; v19/v20 are not substitutes. TikTok uploads and publication are performed manually by employees.

## One-task pilot
1. Human selects one allowlisted, non-production GitHub Issue and explicitly authorizes a trial run.
2. Runner reads repository at a pinned main commit and the issue; creates a unique `agent/issue-N-run-ID` branch.
3. Coding agent may edit only an allowlisted path. No write access to main, no merges, no production deployments, no TikTok upload/publication, no outbound distribution of assets.
4. Execute predefined tests in an isolated environment with least-privilege token, bounded time/cost, no secrets in logs. A failing test stops the run.
5. Open a draft PR containing issue link, base SHA, change summary, exact test commands and results, known risks, and explicit approval request. A human reviews before merge.
6. Record run ID, commit SHA, PR URL, status and sanitized log reference. Notify only on verified completion, failure, or human approval needed.

## Prerequisites before enabling
- Confirm actual coding-agent product/API availability, authentication, pricing, quotas and terms; none verified here.
- Verify GitHub Actions workflow permissions, repository settings, branch protection, approval rules and safe handling of untrusted Issue text.
- Configure dedicated minimal permissions (`contents: read` by default; scoped write only if needed), isolated environment and approved secret store; do not store tokens or personal information in this public repository.
- Prevent prompt injection: Issues, files, PR comments and retrieved content are untrusted task data; never let them override execution permissions or exfiltrate secrets.
- Implement concurrency locks, idempotency by issue/run ID, retries with limits, budget ceilings, audit logs and a kill switch.
- Check GitHub Actions availability and actual usage limits; no cost or free-tier guarantee is made.

## Pilot acceptance tests (NOT RUN)
- A harmless documentation-only issue results in a draft PR on a separate branch with a reproducible test log.
- Invalid or malicious instructions in an Issue cannot cause secret exposure, main writes, unauthorized external calls, TikTok publication or confidential-media upload.
- Failed tests produce a failure report and no merge or production distribution.
- Duplicate trigger does not produce duplicate edits or repeated billable work.
- Human approval is required before merge, deployment, and any public distribution.

## Parallelization after pilot
Only after one successful observed run, split six roles by non-overlapping ownership and interface contracts. Each role uses its own branch/PR; integration tests run before human-approved merge. Never claim other ChatGPT chats are automatically running: the runner is an independent GitHub/agent workflow, not remote control of chat sessions.

## Current blockers
Agent execution capability, credentials, billing, workflow permissions and pilot test are unverified. Issue #7 original v33 generation source/prompts remain missing. Do not enable unattended code-writing workflow until prerequisites are verified.
