# Drive delivery gate (2026-09-19)

Status: BLOCKED, not production ready. This document is not implementation or evidence of upload.

Source: Actions artifact 10537910824 (`pi5-v9-review-only`) from run 35321564044. The artifact is a ZIP; extract `pi5_review_20s.mp4` and verify SHA-256 `c5b0bc27be175b9c990cb4ef91d63ef2c35d045ed890c95cb6c02d329c0ae472` before any delivery. This is a distinct integration-test video, not the original frozen local video. QUALITY_NOT_APPROVED / REVIEW_ONLY / posting_allowed=false.

Target: restricted Drive folder ID `14rtOvwFKmycVO5Irq1X8QJ4-vgO2xUMk`. Folder creation and owner-only status were reported by agent ②; recheck permissions before upload. Never upload to TikTok or publish, merge PRs, expose credentials, or commit video bytes.

Blocking requirements: a supported authenticated Drive upload mechanism from an Actions runner, or a verified connector bridge that converts the extracted MP4 into a Drive-upload-compatible file reference. GitHub artifact ZIP references are NOT MP4 references. Do not upload the ZIP as if it were the MP4. Drive credentials are not known to be configured; do not invent a secret name or claim access.

Acceptance evidence: (1) exact source run/artifact ID and extracted MP4 SHA; (2) authenticated upload to the restricted folder with returned Drive file ID and verified restricted permissions; (3) download actual MP4 bytes back from Drive and compare SHA-256; (4) Actions run URL, relevant logs with secrets redacted, and file ID. Until all pass, Drive delivery remains incomplete. If credentials are missing, request the minimal owner-side configuration without asking the owner to paste credentials into chat.
