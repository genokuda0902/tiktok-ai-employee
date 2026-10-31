# cycle1109 — Japanese-first UI chrome (review only)

## Difference from cycle1107
cycle1107 retimed 7 scene cuts to low-energy voice pauses. This cycle does **not** change the cut points or voice timing. It replaces visible English template labels with Japanese on all 8 scenes:
- Global top bar: AI WORKFLOW -> genre label, VOICE -> 音声, STEP -> 手順
- Global footer: LOCAL DEMO / HUMAN REVIEW ONLY -> 確認用サンプル｜社員承認前・投稿禁止
- Scene 1: FIRST STEP -> 最初の一歩
- Scenes 2–8: KEY IDEA -> 今日の要点; AI WORKFLOW / HUMAN REVIEW -> AI時短術 ／ 公開前確認

The original audio-reactive bars, 8 scene counters, subtitles, and AAC audio packets are retained. This is not an ASR or subtitle semantic verification.

## Reproduction (with legitimately available source media)
Install FFmpeg, Pillow and a Japanese-capable Noto Sans CJK font.
```bash
python cycle1109/code/jp_chrome.py INPUT.mp4 OUTPUT.mp4 --genre ai_work --duration 22.5 --scene1-end 3.133333
python -m unittest discover -s cycle1109/tests -p 'test_*.py' -v
```

## Local actual MP4 QA (not uploaded publicly)
- 22.5 s / 1080x1920 / 30fps / 675 frames / H.264 / AAC 48kHz / 8 chapters
- Full video/audio decode PASS
- AAC ADTS SHA256 identical to source: `da601fdd17eae3cc1c0fe9a0d93843f6c07e1321d33f84f92474819c477d8b18`
- 8 sampled frames: localized header and footer changed, caption region mean delta max 1.805/255 (re-encode)
- Local 7/7 tests PASS; ten genre labels render as PNGs, actual full MP4 tested only for ai_work
- The full review MP4, visual comparisons, QA JSON and source code are shared privately in the conversation.

## CI and safety
GitHub Actions uses synthetic 2-second media only, not private or user-supplied media. No auto-post, merge, paid contract, or public upload of the real MP4. Geometry masks are specific to the 8-scene AI-work template and must be adapted before applying to other layouts.

## Outstanding checks
Independent Japanese ASR and semantic subtitle sync are not verified. The underlying mockup illustrations may still contain English labels. v33 reference original, rights for the inherited visual assets, real smartphone playback, retention impact, employee approval and GitHub Actions billing are unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED — employee approval before manual posting only.**
