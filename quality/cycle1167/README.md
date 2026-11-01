# Cycle1167: narration-card scene progress rail (human review)

**Change vs cycle1165:** Instead of another header transition effect, add a subtle 620x18 px progress indicator in the existing narration card at (130,1600). Its fill resets at all eight scene boundaries and reaches 100% at each scene end. The source Japanese captions and audio are not rewritten.

- Shared renderer: `code/scene_progress_rail.py` with 10 genre color presets.
- Tests: `tests/test_scene_progress_rail.py`; checks reset, monotonicity, geometry, palette and opacity.
- CI: `.github/workflows/quality-cycle1167.yml` renders synthetic 22.5s H.264/AAC, decodes and compares AAC packets.
- Private source video and actual output MP4 **must not** be uploaded to this public repository.
- The progress rail represents scene elapsed time only; it is **not** a word-level caption synchronization test.
- Reference v33 original, independent Japanese ASR, commercial rights, phone playback, employee approval, and actual Actions billing remain unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, payment or auto-posting.

Local verified actual MP4 and QA are shared separately in the conversation, not stored in GitHub.
