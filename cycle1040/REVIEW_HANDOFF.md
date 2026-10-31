# cycle1040 — original robot opening / REVIEW ONLY

## Unique improvement from cycle1038
- Replaces only the first 45 frames (0.000–1.500s) of the previous 23.033s AI-work MP4 with an **original, procedurally drawn** robot mascot: blinking eyes, waving arm, halo/HUD and bold Japanese question.
- Keeps the original 1.5–23.033s spreadsheet proof, operation tutorial, three-shot recap and CTA. Uses a direct cut at 1.5s after rejecting a ghosted alpha transition in the first local trial.
- The previous cycle1038 changed only the final 2.733s; this is a distinct opening/character-variety improvement.
- Reusable ten-genre color palettes, but only the `ai_work` private source passes approval gating; other genres fail closed.

## Local actual MP4 evidence (NOT uploaded to public GitHub)
- Input cycle1038 SHA-256: `64971783c4bc51007cdb65a09014952a744a1fad8a87ce0f8bbf7dccef571623`.
- Output cycle1040 SHA-256: `ac8cc088a379d21903b2bef186c451aa4d2b3acbe937c30cffb0b796d28702b4`.
- 23.033333s / 691 frames, 1080x1920 H.264 30fps; AAC 48kHz Japanese-tagged, full A/V decode PASS.
- Audio ADTS SHA unchanged: `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e`.
- All 691 frames compared at 270x480: lower-caption ROI max mean absolute delta **1.1012/255**; changed first-45-frame upper-region mean **52.8672/255**; after frame 45 upper-region max **1.655/255** (encoding drift). 8 SRT cues non-overlapping, ending at 23.033s.
- 8 audio cue segments contain signal (RMS -18.37 to -20.02 dBFS), **not** proof of speech content; source contains background audio.
- 11 local unit tests PASS. Synthetic CI does not validate the actual private 23s MP4.

## Research and comparison
- Inspected user's original `ChatGPT×Excel時短術16コマ絵コンテ.png` directly from Library: 16 scenes/~36s with a cinematic robot, person in trouble, ChatGPT→Excel operation, chart, Before/After, CTA and ending.
- Accessible summaries of `TikTok市場分析` / `TikTok動画研究`: 0–1.5s hook, one message, real UI, short action cuts, Before/After, readable captions, save CTA and employee manual approval.
- Full original research chat/task transcripts and original `AI_Jitan_v33_REAL_SPREADSHEET(1).mp4` are NOT accessible. No claim of v33 parity. Current robot is flat original vector art, **not** the cinematic 3D robot in the storyboard.
- Latest main checked: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`. Inspected `PROJECT_HANDOFF.md` and `recovery/v33/RECOVERY_STATUS.md`, existing cycle1038 code, PR #439 and parallel PR #440 (not modified).
- This work is a reimplementation, not recovered original v33 code.

## Reproduce offline with private source
```bash
python cycle1040/source/mascot_intro.py --source PRIVATE_CYCLE1038.mp4 --dest PRIVATE_CYCLE1040.mp4 --report qa.json --expected-sha 64971783c4bc51007cdb65a09014952a744a1fad8a87ce0f8bbf7dccef571623 --review-only
python cycle1040/source/verify_review.py --source PRIVATE_CYCLE1038.mp4 --dest PRIVATE_CYCLE1040.mp4 --srt captions_review_only.srt --report roi_qa.json
```

## Gates still missing
- No independent Japanese ASR; spoken meaning, pronunciation, and precise caption timing not independently verified.
- Inherited media publication rights, real-phone playback, employee approval, original reference v33 quality, and actual GitHub Actions billing are unverified.
- `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`. No merge, no auto-post, no public upload of private video/audio, no paid contract.
- Next: independent Japanese speech/caption alignment, then approved high-quality image-first cinematic character assets and a new-topic review render.
