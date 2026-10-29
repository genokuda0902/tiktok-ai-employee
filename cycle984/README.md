# cycle984: CTA step counter and completed-step ticks (REVIEW ONLY)

This is an **incremental** AI-work video edit based on the private cycle982 MP4; it does not recover the original v33 renderer. Previous cycle982 introduced real LibreOffice Calc GUI formula entry; cycle983 (parallel PR #384) independently brightened shadow detail. This cycle does neither: it improves **end-CTA comprehension** at 20.30–23.033s with a visible 1/3 → 2/3 → 3/3 indicator and ticks on prior steps. It preserves the source's own card-highlight animation, avoiding duplicate borders. Only upper artwork y<1440 is overlaid.

Run locally (private source is never in this repository):

    python cycle984/cta_focus.py --source /private/cycle982.mp4 --output /private/cycle984.mp4 --work /private/work

Source/output checks are local, not GitHub Actions. Real private video, screenshots, AAC and user assets are **NOT** committed. Synthetic CI runs 9 unit tests and a 2-second synthetic H.264/AAC integration. 10 genre IDs are declared but only ai_work CTA geometry is reviewed; all other real layouts fail closed.

## Research and reference provenance
Available summaries of TikTok市場分析 and TikTok動画研究 emphasize early hook, clear readable subtitles, purposeful cuts, real UI and human review. Full source chats unavailable. The user's 16-panel ChatGPT×Excel storyboard was directly viewed this cycle; original v33 MP4 unavailable. Reference has 16 panels/~36s and richer cinematic scenes; current review video remains 8 scenes/23.033s. No quality parity claim.

## Local validation (2026-10-30 JST)
- Input cycle982 SHA256: 0f643009e525bb4e5d775b1f20cc6c0a937c4fe650dcba17cbc7e9ff6bb240eb
- Output cycle984 SHA256: 1e03d7274d2d11c5c2ed80ebd4254bd972cc5acfb251abfa76aec06f5207c63e (verify current file again after any regeneration).
- 1080x1920 H.264 30fps, 691 frames / 23.033s; AAC 48kHz stereo; full A/V decode PASS.
- AAC ADTS SHA256 source/output: ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e, identical.
- 9 local unit tests PASS. All 691 frames compared at quarter resolution: protected caption y>=1440 max mean pixel difference 0.28175/255; outside CTA max 0.61856/255; CTA card ROI mean 0.63813/255. Technical pixel metrics are not a viewer-quality score.
- Independent Japanese speech transcription/semantic caption sync, rights, smartphone playback, employee approval and Actions billing are **NOT verified**.

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, posting, publication, confidential source upload or paid-service purchase.
