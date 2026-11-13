# cycle1420 — review only
- Prior cycle1419: 75 source PNG frames / 15 seconds (5 fps), output encoded 25 fps; 5 scene-timed SRT cues; silent.
- Current local cycle1420: 150 source PNG frames / 15 seconds (10 fps), encoded 25 fps; blinking input cursor; 5 scene-timed SRT cues; silent.
- Local MP4 SHA256: 138b9e08143407726f5470be6c9d4bcfee6015bf153b13c456388462d07ed193.
- Full renderer and MP4 remain local artifacts, NOT committed. This PR saves the reusable timing logic and tests, not a complete CI pipeline.
- No Japanese voice, no speech-aligned captions, no user quality approval. DO NOT MERGE OR POST.
- Next priority: obtain licensed/offline Japanese TTS and commit fully reproducible rendering plus CI artifact.
