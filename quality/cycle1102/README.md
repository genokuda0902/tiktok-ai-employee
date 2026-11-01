# cycle1102 — evidence close-up before final CTA (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** The actual user review MP4 is not uploaded to GitHub. Source and voice rights remain unverified. No automatic posting, merging, or paid services.

## Difference from cycle1100
cycle1100 highlighted the Calc formula at 6.5–8.3s. cycle1102 instead inserts a **1.3-second close-up of the existing fictional Calc evidence at 20.3–21.6s**, then returns to the original full-frame CTA. This adds one purposeful visual cut without changing the data or audio, preserving the Japanese subtitle region below y=1280. All ten genre identifiers share the renderer; the complete local MP4 was tested only for ai_work.

## Private review verification
Source SHA256: 739599eafb7b2150ade1aa79aeef1dbd4f0390990c6236c33a4cc7ebc8754f54.
Output SHA256: fe10b5dfe6ddab7fe1de208146eea5fe62147fded29ed8ddb7de6ff6c0ff3ca6.
Actual local MP4: H.264 1080x1920 30fps, 691 frames, 23.033s, AAC 48kHz, full video/audio decode PASS, original AAC ADTS bitstream identical. Picture ROI mean delta during target frames: 48.088/255; outside: 0.249/255. Subtitle-protected region maximum frame mean difference: 0.279/255. Nine unit tests PASS.

20ms audio RMS is measured across eight *approximate* segments; all have nonzero energy. This **does not** identify Japanese speech, transcribe words, or prove subtitle synchronization. Independent ASR, phone playback, rights, employee approval, v33 quality parity, and actual GitHub Actions billing are unverified.

## Reproduction
```bash
python3 quality/cycle1102/proof_closeup.py --source /private/cycle1100.mp4 --source-sha 739599eafb7b2150ade1aa79aeef1dbd4f0390990c6236c33a4cc7ebc8754f54 --manifest quality/cycle1102/manifest.json --out /private/cycle1102.mp4 --report /private/qa.json
```
CI runs on synthetic H264/AAC only. The original v33 generation code is still not recovered.

## References and safety
Accessible summaries of TikTok市場分析 and TikTok動画研究: strong first 1.5s hook, short purposeful cuts, real UI, before/after, readable captions, manual posting. The user-provided 16-panel storyboard was directly inspected this cycle. The original v33 MP4 and full research chat transcripts were not directly accessed. Reference has cinematic person/robot, real app demo, 16-panel ~36s storyboard, whereas this review is 8 original scenes plus a close-up insert in 23.03s. No reference-quality claim.
