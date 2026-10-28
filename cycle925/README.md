# cycle925 — readable one-action CTA (REVIEW ONLY)

Distinct from cycle923's seven scene wipes (#306), cycle924's scene03 report preview (#307), and earlier cycle911's three-step safe-area CTA. This pass simplifies the last scene into a single concrete example and three large, sequential action verbs, with high-contrast editorial cards and no claim of time saved. The new frame art uses local Pillow only (no external assets).

- Source: local cycle923 MP4 SHA256 `35a7483d2c2916ed876bf022d17d71438318bca270e1e7853a76d01bcd8ec0d4`.
- Local finished MP4: `cycle925_ONE_ACTION_CTA_JP_HUMAN_REVIEW.mp4`, SHA256 `964bf6d21980cd42e6fbe321d51aca66f237df1bd1845c4cfa4da44e0f096c14`. Shared in private ChatGPT artifact only; **not** committed here.
- Changes only scene08 frames 609–690 (82 frames) at 1080x1920, keeps existing subtitle/footer y>=1460 intact at overlay source level.
- 10 configurable fictional genre examples; only AI-work MP4 rendered. No made-up actual results.
- Local technical QA: 13/13 pass; full decode, 691 frames, 30fps, AAC48kHz bitstream identical, caption region max quarter-res MAE 2.043. This is not a semantic Japanese ASR or commercial rights test.

## Reproduce with local private source

```bash
python cycle925/src/one_action_cta.py --source /private/cycle923_EDITORIAL_WIPES_JP_HUMAN_REVIEW.mp4 --output /private/cycle925_ONE_ACTION_CTA_JP_HUMAN_REVIEW.mp4 --expected-source-sha 35a7483d2c2916ed876bf022d17d71438318bca270e1e7853a76d01bcd8ec0d4
python -m unittest discover -s cycle925/tests -v
```

Local renderer needs ffmpeg, OpenCV, Pillow, NumPy, and installed Noto CJK fonts. CI intentionally uses only stdlib and synthetic checks. No user media is stored in public GitHub.

Research context: available summaries of TikTok市場分析 / TikTok動画研究 and 16-panel user storyboard favor immediate hooks, visual variety, real-world proof, legible Japanese, and human review. Original v33 MP4 unavailable. No independent Japanese ASR, spoken-caption timing check, rights clearance, smartphone test, employee approval, or Actions billing confirmation. No auto-posting, paid services, or merge.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
