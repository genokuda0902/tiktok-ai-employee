# cycle1066 — subtitle-aligned habit visual and independent acoustic audit

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Reimplementation, not v33 source. No auto-post, merge, paid service, or unapproved public media upload.

Distinct from cycle1064: replace only scene 8 (frames 609–690, 20.300–23.033s), whose previous Before/After image did not directly illustrate the inherited spoken/captioned idea of making small time savings habitual. New original three-stage illustration: `今日:1つだけ試す → 明日:使える形で残す → 週末:続けるか見直す`. Ten genre accent themes, one full ai_work MP4. Existing Japanese audio and burned-in captions are inherited unchanged; do not claim independently verified semantic speech alignment.

A separate audio energy audit measures signal presence per eight timed SRT intervals. It is **not ASR** and cannot validate Japanese pronunciation, word-level timing or semantic correctness. The original 20.300s boundary remains a human listening priority.

## Private reproduction

```bash
python -m unittest quality.cycle1066.test_habit_story -v
python -m quality.cycle1066.habit_story --smoke
python -m quality.cycle1066.habit_story --source /private/cycle1064.mp4 --out /private/cycle1066.mp4 --work /private/work --source-sha256 SHA256 --srt /private/captions.srt --audit-out /private/audio_audit.json
```

The input MP4, its inherited audio, all extracted frames, audit data and final MP4 stay private; only source/test/workflow/README may be committed. Synthetic CI is not a full real-MP4 test.

Research: accessible summaries of TikTok市場分析/TikTok動画研究 (first-second hook, real app demonstration, purposeful edits, Before/After, readable Japanese captions, employee approval) and user's 16-panel/36s ChatGPT×Excel storyboard. Full research chat transcripts and v33 original MP4 inaccessible this run. Compared to the reference, this remains 8 scenes/23s, without cinematic human/robot scenes or continuous app operation.

Remaining: independent Japanese speech transcription/meaning and listening, inherited asset/voice rights, smartphone playback, human approval, retention and Actions billing verification. Employee review followed by manual posting only.
