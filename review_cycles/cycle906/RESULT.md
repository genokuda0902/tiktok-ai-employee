# cycle906 — evidence-chain motion, review only (2026-10-28 JST)

**Change vs cycle904:** Adds an animated 3-step, 81-frame proof-chain ribbon in scene05:
元データ → AIの下書き → 人が照合, with one highlighted step at a time.
The source data, results and checking scenes are **fictional example UI**, not proof of a real-world claim. Overlay is y=1200–1298, below the original result card and above caption/HUD band y>=1400. First version y=1060 obscured "この数値は、まだ確認中"; rejected and corrected before delivery.

**Concurrent work:** Draft PR #278/cycle905 improves the prompt Before/After sequence in scene06. This branch is independent from main and does **not** incorporate cycle905 private MP4 or code.

**Private local input:** cycle904 SHA256
29ecff18efa6b515f6732c1cc3e644520b22930fc528b7c8352f6ed8fe5a992b.
**Final output:** cycle906 SHA256
9594572d211c14d7bdcd292a251ce16c50fb9cf069b76c5286c4a4cde49b261e.
Finished video is in the ChatGPT review session only, NOT committed to this public repository.

**Reproduce locally** with *privacy-cleared source only* (do not upload it):
1. Install free Pillow, ffmpeg and Noto CJK fonts.
2. Create a private JSON manifest with genre=ai_work, source_sha256=<local-source-sha> and all boolean policy fields in test_proof_chain.py explicitly set to false.
3. Run: python review_cycles/cycle906/proof_chain.py --source /path/to/PRIVATE.mp4 --output /path/to/NEW_PRIVATE.mp4 --manifest /path/to/PRIVATE.json --workdir /tmp/cycle906 --report /path/to/PRIVATE_QA.json.
4. Run: PYTHONPATH=review_cycles/cycle906 python -m unittest discover -s review_cycles/cycle906 -p 'test_*.py' -v.

**Local verified:** 13/13 tests; H264 1080x1920 30fps 691 frames/23.033333s, AAC 48kHz bitstream identical, full A/V decode PASS, 81/81 modified scene frames detected; 1/4-resolution subtitle band y>=1400 max mean absolute pixel diff 1.225 from re-encoding (not zero). Real phone playback not checked. Independent Japanese ASR, semantic caption timing, licensing, employee approval, and actual Actions charges NOT verified. No release approval.

**Reference provenance:** Accessible summaries from TikTok市場分析/TikTok動画研究 and the user-provided 16-panel storyboard inspected; full original research chat transcripts and original v33 MP4 not accessible in this run. The storyboard has richer photographic imagery and actual spreadsheet/UI shots; this 8-scene sample remains far below v33 visual variety.

**Safety:** HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No automatic TikTok posting, public media upload, merge, paid contract, or paid API. CI tests only code and synthetic PNGs; it does NOT validate the completed private MP4. Next: independent Japanese speech transcription + meaning/timing alignment; image-first rights-approved assets and device playback.
