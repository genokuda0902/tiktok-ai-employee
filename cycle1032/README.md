# cycle1032 — repair missing June chart (review only)

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. This is a reimplementation, NOT original v33 code. No merge, auto-post, public media upload or paid service.

## Distinct improvement from cycle1030
The scene05 chart claimed to compare 4–6月 and displayed totals A46/B29, but June bars were blank. This cycle replaces only frames 342–428 (11.40–14.30s) with all six **fictional** values:
- 4月: A12/B8; 5月: A16/B9; 6月: A18/B12
- Sum A=12+16+18=46, B=8+9+12=29.
- Three sequential month highlight beats, explicit “架空の例” label, no overlay on subtitle y>=1490.

The chart renderer accepts 10 genre identifiers and refuses missing fictional-data provenance. A complete MP4 was rendered for ai_work ONLY. Other genres need their own approved source and data. The private input video/audio/stills/storyboard are never committed.

## Reproduction with private cycle1030 input
Requirements: Python3, Pillow, ffmpeg/ffprobe, fonts-noto-cjk, pytest. No network/API required.

    python3 -m pytest -q cycle1032/tests
    python3 cycle1032/source/three_month_evidence.py --source /PRIVATE/cycle1030_CORRECTION_PROOF_JP_REVIEW_ONLY.mp4 --output /PRIVATE/cycle1032_REVIEW_ONLY.mp4 --report /PRIVATE/qa.json --expected-source-sha d6bdaf8339cbce07c551670b828ef07c74175d654979b248b42df2eccdd2adf3 --genre ai_work --review-only

CI uses a synthetic 2-second A/V clip only. It does not access the private completed video.

## References / unverified gates
Consulted accessible summaries of TikTok市場分析 and TikTok動画研究: immediate hook, purposeful cuts, practical UI, Before/After, readable captions, manual employee approval. Full original research chats unavailable. Directly inspected user's ChatGPT×Excel時短術16コマ絵コンテ.png from Library (16 panels, ~36s; cinematic robot/person, ChatGPT/Excel demo, CTA). Original v33 MP4 inaccessible; no quality-equivalence claim.

Verified main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, open PR #431 and parallel #432, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, src/build_daily.py (still silent -an), and prior cycle1030 code. Audio stream equality does NOT verify Japanese spoken text, pronunciation, or subtitle timing. Rights, phone playback, employee approval, reference parity, retention and actual Actions billing remain unverified.

Next: independent Japanese speech/caption audit using offline ASR if available, otherwise eight timecoded listening WAV clips/checklist; then approved cinematic imagery to narrow the reference gap.
