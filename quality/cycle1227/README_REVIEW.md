# cycle1227 — central slide detail enhancement (REVIEW ONLY)

Previous cycle1225: chapter progress micro-animation.
This cycle: **selective, bounded unsharp** on the central slide rectangle (x64..1015, y480..1199). Japanese narration card, subtitle, header and footer are outside the modified ROI. The goal is clearer small Japanese/Excel text, not synthetic replacement of content.

- 10 genre identifiers share the same safe-area renderer; AI sample only.
- Input: prior cycle1225 local 22.237s 1080x1920 H.264/30fps/667-frame MP4.
- Output: local 22.237s 1080x1920 H.264/30fps/667-frame MP4; 8 chapter markers preserved.
- **Original Japanese AAC packets are bit-for-bit identical** (ADTS SHA256 verified); no new voice or rights-unclear imagery.
- Full-length A/V decode passed locally; 10/10 local unit tests; synthetic 2s/60-frame/8-chapter smoke passed.
- Eight actual frames: mean central strong-edge strength 297.54 → 329.23 (about +10.65%). This is an *edge-strength metric*, not a user readability or reference-video quality score.
- Eight actual frame samples: maximum average pixel difference in narration-card safe area 0.195/255; heading 0.552/255; footer 0.158/255. Re-encoding affects pixels outside ROI slightly.
- **Independent Japanese ASR, subtitle meaning and speech timing: NOT VERIFIED.** No model was locally available. An audio energy/silence audit alone cannot establish correct words.
- v33 reference original, original asset rights, phone hardware playback, staff approval, Actions billing: NOT VERIFIED.
- Source user/reference media and the actual full MP4 are **not** committed to public GitHub. CI tests only synthetic rights-safe footage.
- No paid APIs, no automatic posting, no merge. Publication status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

Next: independently transcribe the Japanese narration and check caption text/time against 8 chapter boundaries using a verified offline ASR model; if unavailable, preserve explicit NOT VERIFIED.
