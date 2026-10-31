# cycle1038 — source-reused three-shot recap (REVIEW ONLY)

## Why this cycle
Distinct from cycle1036's opening hook and parallel cycle1105's scene dip: the last 2.733 seconds now show three rapid *real source-derived* evidence shots (completed sheet, AI prompt, arithmetic check) followed by a clear one-action CTA. This adds three micro-shots without claiming to add three full narrative chapters.

## Actual private local MP4 (NOT uploaded to public GitHub)
- Input cycle1036 SHA256: `5adb8836b387dd09e4c7d184bcbe72ac5519a5df23f2bb1877d8c467a4c87148`.
- Output SHA256: `64971783c4bc51007cdb65a09014952a744a1fad8a87ce0f8bbf7dccef571623`.
- 23.033333s, 691 frames, 1080×1920 H.264 30fps, AAC 48kHz Japanese-tagged; full video/audio decode PASS; original/output ADTS audio SHA256 identical `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e`.
- Source stills: frames 195/303/474; recap starts frame 609. Bottom subtitle/approval/waveform region y>=1280 never covered by overlay. Quarter-resolution every-5-frame caption ROI max mean difference 0.9842/255, modified top ROI mean 61.7405/255. 9 local tests PASS.
- Ten genre palette configurations are unit-tested, but other genre media is not approved and production render fails closed; only ai_work full video tested.
- GitHub CI is synthetic 2-second H.264/AAC only; NOT the actual private MP4. The MP4 and human-listening WAVs are provided in the ChatGPT review package.

## Sources and restrictions
- Main SHA `18e084c38db0dc55db7dfc0532b9451b1167f2aa`; prior open PR #437 used as base. Parallel PR #438 inspected, not modified. Main PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md inspected.
- Accessible prior TikTok market/video research summaries: strong 0–1.5s hook, action-based cuts, real UI, Before/After, one message, legible subtitles, save CTA. User's 16-panel/~36s storyboard was described in previous runs; original image not directly retrieved in this run. Original v33 MP4 and full original research chat transcripts unavailable.
- Independent Japanese ASR/transcript meaning and 8-cue alignment NOT verified; inherited asset rights, smartphone playback, employee approval, actual Actions billing NOT verified. Current 8-chapter/23s video is not reference-equivalent.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, no automatic post, no private media GitHub upload, no paid service.

## Reproduce offline
`python cycle1038/source/recap_cuts.py --source <private_cycle1036.mp4> --dest <new_private_output.mp4> --report <new_report.json> --expected-sha 5adb8836b387dd09e4c7d184bcbe72ac5519a5df23f2bb1877d8c467a4c87148 --review-only`

## Next priority
Independent Japanese voice transcription and eight subtitle cue alignment (do not treat audio bitstream preservation as proof), then approved image-first shots and real phone playback. No new-topic publishing until review and rights approval.
