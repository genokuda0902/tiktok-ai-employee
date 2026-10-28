# cycle920 — narration-energy camera accents (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. This is a reimplementation, NOT the original v33 engine. No public media, posting, merge, paid API or automatic approval.

## Change from cycle919
- cycle919 PR #299 used an illustrated before/after final scene; parallel PR #300 edited review-instruction scene06.
- cycle920 changes **camera motion in all eight existing scenes**: 100 ms audio RMS selects a local speech-energy peak near the center of each scene, then triggers one 5.5% zoom/pull-back accent. Eight audio-driven camera accents total. This does **not** recognize Japanese words or validate narration/subtitle semantics.
- Top y0–1379 is transformed. Bottom y1380–1919, including burned captions, is inherited and not intentionally modified.
- Ten genre identifiers use one code path; only **ai_work** was rendered. 8 source scenes remain 8 scenes; accents do not create 16 independent reference scenes.

## Reproduce locally (PRIVATE MP4 required)
Python 3, ffmpeg with libx264. No cloud API.
```sh
python3 review_cycles/cycle920/audio_camera_punch.py \
  --source /private/cycle919_EMOTIONAL_BEFORE_AFTER_REVIEW_ONLY.mp4 \
  --output /private/cycle920_AUDIO_PUNCHED_REVIEW_ONLY.mp4 \
  --manifest /private/manifest920.json --genre ai_work
python3 -m unittest discover -s review_cycles/cycle920 -p 'test_*.py' -v
```
Never commit or publicly upload the source or output MP4.

## Actual private local video QA (not run in GitHub CI)
Source cycle919 SHA256: `d5a4b8f8cbc418dd62484caabd3a7e2c4ed1270e02e1fbf7014d302cd116881e`.
Output cycle920 SHA256: `288413797067240e98db15becfccd1efd8cc9b8cbc4aaf34d2b001e4f836b74d`.
H.264 1080x1920 / 30fps / 691 frames / 23.033s; AAC 48kHz.
Full A/V decode PASS; AAC ADTS SHA identical to source (`2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`).
Eight accent peaks, quarter-res upper-area minimum frame MAE 18.345, mean 26.771; caption-band maximum MAE 0.457, bottom region maximum MAE 0.407 (re-encoding noise). Ten offline unit tests PASS.
**GitHub CI only tests the code and safety policy, not the finished MP4.**

## Research, references and limitations
Available summaries of TikTok市場分析 and TikTok動画研究: hook in 0–1.5s, 15–25s, purposeful cuts, image-first, real UI demonstration, before/after, short Japanese captions, human approval and manual posting. Previously inspected user 16-panel ChatGPT×Excel storyboard is known through prior review notes; storyboard original and original v33 MP4 were NOT accessible in this run. Full research chat transcripts also unavailable.
The 8-scene illustrated output is not reference-equivalent cinematic human/robot footage or 16 distinct scenes.
Independent Japanese ASR, narration/subtitle meaning and timing, inherited media rights, smartphone playback, employee approval, retention and actual Actions billing UNVERIFIED. No automatic posting or paid contract.
