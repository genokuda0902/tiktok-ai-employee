# cycle863 — evidence-backed Before/After motion card (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Reimplementation; NOT original v33. No posting, merge, paid service, or unapproved media upload.

## Actual change vs cycle862

- Replaced **scene 6 frames 425–506** (82/691, 14.167–16.900 seconds) within x40..1039, y350..1439 with an original staged Before/After card. The existing fictional Calc example is visually explained as **17 → 18**, with the actual previously recorded Calc screen as supporting evidence, not as a claimed AI-generated result.
- First beat introduces the unverified number; second reveals the corrected value; third reinforces checking source data. No robot motion, fabricated UI, performance claim, or new copyrighted asset.
- **10-genre** templates share motion, typography, safe region, fail-closed source manifest and tests. Only `ai_work` was rendered into a full Japanese review MP4.
- Original AAC elementary stream copied unchanged. Burned-in Japanese subtitles outside the picture ROI are preserved. No independent speech transcription, meaning/word-level alignment, or pronunciation validation is claimed.

## Reproduce with local private review media only

```bash
python3 -m pip install pillow numpy
PYTHONPATH=cycle863 python3 -m unittest discover -s cycle863 -p 'test_*.py' -v
python3 cycle863/proof_compare.py --source /private/cycle862_ACTIONABLE_OUTRO_JAPANESE_REVIEW_ONLY.mp4 --output /private/cycle863_PROOF_BEFORE_AFTER_JAPANESE_REVIEW_ONLY.mp4 --manifest /private/source_manifest.private.json --report /private/render_report863.json
PYTHONPATH=cycle863 python3 cycle863/verify_review.py /private/cycle862_ACTIONABLE_OUTRO_JAPANESE_REVIEW_ONLY.mp4 /private/cycle863_PROOF_BEFORE_AFTER_JAPANESE_REVIEW_ONLY.mp4 /private/verification863.json
```

Private manifest must equal `POLICY` from `proof_compare.py` plus SHA-256 of the local MP4. Never commit source MP4, extracted screenshot, private manifest, finished MP4, personal information, or source rights-unapproved media.

## Reference and prior research

- Consulted accessible summaries of **TikTok市場分析** and **TikTok動画研究**: first 1–1.5s hook, short purposeful beats, real UI proof, clear Before/After, readable Japanese subtitles, employee-reviewed manual posting. Full original task/chat transcripts were not accessible.
- Directly inspected user-provided **ChatGPT×Excel時短術16コマ絵コンテ.png**, particularly panel 9 (Before/After) and panels 7–8 (spreadsheet-to-chart). Current 8-scene, 23.033-second review master remains less varied/cinematic than 16-panel, ~36-second storyboard.
- Original v33 MP4 (previously documented as 31.553s, 512×910) was unavailable this cycle; no direct visual quality comparison. v33 renderer still not recovered. `PROJECT_HANDOFF.md` and `recovery/v33/RECOVERY_STATUS.md` prohibit robot motion and unapproved assets.
- Checked latest main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, open PR #210 and parallel #211, old `src/build_daily.py` silent `-an` generator, and prior cycle862 code. This PR stacks on #210; #211 remains untouched.

## Validation limits

Local unit tests: 14/14 PASS. Actual finished private MP4: 1080×1920 H264 30fps 691 frames, 23.033s, AAC48kHz. Full A/V decode PASS, source/output ADTS AAC SHA-256 identical, changed picture samples ~92–95 average absolute pixel difference; caption region samples <=0.164; unchanged picture samples <=0.321. These are technical checks only, not speech semantics, rights, retention, smartphone playback, reference equivalence, or staff approval.

CI uses synthetic media and unit tests only; finished private Japanese MP4 is NOT on GitHub Actions. Actual GitHub Actions charges were not independently verified.