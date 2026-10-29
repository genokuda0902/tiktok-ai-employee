# cycle987 — kinetic Japanese chapter headlines (review only)

## Change vs cycle985

Cycle985 added subtle cyan accent bloom to static slide artwork. Cycle987 adds **animated Japanese chapter headlines** across all eight existing AI-work scenes: 0.47-second progressive reveal, moving cyan caret, 0.8-second underline, and an opaque high-contrast title panel. It replaces the existing static headline without rewriting narration or captions. It does not repeat cycle984's CTA step ticks or cycle981's transition wipe.

The source is the private cycle985 review MP4. Real MP4 is **not uploaded to public GitHub**. The branch contains source code, tests and synthetic-only CI. Ten genre palettes are reusable configuration, not ten reviewed videos. Nine non-AI-work layouts fail closed for real footage until separately reviewed.

## Local real-video evidence

- Private output: cycle987_KINETIC_HEADLINES_JP_HUMAN_REVIEW.mp4
- H.264 1080x1920, 30fps, 691 frames, 23.033333s; AAC 48kHz mono, language tag jpn.
- Both source and output fully decode with ffmpeg -xerror.
- Original AAC ADTS SHA256 and output AAC ADTS SHA256 identical: 785b26ef233e7b6d2e2f1dc37b143d89cd8e2aaebb663480ee54d61d45986f43.
- All 691 frames show title ROI changes in their scenes (87,87,87,87,87,87,87,82 frames).
- Caption region y>=1180: max **per-frame mean** pixel delta 1.401/255 over 691 frames, due to lossy re-encoding; the overlay algorithm never touches the region.
- Local unit tests 23/23 PASS. Synthetic 30-frame 1080x1920 video also renders and fully decodes.

## Source / rights / research

Accessible research summaries prioritize first 1.5s hook, demonstrative UI, Before/After, 15–25 seconds, 6–10 scenes and readable Japanese captions. User's supplied 16-panel ChatGPT×Excel storyboard is known through prior conversation notes. Original v33 reference MP4 and full research transcripts were not available in this cycle; no equivalence claim.

Inherited voice is tagged Japanese and preserved bit-for-bit as AAC elementary stream. However, pronunciation, independent Japanese ASR, and subtitle semantic/timing agreement remain **unverified**. Subjective quality, commercial media rights, smartphone playback, employee approval and actual Actions billing also unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid services, posting or public upload of private MP4. Employee approval mandatory before manual posting.
