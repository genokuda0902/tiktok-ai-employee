# Manual posting registry — integration contract (draft, not production)

## Scope
`src/manual_posting.py` is a local SQLite state machine, not a web service. It never uploads to TikTok, publishes, or distributes videos. PR must not be merged/deployed without administrator approval. Do not use confidential v33 prototype assets or treat v20 as v33.

## Inputs from teams
- ① video creation: immutable `video_id`, `account_id`, private MP4 path, source/asset approval evidence, caption and account metadata in a separate trusted store. Never store MP4 in public GitHub.
- ② automation/QA: authenticated trusted report `{passed: true, sha256: <exact SHA256 of MP4>}`. QA producer must perform actual ffprobe/audio/caption/privacy/license checks; a user-supplied JSON boolean is NOT sufficient. The registry checks hash/boolean but cannot independently prove QA provenance or that file bytes are valid MP4.
- ③ employee management: server-verified actor identity, trusted approved roster `{employee_id: {approved: bool, role: 'admin'|'employee'}}`; reject browser-supplied role/identity. Disable access immediately when roster changes. Assignments should be bound to an approved account owner (not yet implemented).

## Workflow / outputs
Admin `register` -> `管理者承認待ち`; admin `approve` -> admin `assign` -> `投稿担当者割当済み`; assignee `review` (rechecks hash) -> `手動投稿待ち`; assignee manually posts in TikTok and `report(url,posted_at)` -> `投稿URL確認待ち`; admin verifies actual account ownership and calls `verify(...,True)` -> `投稿完了`. All mutations write an audit record. Admin `history` sees all; employees only see their assignments. SQLite must reside in protected private storage and have restricted filesystem permissions. `review()` returns a local path only to a trusted server: NEVER expose this path as an unauthenticated download link.

## Required integration work (NOT complete)
1. Authenticate employees server-side and authorize each private download on every request; isolate tenants and ensure the employee owns the target account. No public Drive links.
2. Verify QA report origin/signature, real media properties, and approved asset provenance; ensure file is stored immutably and not a confidential prototype.
3. Implement `動画生成待ち`, `品質検査待ち`, `差し戻し`, `投稿失敗` transitions, retry policy and safe revision/version handling. Existing constants alone are not implementations.
4. Verify canonical URL actually belongs to assigned TikTok account. The `account_matches` flag is a trusted administrator decision, not an automated TikTok check; URL host/path validation is not ownership verification.
5. Implement secure manager/employee UI or form, Drive private storage, LINE WORKS notification, status dashboard, DB backups, migration and concurrency tests. Do not collect TikTok passwords or API tokens.
6. Execute tests and record results. `tests/test_manual_posting.py` uses synthetic bytes and is a registry unit test, NOT a real MP4 quality test or real TikTok posting test.

## Run unit tests
`python -m unittest discover -s tests -p test_manual_posting.py`

## Safety
No TikTok API or automatic posting. Do not upload or deliver videos until all production gates pass. PR is draft and main remains unchanged.
