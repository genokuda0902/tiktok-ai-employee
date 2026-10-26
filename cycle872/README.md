# cycle872 — Cinematic first-3-second proof hook (review only)

Reimplementation, not the original v33 engine. This cycle replaces the first **89 frames** (0–2.967 s) of cycle871's private review MP4 with a moving, original AI-generated office photo and synthetic month-by-month evidence (4月 12/8, 5月 16/9, 6月 18/12, 合計46/29). Unlike the preceding cycle871, which improved scene07 (17–19.6s), this addresses the high-priority first-1.5-second hook and first scene's flat graphic. Existing lower Japanese subtitle region and inherited AAC narration are not modified by design. All synthetic data is explicitly labeled as such.

## Private local render

~~~bash
PYTHONPATH=cycle872 python -m unittest discover -s cycle872 -p 'test_*.py' -v
python cycle872/cinematic_hook.py --source <private-cycle871-mp4> --photo <private-review-photo> --output <new-review-mp4> --manifest <sha-pinned-review-only-manifest.json> --report <render-report.json>
~~~

Manifest requires \`source_sha256\`, \`photo_sha256\`, and **all** keys in \`POLICY\` exactly. Private MP4, photo and inherited Japanese voice are NOT uploaded to public GitHub; the 1s CI synthetic media test does NOT validate this finished private MP4. The photo's public-use rights and the inherited audio license are NOT approved. Do not post or distribute beyond authorized human review.

## Verified local output, 2026-10-27 JST

- Input cycle871 SHA256: \`5766f76ead244655350544dc538458c9e7ef46d36d0740ca4b8ce73b1923a65a\`.
- Output cycle872 SHA256: \`5a4a88601d4618d4b6bd435cbf0c70fefabb668b488568b1573e599e72cadf4a\`.
- MP4: 1080×1920, H264 30fps 691 frames / 23.033333s, inherited AAC 48kHz ADTS hash unchanged \`2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9\`.
- 89/89 target frames visibly changed, scene mean delta 70.842; protected caption region y1490:1840 max mean pixel delta 0.7314 across all 691 frames, full A/V decode PASS, 12 local tests PASS.
- CI only tests portable source and a synthetic one-second MP4. The actual private finished MP4 is provided via ChatGPT sandbox, NOT a GitHub artifact.

## Sources and limitations

Consulted accessible summaries of TikTok市場分析 and TikTok動画研究 (full chats inaccessible). User's 16-panel storyboard directly inspected; original v33 MP4 unavailable this cycle. Still 23.033s / 8 scenes versus 36s / 16-panel reference. This hook uses a generated photographic still, not live-action filmed footage or a real Excel/ChatGPT recording. No independent Japanese ASR for meaning/pronunciation/subtitle timing, smartphone test, retention test, rights clearance, employee approval, or billing verification. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merges, paid services, auto-posting, or private asset uploads.
