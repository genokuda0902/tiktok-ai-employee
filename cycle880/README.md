# cycle880 — review-only kinetic CTA end card

**Distinct from cycle879:** The earlier cycle added an audio-reactive meter and trimmed a silent tail. This cycle replaces only the upper 1340px of scene08 (frames 588–690) with three staged, concrete next actions and a delayed save/try CTA. The inherited 8 Japanese subtitles and audio meter remain in the lower band, and the AAC bitstream is stream-copied. Synthetic, fictional data only; the example is not real AI product footage.

Run locally, without uploading private media:

```bash
python cycle880/kinetic_endcard.py --source PRIVATE_CYCLE879.mp4 --output PRIVATE_CYCLE880_REVIEW_ONLY.mp4 --manifest private_manifest.json --report private_report.json
```

The private manifest must equal: `{"review_only":true,"publication_approved":false,"external_upload":false,"automatic_posting":false,"source_rights_reviewed":false,"source_sha256":"<SHA256 OF INPUT>"}`. Do not commit this manifest or private MP4. Requirements: FFmpeg, Pillow, Noto Sans CJK. The public CI only tests 13 standard-library cases and a synthetic A/V smoke; **it does not produce the Japanese review MP4**.

Reusable `EndCard` configuration supports 10 genres. The demonstration copy is AI-work-specific, so other genres require editorial copy and human review. No independent ASR or Japanese semantic subtitle verification. No v33 parity claim. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; employee approval and manual posting only.
