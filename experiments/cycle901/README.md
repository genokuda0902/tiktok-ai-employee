# cycle901 — provisional evidence clarity (2026-10-27 JST)

Compared with cycle900 pause-gated transitions, this cycle fixes a narrative ambiguity: scene03 presented A45/B28 as a finished example even though later review corrects to A46/B29. A native 900x510 Japanese overlay marks the earlier chart 検証前 / 数値は要確認, calls out fictional data, and previews source reconciliation. The graph and burned captions are preserved.

## Private local media QA

Generated actual cycle901_PROVISIONAL_PROOF_JAPANESE_REVIEW_ONLY.mp4 in private conversation storage, **not in this public repository**. Source cycle900 SHA256 5637ec34a022fa580463c101b217a83e4347a2075dd84501e4f35b2e0e519f4a. Output SHA256 e23ac030112f1b96543b28a862afd0136146ca15f1a525e2242baa5a4ec5aac8. H.264 1080x1920 30fps, 691 frames/23.033s, AAC 48kHz. Original AAC ADTS SHA256 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9 identical. Full A/V decode PASS; 80/81 target frames changed >2 sampled pixel mean; caption-region max 1.0787, non-target max 1.2223. Local 14 unittest checks PASS. CI tests code and policy only, **not the finished private MP4**.

## Render locally

Requires an approved local source MP4, FFmpeg, Pillow, and Noto CJK font. Do not upload private media. Command:

    python experiments/cycle901/provisional_proof.py --source PRIVATE_SOURCE.mp4 --badge badge.png --output review_only.mp4

Result remains HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Research, provenance and limitations

Consulted accessible TikTok市場分析 / TikTok動画研究 summaries (hook, purposeful short scenes, real UI, Before/After, readable subtitles, manual employee approval), and directly inspected user-provided ChatGPT×Excel時短術16コマ絵コンテ.png. Full research chats and original v33 MP4 inaccessible. Verified main 18e084c and unmerged PR #272/#271/#270; read PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md and src/build_daily.py (still silent -an output). Ten genre policies tested; only AI-work MP4 rendered. Independent Japanese ASR/semantic timing, inherited media rights, phone playback, employee approval, original-v33 parity and actual Actions billing unverified. No merge, paid service, auto-post or public private-media upload.
