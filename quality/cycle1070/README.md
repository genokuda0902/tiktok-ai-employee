# cycle1070 — concrete output-format example (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. This is a new implementation, **not** recovered v33 source. No public/private media upload to GitHub, no merge, auto-post, paid API or external distribution.

## Evidence / distinct improvement

- Previous same-stream cycle1068: cleaned stale lower bridge overlays in scenes 1/3/4/5/7, leaving existing narration and subtitles intact.
- Current cycle1070: scene 04's third prompt field 形式 previously showed only generic 表とグラフ用データ; now reveals the more actionable fictional example 月別比較表（CSV形式） with half-second typing followed by a hold. Other scenes and caption band are protected. Ten genres have configurable examples and accents.
- Source video is local, SHA256-pinned, not uploaded or committed. Existing Japanese AAC and eight burned-in caption intervals are inherited; independent speech-to-text and semantic matching remain NOT VERIFIED.

## Run locally (only on rights-approved local source)

~~~bash
python3 -m unittest quality.cycle1070.test_format_reveal -v
python3 -m quality.cycle1070.format_reveal --source /local/review_only.mp4 --source-sha256 EXPECTED_SHA256 --out /local/review_output.mp4
~~~

CI runs synthetic A/V only. Font: Noto Sans CJK. Dependencies: Pillow and FFmpeg/FFprobe; full render on GitHub uses no user media.

## Measured local QA

- Source cycle1068 SHA256: bab502c5ee3e5ef4e8b74e64a866d358559aab55f5948777814e7e550e29a1a8
- New cycle1070 SHA256: 8367ba563af7d1dee6307e2bf188b8c78fd2c06d5c577df1851681889aa98a62
- 23.033333s / 691 frames / H264 1080x1920 30fps / AAC 48kHz stereo.
- Full A/V decode PASS, AAC ADTS bitstream SHA identical; 8 SRT intervals retain measurable audio energy.
- Caption y>=1460 mean pixel delta max 0.8409/255; non-target scenes max mean upper-region delta 1.3702/255. Target field changed 29 frames (313-341). Local 13 tests PASS.
- CI is synthetic-only; it does not verify the private full MP4. No independent Japanese ASR or semantic subtitle validation.

## Research and reference limitations

Accessible summaries from TikTok市場分析 and TikTok動画研究 emphasize fast visual hook, one message per clip, clear Japanese subtitles, actual operation demo, before/after, manual employee approval and posting. User's 16-panel storyboard was directly viewed: robot/people, ChatGPT prompt entry, spreadsheet-to-chart, before/after and CTA. The original research chats and v33 MP4 are not accessible in this cycle. Storyboard ~36s/16 panels vs inherited ~23s/8 scenes; no equivalence claim.

## Next review gates

- Independent Japanese narration transcription and word-level subtitle timing, especially 20.300s.
- Rights, privacy, phone playback, employee approval, Actions billing unverified.
- Do not merge or publish without employee review and manual approval.
