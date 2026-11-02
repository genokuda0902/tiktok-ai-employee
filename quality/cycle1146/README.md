# cycle1146 — legible action takeaway (review only)

Compared with cycle1144's pointer/number guidance, this pass enlarges the tiny scene-02 instruction into a readable cyan-bordered **NEXT** banner, without modifying the Japanese captions or narration. It is an original image overlay, not a recovered v33 scene or a new filmed actor.

The 10-genre renderer requires a pinned SHA-256 source, `HUMAN_REVIEW/PUBLICATION_NOT_APPROVED` policy, safe time window, a short approved Japanese takeaway and fixed content ROI (x=50,y=1095,w=850,h=132, entirely above protected y=1500). No network or posting operations.

Run with a private manifest containing `policy`, `genre`, `source_sha256`, `takeaway`, `start`, `end`:

`python quality/cycle1146/readable_takeaway.py --source PRIVATE.mp4 --output PRIVATE_REVIEW_ONLY.mp4 --manifest PRIVATE.json --report PRIVATE_QA.json`

`PYTHONPATH=quality/cycle1146 python -m unittest discover -s quality/cycle1146/tests -p 'test_*.py' -v`

CI renders only synthetic H264/AAC; real MP4 is a private ChatGPT review attachment and must not be committed or published. Original v33 reference and independent Japanese ASR are not available. No claim of reference-equivalent quality, rights clearance or publication approval.

## Measured local private MP4 (2026-11-02 JST)

- Source cycle1144 SHA256: `18c7da2395524fb490f0d427e190fcbfccd2f40062482c864c389060d4bcde15`.
- Output cycle1146 SHA256: `acf8d9fac8139f08bfa4a71e7fe4900e2c2e6a0b8e44d3923c1dcdf6bdaafbb8`.
- H264 1080x1920 30fps, 691 frames / 23.033333s, AAC 48kHz Japanese-tagged; full video/audio decode PASS.
- Audio ADTS SHA256 source and output identical: `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`.
- 5-frame-step sampled caption ROI (y1500:1830) maximum mean pixel delta 0.7092/255; effect ROI mean pixel delta 42.374/255; outside-effect mean 0.845/255 (recompression).
- 9 local unit tests PASS; synthetic 60-frame A/V render/decode PASS. CI checks synthetic only, not private full MP4.
- Reference storyboard directly inspected: 16 panels/~36s, cinematic robot/person, real UI, Before/After, CTA. Current video remains 8 scenes/23s. Full TikTok research transcripts and original v33 MP4 not accessed.
- Independent Japanese ASR, caption semantic/timing accuracy, rights, phone playback, employee approval and GitHub billing unverified. No merge, automatic posting, paid service or public media upload.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**
