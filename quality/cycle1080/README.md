# cycle1080 — fictional Calc proof before/after (REVIEW ONLY)

Replaces the washed-out mock audit in scene 06 (14.300–17.333s, 91 frames) with an original 3-beat **illustrative** correction: B column alone 46 → B+C 75. Reuses a local screenshot extracted from the preceding real Calc operation in scene 03 as evidence. This is an **illustrative fictional error**, not a claim that AI actually made it, nor a benchmarked speed improvement.

The existing Japanese AAC narration and eight burned-in subtitle intervals are inherited, but **independent Japanese ASR and semantic subtitle match remain unverified**. Scene 06 overlay is transparent below y=1280, protecting subtitles and the lower layout. Ten palettes supported, but only ai_work completed as a private MP4.

```
python -m quality.cycle1080.proof_before_after --source /private/cycle1078.mp4 --source-sha VERIFIED_SHA256 --out /private/cycle1080.mp4 --genre ai_work
python -m unittest quality.cycle1080.test_proof_before_after -v
python -m quality.cycle1080.proof_before_after --smoke
```

Input source must have verified SHA256. No private video, screenshots, voice, assets, or customer data are committed. CI tests only synthetic media. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No automated posting, merge, paid services or license assumptions.
