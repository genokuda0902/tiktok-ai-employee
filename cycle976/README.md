# cycle976 — real Calc-derived audit, review only

Source baseline: private cycle974 MP4 SHA256 `499cb2360f95bfddf9fa61d72875db0dfd47ed14bbaf4ad3a6190d9a001c0097`. The output is not uploaded to GitHub.

Distinct change: scene06 (14.50–17.40s; 87 frames) now includes an actual LibreOffice Calc-exported view of a synthetic workbook with formula results A=46 and B=29, instead of solely vector-drawn arithmetic. Three beats: fictional unverified draft 45, Calc SUM result 46, correction 45→46. It is **not a screen recording** and does not prove AI-generated output.

Reproduce privately:
1. Run `python cycle976/build_calc_proof.py /tmp/fictional_calc_proof.xlsx` with `artifact_tool` installed.
2. `libreoffice --headless --convert-to pdf --outdir /tmp /tmp/fictional_calc_proof.xlsx`.
3. `pdftoppm -f 1 -singlefile -png -r 140 /tmp/fictional_calc_proof.pdf /tmp/fictional_calc_proof`.
4. `python cycle976/real_calc_audit.py --source /path/to/APPROVED_LOCAL_INPUT.mp4 --proof /tmp/fictional_calc_proof.png --output /tmp/cycle976.mp4 --frames-dir /tmp/cycle976_frames`.
5. `python -m unittest discover -s cycle976 -p 'test_*.py' -v`. For media QA, use ffprobe and full ffmpeg decode. Source must be locally authorized. No upload.

Local evidence: output SHA256 `c9715d9a0d9f0a1a7bbba63e8e8f4d9fb0e1109e46705e73198e27799f2b9df2`; H.264 1080×1920 30fps 691 frames, 23.033333s, AAC 48kHz unchanged ADTS SHA; full decode PASS, 9 local unit tests PASS. Sampled subtitle ROI max mean pixel delta 1.121/255. CI is synthetic-only and is not equivalent to private-MP4 QA.

Research: accessible summaries of TikTok市場分析 / TikTok動画研究 and the original 16-panel storyboard were checked. Original v33 MP4 and full original chats inaccessible. The reference has cinematic robot/person imagery and more cuts; this video remains 8 scenes / 23.033s. Independent Japanese ASR, caption semantic alignment, rights, smartphone playback, employee approval, actual Actions billing unverified. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid service, or automatic posting.
