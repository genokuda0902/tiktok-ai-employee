# cycle850 — Three-beat genuine UI close-ups (REVIEW ONLY)

**Baseline:** cycle849 PR #186 (unmerged), local source MP4 SHA256 `a282d4dc231cc140ee0813e20f4830c1dfa9450fdd83a64a7fb1033f23062266`.

## Improvement, not a v33 recreation

In scene 05, 86 frames (336–421, 11.20–14.07 seconds) previously displayed a near-static full spreadsheet view. This iteration uses the existing **fictional** local LibreOffice Calc recording to build three visually distinct micro-shots: `全体を見る → 数字を追う → 合計を確認`. The crop aspect ratio is preserved; hard cuts avoid double-exposed spreadsheet text. The upper scene heading, burned-in bottom Japanese captions, and original AAC stream are retained. One reusable shot/genre template supports ten genres, but only `ai_work` was rendered as a full review MP4.

## Local reproduction (no external services)

```bash
PYTHONPATH=cycle850 python -m unittest discover -s cycle850 -p 'test_*.py' -v
python cycle850/three_beat_capture.py --source /private/review-only-cycle849.mp4 --capture /private/fictional-calc-capture.mp4 --output /private/cycle850-review.mp4 --report /private/cycle850-qa.json
ffmpeg -v error -xerror -i /private/cycle850-review.mp4 -f null -
```

Inputs **must stay local**, must be independently privacy/licensing reviewed before any publication, and must match the fail-closed manifest hashes. This repository stores only code, tests, workflow, and documentation. GitHub CI uses **synthetic** color/tone and a generated test UI, never the Japanese finished video.

## Verified local result and remaining gates

- 1080×1920 H.264 30fps, 691 frames, 23.033s, AAC 48kHz; 86 edited frames, two micro-cuts at 365 and 394.
- Audio AAC elementary stream identical to cycle849. FFmpeg full AV decode PASS; 13 local unit tests PASS.
- The finished review MP4 is available **only** via the ChatGPT run attachment (not in this public repo).
- Prior `TikTok市場分析` / `TikTok動画研究` summaries and the user's 16-panel storyboard consulted. Full chats and original v33 MP4 remain inaccessible for direct comparison. Storyboard is 16 panels vs this template's eight major scenes; cinema-grade actors/lighting remain missing. Handoff specifically cancels the animated 3D robot scope.
- Independent Japanese transcription, pronunciation, semantic/word-level subtitle alignment, rights approval, employee approval and phone playback are **NOT** verified.
- `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`; no merge, posting, external upload, or paid contract.

Next: verify spoken Japanese and subtitle timing independently; then move toward approved photo-first imagery rather than endlessly adjusting transitions.