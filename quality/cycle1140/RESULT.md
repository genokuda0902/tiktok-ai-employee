# cycle1140 — review-only subject camera motion

2026-11-02 JST. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Delta
cycle1138 applied a moving cyan key light for 29 frames. This distinct cycle applies a subject-local 56-frame (1.867s) eased 1.08x camera push/pull. An initial prototype ghosted the title's Japanese overhanging callout, so it was rejected; a mandatory 90px title guard was added. No scene, subtitle, narration or CTA changes. Ten genre names share strict hash/rights/ROI gates, but only AI/Excel was rendered.

## Actual private local video, not in GitHub
Input cycle1138 SHA256: 4a881fc32e9bd03117801c6c82f9c4e96795b2a172d71be9541d4d5b5eef3f45.
Output cycle1140 SHA256: 20e3fb916ef5654c4d333863c907c35f348f4daab1fbcc7caa5a7fe6f1fcd775.
H264 1080x1920 30fps 691 frames / 23.033s, AAC jpn 48kHz. Full A/V decode PASS. AAC ADTS SHA256 both: 27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65.
At frame 30 subject MAE 28.017/255, title guard MAE 1.694/255, subtitle ROI MAE 0.335/255; re-encoding creates nonzero differences. Local 12 unit tests PASS, 75-frame synthetic video generated and decoded. GitHub CI only tests synthetic media.

## Research, safety, reference
Accessible TikTok市場分析 / TikTok動画研究 summaries: first 1.5s hook, 15-25s, real UI, Before/After, readable Japanese captions, manual employee approval. User-provided 16-panel Excel/ChatGPT storyboard inspected in prior cycles, with cinematic robot/person, spreadsheet, chart and CTA; full original research transcripts and v33 MP4 inaccessible this run. Reference ~16 scenes/~36s vs current 8 scenes/23s. No independent Japanese ASR/semantic subtitle match, source rights approval, phone playback, employee approval, or real Actions billing audit. No merge, posting, paid services or private-media upload.

Reproduce: python quality/cycle1140/subject_push.py --source PRIVATE_PREVIOUS.mp4 --output PRIVATE_NEXT.mp4 --manifest PRIVATE_APPROVAL_MANIFEST.json --report PRIVATE_QA.json
Never commit the private manifest or video.
