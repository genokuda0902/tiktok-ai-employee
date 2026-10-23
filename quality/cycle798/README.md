# cycle798 — animated copy→paste demonstration (review only)

**Defect:** cycle797 showed a graph and a later spreadsheet but did not animate the actual transfer of AI-organized rows into a sheet. The user-supplied 16-panel storyboard includes a separate Excel paste step. This cycle replaces frames 348–419 (11.6–14.0 seconds) with an original animated synthetic four-row copy/paste illustration. It is **not** an actual AI/Excel screen recording and does not claim that real software executed.

## Reproduce local review video

Requires Python 3.11+, Pillow 11.3, FFmpeg/FFprobe and Noto CJK fonts. Existing `cycle797_CROP_SAFE_HOOK_REVIEW_ONLY.mp4` must be local and must **not** be committed/uploaded due to rights not yet verified.

```bash
python -m unittest discover -s quality/cycle798 -p 'test_*.py' -v
python quality/cycle798/copy_paste_story.py --config quality/cycle798/config.json --segment /local/cycle798_segment.mp4 --source /local/cycle797_CROP_SAFE_HOOK_REVIEW_ONLY.mp4 --output /local/cycle798_COPY_PASTE_DEMO_REVIEW_ONLY.mp4
```

Original text/vector shapes only, synthetic 1–4月 numbers 120000/150000/200000/180000 = 650000. The upper AI result and lower spreadsheet are large and separately labeled; four rows appear one by one. The 10-genre contract is the list in config; only the AI-efficiency example was rendered. `mode=review_only` and all approval flags false are enforced; no external material, personal data, payment, posting, merging or automatic publication.

CI generates **2.4 seconds of original animation with a synthetic 440Hz tone**, NOT a full Japanese-narrated video. The inherited audio remains local only. Local review MP4 has inherited audio copied bit-for-bit. Semantic narration/subtitle alignment, voice naturalness, rights, phone playback, v33 comparison and employee approval remain unverified.

## Previous vs current

cycle797: fixed clipped opening Before/After cards (0–3.2s). cycle798: **different problem**, makes the 11.6–14.0s transfer step visually progressive. Next: independently verify Japanese narration/caption semantic alignment, acquire approved original v33 MP4, and establish rights-safe reproducible full CI video.
