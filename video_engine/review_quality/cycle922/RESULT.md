# cycle922 — Speech activity review timeline (2026-10-28 JST)

Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No auto-post, no merge, no paid API, no private MP4 in this public repository.

## Source checks
- main at review start: 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Open PR #301 (cycle920), #302 (cycle921), plus other unmerged review PRs checked; this is an independent main-based draft branch.
- PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, archive/v33/README.md and current render source reviewed.
- Past TikTok市場分析 and TikTok動画研究 conclusions: hook 0–1.5s, concise cuts, authentic UI, Before/After, legible Japanese captions, manual posting after approval. Full original chat text unavailable.
- User's 16-panel ChatGPT×Excel storyboard image was directly inspected from Library: realistic robot/person, ChatGPT+Excel UI, diverse shots, subtitles, CTA. Reference original v33 MP4 unavailable; no frame-by-frame parity claim.

## Delta versus cycle920
- cycle920: 8 audio-energy camera accents, max 5.5% zoom.
- cycle922: replaces the existing lower progress bar with a 23-second VAD-derived speech activity map, scene separators, and moving speech/silence playhead. Leaves burned Japanese caption glyphs and existing waveform untouched.
- New fail-closed checks for missing audio, too little VAD activity per scene, absent visual caption ink, unexpected geometry and missing review-only filename. VAD is only an acoustic heuristic, not independent Japanese transcription or caption semantic matching.
- Supports 10 genre configuration names. Only ai_work was rendered.

## Actual locally verified private MP4
- File: cycle922_SPEECH_TIMELINE_REVIEW_ONLY.mp4 (provided only in ChatGPT, not GitHub).
- Input cycle920 SHA256: 288413797067240e98db15becfccd1efd8cc9b8cbc4aaf34d2b001e4f836b74d.
- Output SHA256: 55df9ea3a14d7fc92b75b92ada1139a8d1329d26f448377c46f3b042af58fc38.
- 1080×1920, H.264 30 fps, 691 frames, 23.033333s, Japanese AAC 48kHz (inherited, not re-recorded).
- Full video/audio decode PASS. AAC ADTS elementary-stream SHA256 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9 identical to cycle920.
- Original Japanese caption-text region: maximum mean pixel difference 1.586 (all 691 frames, sampled resized ROI), mean 1.487. All 691 frames changed in intended progress-track region; track mean pixel difference 36.052.
- 8 scene VAD-activity fractions: 0.8333, 0.8144, 0.8454, 0.8750, 0.9072, 0.8969, 0.8767, 0.8230. This does NOT prove all activity is spoken Japanese.
- Local unit tests: 13/13 PASS.
- Independent Japanese ASR, word-level subtitle timing, voice pronunciation, original v33 comparison, smartphone playback, material commercial rights, employee approval, and actual GitHub Actions billing: NOT VERIFIED.

## Reproduction (approved local review assets only)
Requirements: local FFmpeg, Python 3.11+, numpy, opencv-python, webrtcvad (no paid services). Supply your own authorized review-only MP4:
python speech_timeline_cycle922.py --input approved_source.mp4 --output cycle922_SPEECH_TIMELINE_REVIEW_ONLY.mp4 --manifest manifest922.json --genre ai_work

This is a reimplementation, not the recovered v33 generator. The public CI tests pure code, policies, and synthetic conditions; it does NOT inspect the private finished MP4.

## Next
Priority: acquire an authorized offline Japanese ASR model and compare transcript with each displayed subtitle at scene/word timing, with a fail-closed gate. Then improve cinematic 16-scene image-first diversity, smartphone review, rights and employee sign-off before any manual TikTok post.
