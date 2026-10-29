# cycle985 — caption-safe accent bloom (review only)

## Change from cycle983

Previous cycle983 recovered dark details on all eight AI-work scenes. This cycle adds a separate, bounded cyan-accent light diffusion on artwork y=150..1179, using a two-radius Gaussian halo from HSV-selected accents. Header y<150 and caption/footer y>=1180 are not touched by the algorithm; codec re-encoding can still change their decoded pixels. The 10-genre hue registry is present, but only ai_work is layout-reviewed on real footage. Others fail closed without --synthetic.

## Private local deliverable

output/cycle985_ACCENT_BLOOM_JP_HUMAN_REVIEW.mp4 (not committed to public GitHub). Based on private cycle983 MP4; inherited Japanese narration and subtitles retained. Original v33 reference media unavailable. Prior TikTok research: first 1.5s hook, 15–25s, 6–10 cuts, concrete demonstrations, safe captions, manual approval. This change is a controlled aesthetic pass, not proof of reference parity.

## QA

- MP4 1080x1920, 30fps, H.264/AAC 48kHz, 23.033s, 691 frames; both streams fully decode.
- Audio AAC ADTS SHA256 identical to cycle983: 785b26ef233e7b6d2e2f1dc37b143d89cd8e2aaebb663480ee54d61d45986f43.
- Caption region y>=1180 max frame-mean absolute pixel delta 1.590/255 after lossy re-encode (not bit-identical).
- Art region y=150..1179 mean absolute pixel delta 1.849/255 over sampled frames; effect is deliberately subtle.
- 7 local unit tests pass; 10 genre profiles validated synthetically. GitHub CI independently runs synthetic vertical A/V video, not the private deliverable.
- Independent Japanese ASR and semantic/timing subtitle verification unavailable. No claims about voice naturalness, commercial media rights, phone playback, employee approval, or reference v33 parity.

## Release

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No paid services, auto-posting, unauthorized merge, or publishing. Employees must approve before manual posting.
