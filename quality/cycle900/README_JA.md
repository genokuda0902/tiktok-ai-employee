# cycle900 — narration-pause-gated cut sweeps (review only)

2026-10-27 JST. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Difference and provenance
Prior cycle898 added a 5-bar narration-responsive visualizer. Parallel cycle899 PR #270 added a three-step end CTA. This cycle adds **seven short, subtle directional light sweeps at existing scene boundaries** only when 130-ms audio RMS <= 0.025. All effects stay within y50–1430, above the burned subtitle region starting y1490. No cut is retimed; no audio is replaced. 10 genre IDs share the same renderer and fail-closed release policy.

The local source was **cycle898** MP4 SHA256 `1015c17b738567d2b128c6a5517f92f0513da9952253c46d0664e553ef0d5316`. cycle899's private completed MP4 was NOT available in this workspace. No direct comparison against cycle899's actual video is claimed. This is an independently branched, non-merged change from main.

## Verified local video (NOT in public GitHub)
`cycle900_PAUSE_GATED_TRANSITIONS_JAPANESE_REVIEW_ONLY.mp4`
SHA256 `5637ec34a022fa580463c101b217a83e4347a2075dd84501e4f35b2e0e519f4a`.
H.264 1080x1920, 30fps, 691 frames, 23.033333 seconds, AAC 48kHz stereo. Full A/V decode PASS; original AAC ADTS SHA256 identical `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
All 7 scene boundaries passed RMS gate (0.000783–0.004535), 35 affected frames. Compared all 691 frames: edited-region mean pixel delta 3.719 vs 1.790 for other frames; subtitle band max mean pixel delta 2.647 (re-encoding noise, NOT pixel-perfect). Local 13/13 unit tests PASS. The real finished MP4 is only a private conversation attachment, NOT a GitHub artifact; CI cannot verify that exact MP4.

## Reproduce locally with a rights-approved source
```bash
python -m pip install numpy opencv-python-headless
python -m unittest discover -s quality/cycle900/tests -p 'test_*.py' -v
python quality/cycle900/src/voice_pause_transitions.py --source /private/source.mp4 --output /private/review.mp4 --sha256 <exact_source_sha256> --report /private/render_report.json
PYTHONPATH=quality/cycle900/src python quality/cycle900/src/verify_local.py /private/source.mp4 /private/review.mp4 /private/qa.json
```

## Reference, safety and remaining gaps
Accessible prior summaries of `TikTok市場分析` and `TikTok動画研究`: first-1.5s hook, 15–25s, purposeful cuts, real operation footage, clear Japanese captions, manual employee-reviewed posting. Full research chats inaccessible. User's 16-panel AI時短ラボ storyboard inspected: cinematic robot/person/ChatGPT+Excel demonstrations, rich shot variety. Original v33 MP4 inaccessible, and no direct parity claim. Natural robot motion remains explicitly out of scope in authoritative handoff.

No independent Japanese ASR, spoken-caption semantic/timing validation, smartphone playback, inherited media license/publication rights, employee approval, or actual Actions billing verification. Never publish or auto-post. No confidential assets, MP4, screenshots or private audio uploaded to GitHub. No merge, paid service, or external posting.
