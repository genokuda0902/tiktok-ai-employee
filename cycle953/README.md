# cycle953 — cinematic human + robot illustration (PRIVATE HUMAN REVIEW ONLY)

## Distinct improvement over cycle952
Cycle952 repaired a caption/active-step mismatch in scene02's static UI. This cycle **replaces the entire upper scene02 (2.90–5.80s, 87 frames)** with a generated cinematic human+robot illustration from the user's Library, subtle 1.025x camera push-in and three sequential task examples. It retains the original burned Japanese subtitle strip and AAC audio. This is an **illustration**, not a recording of actual ChatGPT/Excel operation. The inserted scene says "イメージ映像 / 架空の作業例".

This makes one scene more visually varied but is not a 16-shot cinematic reproduction of the user's reference.

## Verified local private deliverable
- MP4: cycle953_CINEMATIC_HUMAN_ROBOT_JP_REVIEW_ONLY.mp4
- Source cycle952 MP4 SHA256: 60f40686707c510f293be2a65f52d65e4b78cd2c8a8ca8bb9de38a69aa916003
- Generated Library image SHA256: b3f82d1a0d02b30966840af80e114d43fb922e24c8f424e5ccfdb8078209bbaf (not committed)
- Output MP4 SHA256: bc3db2e24d13dc93c64c9cc556b6319c23177135c7ddf56dedf389e21832171b
- 1080x1920 H264 30fps 691 frames, 23.033333s, AAC 48kHz stereo.
- Full A/V decode PASS; AAC ADTS SHA256 identical to source 37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27.
- 87 modified frames. Mean upper-region pixel difference 42.442 (1/8 downsample); max mean caption-strip difference 1.177/255, outside edit window 1.789/255 (re-encoding).
- Local 24 synthetic tests PASS; full MP4 technical QA PASS. CI tests code and synthetic frames only; private full MP4 is not on GitHub.
- Ten genre configurations present, but **only ai_work scene/asset geometry reviewed and rendered**. Other genres fail closed pending asset and layout review.

## Reproduction (private local inputs required)
python cycle953/cinematic_scene.py --source /private/cycle952.mp4 --asset /private/library-generated-illustration.png --output /private/cycle953.mp4 --manifest /private/private_manifest.json --qa /private/qa953.json

Manifest fields required: genre, source_sha256, asset_sha256, asset_origin=user_library_generated_image, asset_review_only=true, publication_approved=false, geometry_reviewed=true, source_scene=2, caption="まず、繰り返している作業を書き出そう。".

python -m pytest -q cycle953/test_cinematic_scene.py

python cycle953/verify_output.py /private/cycle952.mp4 /private/cycle953.mp4 --json /private/qa953_full.json

No source MP4, user Library image, private manifest, or confidential media committed. **Do not upload private media to this public repo.**

## Research and remaining gaps
- Consulted accessible summaries of TikTok市場分析/TikTok動画研究: hook in 0–1.5s, 15–25s, short meaningful cuts, real operations, Before/After, readable Japanese captions, manual employee-reviewed posting. Full original chat/task transcripts inaccessible.
- Directly inspected user's ChatGPT×Excel時短術16コマ絵コンテ.png (16 storyboard panels with human/robot, UI, chart, CTA). Original v33 MP4 unavailable for direct side-by-side comparison.
- Checked main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, open PRs, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md and src/build_daily.py (still silent). The original v33 renderer remains unrecovered.
- **Unverified:** independent Japanese ASR, pronunciation, semantic/timing match of speech to captions, source image rights for publication, smartphone playback, employee approval, subjective quality, actual GitHub Actions charges.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, automatic posting, paid service, external confidential-media upload, or public release.
