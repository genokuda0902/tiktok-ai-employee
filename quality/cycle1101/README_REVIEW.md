# cycle1101 — motion-safe three-step learning rail (review only)

Previous cycle1031 fixed seven overlapping/cropped Japanese scene headlines. This cycle adds a **compact three-stage learning rail** in scenes 4 and 5 (8.60–14.10 s), with a highlighted active item: purpose → conditions → format, then numbers/evidence → dates/names → categorical claims.

The first implementation tried to outline rows inside animated UI screenshots. Actual frame review revealed drifting boxes; it was **discarded**, not delivered. The final rail stays in a fixed, measured safe area y=1630..1724 below the burned subtitles (ending near y=1620), above the original progress bar (~y=1745). The central moving screenshots remain untouched.

Local private source: cycle1031 22.5 s review-only MP4. Actual local output: cycle1101_GUIDED_3STEP_RAIL_JP_HUMAN_REVIEW.mp4 (not committed/uploaded to this public repository).

Local QA: H.264 1080x1920 30fps, 675 frames, 8 chapters, 22.5s, AAC 48kHz language tag jpn. Full A/V decode PASS. AAC ADTS SHA-256 before/after both da601fdd17eae3cc1c0fe9a0d93843f6c07e1321d33f84f92474819c477d8b18. 135 sampled frames: max grayscale difference in caption region y1180:1625 0.685/255, upper region max 0.6651/255; changed rail minimum difference 46.2036/255; outside target scenes rail max 0.0171/255. Local 14/14 tests PASS.

10 genre color presets; actual full MP4 checked only ai_work. CI runs unit tests plus **synthetic** MP4 render/decode, not the private real 22.5-second video. No independent Japanese ASR, subtitle semantic sync, original v33 direct comparison, source-rights confirmation, smartphone playback, employee approval, retention proof, or actual Actions billing confirmation.

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid contract, posting or public upload of private source media.