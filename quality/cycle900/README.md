# cycle900 — native Japanese human-review panel (private video, review only)

## Distinct change vs cycle899

cycle899 animated a 3-step CTA action path in the final scene. This cycle redesigns **scene 05, 11.60–14.49s**, into a native-resolution 940×1020 Japanese human-verification panel with sequential attention to **数字と根拠 → 抜け・誤り → 伝わる表現**. A fictional example and explicit "AIが自動で確認した結果ではありません" notice prevent automatic-verification claims. The text and panel are rendered with Pillow and Noto CJK; no external photos, stock assets, or user information are introduced.

## Private local deliverable verified

Source: locally available cycle899 private MP4. New private MP4: H.264 1080×1920 / 30fps / 691 frames / 23.033s, AAC 48kHz mono. Full audio/video decode PASS; AAC ADTS stream SHA exactly identical. 16/16 local technical QA checks PASS and 11/11 unit tests PASS. Caption region sampled max MAE 1.177 and unchanged-scene sampled max MAE 0.704 (re-encoding noise); scene05 sampled min MAE 47.88. Three focus states are visibly distinct. Finished MP4 and private inherited images/audio are **not** uploaded to this public repository. CI checks code, tests and synthetic overlays only.

## Local reproduction

Requires Python 3.11, Pillow, Noto Sans CJK JP fonts, FFmpeg/FFprobe:

1. `python -m unittest discover -s quality/cycle900/tests -v`
2. `python quality/cycle900/src/review_panel.py /tmp/c900-overlays`
3. `bash quality/cycle900/src/render_review.sh /private/source_cycle899.mp4 /private/output_cycle900.mp4 /tmp/c900-overlays`

The overlay timings are tailored to the reviewed 23.033s source; adapt timing only after inspecting another source.

## Research, ten genres, limits

Consulted accessible summaries of TikTok市場分析 / TikTok動画研究 (strong first 1.5s, short scenes, real UI proof, clear Japanese captions, Before/After, CTA), the prior 16-panel storyboard notes and the actual cycle899 private MP4. Original v33 MP4 and full research transcripts unavailable for this run. Code validates 10 genre identifiers; only one AI-work video was rendered.

Independent Japanese ASR/semantic subtitle matching, inherited media rights, phone hardware playback, human approval, reference-video parity and actual Actions billing remain unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No auto-posting, public media upload, paid service, or merge. Manual posting only after employee approval.
