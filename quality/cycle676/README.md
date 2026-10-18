# Cycle676 — Evidence focus (review only)

- Baseline: cycle675 local MP4; original v33 is not available in this run.
- Improvement: emphasize formula entry at 10.0–11.9s and verified result at 12.0–13.9s.
- Render: python quality/cycle676/src/focus_renderer.py --input baseline.mp4 --output cycle676.mp4 --cues quality/cycle676/focus_cues.json
- Local checks: 1080x1920, H.264/AAC, 20s, 11 unit tests.
- The reference storyboard was consulted; the reference v33 MP4 itself was not accessed.
- Japanese narration was not generated; subtitle/speech alignment is unverified.
- Inherited video assets have not been cleared for public use.
- PUBLICATION_NOT_APPROVED; no merging or posting. Manual employee approval required.
- Local reproducibility bundle contains renderer, tests, focus config, comparison and MP4.
