# cycle1020 — caption panel refresh + human audio review (review only)

2026-10-31 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, post, paid service, private media upload, or delivery to employees.

## Inputs and research
- Existing `cycle1018` local MP4 SHA256 `779db27ac4d0a0644d1d8f12d65a4766fafd0c6c6346b2eaa12e0d43795c5172` is explicitly pinned. Its original 8-cue on-screen text SRT is reused, **not independently transcribed**.
- Past `TikTok市場分析` / `TikTok動画研究` summaries were consulted: first-second hook, concrete result, real UI, readable Japanese captions, human approval.
- User's 16-panel storyboard was directly viewed in the file Library. Original v33 MP4 and full research chats were not available. Reference has 16 panels / ~36 seconds, cinematic robot/person, ChatGPT and spreadsheet scenes.
- Main verified `18e084c38db0dc55db7dfc0532b9451b1167f2aa`; previous draft PR #419 is the base. Parallel PR #420 is not modified. `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md` and `src/build_daily.py` were checked; main's daily generator still uses `-an`.

## Distinct improvement
- Replaces old black, flat burned subtitle strip with an original, higher-contrast two-line Japanese panel, consistent 59px font, teal guide rail, and 01/08 to 08/08 cue index. The visual effect is confined to y1490:1710 of 1080x1920, preserving the existing bottom audio visualization.
- Strict caption time/gap, text fit, input SHA, codec, language tag, review-only and no-overwrite checks. Supports 10 genre keys; only AI-work has a verified full-length input.
- `audio_review.py` exports eight **local-only** 16kHz mono WAV review clips and an unfilled human listening checklist. This is NOT ASR, pronunciation verification or subtitle synchronization proof.

## Reproduce (approved local source only)
```sh
python cycle1020/source/caption_panel.py --source /path/to/cycle1018_COMPLETE_PROMPT_JP_REVIEW_ONLY.mp4 --srt cycle1020/fixtures/captions.srt --output /path/to/cycle1020_review.mp4 --report /path/to/qa.json --genre ai_work --review-only
python cycle1020/source/audio_review.py --source /path/to/cycle1020_review.mp4 --srt cycle1020/fixtures/captions.srt --out /path/to/private_audio_review
```

## Verified local QA
- MP4 SHA256 `3442c9e039947f625c907f0aba0815466408e46efd549cf9e9be5c2be96e480e`, 1080x1920, H.264, 30fps, 691 frames, 23.033333s, AAC 48kHz tagged Japanese.
- Full video/audio decode PASS, AAC ADTS payload unchanged; 8 captions reused, no selectable subtitle track. Nine sampled frames show mean change in caption strip 41.555–50.018/255, outside strip 0.271–0.496/255 (re-encode).
- Local 7 unit tests PASS, 2-second synthetic A/V test PASS; 8 review WAV clips generated. CI checks synthetic A/V, not private full MP4.
- No independent Japanese ASR model available. Speech content, timing, source rights, employee approval, mobile-device playback, reference parity and actual Actions billing remain unverified.

## Next
1. Complete human listening on 8 WAVs or install a legal offline Japanese ASR model; compare transcript with all eight SRT cues and fix misalignments.
2. Source approved images / new-topic narration, improve 8-scene vs reference 16-panel diversity, and perform employee review.
3. No automatic TikTok posting; manual posting only after approval.
