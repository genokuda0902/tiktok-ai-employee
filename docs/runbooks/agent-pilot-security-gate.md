# Codex pilot: security gate and operator runbook

Status: BLOCKED. Do not merge PR #13 or run the API-billed workflow until every gate is verified and recorded in Issue #14. This is a public repository. Never paste an API key in an Issue, PR, chat, file, workflow input or log.

## Current evidence and known risks (2026-09-18)
- `.github/workflows/agent-doc-pilot.yml` exists on `feature/agent-runner-safety-plan` only. No successful run or draft PR produced by the agent is verified.
- It uses mutable third-party action tags (`openai/codex-action@v1`, `actions/checkout@v4`, `actions/upload-artifact@v4`, `actions/download-artifact@v4`), which must be pinned to audited commit SHAs before activation. The annotated `openai/codex-action` v1 tag was resolved via GitHub to commit `86365089eb2b84e0a8fb0717b304f8bdcb13b20e` on this date; this lookup alone is NOT a code audit or approval.
- The generation job can read repository files and receives `OPENAI_API_KEY`. A prompt prohibition is not a security boundary against malicious repository content or compromised actions. Verify the action implementation, sandbox/network behavior and token exposure; isolate the job from all unrelated secrets. Do not include confidential source/media in this public repository.
- Artifact content is uploaded before human review and can be visible to people with repository access. Validate against accidental sensitive content, not just path and byte count, before upload/push.
- Draft-PR job has `contents: write` and `pull-requests: write`; verify repository workflow permission settings, branch protection, actor restriction and no bypass. Prefer separate protected environments and approval before granting write token. Never grant main write to the generation job.
- The current `git -c http.extraheader=... push` constructs a token-bearing command; replace with a reviewed authentication method and confirm masking before activation. No production or TikTok credentials may be accessible.
- Workflow currently only checks that `OPENAI_API_KEY` is nonempty, not validity, billing budget, available quota or authorized account. These cannot be verified through this GitHub connector.

## Operator-only setup (do not paste secret values)
1. In GitHub repository Settings > Secrets and variables > Actions, add repository secret `OPENAI_API_KEY` using a dedicated, restricted API key; never commit it. Confirm key's project budget and alerts in the API provider dashboard. If an environment with required reviewers is available, use an environment-scoped secret instead and adapt the workflow accordingly.
2. In Settings > Actions > General, inspect allowed actions, default `GITHUB_TOKEN` permissions, whether Actions may create/approve PRs, and workflow approvals. Restrict defaults to read-only; grant narrowly per job. Verify branch/ruleset protection for `main` and required review.
3. Resolve and review exact SHA pins for every external action. Audit `codex-action` inputs, output/log behavior, model settings, network access and pricing against current official documentation. Record versions and date in Issue #14.
4. Replace unsafe token handling; add deterministic secret/PII checks on generated artifact and failure cases, and prevent duplicate runs/cost with concurrency and explicit manual confirmation. Review workflow diff before merging PR #13.
5. Only after a human reviews and approves the changes, merge PR #13; then explicitly dispatch the workflow once with `RUN_DOC_PILOT`. Do not enable schedule or Issue-triggered execution.
6. Inspect the exact Actions run URL, step conclusions, output artifact, new branch and draft PR. Record immutable SHAs and observed results in Issue #14. A workflow file existing is not a successful execution.
7. If any check fails, stop; rotate exposed credentials if applicable, disable workflow and report the incident. No auto-merge, production deployment or TikTok posting.

## Current stop condition
No verified secret configuration, branch protection, action audit, actual workflow execution, generated PR or cost limit. Do not call the pilot or six-agent system complete.
