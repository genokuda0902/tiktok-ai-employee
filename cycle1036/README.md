# cycle1036 — kinetic Japanese first-second hook (PRIVATE HUMAN REVIEW ONLY)

**Reimplementation, not recovered v33. PUBLICATION_NOT_APPROVED.**

## What changed from cycle1034
cycle1034 added an 11-frame scene03→04 wipe at 8.533–8.900s. This cycle instead adds an **original 36-frame/1.2-second Japanese headline animation** at the very beginning. The bold cyan-bordered card asks 「まだ手作業で 集計してるの？」 and fades away to reveal the original before/after proof. No new photographic, user, confidential, or licensed media are added. The existing eight-scene, 23.033s structure and burned Japanese subtitles remain.

This is distinct from cycle1010's 1.5-second before/after spotlight and cycle1103's Japanese caption plate: the new graphic is a typography-first question → proof reveal with ten reusable genre-specific question pairs.

## Reproduce locally, with approved private input only
Requires FFmpeg/ffprobe, Python3, Pillow, Noto Sans CJK font. Original input is the private cycle1034 review MP4, **not** committed to GitHub.

    python3 -m unittest discover -s cycle1036/tests -p 'test_*.py' -v
    python3 cycle1036/source/kinetic_hook.py \
      --source /private/cycle1034_SCENE_TRANSITION_JP_REVIEW_ONLY.mp4 \
      --output /private/cycle1036_KINETIC_HOOK_JP_REVIEW_ONLY.mp4 \
      --report /private/cycle1036_qa.json \
      --expected-sha 00fe0dc8648f9c28b3e12f06717977a2809d0d1043ee51526c27f764e0e24164 \
      --genre ai_work --review-only

Ten genre text presets are unit-tested. The other nine genre video renders **fail closed** until their approved source and SHA are available. No auto-post, no public source-media upload, no merge.

## Local real MP4 verification, 2026-10-31 JST
- Source SHA256: 00fe0dc8648f9c28b3e12f06717977a2809d0d1043ee51526c27f764e0e24164
- Output SHA256: 5adb8836b387dd09e4c7d184bcbe72ac5519a5df23f2bb1877d8c467a4c87148
- H.264 1080×1920, 30fps, 691 frames, 23.033333s; AAC 48kHz Japanese-tagged audio. Full A/V decode PASS.
- Source/output AAC ADTS elementary audio SHA256 identical.
- Local 13/13 unit tests PASS; 2s synthetic A/V render PASS.
- All 691 frames compared at 1/4 resolution: subtitle ROI y1490–1840 max per-frame MAE **1.524/255**; after-hook whole-frame max MAE **1.3031/255**; opening upper region mean MAE **28.3402/255**. Pixel differences outside the overlay are expected from H.264 re-encoding; they are not proof of perfect visual identity.
- Private real MP4 and before/after montage are in the ChatGPT review package only, **not GitHub**. GitHub CI validates only synthetic 2s media and unit tests.

## Research, reference and limits
Accessible prior TikTok市場分析/TikTok動画研究 summaries: first 1.5s hook, strong visual proof, readable captions, before/after, human-reviewed manual posting. Full original task/chat transcripts inaccessible. User's 16-panel ChatGPT×Excel storyboard was directly inspected: 16 scenes/~36s, cinematic people/robot, real UI, CTA. Original v33 MP4 is unavailable in this run. Our current 8 scenes/23s still lack cinematic cut diversity and genuine operation continuity.

Independent Japanese transcription, narration meaning/pronunciation, eight-cue subtitle semantic/timing match, rights, smartphone playback, employee approval and actual Actions billing remain **unverified**. No reference parity or publishing-quality claim.
