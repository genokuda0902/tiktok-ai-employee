# cycle960 — first-two-second evidence preview (REVIEW ONLY)

2026-10-29 JST. Independent of parallel PR #358 (mobile subtitle panels); based on unmerged PR #357. Reimplementation, **not recovered v33**.

**What changed:** cycle958 had a static Before/After opener with no concrete spreadsheet evidence until 11.6 seconds. This experiment extracts a frame at 13.8 seconds from the same **private** 23.033s demo and displays the fictional Calc result `12+16+18=46` / `8+9+12=29` as a 410×310 px proof card over the After panel between 0.35–2.34s. A 0.18s fade-in and 0.28s fade-out avoid hard overlays. The original Japanese voice, subtitles and bottom voice wave remain intact; there is no external asset. **This is a real Calc recording with fictional values, not a newly recorded screen capture.**

Reproduce locally with the exact private review source (SHA-256 `ac5fcfcfc744edbf9ec4cf7080e53ce88a9e7a9512021593119188ed66bbb22a`):

```sh
python -m pytest -q cycle960/test_hook_proof_preview.py
python cycle960/hook_proof_preview.py --source /private/cycle958.mp4 --output /private/cycle960.mp4 --qa /private/render_qa960.json
python cycle960/verify_output.py --source /private/cycle958.mp4 --output /private/cycle960.mp4 --qa /private/qa960_full.json
```

Needs Python, Pillow, OpenCV/numpy (verification only), Noto CJK fonts, ffmpeg/ffprobe. GitHub CI runs 19 isolated synthetic tests and checks no private media is committed; it does **not** validate the full private MP4. The full MP4 is shared only through the private ChatGPT review attachment.

Research: accessible summaries of `TikTok市場分析` and `TikTok動画研究`; user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` directly inspected (16 panels, early hook, cinematic robot/person, real ChatGPT/Excel demonstration). Complete original chats and original v33 MP4 were unavailable. This remains an 8-scene video and is not comparable to v33 quality by direct playback.

10 distinct genre evidence profiles are configured; only `ai_work` has reviewed source/geometry. Nine others fail closed. No posting, merge, new paid services, or public publication. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Rights, independent Japanese ASR/transcription, phone playback, and employee approval remain unverified.
