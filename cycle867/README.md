# cycle867 — animated source-to-result audit (private review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Reimplementation, not original v33. No automatic posting, no unapproved media uploads, no paid services.

## Improvement over cycle866

Replaces scene 05, frames 336–421 (11.200–14.067 seconds), where an inherited Calc crop zoomed so far that month names were cut and a small `02/03` overlay obscured the header. A new original high-resolution graphic presents **source → calculation → result**, clearly shows fictional 4–6月 values (A=12+16+18=46; B=8+9+12=29), and labels the material as an illustrative fictional example. No actual ChatGPT analysis, real sales, or original v33 engine is claimed. The existing Japanese narration and burned subtitle strip are retained. The shared visual renderer accepts 10 genre editorial headline variants; only the AI-work example has been exported to the full MP4.

The visual is **procedural original artwork**, not a newly licensed photograph. This solves a readability and traceability issue; it does **not** close the cinematic photographic gap to the 16-panel reference.

## Reproduce with private input

```bash
python -m pip install pillow numpy opencv-python-headless
PYTHONPATH=cycle867 python -m unittest discover -s cycle867 -p 'test_*.py' -v
python cycle867/audit_focus.py --source /PRIVATE/cycle866_REVIEW_ONLY.mp4 --output /PRIVATE/cycle867_REVIEW_ONLY.mp4 --manifest /PRIVATE/source_manifest.private.json --report /PRIVATE/render_report867.json
python cycle867/verify_review.py /PRIVATE/cycle866_REVIEW_ONLY.mp4 /PRIVATE/cycle867_REVIEW_ONLY.mp4 /PRIVATE/verification867.json
```

The **private** manifest must equal `POLICY` plus `source_sha256` of the private source. Do not commit private media, extracted frames, the manifest, audio, or reference video. The GitHub CI runs unit tests and a **synthetic 1-second video+audio smoke test only**, not the real Japanese video.

## Evidence and limitations

- Consulted accessible summaries of `TikTok市場分析` and `TikTok動画研究`: 0–1.5s hook, ~15–25s, real demonstrations, readable captions, before/after and human review. Full chats not accessible.
- Inspected user-provided 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` this run, especially panels 4–8. Original v33 MP4 unavailable, so no direct visual equivalence claim.
- Verified repository `main` `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, unmerged PRs, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, and existing `src/build_daily.py` (still silent `-an`, not v33).
- Real local MP4: 1080×1920 H.264, 30fps, 691 frames, 23.033s, AAC 48kHz. Full decode PASS. Prior AAC elementary stream SHA identical. Subtitle pixel ROI y=1490–1839 checked across all 691 frames; maximum per-frame mean delta 0.113, p95 0.080. Local 13 unit tests PASS.
- **Not verified**: actual Japanese narration words/pronunciation, semantic timing of speech and subtitles, source-media publication rights, smartphone playback, employee approval, actual GitHub Actions billing. Do not publish.