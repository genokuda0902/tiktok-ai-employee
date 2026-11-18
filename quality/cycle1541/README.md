# Cycle 1541 — audio loudness gate (review only)
Input: locally generated cycle1540 review MP4 (not committed; no confidential assets uploaded).
Run: python quality/cycle1541/normalize_audio.py input.mp4 output.mp4
Test: cd quality/cycle1541 && python -m unittest -v
Effect: FFmpeg EBU R128 loudnorm target -16 LUFS, true peak -1.5 dBTP, LRA 11; video stream copied. This does NOT create Japanese narration or certify caption synchronization.
Local result: 12.10s H.264 1080x1920 + AAC, FFmpeg decode PASS, 2 tests PASS. GitHub Actions and user acceptance pending.
Prior cycle1540: moving operation focus pointer, effects-only audio. New cycle: normalized audio loudness; no additional visual decoration.
Reference original v33 inaccessible in this run; handoff records 31.553333s and AAC. DO NOT PUBLISH; manual employee review required.
