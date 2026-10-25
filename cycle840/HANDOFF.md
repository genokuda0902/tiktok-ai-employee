# cycle840 — integrate cycle838 dissolves with cycle839 narration pacing (2026-10-25 JST)

## Verified baseline and change
- Source: private cycle838 review MP4 SHA-256 7dcfa1a2e5d29ed700b781a96640b0f03f586a3dffe800de77feb43ae59d2fb1. Its audio lasts **25.833 seconds** in this runtime, not 0.704 seconds. PR #167 separately reported an incomplete cycle837 copy in another runtime; do not conflate these observations.
- PR #167 introduced seven 12-frame (0.4s) silence trims, but its local review lacked cycle838's dissolves. Cycle840 **uses the actual cycle838 source** and applies the same shared A/V edit decision list to preserve all seven image-region dissolves.
- Source: 775 frames / 25.833s / 1080x1920 H.264, AAC 48kHz 25.833s. Output: 691 frames / 23.033s, AAC 48kHz 23.033s; seven silence trims remove 2.8s.
- Frame 103 of cycle838 maps to frame 91 of cycle840. Central image-region MAE=0.994, protected caption-region MAE=0.020; cycle837 vs cycle838 image-region MAE=20.693. This supports **retention of the dissolve** despite re-encoding.
- Full audiovisual decode PASS; 11 offline unit tests PASS. Actual MP4 provided only via private ChatGPT sandbox, never GitHub.
- Fixed a real ten-genre name mismatch: cycle833 layout uses productivity, cycle839 EDL uses product_comparison_lifestyle. Cycle840 explicitly maps the canonical layout key to the pacing alias; all 10 layout genres are accepted, unknown names rejected.
- Added source SHA pinning, missing/short audio duration rejection, full decode, audio activity threshold, and review-only manifest gates.

## Reference and research access
- Inspected user's 16-panel ChatGPT×Excel storyboard from Library. Reference original v33 MP4 is **not available** in this runtime; no direct comparison.
- TikTok市場分析 and TikTok動画研究 full task/chat transcripts unavailable. Earlier accessible research summaries favor early hooks, readable captions, demonstrations, image-first quality, and human approval.
- Authoritative PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md inspected; robot animation and Wan 2.2 out of scope; employee manual posting only.

## Security and unfinished gates
- Public CI runs only offline unit tests and **synthetic** A/V smoke from cycle839. It does not build or host the Japanese review MP4.
- Japanese narration semantic correctness, word-level subtitle synchronization, smartphone playback, reference-v33 parity, public media/voice rights and employee approval **not verified**.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No auto merge, posting, external upload or paid service.

## Reproduce with a locally authorized source
PYTHONPATH=. python3 cycle840/integrated_review.py --source cycle838_REVIEW.mp4 --manifest local_fictional_manifest.json --output cycle840_REVIEW.mp4

PYTHONPATH=. python3 -m unittest discover -s cycle840 -p 'test_*.py' -v
