# cycle817 — Root-cause depth animation (2026-10-24 JST)

## Concrete delta from cycle816
- cycle816 introduced animated BEFORE → focus → AFTER at frames 270–359 (9–12s).
- cycle817 changes **only frames 360–449 (12–15s)**: a previously static 3×「なぜ？」 panel becomes a progressive three-layer WHY investigation with connected arrows, step highlighting and reveal. This is a generic educational example, not a real-world diagnosis or performance claim.
- Ten genre accent keys, Japanese font and caption-safe opaque panel are shared. No third-party or confidential images were introduced.
- All other scenes are retained from the cycle816 private review source, subject to H.264 re-encoding differences.

## Local reproduction
```bash
python -m pip install pillow
PYTHONPATH=quality/cycle817 python -m unittest discover -s quality/cycle817 -p 'test_*.py' -v
python quality/cycle817/root_cause_depth.py \
  --source /private/cycle816_PRIORITY_REVEAL_REVIEW_ONLY.mp4 \
  --output /private/cycle817_ROOT_CAUSE_DEPTH_REVIEW_ONLY.mp4 \
  --genre sales_business --fictional-example
ffmpeg -v error -xerror -i /private/cycle817_ROOT_CAUSE_DEPTH_REVIEW_ONLY.mp4 -f null -
```

## Verified local QA
- Source SHA-256: `a516461bee7e77c134955fc9d8c46e3a1167fd1028228a391e7d20260e24baaf`.
- New review MP4 SHA-256: `13d57b63743cc014edfff48a9c596eb56f1305d1a74d1d2ea2e0c5e2998bf009`.
- 1080×1920, 30fps, 718 frames, 23.933333 seconds, H.264 video, AAC 48kHz audio; complete video+audio decode PASS.
- AAC ADTS stream identical to cycle816 (inherited Japanese audio, **not independently transcribed**).
- 13 local unittest cases PASS; visual spot-check of changed 12.2/13.1/14.3-second frames.
- Mean RGB pixel delta at 12.5/13.5/14.5s: 7.5547 / 8.8711 / 9.9562; unchanged 4.5/10.5/19.5s: 1.1303 / 1.0357 / 1.1140 (re-encoding).
- Local review MP4 delivered in conversation sandbox, **not** committed to public GitHub because inherited voice/media rights are not independently cleared. Public CI only renders synthetic color+tone video, not the Japanese review video.

## Research and quality limitations
- Used earlier confirmed summaries of `TikTok市場分析` and `TikTok動画研究`: fast hook, short cuts, demonstration, Before/After, readable captions, retention learning, human review. Full original task/chat transcripts inaccessible.
- Directly inspected user-provided 16-panel `AI時短ラボ 16話構成ストーリーボード.png` in Library. Original reference v33 MP4 inaccessible, so no direct comparison or parity claim.
- Reference storyboard includes cinematic photo/3D lighting, character and realistic software interactions. The review video remains predominantly flat dark UI cards and does **not** match reference visual quality.
- Japanese speech content/naturalness and semantic subtitle match, inherited media rights, phone playback and employee approval are NOT verified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid services, confidential uploads or automatic posting.
