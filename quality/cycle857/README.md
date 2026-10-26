# cycle857 – eight independent high-resolution AI photos (review only)

This is a stacked, unmerged quality-improvement cycle based on cycle856. The new full-size photo stage is 900×1250 pixels (previously 630×630), a 183.4% increase in displayed area. Eight independent source images meet the minimum 900×1500 dimensions, and foreground crops never upscale source pixels. Six were introduced in cycle856; the remaining two were previously generated in the user's conversation and are now integrated. **Not all eight images were newly generated in cycle857.**

Eight scene cuts are aligned to silences between 24 Japanese narration subtitle beats; the final video has exactly 691 frames at 30 fps (23.033 seconds) and 1080×1920 pixels. The inherited Japanese AAC audio is kept bitstream-identical.

This PR contains the reusable 10-genre photo-quality/timing core, actual 24 subtitle beats, nine unit tests, and GitHub Actions CI. The complete MP4 generator, synthetic image sources, Japanese audio, final MP4, and QA evidence are provided separately in the cycle857 local review ZIP. **GitHub CI tests the shared core, not the finished Japanese MP4.**

Synthetic people and images, inherited voice provenance, subtitle phoneme alignment, reference-video comparison, and phone playback require human review. No publishing, auto-posting, paid contracts, or merge. Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
