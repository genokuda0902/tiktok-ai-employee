# cycle944 — original ambient sound bed with narration-first ducking

Review-only, no sampled/copyrighted music, no paid services. Changes **audio only** vs private cycle942 MP4: a deterministic non-melodic 3-tone synthesized ambience with 7 gentle scene-transition swells; 20ms RMS-based voice ducking to approximately -43 dB gain during speech and -31 dB in pauses. Original H.264 video and burned Japanese subtitles are stream-copied, not changed. Ten genre presets are tested; only AI-work full MP4 is rendered.

Reproduce locally (private approved-for-review source only): `python cycle944/src/voice_first_ambience.py --source SOURCE.mp4 --output REVIEW_ONLY.mp4 --genre ai_work`. Dependencies: FFmpeg, numpy, pytest. `pytest -q cycle944/tests/test_voice_first_ambience.py`.

Important: Audio energy detection is NOT Japanese speech recognition or semantic subtitle synchronization. Inherited source rights, smartphone playback, human quality review, independent ASR and employee approval remain unverified. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Never upload private media or auto-post. PR remains draft/unmerged.
