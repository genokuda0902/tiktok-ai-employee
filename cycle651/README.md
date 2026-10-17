# cycle651: Japanese TTS recovery and synchronized slides

This work-in-progress branch is NOT approved for publication. No automated posting, no paid service, no merge.

Primary fix: render Japanese narration from exact per-scene scripts using free edge-tts on a GitHub-hosted runner; derive scene durations from generated audio, burn matching Japanese subtitles into 1080x1920 slides, and verify MP4 decode. The offline fallback keeps reused audio and labels captions as editorial/unverified. Ten genre keys share one data-driven renderer.

A CI result is not claimed until a completed workflow and downloadable artifact are verified. Rights and employee review remain required.
