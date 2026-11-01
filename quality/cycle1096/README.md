# cycle1096 — speech-preserving CTA + acoustic-presence QA (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original v33 generation engine not recovered. No merge, auto-post, paid service or upload of the private Japanese MP4 to public GitHub.

## Change from cycle1094
- cycle1094 changed only opening robot zoom; cycle1096 changes the final scene only: at frame 659 (21.967s) a Japanese action cue 「次は1つ試す」 fades into the previously unused top-right header region (x510, y48, w365, h120) and remains until frame 690. All existing eight Japanese captions are retained.
- Initial trial overlapping the progress bar and second trial overlapping the calculation text were rejected. Final version was visually checked for text separation.
- A 20ms RMS acoustic-presence check covers all eight chapter intervals and detects last above-threshold energy at approximately 22.40s. It is NOT ASR, and does NOT prove speech, meaning, pronunciation or word-level caption sync.
- Ten-genre palette presets, SHA256-pinned local input, fail-closed fictional-data/privacy/rights/review-only manifest and synthetic A/V smoke test.

## Reproduction (private media never committed)
Run the ten tests: python3 -m unittest discover -s quality/cycle1096 -p 'test_*.py' -v
Run synthetic CI smoke: python3 -m quality.cycle1096.cta_voice_guard --smoke
Run real review render: python3 -m quality.cycle1096.cta_voice_guard --source PRIVATE_CYCLE1094_MP4 --source-sha 7baf6bae7d23666b5f1fef7ce051a92838d9248b6587632d51c89c09be31506f --manifest quality/cycle1096/manifest.json --out PRIVATE_CYCLE1096_MP4 --report PRIVATE_QA_JSON

## Verified local result (2026-11-01 JST)
- Actual private MP4: H264 1080x1920 30fps, 691 frames / 23.033333s, AAC 48kHz stereo; full A/V decode PASS.
- Original and output AAC ADTS hashes identical, without narration re-encoding.
- 10 local unit tests PASS; 23-second synthetic A/V render/decode PASS.
- Acoustic energy detected in 8/8 intervals. No independent Japanese ASR or semantic alignment verified.
- The original and output MP4 remain private; GitHub CI tests synthetic media, NOT the actual finished Japanese video.

## Reference and next tasks
- Consulted available previous summaries of TikTok市場分析 and TikTok動画研究; original task/chat transcripts inaccessible.
- Directly inspected user-provided ChatGPT×Excel時短術16コマ絵コンテ.png. Original reference v33 MP4 not accessible this cycle.
- Storyboard has 16 panels, 3D robot, person and real UI; current 8-scene/23-second video is NOT equivalent.
- Next: offline independent Japanese ASR and all eight subtitle meaning/timing checks (especially 20.300s onward), smartphone playback, release rights and employee approval. Actions billing and nine other full-genre renders remain unverified.
