# cycle1241 — TikTok mobile safe disclosure (HUMAN_REVIEW)

Previous cycle1239 placed disclosure text at y≈1750, where TikTok's caption UI can cover it. This change moves disclosure to x570–1030, y482–525 (between heading and slide), and clears y1710–1919 to preserve platform UI space. The central slides, Japanese narration caption panel, chapter timing and AAC source are retained except H.264 re-encoding. Geometry is fail-closed for 1080×1920; ten genre palettes are supported. This is not a claim that TikTok's live UI has been measured on-device.

Run `python3 -m unittest discover -s cycle1241/tests -p 'test_*.py' -v` and `python3 cycle1241/tests/ci_smoke.py`.

No private media, v33 reference footage or user data are committed. PR is review-only. Japanese ASR, semantic subtitle alignment, source rights, smartphone playback and employee approval remain pending. No automatic posting or merging.

First local attempt wrongly placed the mask at y1450 (covering subtitles) and badge at y377 (overlapping headline). Both were corrected to y1710 and y482 before final MP4. First final re-encode truncated one AAC packet due to -frames:v; removed frame cap and verified bit-identical AAC.
