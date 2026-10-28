# cycle940 — scene-level Japanese narration matching (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No posting, merge, paid services, external private-media upload or commercial-use clearance.

## Distinct change from cycle939
cycle939 improved the video by enlarging weekly report cards in scene 02. This cycle leaves every H.264 frame, all on-screen graphics, and every burned Japanese subtitle **bitstream-identical** while applying bounded, scene-aware audio gain matching to the 8-scene Japanese narration. Scene gain offsets are capped at ±1.2 dB, with 240ms smoothstep transitions at cuts and -1 dBFS ceiling. The algorithm is shared across ten genre presets; only the AI-productivity review MP4 was rendered.

## Private local verification
- Output: cycle940_SCENE_VOICE_LEVEL_JP_HUMAN_REVIEW.mp4; SHA256 1a95ba8cb07db2552ded77ea834c1ec957b6a59ddc29a899bb1fae524c9374d0.
- Source cycle939: SHA256 eeeb533effdb15620aceebca5b1be450065fceafa68ce1af95cabd2dc121eabd.
- 1080×1920 H.264, 30fps, 691 frames; AAC 48kHz mono; 23.033s. Full A/V decode PASS.
- H.264 elementary stream SHA256 equal, guaranteeing pixel-identical video and subtitles.
- Decoded active scene RMS spread: **1.207 dB → 0.260 dB** (79% reduction). Output decoded peak -1.020 dBFS. A/V RMS-envelope lag estimate 10ms (window size 10ms), correlation 0.983669.
- 14/14 local unit tests PASS. CI tests only the portable synthetic Python logic, **not** the private full Japanese MP4.
- The source video and audio have not been uploaded to GitHub. This is review-only.

## Reproduce locally (no paid APIs)
Requires local FFmpeg, Python 3 and NumPy. Use only an authorized private review source MP4.

    python cycle940/src/scene_voice_leveler.py --source PRIVATE_REVIEW.mp4 --output PRIVATE_OUTPUT.mp4 --report voice_level_report.json --genre ai_productivity
    python -m unittest discover -s cycle940/tests -v

## Research and limits
Accessible prior TikTok市場分析 and TikTok動画研究 summaries emphasized short hooks, purposeful scene changes, legible Japanese subtitles, real evidence, and human-approved manual posting. User's 16-panel ChatGPT×Excel storyboard has been described in previous accessible results. The original v33 reference MP4 and independent Japanese ASR model were not accessible. **Voice loudness consistency does not verify semantic subtitle matching, pronunciation, or listening preference.** Inherited media commercial rights, smartphone hardware playback, employee approval, and actual GitHub Actions billing remain unverified. No claim of reference-equivalent or post-ready quality.
