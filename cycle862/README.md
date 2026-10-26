# cycle862 — actionable, evidence-backed outro (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. This is a new implementation, **not** recovered v33.

## Change vs cycle861

- Previously the final scene (19.6–23.033s) only showed a Writer Before/After screenshot, ending without an actionable next step. The last **60 frames (21.033–23.033s, frames 631–690)** now show a visually progressive save-and-try checklist, **three concrete steps**, two inset screenshots from actual fictional-data Calc/Writer recordings, and a noninteractive CTA: **「保存して実践」**.
- All other frames remain the same except for video re-encoding. The Japanese AAC elementary stream is bit-for-bit identical to cycle861. Burned-in subtitles remain protected below y1490. The new CTA visually reinforces the final subtitle 「小さな時短を、毎日の習慣にしよう。」; **no independent Japanese speech transcription or semantic sync is claimed**.
- Code supports 10 genre palettes and tailored three-step copy, but **only the AI-work MP4 was rendered**. No paid media, fake UI/cursor, new photography, or public upload.

## Run locally with private review footage (never commit it)

```bash
python -m pip install 'Pillow>=10,<13' numpy
PYTHONPATH=cycle862 python -m unittest discover -s cycle862 -p 'test_*.py' -v
python cycle862/actionable_outro.py --source /private/cycle861_REAL_UI_MONTAGE_JAPANESE_REVIEW_ONLY.mp4 --output /private/cycle862_ACTIONABLE_OUTRO_JAPANESE_REVIEW_ONLY.mp4 --manifest /private/source_manifest.private.json --report /private/render_report862.json
python cycle862/verify_review.py /private/cycle861_REAL_UI_MONTAGE_JAPANESE_REVIEW_ONLY.mp4 /private/cycle862_ACTIONABLE_OUTRO_JAPANESE_REVIEW_ONLY.mp4 /private/verification862.json
```

The private manifest is exactly `POLICY` plus `source_sha256`. Source/output video, private manifest, extracted images and Japanese voice are **never committed**. Synthetic-only GitHub Actions runs 12 unit tests and a 1s H264/AAC decode smoke; it does not prove the private MP4 was reproduced in CI.

## Research and safety

Available `TikTok市場分析`/`TikTok動画研究` summaries: strong first 1.5s hook, short purposeful shots, real UI, Before/After, readable Japanese subtitles, manual review. Full original research chats are inaccessible. User's 16-panel ChatGPT×Excel storyboard was directly opened; it contains a prominent CTA (panel 11) and cinematic high-quality robot/person shots. The original v33 MP4 remains inaccessible. The new CTA addresses a missing storyboard beat, **not** cinematic/visual parity. Existing media and audio publication rights, phone playback, independent ASR/voice naturalness, staff approval and Actions billing are unverified. No merge, auto-post, purchase, external footage upload or employee distribution.