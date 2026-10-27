# cycle885 — mobile Japanese caption readability

**Status:** HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

Distinct from cycle884's 7 eased dissolves: increase the 24 Japanese caption
cues from **66px to 71px** (+7.58%), using measured Noto CJK glyph widths and
the 930px inner caption-card safe width. Keep wording, timing, highlighted
words, video source, and inherited Japanese audio packet data unchanged.
For other content/genres, shrink only when the text would exceed safe width.

Quality control: treat 24 highlighted subcues as 8 full sentences when
measuring reading speed; do not mistake repeated karaoke text for 24 new
sentences. Local sample: maximum 8.27 Japanese characters/sec across sentences.

**Local-only verification:** MP4 1080x1920, H.264 30fps 691 frames,
23.033 seconds, AAC 48kHz; full audio/video decode; inherited audio packets
identical; 20/20 technical QA checks; 10 local Python unit tests.
CI validates the reusable pure-Python module and tests only, **not the MP4**.
Standalone CI skips the source-dependent integration test.

**Rights and quality limitations:** inherited narration rights unverified;
no independent Japanese ASR/pronunciation or semantic matching; original user
reference video not accessible for direct comparison; no smartphone hardware
playback; no employee approval. Never auto-post, auto-merge or publish.

Source and tests are free/open dependencies; rendered local MP4 remains
review-only and is not uploaded to public GitHub.
