# cycle952 — caption-to-active-step visual alignment (review only)

This cycle fixes a visible, manually confirmed semantic mismatch in scene02: the burned Japanese caption says **「まず、繰り返している作業を書き出そう。」**, but the 3-step card highlights **②合計を確認** and then **③報告にまとめる** during 3.9–5.8s. The replacement keeps **①数字を入力** highlighted while that subtitle is displayed. This is a visual alignment check, NOT independent speech recognition.

- Source: private cycle951 MP4, SHA256 `950b8d4d336cdb5f4ba4a774348e19c4f0dfc8bff98046e2eeeed2a9d2976c2d`.
- Output: private review MP4 generated locally, **never committed to this public repository**.
- Scene02 3.78–5.76s; all other scenes and burned captions retained in source; AAC bitstream copied.
- The renderer requires SHA-locked source and a human-reviewed per-scene manifest; all 10 genre identifiers accepted by validation, but **only AI-work geometry approved**. Never claim automatic cross-genre visual correctness.
- Reimplementation, not recovered v33. Full v33 original and full historical chat transcripts unavailable; user's 16-panel storyboard and prior research summaries reviewed.
- Original v33 source and user media rights not recovered; Japanese ASR, human audio listening, subtitle semantic/timing proof, smartphone playback, rights and employee approval **UNVERIFIED**.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No auto-post, merge, paid service or private media upload.

To reproduce locally after obtaining the approved private source:
```bash
python -m pytest -q cycle952/tests/test_scene_focus_lock.py
python cycle952/src/scene_focus_lock.py --source /private/cycle951.mp4 --output /private/cycle952.mp4 --manifest /private/cycle952_manifest.json --qa /private/qa952.json
```
Manifest must contain genre=ai_work, source_sha256, source_scene=2, caption matching the burned text, active_step=1, geometry_reviewed=true. CI tests synthetic frames only; it does **not** verify private MP4.
