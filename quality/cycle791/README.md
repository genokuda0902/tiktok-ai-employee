# cycle791 — scene-summary captions + full-duration CI fixture (review only)

Base: cycle790 Draft PR #75, 23.843s, 1080x1920, 30fps, H.264/AAC. Latest main remains separate; no merge.
Previous: opaque scene wipe fixed double-exposed text around 13.7s. This cycle adds 9 one-line scene-summary captions to reserved mobile-safe lower band, 10-genre configuration and fail-closed tests. **These are scene summaries, not verified narration transcripts.**
Local command (requires an approved-for-internal-review input video; no input media committed):
python quality/cycle791/render_summary_captions.py --input /path/to/cycle790.mp4 --output /tmp/cycle791_REVIEW_ONLY.mp4 --config quality/cycle791/config.json --ass /tmp/cycle791.ass --report /tmp/cycle791_report.json
Local QA: 12/12 unit tests, 9 captions visible, 23.843s/714 frames, full decode PASS, source AAC and decoded PCM byte-identical, main image nearly unchanged. Local video shared only as conversation artifact; not committed because rights are unverified.
CI: generates a **separate full-duration 23.84s synthetic-tone technical fixture** with Japanese scene summaries; it is NOT the original 23.843s user video and contains NO Japanese narration. Does not reproduce or certify the original content.
Reference research: 1 message/video, 0–1.5s hook, 15–25s, scene-based, image-first, safe area, CTA; storyboard 16 panels. Original v33 MP4 not accessible; no direct quality comparison.
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No publishing, paid services, auto-posting or merging. Pending: human verification of voice/caption semantics, rights, mobile playback, v33 original and full user video CI reproducibility.
