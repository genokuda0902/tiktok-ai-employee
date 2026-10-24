# cycle812 — three-beat opening hook (REVIEW ONLY)

## Change from cycle811

The opening `WHAT → WHY → HOW` card was static. Replace only frames **0–89**
(0.0–3.0 s) with an original, fully opaque animated `目的 → 原因 → 行動`
card. Steps activate at frames **0, 21, 42**, a light streak moves across the
card, and the progress indicator advances each frame. Existing upper heading,
Japanese bottom subtitle, remaining 628 frames, and inherited Japanese AAC
stream are preserved. A single template supports ten genres with validated
accent colors and no real employee/customer data.

## Reproduction

Local dependencies: free Pillow, FFmpeg and a Noto CJK font. Run:

```bash
PYTHONPATH=quality/cycle812 python -m unittest discover -s quality/cycle812 -p 'test_*.py' -v
python quality/cycle812/kinetic_hook.py \
  --source cycle811_ACTION_CARD_NO_GHOST_REVIEW_ONLY.mp4 \
  --output cycle812_KINETIC_QUESTION_REVIEW_ONLY.mp4
ffmpeg -v error -xerror -i cycle812_KINETIC_QUESTION_REVIEW_ONLY.mp4 -f null -
```

GitHub CI uses *synthetic color and tone only*. The private full MP4 and its
inherited Japanese voice are **not** committed or uploaded to public GitHub.

## Provenance, limitations and gates

- Checked main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, `PROJECT_HANDOFF.md`,
  `recovery/v33/RECOVERY_STATUS.md`, and unmerged PRs #115 and #116.
- Prior research summaries of `TikTok市場分析` and `TikTok動画研究` consulted.
  Full task/chat research was unavailable.
- User's `ChatGPT×Excel時短術16コマ絵コンテ.png` inspected directly. Original
  v33 MP4 (31.553 s reference) was unavailable for direct comparison.
- This is **not** original v33 code and does not achieve the reference's
  photographic/cinematic robot, actual spreadsheet demo, or 3D quality.
- Japanese narration was **inherited** and the AAC elementary stream is
  verified identical to cycle811; independent Japanese ASR and subtitle
  semantic/word alignment were **not** tested.
- Rights, employee approval and real-device playback are **unverified**.
- `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`; no automatic TikTok posting,
  no merge, no paid service or production delivery.

Next: approved image-first footage and independent speech/caption review.