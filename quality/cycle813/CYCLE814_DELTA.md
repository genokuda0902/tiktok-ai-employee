# cycle814 — readable real-screen focus (REVIEW ONLY)

## Prior cycle813 -> cycle814 delta
- cycle813 placed an actual sanitized LibreOffice Calc capture in frames 90–179 but the entire toolbar and cells were tiny on a phone-sized vertical video.
- cycle814 crops **original-resolution** capture pixels before resize, smoothly zooms from a 960px-wide overview to a 630px focus (1.52x relative text scale), pans from goal B2 to calculated gap D2, and holds the last frame so **20 -> 12 -> 8** remains visible.
- Number annotations are delayed until the corresponding source-capture values are actually visible; the screenshot is real local GUI recording with fictional numbers.
- Shared ten-genre accents, crop geometry checks, safe-area contract and nonpublication gates. No new user/private assets uploaded to GitHub.

## Local verification (2026-10-24)
- Input: cycle813 MP4 SHA256 `ac4aee47e6f82af1e0630bbd51669c3e3dd838e389c05689fd22f5d6d29db3e1`.
- Output: cycle814 private MP4 SHA256 `66ebd1f7fd81dcdfef2ce1fba09106f91f28fd36140d68cfcc799402fb8feda2`.
- 1080×1920, H.264 30fps, 718 frames, 23.933333s, AAC 48kHz; full A/V decode PASS, AAC ADTS hash identical to input.
- Local Python unit tests **13 PASS**.
- Mean full-frame RGB absolute difference vs cycle813: **7.7965** at 4.5s; **8.1513** at 5.7s; control 7.2s **1.2490** (re-encode noise).
- Scene contact sheet visually inspected for 8 subtitle regions. This is NOT independent ASR or speech/caption semantic validation.
- Local review MP4 and original real Calc capture are private conversation artifacts, **not committed** to this public repo.
- CI creates a synthetic color/tone MP4 and synthetic screen capture; never treat it as Japanese voice or the real review video.

## Reproduction (private assets required)
```bash
PYTHONPATH=quality/cycle813 python -m unittest discover -s quality/cycle813 -p 'test_*.py' -v
python quality/cycle813/calc_screen_insert.py \
  --source cycle813_REAL_CALC_GOAL_REVIEW_ONLY.mp4 \
  --capture real_calc_capture_final.mp4 \
  --output cycle814_CALC_FOCUS_REVIEW_ONLY.mp4 \
  --genre sales_business --target 20 --actual 12 --fictional-data
ffmpeg -v error -xerror -i cycle814_CALC_FOCUS_REVIEW_ONLY.mp4 -f null -
```

## Reference/provenance
- Past TikTok市場分析/TikTok動画研究 research **summaries** were consulted; full task/chat research inaccessible.
- User's 16-panel ChatGPT×Excel storyboard image inspected directly, especially real-operation panels 4–8.
- Original v33 MP4 (31.553s) unavailable in this runtime; no direct frame comparison or quality equivalence claim.
- Main checked at `18e084c38db0dc55db7dfc0532b9451b1167f2aa`; handoff and v33 recovery docs read. Builds on unmerged PR #120, not merged.

## Remaining gates
Independent Japanese ASR and caption meaning/word sync, voice/visual rights, real-device playback, employee review and v33 side-by-side are unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No paid services, merge or automatic posting.
