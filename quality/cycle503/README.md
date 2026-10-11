# cycle503: original ambient cue bed — review only

**Baseline:** cycle502, local 20s 1080x1920 H.264/AAC procedural demo (SHA-256: `110acd55fa67413b651057f09b5ec9cd58850cf6d68a2b7682c954f782a8418c`). Its video is NOT stored in this repository.

**Change:** genre-neutral 2.5s cue rhythm, low-volume original two-tone pad and brief bell accents, boundary fade. The H.264 video bitstream is copied without re-encoding, so visual captions, 600 frames and loop remain unchanged. This improves sound-bed coverage, **not** narration quality, view retention or reference equivalence.

**Local results (2026-10-12 JST):** 15 standard-library unit tests PASS, 20.00s 1080x1920 30fps H264/AAC full decode PASS, unchanged video bitstream MD5 `ea6da9e743bb4fa3b0136f0aa79c2d3a`. Audio 100ms windows RMS>0.002: 16/200 before, 200/200 after. Peak 0.109→0.134 (no clipping). MP4 SHA-256: `2480395c984313e6f3cdf7c4e682269ce36536baf95f9aac943d4f4c5d70805e`.

**Run:** `python3 quality/cycle503/audio_bed.py --base cycle502_seamless_loop_SFX_ONLY_REVIEW.mp4 --out cycle503_REVIEW.mp4 --rights original_procedural --audio-status sfx_only`

**Test:** `cd quality/cycle503 && python3 -m unittest -v test_audio_bed`

**Gates:** native Japanese narration NOT GENERATED (local gTTS connection failed; espeak has no Japanese voice). Spoken-caption synchronization NOT VERIFIED. Reference v33 MP4 original NOT RETRIEVED; 16-panel storyboard inspected. Original confidential v33 demo assets are NOT used. No automatic posting, merging, publication, or quality approval. Human review required.

**CI:** workflow write blocked by connector safety checks; no CI success is claimed. The source video is session-local, so a CI fixture must be independently synthetic, and must never be labeled a quality demo.

**Next:** Restore CI workflow authorization without bypassing safeguards; acquire licensed native Japanese TTS via the existing Aivis workflow; generate measured subtitle timing; secure reference MP4 with rights check; visually review audio levels and quality.
