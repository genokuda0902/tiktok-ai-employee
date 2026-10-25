# cycle846 — Centered transition SFX with voice guard, REVIEW ONLY

**Compared with cycle845:** The same seven original 0.19s SFX now start **~64ms before** each picture cut, so their **acoustic energy centroid** aligns with the cut instead of the cue starting at the cut. A safety guard reduces gain to **25%** if source PCM is loud during the cue (RMS >=0.012). In the locally rendered AI-work review video, 1 of 7 cues triggered the guard. This is measurable cue-to-picture timing improvement, **not** independent perceptual quality proof.

The engine imports `cycle845.transition_audio` from its unmerged parent PR #178, and is intentionally proposed **against that PR branch**, not main. It reuses existing Japanese narration and burned-in captions from the local review-only cycle844 MP4. H264 video elementary stream is byte-identical; audio is re-encoded AAC 192k. Source footage and Japanese narration are not uploaded to GitHub.

Local command (numpy, ffmpeg, ffprobe):

```bash
PYTHONPATH=. python -m unittest discover -s cycle846 -p 'test_*.py' -v
PYTHONPATH=. python -m cycle846.voice_aware_sfx \
 --source /local/cycle844_REVIEW_ONLY.mp4 --output /local/cycle846_REVIEW_ONLY.mp4 \
 --manifest /local/manifest.json --genre ai_work
```

The source must match SHA256 in the manifest. Only fictional review-only inputs pass the existing fail-closed safety gate. Cut frame numbers are specific to this 691-frame AI-work edit and must be recalculated for other genres. Same audio algorithm and tests accept ten genre IDs, **not** ten finished videos. CI uses synthetic H264/AAC only. Full market/video-research chat transcripts and original v33 MP4 were unavailable; the user-supplied 16-panel storyboard was inspected. This is not recovered v33 source.

**Not verified:** Japanese ASR/meaning, word-level subtitle sync, perceived speech clarity, reference-v33 equivalence, image/publication rights, real-phone playback, employee approval. No merge, paid contract, external upload, or posting.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
