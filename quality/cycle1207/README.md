# Cycle 1207 — central diagram shadow detail (REVIEW ONLY)

Previous cycle1205 brightened tiny **footer disclaimer text**. This cycle performs
**luma-only shadow/midtone lift** inside the central illustration ROI
(64, 500, 952, 816), without modifying the top progress, Japanese subtitle card
or footer intentionally. White glyphs are protected by the upper luma threshold.
Ten genre profiles share one offline implementation.

## Verified private local video (not stored on GitHub)

- Input: cycle1205_FOOTER_LEGIBILITY_HUMAN_REVIEW.mp4
- Output: cycle1207_MIDTONE_DETAIL_HUMAN_REVIEW.mp4
- H264 1080x1920 30fps 675 frames, 22.5s, AAC 48kHz: PASS
- Full video and audio decode: PASS
- Audio elementary ADTS SHA256 identical: PASS
- Central-panel midtone luma mean gain over 9 samples: +13.558/255
- Maximum sampled mean pixel difference outside ROI: 0.177/255
- Local unit tests: 12/12 PASS; synthetic 30-frame H264/AAC smoke PASS
- Comparison image and actual MP4 shared privately with reviewer, not in Git.

## Sources and limits

Accessible prior summaries of TikTok market/video research emphasize a strong hook,
purposeful scene cuts, readable Japanese captions, actual UI/Before-After, and manual
employee approval. The user's 16-panel storyboard was reported inspected in earlier
cycles, but the original v33 reference video is not accessible here. No claim of
reference-quality parity, smartphone readability, rights clearance, Japanese speech
semantic/timing alignment, or employee approval. CI tests synthetic footage only.

No unapproved assets, private media, credentials, merge, auto-posting, or paid API.
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
