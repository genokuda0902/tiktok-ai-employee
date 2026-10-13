# Cycle547 — spreadsheet focus zoom (REVIEW ONLY)

Baseline: cycle546, 20s 1080x1920 H.264/AAC, source SHA256 312bbccbf1dd4e5f596bc0ebee013ebfd45447c248a1285ffef1ce09383d6598.
Changed interval: 9.0–12.0s. Enlarge synthetic spreadsheet data 120/150/200/250, animate selection, show =SUM(B2:B5), and reveal 720.
Output MP4 SHA256: fee822f42e2e90764886e0bd73a3b1b419bebd37a45ff0a52e487141137f1c11.
Local QA: 11 tests passed, 600/600 frames decoded, 20.000s, audio stream copy hash matched previous. Japanese speech and semantic caption synchronization NOT verified.
Source and MP4 are in separately shared cycle547 ZIP. Full renderer is NOT committed: GitHub write safety check rejected it. CI workflow creation and draft PR were also blocked.
The committed scene_contract.py and tests/test_cycle547_scene_contract.py are reusable across ten genres, but only ai_work was rendered.
Rights: synthetic assets only. Publication NOT_APPROVED. Human review required; no automatic posting, no merge.
