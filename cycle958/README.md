# cycle958 — Scene-change continuity experiment (REVIEW ONLY)

2026-10-29 JST. Distinct from previous cycle957 three-step closing and parallel PR #356 midtone changes. This is a **reimplementation, not recovered v33 source**.

The cycle957 MP4 has seven abrupt cuts at frames 87, 174, 261, 348, 435, 522, 609. This experiment adds a nine-frame (0.3-second) left-to-right feathered wipe at each cut. The current-frame Japanese caption and voice-wave region (y >= 1490) is not edited by the renderer. The AAC bitstream is copied unchanged. Video is re-encoded.

**Private source SHA256:** f270177b38a04a357fea3f86e6d70c1f8ef3da028004e1845b5f0310dca37e73

**Private output SHA256:** ac5fcfcfc744edbf9ec4cf7080e53ce88a9e7a9512021593119188ed66bbb22a

Local reproduction with approved source, ffmpeg, OpenCV and numpy:
- python -m pytest -q cycle958/test_scene_wipe.py
- python cycle958/scene_wipe.py --source /private/cycle957.mp4 --output /private/cycle958.mp4 --qa /private/render_qa958.json

Local completed MP4: H.264 1080x1920 30fps 691 frames / 23.033s; AAC 48kHz stereo; 63 transition frames processed. Mean immediate-cut pixel jump in artwork (seven boundaries sampled 90x120) 79.718 to 3.792; **this does not prove improved viewer preference**. Full A/V decode PASS. 19/19 local synthetic tests PASS. Protected caption region maximum sampled mean delta 1.0208/255 due to re-encoding. Source and output AAC ADTS SHA256 identical: 37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27.

Reference consulted: accessible TikTok市場分析 / TikTok動画研究 summaries and the user-provided ChatGPT×Excel時短術16コマ絵コンテ.png (16 cinematic robot/person/real-UI shots). Full original research chats and original v33 MP4 inaccessible this run. The eight-scene video still differs in visual diversity, real-app demonstration, cinematic footage and 16-shot structure.

Ten genre identifiers supported, but only ai_work geometry and media reviewed; nine others fail closed. No independent Japanese ASR, speech-caption meaning/timing verification, publication-rights clearance, employee approval, phone playback or actual GitHub billing confirmation. CI tests only synthetic images/code; **private MP4 is not uploaded to public GitHub**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, auto-post, paid service, or public distribution.
