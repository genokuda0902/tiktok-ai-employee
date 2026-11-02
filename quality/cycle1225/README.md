# cycle1225 — chapter progress micro-animation (HUMAN REVIEW ONLY)

Previous cycle1223: seven-band voice meter synchronized to narration.
New change: the existing eight-segment top indicator now fills its *active*
segment smoothly according to actual chapter timestamps (30fps), without
covering slide content, Japanese captions, footer or the voice meter.

- Geometry: 1080x1920 H.264, eight chapters, 30fps; overlay x=76..854 y=153..164.
- Ten shared genre palettes; rendered sample is **AI** only.
- Source AAC packets copied bit-for-bit. No new voice, no new external assets.
- Unit tests: 12. Synthetic A/V smoke: 2 seconds/60 frames + 8 chapters.
- Local full-length sample: 22.237 seconds, 667 frames, full AV decode passed.
- Local visual comparison (34 samples): protected-region max mean pixel
  difference 1.1634/255 (central slide), captions 0.4729/255.
- Visual comparison and MP4 are in the user-facing review package, **not** on
  public GitHub. No source user videos or copyrighted media uploaded.
- Independent Japanese ASR, caption semantic/timing match, source rights,
  reference v33 original comparison, smartphone playback and employee approval:
  **NOT VERIFIED**.
- Publication: **NOT APPROVED**. Manual posting only after staff review.

CI checks only synthetic media, not the full user-facing MP4.
No auto-posting, no merging, no paid service. 
