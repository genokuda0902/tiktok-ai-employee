# cycle879 — audio activity–aware captions (review only)

**Distinct from cycle878:** all 8 caption texts and prior scene footage retained; audio RMS at 30fps drives a small waveform-like meter beneath the Japanese captions. A long **0.597s** low-energy tail after the final voice activity was detected; the final cue end was shortened from **23.03s to 22.55s** (0.12s postroll). This does **not** prove the Japanese words, voice naturalness, or phoneme timing match the captions.

Use only with a local, rights-reviewed private input MP4 and an explicit fail-closed SHA256 policy manifest. `audio_caption_audit.py` produces a local review MP4 and an audit JSON. The completed video and extracted voice are **not** uploaded to GitHub. The CI workflow tests source code against synthetic audio only.

Example local command:

```
python cycle879/audio_caption_audit.py --source PRIVATE_SOURCE.mp4 --output PRIVATE_REVIEW_ONLY.mp4 --manifest private_source_manifest.json --report private_audio_audit.json
```

Requires FFmpeg and Pillow, with no external network, payment or API. Audio activity is measured with mono PCM energy and a fixed -32 dBFS threshold, **not** Japanese ASR. For mixed music/voice this gate is insufficient; do not auto-approve. Reuse `validate_cues` and `analyze` for 10 genres; only AI-work has a completed MP4. Manual employee review before any TikTok post. No merge/auto-post.
