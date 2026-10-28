# cycle937 — Japanese narration clarity EQ (HUMAN_REVIEW)

## Distinct change
cycle936 used scene03 depth of field. cycle937 changes **only the audio**: gentle 75 Hz high-pass, +1.4 dB presence at 2.8 kHz, 14.5 kHz low-pass and 0.88 peak ceiling. H.264 video and burned Japanese subtitles are copied bit-for-bit. Ten genre presets are supported. This is a technical voice-clarity *attempt*, not a verified listening preference or independent Japanese ASR result.

## Private MP4 evidence
- Output: `cycle937_NARRATION_CLARITY_JP_HUMAN_REVIEW.mp4` (private ChatGPT attachment, **not public GitHub**)
- SHA256: `b46dc50d7dacfe44ad7c3649c6467ea6687e989071c9e17d477e85f384e9f663`
- Source cycle936 SHA256: `d284c11692cde78af184c53175ac49723a2f20ef66f0a236865008f73bdfe0ad`
- 23.033 s, H.264 1080x1920, 30 fps, 691 frames, AAC 48 kHz mono
- Full audio/video decode PASS; Annex-B H.264 SHA256 identical source/output, so captions and every frame are identical
- Integrated loudness -16.6 LUFS before and after; true peak -1.8 to -1.1 dBFS; speech-envelope lag 0 ms
- 30–75 Hz spectral power 0.21x, 2–4 kHz power 1.318x (objective DSP effects; not human intelligibility scores)
- 10/10 local unit tests PASS; GitHub CI runs code tests only

## Reproduce (free FFmpeg)

```sh
python cycle937/src/audio_clarity.py --source PRIVATE_REVIEW.mp4 --output OUTPUT_REVIEW.mp4 --genre ai_productivity
python -m unittest discover -s cycle937/tests -v
```

## Research and limits
Accessible summaries of prior TikTok market analysis and video research emphasize a 1–1.5 s hook, short purposeful scenes, real operation evidence, Before/After, readable Japanese subtitles, and employee-reviewed manual posting. The user's 16-panel `ChatGPT×Excel時短術` storyboard is known from prior notes; original v33 MP4 and complete research transcripts were not directly accessible. This pass does not solve the remaining cinematic scene diversity gap.

Not verified: independent Japanese ASR / subtitle meaning and timing, perceptual listening improvement, source media commercial rights, smartphone hardware playback, v33 direct comparison, employee approval, actual Actions billing. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid contract, auto-post, or private MP4 in public GitHub. Manual publication only after employee approval.
