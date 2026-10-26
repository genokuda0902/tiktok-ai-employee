# cycle866 — single-layer evidence chart (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is an original, procedurally drawn **fictional** bar chart, not an AI-generated Excel export, not the original v33 engine, and not a public-ready video. No paid service, external upload, auto-post, merge, or public distribution of inherited media.

## Change from cycle865

The old scene 03 (frames 170–250, 5.667–8.367 seconds) had an inherited card-on-card stack that visibly clipped a heading and made the chart hard to read. Replaced the entire scene body y=330..1449 with one nonoverlapping card and staged 4–6月 comparison for fictional sales A/B. A=12+16+18=46; B=8+9+12=29. The final card prompts the viewer to check source evidence. The original top scene heading and burned Japanese subtitle region below y1490 are preserved. Original graphics are generated from Python/Pillow; no new third-party photo or video is added.

The reusable renderer contains ten genre headline variants and explicit no-overlap geometry checks. **Only AI-work** has been rendered as a full Japanese review MP4.

## Local reproduction (private input only)

```bash
python -m pip install pillow numpy opencv-python-headless
PYTHONPATH=cycle866 python -m unittest discover -s cycle866 -p 'test_*.py' -v
python cycle866/clean_story_panel.py --source /PRIVATE/cycle865_CLEAN_HOOK_JAPANESE_REVIEW_ONLY.mp4 --output /PRIVATE/cycle866_SINGLE_LAYER_EVIDENCE_JAPANESE_REVIEW_ONLY.mp4 --manifest /PRIVATE/source_manifest.private.json --report /PRIVATE/render_report866.json
PYTHONPATH=cycle866 python cycle866/verify_review.py /PRIVATE/cycle865_CLEAN_HOOK_JAPANESE_REVIEW_ONLY.mp4 /PRIVATE/cycle866_SINGLE_LAYER_EVIDENCE_JAPANESE_REVIEW_ONLY.mp4 /PRIVATE/verification866.json
```

Private manifest must exactly match `POLICY` in `clean_story_panel.py` plus `source_sha256`. **Never commit** the manifest, inherited MP4, extracted frames, original narration, or finished video to a public repository. The GitHub workflow runs unit tests and a **synthetic 1-second** A/V smoke test only; it does not render or validate the real Japanese review MP4.

## Research and safety

Accessible past summaries of `TikTok市場分析` and `TikTok動画研究`: strong opening, ~15–25 second short video, real demonstrations, readable captions and clear Before/After. Original task/chat transcripts unavailable. The user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` was inspected; panel 6 uses a clean results chart. Original v33 MP4 not accessible. `PROJECT_HANDOFF.md` and `recovery/v33/RECOVERY_STATUS.md` prohibit unapproved private imagery, robot motion and unapproved auto-posting. This 8-scene result remains far from the 16-panel cinematic reference.

Local source/output stream verification: H264 1080x1920 30fps 691 frames, AAC 48kHz, full decode PASS, source/output AAC ADTS SHA identical, protected caption region mean sampled delta < 0.1, 81 changed frames. Japanese narration content, pronunciation, speech-caption semantics, source rights, phone playback, employee approval, reference parity and actual Actions billing are NOT verified.