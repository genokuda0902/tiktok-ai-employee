# cycle998 verified review-only result — 2026-10-30 JST

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, no auto-post, no paid service.

## Research and references
- Accessible summaries of past \`TikTok市場分析\` and \`TikTok動画研究\`: 0–1.5s hook, real UI, clear Before/After, readable Japanese subtitles, manual employee approval.
- User-provided \`AI×会社員の1日：未来を変える32秒.png\` was directly inspected: 16 panels / 32s, cinematic blue/orange human/laptop/ChatGPT/Excel, UI, robot, city, CTA. Separate ChatGPT×Excel storyboard previously documented at ~36s. Full research chat transcripts and original v33 MP4 were not accessible.
- main at inspection \`18e084c38db0dc55db7dfc0532b9451b1167f2aa\`; reviewed open PR #397 (cycle996), parallel #398 (cycle997 FFT), PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, cycle996 code and tests. Branch stacked on unmerged #397; no merge.

## Distinct change vs cycle996
- cycle996 used 5-frame cross-dissolves at 174,348,522; direct frame inspection showed obvious double-exposed robot/face/UI/text at cuts.
- cycle998 renders each frame from exactly one source frame, adjusting artwork ROI luma with 6-frame ramps on each side. Input is the pre-dissolve cycle994 private MP4, preserving all earlier scene content. 10-genre fail-closed gate, 7 unit tests and 2-second synthetic-only CI smoke render.
- Measured single-frame central-luma jumps at cuts:
  - frame 174: source 127.501, cycle996 36.732, cycle998 **16.444** (87.10% reduction vs source)
  - frame 348: source 115.408, cycle996 36.101, cycle998 **17.099** (85.18% reduction)
  - frame 522: source 84.562, cycle996 24.653, cycle998 **12.867** (84.78% reduction)
- These are numerical discontinuities, not human-perceived quality guarantees. cycle998 may create short exposure pulses and still needs human visual review.

## Real local MP4, never committed to public GitHub
- \`cycle998_GHOST_FREE_FLASH_GUARD_JP_REVIEW_ONLY.mp4\` SHA256 \`4f62c4856de8dac0d643449098a5db26b9dc725d594bd1dd1b43990c9fe7fbf6\`.
- 1080×1920, H264, 30fps, 691 frames, 23.033333s, Japanese-tagged AAC 48kHz and mov_text Japanese subtitles.
- Full A/V decode PASS. Audio and subtitle elementary stream hashes identical across cycle994, cycle996, cycle998. All 691 frames caption-region mean absolute pixel difference max 1.1827/255, average 0.9207/255 (re-encode differences, ROI untouched in pixel processing).
- Local unit tests 7 PASS. Local synthetic 2s/60-frame renderer+decode test PASS (sine tone is not Japanese speech).
- Independent Japanese ASR/transcript-vs-subtitle semantic alignment, phone playback, public asset rights, staff approval, actual GitHub Actions charges NOT verified.

## Reference gap and next
- 8 scenes/23s vs 16 panels/32s reference (and separate ~36s storyboard), still short of cinematic person/robot continuity and real ChatGPT-to-Excel interaction.
- Prioritize independent Japanese ASR/subtitle verification and safe-licensed multi-scene material. No claims of v33 parity or publication quality.
