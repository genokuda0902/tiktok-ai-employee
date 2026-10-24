# cycle810 — animated result evidence (PRIVATE REVIEW ONLY)

2026-10-24 JST. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Reimplementation, NOT original v33 source. No merge, posting, public release, billing or confidential uploads.

## Research and reference provenance
- Latest main SHA: 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Read PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, quality/cycle809/README.md; inspected open Draft PR #112 and parallel photographic PR #111.
- TikTok市場分析 / TikTok動画研究: prior research summaries consulted, but complete task/chat transcripts inaccessible. Guidance: first 1.5 s hook, one idea/video, image-first, short scenes and readable Japanese captions.
- User-supplied ChatGPT×Excel時短術16コマ絵コンテ.png inspected directly from Library this cycle. Original reference v33 MP4 unavailable, so no direct comparison. Storyboard uses real demos, visual proof, Before/After and cinematic imagery.
- Read AI JITAN STUDIO quality instruction document: 1080×1920, no invented real metrics, captions in safe area, manual posting only.

## Change vs cycle809
Scene 8, frames 628–717 (20.933–23.933s): static four-bar chart becomes animated fictional weekly comparison, 8→20, +150% arithmetic, explicit 架空の例 badge and high-contrast Japanese labels. Ten-genre configuration uses fictional examples and rejects unsafe labels. Not a real employee or company result. Existing Japanese narration and subtitles are inherited unchanged; scene 2 simulated goal entry remains unchanged.

## Reproduce
Python 3.11, Pillow==11.3.0, ffmpeg, ffprobe, Noto CJK Bold font (CYCLE810_FONT override).
- python -m unittest discover -s quality/cycle810 -p 'test_*.py' -v
- python quality/cycle810/result_growth.py --source cycle809_GOAL_UI_REVIEW_ONLY.mp4 --output review_output/cycle810_RESULT_GROWTH_REVIEW_ONLY.mp4
- ffmpeg -v error -xerror -i review_output/cycle810_RESULT_GROWTH_REVIEW_ONLY.mp4 -f null -

Do not upload the rights-unapproved Japanese voice source or output to public GitHub. CI deliberately uses synthetic sine-tone audio and a blank synthetic color video; CI does NOT verify Japanese speech.

## Verified local QA
11/11 unit tests PASS; 1080x1920 H.264 30fps, 718 frames, 23.933333 s, AAC 48kHz, full A/V decode PASS.
Output SHA256: 9a13129e3fe768385d6d01971f5443f09f60e31b9986cf5c50fe397fd8eaa7de
Input cycle809 SHA256: 48c6bd1b0b3770311e00cec62293dd3e570431bdd0ea44b2c89bb71e29bbac73
Preserved AAC ADTS SHA256: d9f3e2c986b32eda17ee64c3c89fc2ec2d428121715076c6d686edde85cd9093
Final Japanese-narrated review MP4 is available privately in ChatGPT, not in this public repository.

Unverified: independent Japanese ASR transcription, semantic caption sync, voice naturalness, source voice/image rights, smartphone playback, original v33 MP4 direct comparison and employee approval. NO AUTO POST.
