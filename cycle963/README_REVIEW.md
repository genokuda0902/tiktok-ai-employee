# cycle963 — original scene transition sound (review only)

Input: cycle962 AUDIO_LOUDNESS_JP_HUMAN_REVIEW MP4, SHA256 a2db222febdb59773740edeac0c7410d2ca6ca376fb76bf4727f993a8f754aec.

## What changed

Seven deterministic 140ms original synthesized non-musical UI sounds on visually detected scene changes. Sounds are attenuated by 9dB where narration is active. No stock music/SFX, third-party media, paid APIs, or auto-posting.

Previous cycle962 normalized EBU R128 narration loudness. This cycle adds original transition sound design, rather than repeating normalization.

Ten genre presets are configured; only ai_work is approved for technical review rendering. Other genres fail closed.

## Actual local MP4 QA (not uploaded to GitHub)

- H.264 video bitstream identical to input (all artwork and burned Japanese subtitles retained)
- 1080x1920, 30fps, 691 frames, full audio/video decode PASS
- AAC 48kHz Japanese-tagged audio, -16.25 LUFS, -1.57 dBTP
- 7 added original sounds, 8 local unit tests PASS
- Speech waveform correlation with original: 0.99987
- Output MP4 SHA256: see local qa963.json

This repository CI uses only generated synthetic audio/video, not the user's media.

NOT VERIFIED: independent Japanese speech transcription, semantic subtitle timing, smartphone playback, v33 source-video comparison, inherited-media commercial rights, employee approval, actual Actions billing.

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge or automatic posting. Manual posting only after employee approval.

Reproduce with an authorized source MP4:

python3 cycle963/transition_earcon.py --input source.mp4 --output review.mp4 --report render.json --genre ai_work

Requires free open-source FFmpeg and NumPy.
