# Cycle809 — photo/editorial hybrid (HUMAN REVIEW ONLY)

## Change versus cycle808 (#109)
Replaces the purely native-vector visual panels with an eight-scene **photo + sharp native text/diagrams** composition. Source photos are crops of ChatGPT-generated material; crop sharpness is not a guarantee of photographic detail. Includes a photo focal card, genre-dependent accent, independent Japanese subtitle panel, and micro camera zoom. A subset of original source photographs includes pre-rendered text; publication remains blocked pending visual review.

## Actual private local review render
- `cycle809_PHOTO_HYBRID_HUMAN_REVIEW.mp4`
- 1080x1920; H.264; 30 fps; 775 frames; 25.833333 seconds.
- AAC Japanese Open JTalk audio inherited **unchanged** from cycle808, not freshly synthesized.
- Full audio+video FFmpeg decode: PASS. Audio elementary stream hash equal to prior MP4.
- MP4 SHA256: `45d62e2284a5f6516dbff342d7605986de3908d6b3d9c5e9b8b73fe9822cf1d6`.
- The actual MP4, image assets, renderer and detailed QA are **private ChatGPT conversation attachments**, not GitHub repository files or CI artifacts.

## GitHub scope
This PR saves a portable 10-genre contract, a working FFmpeg slideshow assembler (`assemble_mp4.py`), and eight contract/assembler tests. The assembler was locally smoke-tested with the eight private slides and inherited narration (1080x1920, 775 frames). The full photo renderer is shared separately in the conversation ZIP because images, source voice, and their license/rights review are not cleared for publication to this public repository. GitHub CI tests the contract and assembler functions only, **not the full MP4**.

## Review gates
`HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`. No auto-post, paid API, merge, or publishing. Original voice model licensing/attribution, independent ASR speech/caption match, mobile-device playback, source image rights, and reference-video quality parity are NOT verified. Employees must explicitly approve before any manual TikTok posting.
