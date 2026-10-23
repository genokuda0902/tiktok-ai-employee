# Cycle791 — RMS-guided Japanese subtitle timing (human review only)

Improvement over cycle790: adjust the **16 Japanese caption cues** using measured audio activity onset/offset per 8 scenes, instead of fixed clock guesses. Preserve the earlier progressive karaoke coloring, 1080×1920 artwork, 8 scene-specific focus highlights, and exact inherited AAC packet payload.

This is a **heuristic**, not speech recognition or forced alignment. Word/phoneme timing and pronunciation remain unverified. The input voice and images are not uploaded because inherited narration rights are unverified. No paid API, merge, posting, or employee approval is implied.

## Reproduce with your locally supplied review assets

Requirements: Python 3.11, numpy, FFmpeg/libass, Noto CJK font.

```bash
python -m unittest discover -s cycles/cycle791/tests -v
python cycles/cycle791/src/audio_cue_renderer.py \
  --input cycle790_FOCUS_PULSE_HUMAN_REVIEW.mp4 \
  --strip caption_clean_strip.png \
  --output cycle791_AUDIO_ALIGNED_HUMAN_REVIEW.mp4 \
  --work /tmp/cycle791 --genre science
ffmpeg -v error -xerror -i cycle791_AUDIO_ALIGNED_HUMAN_REVIEW.mp4 -f null -
```

`caption_clean_strip.png` is a 1080×160 crop (x=0..1079,y=1390..1549) from the caption-free original slide background; the renderer replaces old burned-in captions before adding updated ones.

## CI scope

GitHub Actions unit-tests RMS alignment and renders a **synthetic-tone technical smoke** video. It cannot certify the inherited Japanese narration or publication readiness. The finished narration MP4 and reproducibility package are delivered in the conversation, not in public GitHub. Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Manual posting only after employee approval.
