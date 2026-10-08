# Video production v2: review-only evidence (2026-09-27 JST)

## Checkpoint that must not be overwritten

- Existing source run: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/36261124051
- Source commit `08d0f5c84822a43ee92947deb7d9357a5c7d6003`; Artifact `10912516118`; `video_e2e_test_0001_v1/video.mp4` inside artifact as `video.mp4`.
- Independent Engine ② receive SHA and producer SHA: `1da0077100794688c3fc898c1b89dd4680a313c4878d38fcced399400806ed7a`.
- Google Drive private review file `17KYfFDppLmPaIbNdrseudG32Z_v8JVG4`; connector upload, fresh readback, SHA, ffprobe and full decode succeeded. No public/domain permission observed. Connector operation is not unattended Actions delivery.

## Follow-up review-only artifacts

- Caption revision `revision-test-001`, same video ID, version 2, trace `trace_36261124051_10912516118`: Drive file `12U5_yR7uDbtnsYCrNPJY4I6ELnZL0n3z`, SHA `7cec8eddee9cfe0e94e3f607784c7ae7fb33c955cc3ad5ae22f2b945fd819d6a`. The later ASS safe-zone code change changes subsequent render hashes; do not associate this Drive file with a later test render SHA.
- Separate Japanese narration test ID `video_jp_review_0001`: Actions https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/36262287848, Artifact `10912987040`, SHA `9e1cbf5fb018efa14571c39f4631d984d92fdd86b477d95bf24d17a1c81d1939`, duration 22.254 s, 30fps, 1080x1920 H.264/AAC, full decode. Voice/BGM/SFX are separate tracks mixed into the output; BGM/SFX are synthetic test tones. Private Drive file `1w-ZmbAgYFBfRlHrqMsLH__NMnNgn5FHn`, SHA readback matched.
- Flow voice model is listed with a **custom licence** on https://hub.aivis-project.com/aivm-models/76a774e4-cc4d-4d8c-879e-8d2be3d30dad. Commercial publication permissions remain unverified. Human pronunciation and phone-screen review remain pending.

## Current system boundary

- The employee and posting logic from the unmerged feature branches is copied and adapted in this PR without merging them into main. Integration tests use an explicit fake identity; real Google ID tokens require a configured client ID and actual login. Fake authentication is not real employee authentication.
- The SQLite review state stores revisions, digests, Drive IDs, audit and analytics fixture records, preserving null separately from zero. It rejects publication of unapproved content. Analytics fixture results do not represent actual TikTok activity.
- The `drive_persist.py` adapter is parameterized but not exercised with Actions credentials. In an earlier isolated workflow, the selected Actions Drive identity failed folder lookup with `reason=notFound` (run 35735326695). The connected Drive connector has access and was used for verified manual transfer. Configure an approved private runner credential or the existing Apps Script HMAC gateway before claiming unattended Drive delivery.
- `SYSTEM_E2E_COMPLETE=NO`; `CONTENT_QUALITY_APPROVED=NO`. No PR merge and no TikTok upload.
