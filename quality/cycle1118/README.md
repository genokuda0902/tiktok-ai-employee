# cycle1118 — optional Japanese scene-caption track (REVIEW ONLY)

This is a **reimplementation/review aid**, not recovered v33 code. The 23.033-second/8-scene source is the private cycle1116 review MP4, SHA256 `36c940b02ebf5818477c04ee51329a0efac3fb51534ab2a836af17e0e78945e6`.

## Distinct change
Unlike cycle1116's high-contrast disclaimer, this cycle adds a **selectable Japanese `mov_text` subtitle track** to the MP4, plus a standalone UTF-8 SRT with eight **manually transcribed visible scene captions**. The underlying H.264 and AAC elementary streams remain bit-identical. This enables caption extraction and accessibility/review comparison without re-encoding the footage or audio. Because captions are already burned into the source, the soft track may be marked **default=1** by FFmpeg MP4 muxing even when requested otherwise. In the verified local MP4 it **is default=1**, so some players may display duplicate captions over existing burned-in captions. Disable the selectable track in the player or use the prior clean cycle1116 MP4. Some mobile/TikTok players may strip or ignore the track; the SRT is the review fallback.

**Important:** The SRT is transcribed from the existing **on-screen text**, NOT independently from spoken Japanese. Therefore this does **not** close the independent ASR / speech-to-caption semantic alignment gate.

## Reproduce with an authorized private review source

```bash
python quality/cycle1118/caption_accessibility.py  --source /private/cycle1116_PROVENANCE_BANNER_JP_REVIEW_ONLY.mp4  --source-sha 36c940b02ebf5818477c04ee51329a0efac3fb51534ab2a836af17e0e78945e6  --out /private/cycle1118_OPTIONAL_JAPANESE_CAPTIONS_REVIEW_ONLY.mp4  --srt /private/cycle1118_scene_captions_NOT_ASR.srt  --report /private/cycle1118_qa.json
python -m unittest discover -s quality/cycle1118 -p 'test_*.py' -v
```

Fail closed for mismatched source SHA, existing outputs, unsupported A/V, wrong dimensions/FPS, incomplete/overlapping/too-fast captions, simple email/phone patterns. The CI uses a **synthetic 3-second video only**; the private MP4, audio, frames, and subtitle content from the real user video are **not committed**.

## References, safety and remaining work

Accessible summaries of TikTok市場分析 / TikTok動画研究: hook in first 1.5s, purposeful cuts, real UI, Before/After, readable Japanese text, manual employee approval. Full task/chat transcripts not accessible. User's 16-panel ChatGPT×Excel storyboard consulted: 16 panels/~36s vs current 8 scenes/23s, much richer live action/robot/GUI and transitions. Original v33 MP4 and renderer not accessible.

Independent Japanese ASR, meaning/timing alignment, phone playback, rights, employee signoff and actual Actions billing remain **unverified**. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, payments, public private-media upload.
