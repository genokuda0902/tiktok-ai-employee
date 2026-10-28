# cycle941 — safe micro-motion (HUMAN REVIEW ONLY)

Compared with cycle940's eight-scene narration-level matching, this cycle adds feather-masked, eased 2.2% maximum micro-motion to illustration regions in scenes 1, 3, 7 and 8. Header, Japanese burned-caption area, progress and footer remain outside the transform. Source AAC is copied at bitstream level.

Ten genre-specific motion amplitudes are supported, but only the AI-productivity genre was rendered. The local 1080x1920/30fps review MP4 has 691 frames, full A/V decode, and 10/10 technical checks. The video itself is **not** uploaded to GitHub; CI validates renderer logic and synthetic pixels only.

No independent Japanese ASR, human listening approval, v33 original comparison, inherited-material commercial rights clearance, phone playback or employee approval has been completed. Existing illustrated UI is a demo, not real PC-operation footage. No posting, merge, paid contract, or automatic upload.

Local usage (FFmpeg, OpenCV and NumPy required):

```sh
python -m unittest discover -s cycle941/tests -v
python cycle941/src/safe_motion.py --source source.mp4 --output review.mp4 --report report.json
```

PUBLICATION_NOT_APPROVED. Employee review and manual posting only.
