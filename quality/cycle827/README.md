# cycle827 — Japanese fictional source-to-output proof (REVIEW ONLY)

## Change from cycle826

The cycle826 animated prompt demo at 9.687–12.917 seconds is retained. The following 12.917–16.150s scene used a static three-item checklist. Now it shows a source-data cross-check: **fictional A=12, B=8 → 12+8=20 → verified**. This is a truth-checkable arithmetic example, **not** a real service screenshot, real employee/customer data, verified time saving, or a business result. The same overlay renderer and palette supports all ten genres; the complete reviewed MP4 is ai_work only.

## Reproduction

Free FFmpeg/ffprobe, Python 3.11, Pillow and NotoSansCJK fonts:

```bash
python -m unittest discover -s quality/cycle827 -p 'test_*.py' -v
python quality/cycle827/proof827.py --source cycle826_AI_WORK_LIVE_PROMPT_JAPANESE_REVIEW_ONLY.mp4 --output cycle827_AI_WORK_SOURCE_PROOF_JAPANESE_REVIEW_ONLY.mp4 --genre ai_work --report qa827.json
ffmpeg -v error -xerror -i cycle827_AI_WORK_SOURCE_PROOF_JAPANESE_REVIEW_ONLY.mp4 -f null -
```

CI independently builds a full 25.833s Japanese Open JTalk narrated video from original fictional assets, retaining 24 Japanese caption states. It also checks TTS input text versus subtitle text. The original cycle826 local MP4 and inherited voice are **not committed**. CI/local visuals may differ because their earlier source scenes differ; the cycle827 overlay is shared.

## Provenance, comparison, boundaries

- Main at start: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`; stacked on Draft PR #143, while #144 remains parallel and unmerged. Read `PROJECT_HANDOFF.md` and `recovery/v33/RECOVERY_STATUS.md`.
- Consulted prior summaries of `TikTok市場分析` and `TikTok動画研究`; full task/chat transcripts unavailable. User's `ChatGPT×Excel時短術16コマ絵コンテ.png` was directly inspected. Original v33 reference MP4 was unavailable for direct comparison.
- Local 25.833s video: H264 1080x1920, 30fps, 775 frames, AAC 48kHz, full A/V decode PASS, inherited audio bitstream unchanged. Earlier locally generated review variant SHA256 `341c441baba0e9ce21f7e75a00720c0a9aaab7328418ee32204a2f580c7cb6d0` (note: local variant may differ visually from CI source).
- Independent transcription of audible Japanese, pronunciation, word-level sync, smartphone playback, source-asset publication rights and employee approval **not verified**. Technical QA is not a publication-quality judgment.
- No merge, purchase, personal data, public distribution, TikTok auto-post, or approval bypass. `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`.

Next: independently audit Japanese speech content/synchronization and move beyond simulated UI to approved image-led cinematic work scenes, then compare to original v33 when accessible.
