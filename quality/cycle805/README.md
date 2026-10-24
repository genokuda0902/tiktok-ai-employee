# cycle805 — new-topic business video / original editorial graphics (REVIEW ONLY)

**Why:** cycle803 reused the same AI/Excel topic and old narration. This cycle demonstrates a *new sales/business topic* with **new Japanese narration and caption text from the exact same script manifest**, and original non-stock artwork. This is a new-topic test, not a reproduction of reference v33's realistic actors or 3D visuals.

## Provenance and limitations

- Reference: user-supplied 16-panel AI時短ラボ storyboard in ChatGPT Library. Original v33 MP4 and full TikTok市場分析/TikTok動画研究 transcripts inaccessible; summaries only.
- Voice: free Open JTalk, created in **cycle804** GitHub Actions run 40047591409; voice_timing.json and m4a retrieved from verified artifact 12541712495. Audio is **not committed** to repository. Human evaluation of naturalness and licensing still required.
- Eight scenes, 1080×1920, 30fps, caption text identical to script. Timing aligns at sentence boundaries (WAV lengths), **not** word/phoneme level; no ASR confirmation.
- Graphics are original Pillow vector-style editorial slides. No private imagery, faces, real customer data or third-party logos.
- A *single* genre is rendered in this cycle; ten palette/contract configs are tested, not ten completed videos.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No automatic posting, merge, purchases, employee distribution or claim of v33 parity.

## Local generation

1. Obtain cycle804_business_japanese_voice.zip from GitHub Actions run 40047591409 (artifact 12541712495).
2. Unzip to a local folder (example /tmp/cycle805_voice).
3. Run unit tests: python -m unittest discover -s quality/cycle805 -p 'test_*.py' -v
4. Run: python quality/cycle805/render_editorial.py --audio /tmp/cycle805_voice/cycle803_business_japanese.m4a --timing /tmp/cycle805_voice/voice_timing.json --slides-dir /tmp/cycle805_slides --output /tmp/cycle805_review.mp4
5. Verify: ffmpeg -v error -xerror -i /tmp/cycle805_review.mp4 -f null -

GitHub Actions retrieves the cycle804 voice artifact with actions:read, tests the renderer, generates a full review-only MP4, and uploads an artifact with 7-day retention. Review the rights of the synthetic voice before use.
