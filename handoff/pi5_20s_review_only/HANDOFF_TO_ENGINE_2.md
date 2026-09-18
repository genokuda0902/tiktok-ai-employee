# ① → ②: frozen integration-test artifact (NOT APPROVED)

Status: `QUALITY_NOT_APPROVED`; `REVIEW_ONLY`; `posting_allowed=false`; `human_approval_required=true`. Never upload to TikTok, publish, post or merge on the basis of this document. Drive storage is permitted only as a restricted integration test with appropriate access controls; no public sharing.

## ① source artifact, independently verified in local environment
- Name: `pi5_20s_REVIEW_ONLY.mp4`
- ①-local path: `/mnt/data/pi5_handoff_20s/pi5_20s_REVIEW_ONLY.mp4` (NOT a path accessible by ②)
- SHA-256: `97b89ecba37e93d3770c0f37beac0c4a2ad2c8456de6012dd3d64d0950450fe0`
- ffprobe: video 1080x1920; audio stream present; format duration 20.000000 seconds.
- ①-local handoff ZIP: `/mnt/data/pi5_handoff_20s/handoff_to_2_FROZEN_REVIEW_ONLY.zip` (not hosted in GitHub; no binary committed).
- Manifest: `/mnt/data/pi5_handoff_20s/handoff_manifest.json`.
- Quality issues: https://github.com/genokuda0902/tiktok-ai-employee/issues/22.

## ② required receipt procedure
1. Obtain the ZIP or MP4 via an authorized shared file-transfer channel. A path in ①'s `/mnt/data` does NOT constitute delivery to ②. Do not infer receipt from this spec.
2. Extract MP4 to ②-accessible storage and compute `sha256sum pi5_20s_REVIEW_ONLY.mp4`; require exact hash above. Run `ffprobe -v error -show_entries stream=codec_type,width,height -show_entries format=duration -of json pi5_20s_REVIEW_ONLY.mp4` and `ffmpeg -v error -xerror -i pi5_20s_REVIEW_ONLY.mp4 -f null -`.
3. Store the MP4 in a non-public Drive location with restricted permissions; record Drive file ID, size, SHA-256 of downloaded Drive bytes, uploader run URL, and timestamps. Do not mark delivery complete before byte-for-byte verification.
4. Return acknowledgement in issue #22 with ②'s durable file ID/path, checksum, ffprobe result, Drive file ID, and job/Actions URL. Only after acknowledgement may the handoff status change from `PENDING_RECEIPT` to `RECEIVED_FOR_INTEGRATION_TEST`.
5. Downstream metadata must preserve `QUALITY_NOT_APPROVED`, `REVIEW_ONLY`, `posting_allowed=false`, `human_approval_required=true`. No publication or automatic posting.

## ① execution record
Local source SHA-256 and ffprobe rechecked 2026-09-19 (JST). This documentation commit does NOT upload MP4, prove ② receipt, or establish Drive persistence. ② acknowledgement: PENDING. PR remains unmerged.
