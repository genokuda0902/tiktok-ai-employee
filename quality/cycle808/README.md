# cycle808 — kinetic action beats (review only)

2026-10-24 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, no posting, no paid services. Original reimplementation, not recovered v33 source.

## Research and provenance

- Checked latest main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, open PR #108 and parallel #106/#107.
- Prior `TikTok市場分析` and `TikTok動画研究` summaries: clear first 1.5 s, short visual scenes, one idea per video, demonstrations/Before-After, Japanese subtitles in safe area, human approval. Full task/chat transcripts were **not accessible**.
- User-provided `AI時短ラボ 16話構成ストーリーボード.png` visually inspected. Original v33 MP4 was not accessible. No quality parity claim.
- Source: cycle807 local MP4 SHA-256 `3a9b1b8824ac11d7b345592718808db7e5458fb15b36d99faa7810cbbf9550a8`. Voice rights and independent spoken-word alignment remain unverified.

## One distinct improvement

Previously scene 6 (14.83–17.97 s) showed a static generic `誰が / 何を / いつまで` checklist. The new overlay presents a **three-step animated action plan** with numbered beats, concrete example actions and a progress cue. This is different from cycle807's scene-3 KPI animation. Frames 445–538 only are changed. Original audio and caption remain untouched.

The alpha overlay stays in x=130..950, y=742..1302, outside the existing Japanese caption at ~y=1412. Ten-genre palette and validation are included; one actual sales_business video was generated. No private imagery or company metrics were added.

## Reproduce

```bash
python -m pip install Pillow==11.3.0
python -m unittest discover -s quality/cycle808 -p 'test_*.py' -v
python quality/cycle808/action_sequence.py --source cycle807_KPI_EVIDENCE_REVIEW_ONLY.mp4 --output review_output/cycle808_ACTION_BEATS_REVIEW_ONLY.mp4
ffmpeg -v error -xerror -i review_output/cycle808_ACTION_BEATS_REVIEW_ONLY.mp4 -f null -
```

Requires FFmpeg, ffprobe and Japanese Noto Sans Bold font (`CYCLE808_FONT` override).

## Verification and safety

- Local: 14 tests passed; 1080×1920, 30 fps, 718 frames, 23.933333 s, H.264/AAC 48kHz, full A/V decode PASS.
- Original AAC elementary bitstream preserved, SHA-256 `d9f3e2c986b32eda17ee64c3c89fc2ec2d428121715076c6d686edde85cd9093`.
- Local output SHA-256 `c3ed27226338159ec6a537bbdab4740a79087d50be71f3a8000117561bb5ec2a`.
- CI uses **synthetic video and sine-wave audio**, not rights-unapproved Japanese voice, and uploads only QA JSON metadata. CI does not establish Japanese speech correctness.
- Independent Japanese ASR, naturalness, source voice licensing, original v33 direct comparison, smartphone playback, and employee approval are NOT VERIFIED.
- Employee approval before manual posting only; no automatic TikTok posting, merge, or billing.
