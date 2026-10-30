# cycle991 | speech-aware original transition cues

**Source:** cycle987 pre-SFX MP4 (not cycle989; prevents double cues).
**Difference from cycle989:** replace fixed-gain original 185 ms cues at 7 boundaries with speech-aware attenuated cues. Preserve all 691 original H.264 frames and baked Japanese captions at the video packet level. Keep 48 kHz Japanese-tagged AAC narration and manual-review-only publication policy.

Gain: clamp(0.045/(0.010 + local narration RMS), 0.18, 0.85). 0.36 s speech-context window. All effects synthesized locally, deterministic, no third-party audio assets or paid APIs. Works for any genre with scene-boundary frames supplied.

**Local real-MP4 QA:** full A/V decode PASS, 1080x1920 30 fps 691 frames PASS, video packet hash unchanged PASS, 7/7 cues attenuated PASS, non-cue audio RMSE 0.001083 versus clean source, 7/7 unit tests PASS. Cue residual RMS reductions vs cycle989: 59.77%, 14.92%, 75.59%, 76.96%, 75.13%, 58.97%, 75.95%. These are technical sound-effect amplitude reductions, **not proven subjective speech quality improvements**.

**Limitations:** Independent Japanese ASR/caption synchronization, reference v33 original, smartphone playback, source asset commercial rights, employee approval and actual paid Actions billing unverified. Do not publish or merge automatically.

**CI:** Generates only synthetic 1080x1920 test media. The real Japanese MP4 is not uploaded to GitHub.

**Source/review artifacts:** cycle991/output/cycle991_SPEECH_AWARE_CUES_JP_HUMAN_REVIEW.mp4, qa991.json, diff_cycle989_to_991.json. Real MP4 stays outside the repository.
