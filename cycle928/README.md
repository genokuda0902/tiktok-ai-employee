# cycle928 — Audio-reactive header meter (review only)

## Difference from prior cycles
cycle927 added a visible **unapproved human-review gate** to scene05. cycle928 instead replaces the *static* header equalizer throughout the existing 23.033s video with an **audio-envelope-driven** animated meter, preserving Japanese narration, burnt-in captions, and scene content.

The animation is driven by the RMS amplitude of the **inherited AAC audio**. It does **not** perform speech recognition or verify that narration and captions mean the same thing.

## Rendering
Requires Python 3, Pillow, FFmpeg, and the source MP4 in a private working directory. Example:

```bash
python cycle928/src/voice_meter.py \
  --source /private/source.mp4 \
  --output /private/cycle928_REVIEW_ONLY.mp4 \
  --genre ai_work \
  --expected-source-sha <verify-original-sha>
```

10 genre accent palettes are supported; **only ai_work was rendered as a complete MP4**. Unsupported genres fail closed. Source MP4 and output MP4 are **not committed**.

## Local QA (not CI)
Private full-MP4 QA: 691 frames, H.264 1080x1920/30fps, 23.033s, AAC 48kHz with ADTS bitstream hash identical to cycle927, all-frame decode, subtitles and main visuals preserved within re-encode tolerance, 15/15 checks PASS. Local renderer tests: 10/10 PASS.

Source SHA256: `0693fabe3eb8790d5214da440ffc0dbb12be27f89d4511cb9057fa9fb214ec12`
Output SHA256: `13f43b925201f65425623c2e730007ab4bebe3e6ff37edc668286c5c58d9a0a9`

## Restrictions
No source footage, personal data, private audio, completed MP4, or unapproved material is uploaded. No paid services, merge, or auto-post. Independent Japanese ASR / semantic timing, reference v33 original, inherited rights, phone playback, and employee approval remain **unverified**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Employee approval and manual posting only.
