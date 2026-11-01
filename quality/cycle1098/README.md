# cycle1098 — three-stage Writer proof spotlight (REVIEW ONLY)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. New original reimplementation, NOT recovered v33 source. No private MP4, extracted voice, user images, personal data or rights-unverified source media committed.

## Distinct change vs cycle1096

cycle1096 added a safe final CTA at 21.967s and acoustic presence QA. This cycle changes the **Writer document** at 17.500–19.900s: a soft cyan outline walks through the fictional template's **目的 → 条件 → 形式** lines. This guides the eye through the actual on-screen document instead of adding an unrelated CTA. All 10 genres have selectable accents; the complete MP4 is tested only for ai_work. This is an animation over a still software screenshot, not live app interaction.

## Local completed media (not committed)

Source: cycle1096 MP4 SHA256 `53bb7306b829054c0379d46cb6422f164f7be54153af67637d1b549331686831`.
Completed cycle1098 MP4 SHA256 `71be71788fd58ffdf17862d61c4984c6ad5637ea44d4fe277b59748dd4f82cea`.
23.033s / 691 frames / 1080x1920 / 30fps / H264 and inherited Japanese-tagged AAC 48kHz stereo.
Full video/audio decode PASS; AAC ADTS bitstream identical; 10 local unit tests PASS.
All 691 frames, 1/4-spatial sampled: caption region y1490:1840 max per-frame mean difference **0.9865/255**; modified document region mean difference **2.0289/255**; outside-target max full-frame mean difference **1.4308/255**. These are pixel metrics, not proof of speech/subtitle meaning.
Loudness measured: integrated -16.26 LUFS, true peak -3.29 dBTP.
Source, output, compare JPG and QA JSON are in the private ChatGPT review package only.

## Offline reproduction (requires private approved-for-review source)

```bash
python3 -m unittest discover -s quality/cycle1098 -p 'test_*.py' -v
python3 quality/cycle1098/proof_spotlight.py \
 --source /private/cycle1096_SPEECH_SAFE_CTA_JP_REVIEW_ONLY.mp4 \
 --source-sha 53bb7306b829054c0379d46cb6422f164f7be54153af67637d1b549331686831 \
 --out /private/cycle1098_WRITER_PROOF_SPOTLIGHT_JP_REVIEW_ONLY.mp4 \
 --manifest quality/cycle1098/manifest.json --report /private/cycle1098_qa.json
```

CI creates a **synthetic** 23s H264/AAC source and tests rendering and decode; it does NOT access or validate the private completed Japanese MP4.

## Research and release gates

Accessible previous TikTok市場分析/TikTok動画研究 summaries: strong first-second hook, purposeful cuts, readable Japanese subtitles, real UI, before/after, manual posting after employee review. Original research chat full texts unavailable. User's 16-panel ChatGPT×Excel storyboard directly inspected this cycle; original reference v33 MP4 unavailable this cycle. Reference storyboard 16 cuts/~36s and original v33 31.553s vs current 8 scenes/23.033s; cinematic human/robot footage and cut variety remain weaker.

Independent Japanese ASR and 8 caption semantic/word-timing verification, mobile-device playback, commercial asset/voice rights, employee approval, actual Actions billing and reference quality parity remain **UNVERIFIED**. No merge, auto-posting, external media upload, paid service, or production delivery. Next priority: independent Japanese speech transcription + subtitle alignment, especially 20.3s onward.
