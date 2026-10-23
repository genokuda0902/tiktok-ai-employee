# cycle794 — Artwork-only scene wipes (human review)

- Previous cycle: 793 (large vector illustrations and corrected LED schematic).
- New improvement: seven 0.20s wipes restricted to the central artwork rectangle (x=90..990, y=560..1180).
- Headers, burned-in Japanese captions, scene labels, and original 14.314s timeline remain outside the wipe.
- Existing Japanese AAC narration is stream-copied, not regenerated. Its provenance/rights and naturalness are **unverified**.
- Reusable theme config includes ten genres. Only the science sample was rendered locally; cross-genre quality is **not verified**.
- Local output: `cycle794_SOFT_TRANSITIONS_HUMAN_REVIEW.mp4`, 1080×1920, 30 fps, 429 frames.
- CI workflow builds a **synthetic beep-audio smoke test only**, not the final Japanese video. Its success must not be represented as approval for publication.
- No posting, merging, or paid subscriptions. Employee review required before any manual upload.

Local reproduction (with cleared input media):
```bash
python quality/cycle794/render.py --input approved_source.mp4 --output output.mp4
python -m unittest discover -s quality/cycle794 -p 'test_*.py'
```
