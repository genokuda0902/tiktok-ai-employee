# cycle915 — evidence-first review UI (review only)

## Delta from cycle914
Scene 05, 11.6–14.5s (source frames 348–434), changes from a static checklist to an original large-type evidence review: flag an unsupported claim, examine three checks, and show a non-assertive corrected phrasing. This differs from cycle914's textured paper report in scene 03. The other seven scenes and inherited Japanese narration remain unchanged.

## Reproduction
Use the **private** cycle914 MP4 only after rights clearance. Locally install Pillow and Noto Sans CJK fonts, then run `python evidence_review.py --out frames`. Overlay the 87 generated 1080×1160 frames at (0,300) during 11.6–14.5s using ffmpeg, encode H.264 at 1080×1920/30fps, and stream-copy original AAC audio. **Do not commit the private MP4 or inherited assets.**

## Actual private QA (not CI)
Output SHA256: `__SHA256__`.
23.033333s; 691 frames; H.264 1080×1920 30fps; AAC 48kHz bitstream identical; full A/V decode pass; 87/87 edited frames visibly changed; outside scene mean pixel MAE 0.169 at quarter-resolution; subtitle band MAE 0.092; 15/15 local technical QA; 11/11 local render tests.

The CI workflow tests source syntax, ten genres and review-only policies; it does **not** test the private MP4.

## Safety
Fictional sample text and original vector UI only. No posting, merge, paid service, or public upload. Inherited audio and imagery rights, independent Japanese ASR and caption semantic/timing agreement, original reference v33 comparison, smartphone playback, employee approval and actual Actions billing are unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**
