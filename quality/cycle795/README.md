# cycle795 — protected CTA restoration (review-only)

cycle794's end-card scene-summary bar overlaps the pink save CTA around 21–23.843s. The clean cycle790 frame is unobstructed. This reimplementation restores only the protected CTA band (y=1300–1540) from the time-aligned local cycle790 video, preserving the rest of cycle794 and its audio. It is not recovered v33 source.

Local command (input media supplied separately, NOT committed):

    python quality/cycle795/protected_region_restore.py --config quality/cycle795/config.json --dirty /path/to/cycle794_UI_FOCUS_GUIDANCE_REVIEW_ONLY.mp4 --clean /path/to/cycle790_OPAQUE_WIPE_REVIEW_ONLY.mp4 --output /path/to/cycle795_CTA_UNOBSTRUCTED_REVIEW_ONLY.mp4 --report /path/to/qa.json

Ten-genre contract, 1080x1920/30fps, time-aligned clean-reference guard, CTA coverage and fail-closed rights validation. The workflow uses separate synthetic colored panels and sine-tone audio; it is NOT the Japanese-narrated final MP4. Private inherited audio/visuals are never committed.

Previous cycle794: black summary bar covered the CTA. cycle795: pink CTA readable, audio AAC/PCM identical, no other scenes intentionally changed. Full historical research chats and original v33 MP4 remain inaccessible; 16-panel storyboard, quality guide and project handoff consulted. Japanese narration semantics, caption-to-speech alignment, phone playback, rights, and employee approval remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. DO NOT MERGE OR POST.
