# cycle864 — cinematic laptop + real Writer evidence (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Not the original v33. No paid service, merge, publication, automatic posting or external media upload.

## Difference from cycle863

Scene 7 frames **507–587**, seconds **16.900–19.600**, now features an original illustrated dimensional laptop with warm/cool studio lighting, an extracted local real Writer screenshot of **fictional** data, staged three-item checkmarks (purpose/conditions/verification), and a save CTA. Replaces a mostly static flat Writer UI. The picture overlay is x=0..1079, y=330..1449; Japanese burned captions remain below y1490. The same renderer exposes ten genre-safe titles, but only AI-work was produced as a full Japanese review MP4. This is original procedural graphic art and inherited screenshot, **not** a newly licensed photograph or true 3D footage.

## Local reproducibility (private source stays private)

```bash
python -m pip install pillow numpy opencv-python-headless
PYTHONPATH=cycle864 python -m unittest discover -s cycle864 -p 'test_*.py' -v
python cycle864/cinematic_laptop.py --source /private/cycle863_PROOF_BEFORE_AFTER_JAPANESE_REVIEW_ONLY.mp4 --output /private/cycle864_CINEMATIC_LAPTOP_JAPANESE_REVIEW_ONLY.mp4 --manifest /private/source_manifest.private.json --report /private/render_report864.json
PYTHONPATH=cycle864 python cycle864/verify_review.py /private/cycle863_PROOF_BEFORE_AFTER_JAPANESE_REVIEW_ONLY.mp4 /private/cycle864_CINEMATIC_LAPTOP_JAPANESE_REVIEW_ONLY.mp4 /private/verification864.json
```

Private manifest must exactly match `POLICY` in `cinematic_laptop.py` plus the source SHA256. Never commit the manifest, source footage, screenshots, audio or finished MP4. The full video is only a private ChatGPT review attachment. GitHub CI runs 12 unit tests and a **synthetic 1-second** H264/AAC smoke test; it does NOT verify the actual private Japanese video.

## Research and baseline

Consulted accessible past summaries of `TikTok市場分析` and `TikTok動画研究`: strong first 1.5-second hook, 15–25s, real UI, clear Before/After, readable Japanese captions, manual employee approval. Original full task/chat texts inaccessible. Directly inspected the user's `ChatGPT×Excel時短術16コマ絵コンテ.png`: 16 panels with studio lighting, robots, live screen demos and energetic scene changes. Original v33 MP4 unavailable this cycle. The 8-scene, 23.033-second video still does not match that reference in footage diversity, live actors or cinematography. `PROJECT_HANDOFF.md` / `recovery/v33/RECOVERY_STATUS.md` prohibit robot motion and unapproved source assets.

## Local verified result

- Baseline cycle863 SHA256: `425454ceeebc894be8471bf39fa0d424447a0f4367621e2c347621ee9f16762b`.
- cycle864 MP4 SHA256: `5fcccffb4f194457230b06b7135e206d087c6985344d37aa5ff4a1075500c80f`.
- 1080×1920, 30fps, 691 frames / 23.033s, H264 video and AAC48kHz Japanese inherited audio.
- Full A/V decode PASS, source/output ADTS audio SHA256 identical: `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- 12/12 local unit tests PASS. Changed-scene mean pixel delta 58.78–69.58; protected subtitle region delta 0.351–0.407 on sampled frames.
- No independent transcription/pronunciation, semantic speech-caption alignment, smartphone playback, rights verification, employee approval, retention, reference-v33 parity or actual Actions billing verification.

Next: acquire approved high-quality new imagery for multiple scenes, independently check Japanese speech and caption semantics/timing, compare with recovered v33 if possible. No public posting without employee approval.