# cycle982 — real Calc GUI review-only scene

This is a **reimplementation**, not recovered v33 source. It replaces only frames 174–260 (5.80–8.70s) in an already approved-for-private-review 1080×1920/30fps source video. It preserves inherited Japanese subtitles below y=1440 and copies the original AAC audio bitstream. **No independent Japanese speech-to-text or semantic subtitle alignment is claimed.**

## Private/local-only source preparation

1. Create a **fictional** Calc workbook with columns 月, 営業A, 営業B and values 4月 12/8, 5月 16/9, 6月 18/12. The sum formulas are B5 `=SUM(B2:B4)` (46) and C5 `=SUM(C2:C4)` (29).
2. Start LibreOffice Calc in an isolated Xvfb desktop (1280×800) and dismiss any first-run banners.
3. Record a 5.5s 30fps screen capture while clicking B5 and C5, entering the formulas, and confirming the results. This is a **genuine local GUI recording**, not a simulated Excel or ChatGPT screen. Do not record real customer data.
4. Keep the screen capture and inherited source MP4 **private/local**; never commit them.

Example, once `source.mp4` and `calc_capture.mp4` exist:

```bash
python cycle982/calc_gui_scene.py --source source.mp4 --screen calc_capture.mp4 --output review.mp4 --work /tmp/cycle982-work
python cycle982/qa_calc_gui_scene.py --source source.mp4 --output review.mp4 --report qa.json
PYTHONPATH=cycle982 python -m unittest discover -s cycle982 -p 'test_*.py' -v
```

## Verified private local output (2026-10-30 JST)

- Input SHA256 `83c53a2f1008de51bf3d2b82f17c08f34a1dc2a12956601eee8c55ed18fec95f`
- Output SHA256 `0f643009e525bb4e5d775b1f20cc6c0a937c4fe650dcba17cbc7e9ff6bb240eb`
- H.264 1080×1920, 30fps, 691 frames, 23.033333s; AAC 48kHz; full A/V decode PASS; AAC ADTS payload identical
- Caption region y>=1440 max sampled mean difference 0.3977/255; outside edited scene max 0.8967/255; changed scene mean 54.6714/255
- 7 local unit tests PASS; GitHub Actions uses **synthetic-only** audio/video and screen fixtures
- 10 genre identifiers, only `ai_work` real scene geometry inspected; others fail closed

## Unverified gates

Original reference v33 MP4, full market research chats, independent Japanese transcription and caption semantic timing, smartphone playback, asset commercial rights, employee approval, actual Actions billing. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, private media upload, or paid service.
