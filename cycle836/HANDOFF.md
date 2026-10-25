# cycle836 — real Writer prompt-template save (2026-10-25 JST)

## Verified baseline and references
- main checked: 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Base: unmerged PR #160 (cycle835 real Calc cross-check); parallel PR #161 (conceptual hook) remains separate/unmerged.
- Read PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, cycle835/HANDOFF.md and 10-genre code.
- TikTok市場分析 / TikTok動画研究 prior research summaries consulted; full transcripts unavailable.
- User's 16-panel ChatGPT×Excel storyboard inspected: hook, real UI, Before/After, readable captions, CTA. Original v33 MP4 inaccessible in this run; no direct parity comparison.

## Change vs cycle835
- cycle835: real LibreOffice Calc source cross-check in scene 5 (12.8–16.1s).
- cycle836: real **LibreOffice Writer** edit/save of fictional reusable AI prompt templates replaces static save illustration in scene 7 (frames 583–671; 19.433–22.400s).
- Isolated local Xvfb capture, fictional document and no personal/customer data. Saved status displayed as 保存状態：SAVED.
- New writer_capture_insert.py is a reimplementation, not original v33. It enforces fictional-only provenance, app type, caption/CTA safe zones, capture length, 10 genre presets, and copies inherited Japanese AAC unchanged.
- Local Japanese review MP4, inherited source and GUI capture are **not uploaded or committed** due to unapproved publication rights.

## Reproduce locally (rights-gated sources)
- PYTHONPATH=. python -m unittest discover -s cycle836 -p 'test_*.py' -v
- python cycle836/writer_capture_insert.py --source cycle835_REAL_GUI_VERIFICATION_JAPANESE_REVIEW_ONLY.mp4 --capture writer_save_capture.mp4 --manifest capture_manifest.json --capture-start 1.5 --out cycle836_REAL_WRITER_SAVE_JAPANESE_REVIEW_ONLY.mp4
- ffmpeg -v error -xerror -i cycle836_REAL_WRITER_SAVE_JAPANESE_REVIEW_ONLY.mp4 -f null -
- bash cycle836/ci_smoke.sh: **synthetic test pattern + sine tone only**; not the Japanese review video.

## Verified local results
- 12 unit tests PASS; synthetic audiovisual integration PASS.
- Japanese review MP4 H.264 1080x1920 30fps / 775 frames / 25.833s; AAC 48kHz, full decode PASS.
- AAC elementary stream bit-identical to cycle835.
- Pixel MAE vs cycle835: 20.8s 35.364; 21.9s 35.195; outside change 11.0s 1.452 and 24.0s 1.348.
- Protected caption region MAE at 20.8s 1.245 (re-encode drift); Japanese subtitle region preserved.
- Review MP4 SHA256 f76f66d97cebda1d6fedfd71e674ef2db27f58f22b44082aa59df00c2fee8624.

## Still unverified
- Japanese pronunciation, semantic speech/caption match, word-level timing, smartphone playback, inherited asset rights, employee approval, original v33 parity.
- Next: independent Japanese voice/subtitle audit; approved native-HD assets; phone playback and employee review.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid API, auto-post or publication.
