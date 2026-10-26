# cycle868 — original illustrated closing scene (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Reimplementation, not recovered v33. No automatic posting, merge, paid service, private asset upload, or release.

## Change since cycle867

Scene 08 (frames 588–690, 19.600–23.033s; **103 frames**) was previously a static checklist. It now displays a new **original procedural illustration** of a friendly AI assistant on a softly lit blue background, a 2-stage Japanese headline, 2% camera zoom, and a delayed '保存して、明日1つ試す' call-to-action. No third-party images or copyrighted robot assets were used in this new segment. This is a 2D original illustration, **not** a licensed photo, photorealistic footage, articulated robot animation, or v33 parity.

The 10-genre shared code uses unique two-line headlines and strict text-width checks. Only `ai_work` was rendered into the complete MP4. Original source video and its AAC voice are reused locally, not uploaded to GitHub.

## Reproduce (requires the private previous review MP4)

```bash
python -m pip install pillow numpy opencv-python-headless
PYTHONPATH=cycle868 python -m unittest discover -s cycle868 -p 'test_*.py' -v
python cycle868/cinematic_closer.py --source /PRIVATE/cycle867.mp4 --output /PRIVATE/cycle868.mp4 --manifest /PRIVATE/source_manifest.private.json --report /PRIVATE/render_report868.json
python cycle868/verify_review.py /PRIVATE/cycle867.mp4 /PRIVATE/cycle868.mp4 /PRIVATE/verification868.json
```

Private manifest must match `POLICY` plus `source_sha256` exactly; no overwrite, unknown genre or source substitution allowed. Do not commit the manifest or private media. CI checks 10-genre code and synthetic H264/AAC only, **not** the real Japanese MP4.

## Verified locally

- Input SHA-256 `1527220d5092c43d75f6aee756f4773d6618246bf5e81937865f89b52867770b` (cycle867).
- Output SHA-256 `315b13067f0ec0518da7bb85837658be7f3b81bbbd41c12eae66d4b3f57dcee4` (cycle868).
- H.264 1080×1920, 30fps, 691 frames, 23.033s; AAC 48kHz stereo; full A/V decode PASS.
- AAC ADTS payload unchanged (`2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`). Subtitle strip y=1490–1839 checked on all 691 frames; maximum mean pixel delta **0.160**. Outside-scene sample max mean delta **0.148**. New scene sampled deltas **64.1–69.9**.
- 18 local unit tests PASS. Actual smartphone playback and independent Japanese speech/semantic subtitle alignment **not verified**.

## References and remaining gap

Accessible prior summaries from `TikTok市場分析` and `TikTok動画研究` indicate an early hook, 15–25s, actual UI demos, readable captions, Before/After and human review; full task transcripts unavailable. The user-supplied 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` was inspected directly; it features a 36-second multi-scene photographic/robot sequence. Original v33 MP4 (31.553s) is not accessible this run. This 23s eight-scene illustration still lacks the reference's photoreal lighting, natural characters, dynamic editing, and 16-panel variety. No claim of reference-quality equivalence.

No source-media rights clearance, employee signoff, phone playback, narration semantic match, or billing check. Publication remains prohibited. Next cycle: prioritize approved high-quality footage and independently verify speech-caption alignment.
