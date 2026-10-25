# cycle835 — real GUI source cross-check (2026-10-25 JST)

## Inputs / research / exact inheritance
- Checked main 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Base is unmerged PR #158 (real Calc formula demo); parallel PR #159 is independent and NOT merged.
- Read PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, cycle834/HANDOFF.md, compositor and tests.
- Prior summaries of TikTok市場分析 and TikTok動画研究 referenced; full task/chat transcripts unavailable.
- User-provided 16-panel ChatGPT×Excel storyboard inspected. Original v33 MP4 unavailable for direct comparison.

## Difference from cycle834
- cycle834: scene 3 (6.467–9.5s), actual Calc formula entry.
- cycle835: scene 5 (frames 384–481; 12.8–16.067s), independent actual Calc GUI source cross-check: fictional AI total 18 vs original 17; correct to 17; difference 0 and OK.
- Isolated Xvfb LibreOffice recording with fabricated workbook, no employee/customer data. Full local MP4 and inherited Japanese voice are not uploaded to public GitHub.
- Ten-genre fail-closed compositor checks provenance and safe zones, copies AAC unchanged, and never grants publication rights.

## Reproduction (local, rights-gated assets)
PYTHONPATH=cycle835 python -m unittest discover -s cycle835 -p 'test_*.py' -v
python cycle835/evidence_insert.py --source cycle834_REAL_CALC_REVIEW_ONLY.mp4 --capture real_calc_check_capture.mp4 --manifest capture_manifest.json --genre ai_work --scene 4 --out cycle835_REAL_GUI_VERIFICATION_JAPANESE_REVIEW_ONLY.mp4
ffmpeg -v error -xerror -i cycle835_REAL_GUI_VERIFICATION_JAPANESE_REVIEW_ONLY.mp4 -f null -

CI uses bash cycle835/ci_smoke.sh with synthetic test pattern and sine tone ONLY.

## Local verification
- Japanese review MP4: H.264 1080×1920 / 30fps / 775 frames / 25.833s, AAC 48kHz.
- AAC elementary stream identical to cycle834; full AV decode PASS; 10 unit tests PASS.
- MAE vs cycle834: 13.7s 51.665, 14.7s 51.339, 15.7s 50.839; outside scene 11s 1.475.
- Caption region preserved by sampled pixel comparison, not by independent speech recognition.
- Actual Japanese pronunciation, word-level subtitle sync, smartphone playback, rights approval and v33 parity NOT verified.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid API, auto-post, or publication.

## Next
Independent speech/subtitle audit, rights-approved native-HD imagery, additional sanitized real GUI clips, phone playback and employee manual approval.
