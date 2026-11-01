# Cycle 1187 — Japanese narration presence EQ (review only)

## Difference from cycle 1185
- Cycle 1185: visual outlines pairing prompt ingredients to examples in scene 04.
- Cycle 1187: audio-only 80 Hz high-pass, +1.3 dB presence at 3.2 kHz and -0.5 dB output trim.
- H.264 bitstream is copied without re-encoding: all 675 frames and burned Japanese subtitles remain identical.
- Same deterministic FFmpeg processor supports 10 genre identifiers; only the AI-work genre's 22.5s private review MP4 was rendered.

## Reproduction
```bash
python tools/quality_cycle1187/voice_presence.py SOURCE_1080x1920.mp4 REVIEW_ONLY.mp4 --genre ai
python -m unittest discover -s tools/quality_cycle1187 -p 'test_*.py' -v
python tools/quality_cycle1187/ci_smoke.py
```

## QA scope
Local final MP4: 1080x1920/30 fps, H.264 675 frames, AAC 48kHz mono, 22.5s, 8 chapter markers, full decode PASS, exact copied video stream hash PASS. Source -16.28 LUFS / -1.59 dBTP; output -16.85 LUFS / -1.59 dBTP; 10ms audio RMS envelope correlation 0.998932. Measured 0-80Hz power ~5.38dB lower and 2.5-4kHz ~0.65dB higher. Technical metrics do not prove a subjective sound quality improvement.

CI renders *only synthetic* 2.2s footage and sine audio. Private source video, Japanese voice, and final review MP4 are NOT committed to GitHub.

Unverified: independent Japanese ASR, subtitle semantic/timing match, reference v33 original comparison, smartphone playback, commercial rights, staff approval, Actions billing. No paid services, no merge, no posting.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**
