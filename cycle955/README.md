# cycle955 — Prompt-template semantic scene repair (PRIVATE REVIEW ONLY)

## Distinct improvement over cycle953
Scene07 previously showed three generic reuse categories while the existing Japanese subtitle said “使える指示は、テンプレートに残す。” This cycle changes **only scene07 (17.4–20.3s, 87 frames)** into an illustrated reusable prompt template with three timed beats: 保存 → 入れ替え → 再利用. It displays the variable placeholders {対象}, {条件}, {形式}, and labels the UI as fictional. It is **not a real ChatGPT screen recording**. The existing burned-in subtitle strip (y>=1490) and original Japanese AAC stream are preserved.

This is a reimplementation, not original v33 source. The 16-panel reference is more diverse and cinematic; no quality parity or publication approval is claimed. The prior cycle953 introduced a human+robot illustration in scene02; this cycle addresses scene07's *meaning/visual alignment*, not another zoom/blur effect. Parallel cycle954 PR #352's scene03 depth-focus was left untouched.

## Reproduction
The private input is exact cycle953 review MP4 SHA256 bc3db2e24d13dc93c64c9cc556b6319c23177135c7ddf56dedf389e21832171b, **not committed to GitHub**. Requires Python 3.11, numpy, Pillow, OpenCV, ffmpeg and Noto CJK font.

    python -m pytest -q cycle955/test_template_scene.py
    python cycle955/template_scene.py --source /private/cycle953.mp4 --output /private/cycle955.mp4 --qa /private/qa955.json

Ten genre label triplets are defined; only ai_work layout/media are approved for **private review**; other genres fail closed.

## Private output verified locally
- Filename: cycle955_TEMPLATE_REUSE_JP_REVIEW_ONLY.mp4 (private ChatGPT attachment, NOT uploaded to public GitHub).
- SHA256: 24af228e2842a53e124cdd8f0b329c10fd3399dba36f0734c500d3597f35e223.
- H.264 1080×1920 30fps, 691 frames / 23.033333 seconds, AAC 48kHz stereo.
- Full video/audio decode PASS; inherited AAC elementary ADTS SHA256 exactly preserved: 37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27.
- 87/87 edited scene frames have mean pixel difference >5; scene upper-region mean difference 52.9313 / 255 (1/8 sampling).
- Protected subtitle region y>=1490 maximum per-frame mean pixel difference 1.5347 / 255; outside-scene max 1.954 / 255 due to H.264 recompression.
- 16 local synthetic tests PASS. CI runs synthetic code/tests, **not private MP4**. Smartphone playback and independent Japanese ASR remain unverified.

## Research, references and safety
- Consulted accessible summaries of TikTok市場分析 and TikTok動画研究: 0–1.5s hook, concrete real UI, Before/After, purposeful cuts, readable Japanese captions, employee-reviewed manual posting.
- Directly inspected the user's ChatGPT×Excel時短術16コマ絵コンテ.png from Library (16 panels, robot/human, real-app-looking UI, graphs, CTA). Full research transcripts and original v33 MP4 were unavailable for direct side-by-side comparison.
- Verified main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, open PRs #351/#352 and others, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md and src/build_daily.py (silent -an output).
- Remaining gaps: independent Japanese speech transcription, pronunciation/caption timing, original v33 source recovery, reference visual parity, inherited media publication rights, employee approval, smartphone playback, actual Actions billing.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, public media upload, automatic posting, paid services, or confidential material in the repository.
