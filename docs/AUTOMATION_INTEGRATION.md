# Automation integration contract (provisional, 2026-09-18)

PR #16 remains isolated. PR #21 renderer and PR #15 QA are draft and must NOT be merged automatically. Main daily-v2 is legacy silent `-an` and its hard-coded score 90 is NOT valid evidence.

## Input
JSON object: `run_id`, `account_id`, `plan_id` (safe ASCII identifiers), `topic` (nonempty string), `script` (nonempty string/list), `generation_settings` (object). Planner additionally requires `approved:true`, `script_approved:true`, `assets_approved:true`, `priority` integer. Trend sourcing and AI script generation are NOT connected; planner selects an already approved candidate deterministically. Do not send confidential material to external services.

## Renderer adapter
Callable `renderer(request) -> {"video_path": "/private/path/video.mp4"}`. `production_renderer` currently raises RendererUnavailable; `mock_renderer` returns `video_path:null` and must never be treated as successful generation. PR #21 currently expects a separate config file with `output`, `narration`, `captions`, `assets`, `scenes`; adapter mapping, asset allowlist verification, renderer command exit code, report and checksum validation are NOT implemented. PR #21 technical_test mode bypasses rights assertions; it must never be used for release. Its current report fields include output, resolution, duration, audio, captions_burned, rights, manual_review and sha256; verify actual behavior on approved assets before integration.

## QA adapter
PR #15 exposes `inspect(video,captions=None,report=None)` returning exit code 0 for HUMAN_REVIEW_REQUIRED and 1 for REJECT_TECHNICAL; the generated JSON `status` is authoritative, not exit code alone. Its resolution_1080x1920 is currently excluded from the required list: fix that before production. PR #16 `inspect_mp4` is a preliminary technical check only and cannot verify rights, visual quality or subtitle burn-in. Never infer human approval from automated checks.

## Status and storage
`queued`, `running`, `retryable_failure`, `failed`, `qa_failed`, `renderer_not_connected`, `awaiting_human_qa`. SQLite uniqueness: run_id and (account_id,plan_id). Attempts capped at 1-5, default 3. Exceptions logged by class name only; notifier receives fixed event codes. Current `safe_handoff` copies a local MP4 only when caller supplies explicit human and rights approvals AND QA has `passed:true` and `human_visual_privacy_approval:true`; this is a local preparation helper, NOT Drive upload or employee delivery. Caller assertions are not an authenticated approval workflow. Secure persistence, atomic locking across distributed runners, verified approval identities, authenticated Drive and LINE WORKS connections, audit events, and 2/day scheduling remain unimplemented. GitHub-hosted runner SQLite is ephemeral and cannot provide durable cross-run deduplication; use persistent transactional storage before scheduling.

## Test commands
`python -m unittest discover -s tests -p 'test_automation_*.py' -v`
No automatic TikTok upload or publish code is allowed. No production delivery until user authorization and end-to-end 6-employee verification.
