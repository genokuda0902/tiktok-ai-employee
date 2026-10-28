# cycle932 — actual fictional Calc GUI capture in scene05 (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is a new image-first reimplementation, not original v33 source or proof of reference parity.

## Improvement vs cycle930 (#315) and parallel cycle931 (#316)

The previous scene05 was a static three-row approval card. This cycle replaces **only scene05, frames 348–434 (11.6–14.5s)** with a newly recorded, real LibreOffice Calc GUI action using **entirely fictional** April–June Sales A/B values. The capture shows blank June Sales A, entering 18, and the formula result changing 28 → 46. The video explicitly says this is fictional and unapproved. This is not a screenshot of ChatGPT or Microsoft Excel and not a real business result. This is distinct from cycle930 scene06 number comparison and cycle931 audio scene SFX.

The capture was recorded locally on a clean isolated Xvfb display, with a locally created fictional workbook. No personal information, real customers, external footage or proprietary media were introduced. **Do not upload the private capture, original MP4, rendered MP4 or workbook to public GitHub.**

## Reproduce locally with approved private inputs

Requires Python 3.11+, Pillow, FFmpeg, Noto CJK fonts and the *authorized* local MP4 and Calc capture. SHA pin protects the source video. All assets remain local.

```bash
python cycle932/src/calc_live_insert.py \
 --source /private/cycle930_EVIDENCE_COMPARISON_JP_REVIEW_ONLY.mp4 \
 --capture /private/real_calc_capture_take2.mp4 \
 --output /private/cycle932_REAL_CALC_SCENE05_REVIEW_ONLY.mp4 \
 --workdir /private/cycle932_render \
 --genre ai_work \
 --expected-source-sha cc9304cb82610e0375e5274c640486d8f6957455f09cfd6a1ad4ed7660698ceb
python -m unittest discover -s cycle932/tests -p 'test_*.py' -v
```

## Local verified result (private)

Source SHA256: `cc9304cb82610e0375e5274c640486d8f6957455f09cfd6a1ad4ed7660698ceb`.
Output SHA256: `8f186fadd541a74aa1dabf8eff52b131e879d9cda7af0696f2ceb938be62148e`.
1080×1920 H.264 30fps, 691 frames, 23.033s, AAC 48kHz Japanese inherited voice. Complete A/V decode PASS. AAC ADTS stream SHA256 unchanged: `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`. Scene05 87 frames visibly changed (min 1/8-scale MAE 45.88); outside-scene max MAE 0.275; protected subtitle band max MAE 0.231. Local 11/11 synthetic unit tests PASS. 10 genre-safe rendering configurations tested; only ai_work full MP4 produced.

## Reference / limits

Consulted available past TikTok市場分析/TikTok動画研究 summaries and directly viewed user's 16-panel ChatGPT×Excel storyboard. Full original chats and original v33 MP4 unavailable. New capture is actual LibreOffice Calc, but only one scene; 8-scene current video still differs from cinematic 16-panel robot/people/Excel/ChatGPT reference. Japanese speech meaning/pronunciation and subtitle semantic/timing alignment, phone playback, inherited media commercial rights, employee approval and Actions actual billing remain unverified. CI runs source/synthetic tests, **not the private completed MP4**. No merge, auto-post, paid service or public private-media upload. Manual posting after employee approval only.
