# cycle834 — actual Calc interaction in a review-only MP4 (2026-10-25 JST)

## Sources checked
- GitHub main: 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Unmerged parallel PR #156 (cinematic hook), #157 (10-genre focal layout); this branch is stacked **on #157**, not merged to main. It uses the locally generated cycle833 review MP4 as video input, so do not claim that CI reproduces the final Japanese review MP4.
- PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md; original v33 source/prompts not recovered.
- TikTok市場分析 / TikTok動画研究: prior summaries only, full transcripts unavailable.
- User's ChatGPT×Excel 16-panel storyboard inspected: screen operation, result verification, 1.5-sec hook, fast cuts. Original v33 MP4 unavailable this run; no direct comparison.

## Change vs cycle833
- The previous static mock laptop for scene 3 (frames 194..284, 6.467..9.5s) is replaced by an **actual recorded LibreOffice Calc GUI** selecting cells and typing =SUM(B2:D2).
- The workbook was created with **fictional** values only; no customer or employee data.
- Frame-safe image box (x62..1018,y390..1390) protects existing title/CTA and bottom Japanese subtitles.
- Audio is copied from the cycle833 source. This does NOT certify pronunciation or subtitle semantics.
- 10-genre reusable compositor and fail-closed tests; actual review MP4 only for AI仕事術.

## Local reproduction (requires approved/review-only source assets)
1. Create fictional workbook in LibreOffice Calc; capture the actual GUI in Xvfb 1366x768/30fps with FFmpeg x11grab (no personal data).
2. Run:
   python cycle834/screen_insert.py --source cycle833_CINEMATIC_HOOK_JAPANESE_REVIEW_ONLY.mp4 --clip calc_real_capture.mp4 --out cycle834_REAL_CALC_REVIEW_ONLY.mp4
3. Run:
   PYTHONPATH=cycle834 python -m unittest discover -s cycle834 -p 'test_*.py' -v
   ffmpeg -v error -xerror -i cycle834_REAL_CALC_REVIEW_ONLY.mp4 -f null -
4. For synthetic CI fixture only: bash cycle834/ci_smoke.sh.

## Security / unresolved
The final Japanese MP4 and inherited audio/image assets are NOT uploaded to public GitHub.
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, posting, paid APIs, rights certification, or employee approval.
Pending: independent Japanese speech recognition/word sync, rights review, phone playback, full v33 video parity.
