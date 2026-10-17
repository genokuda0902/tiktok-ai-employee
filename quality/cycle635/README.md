# Cycle635 — focus path (REVIEW ONLY)

Baseline: cycle634. This cycle adds a reusable, non-strobing, 3-step gaze guide (B2:B5 selection → formula → verified result) to an original clean-room 20-second vertical demo. Captions stay outside the focus overlay. The scene timing and existing non-speech synthetic audio are unchanged.

**Local render:** Pillow + NumPy + FFmpeg, run `python render_cycle635.py` using the complete reproducible local bundle. Only `visual_focus.py` and its isolated tests are stored here unless the full renderer is separately verified in this branch. Do not treat these files as a full MP4 renderer.

**Tests:** `python -m unittest discover -s quality/cycle635 -p 'test_*.py'`

**Reference constraints:** v33 reference is not a redistributable asset. Original v33 source not recovered. Market-analysis and video-research original task transcripts not fully accessible; prior verified guidance: first-1.5s hook, proof/demo, Before/After, short Japanese captions in safe area, action CTA.

**Quality:** 1080x1920 H.264 output from a 540x960 render. 20s / 600 frames. Original synthesized music and cues. Japanese narration **absent**, word-level sync **not validated**. No real AI screen recording. New-topic and real-device comparison against v33 not completed. No rights approval beyond the new original visual and audio elements. HUMAN_REVIEW; PUBLICATION_NOT_APPROVED.

**Next:** obtain approved images, offline Japanese TTS and timed captions; restore full generator in repo and CI. Never auto-publish or merge without authorization.
