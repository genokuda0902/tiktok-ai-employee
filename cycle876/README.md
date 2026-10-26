# cycle876 — source-to-prompt local UI evidence (human review only)

**Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Reimplementation, not the original v33 source. Never merge/publish/post without review. No third-party media upload or paid services.

## Difference from cycle875

Previous scene 04 (frames 251–335, 8.367–11.200s) showed a static offline prompt screenshot with no source-data evidence. This change replaces only the middle picture region (y=285..1449) with an original, clearly labeled **offline simulated UI**: same fictional three-period input data as chart and before/after scenes -> visible typing of a three-part Japanese instruction -> deterministic totals from the source data. The existing burned-in Japanese captions, title and audio track remain inherited; we do not claim semantic narration/subtitle verification. The UI does not contact any AI provider or claim a real ChatGPT/Excel session.

Shared `cycle874.chart_truth.GENRES` is the single source for 10 genre-specific values. Only `ai_work` has been exported to a full review MP4. No external/real customer data, new voice, logos, private image, or actual service access introduced.

## Local reproduction (requires a private cycle875 MP4)

Free dependencies: `pillow`, `numpy`, `ffmpeg`, `fonts-noto-cjk`.

```bash
PYTHONPATH=.:cycle876 python -m unittest discover -s cycle876 -p 'test_*.py' -v
python cycle876/prompt_source_demo.py --source /PRIVATE/cycle875_REVIEW_ONLY.mp4 --output /PRIVATE/cycle876_REVIEW_ONLY.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/render_report.json
```

Manifest is exactly `POLICY` plus `source_sha256`. No manifest, completed video, source video, audio, frames, reference storyboard, or rights-sensitive data is committed. CI only tests source code and synthetic A/V; the private Japanese full video is tested locally.

## Research and limitations

Accessible `TikTok市場分析` / `TikTok動画研究` summaries prioritize first 1.5s hook, concise scenes, demonstrative UI, before/after, Japanese captions and human approval; full original chats unavailable. User's 16-panel/36-second `ChatGPT×Excel時短術16コマ絵コンテ.png` was inspected. Reference original v33 MP4 inaccessible this run. This scene moves toward the reference's panel 4 instruction entry, but the reference has genuine application footage, cinematic people/robot and 16 cuts; ours is a local illustration and 8 scenes.

Remaining gates: independent Japanese speech transcription, semantic caption alignment, smartphone playback, inherited media publication rights, employee approval, original v33 comparison, and actual GitHub billing. Human-approved **manual** posting only.