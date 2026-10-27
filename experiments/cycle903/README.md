# cycle903 — narration-pause candidate caption focus (review only)

**2026-10-27 JST. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Distinct improvement and baseline

Previous accessible private MP4: cycle901 (SHA-256 e23ac030112f1b96543b28a862afd0136146ca15f1a525e2242baa5a4ec5aac8). A parallel unmerged PR #274/cycle902 modifies scene 2, but its finished private MP4 was not accessible and was not used. Cycle903 changes the **burned caption area in all 8 scenes** rather than another mock UI animation: two large Japanese lines remain visible while the emphasized line changes at an automatically selected **low-RMS audio pause candidate** in each scene, with a 5-frame transition. Existing upper visual, waveform and narration are retained.

This is **not speech-to-text** and **not semantic/word-level audio-caption verification**. Background music and acoustic ambiguity can produce an incorrect candidate; human review remains mandatory. The explicit fail-closed release gate blocks publication even if a transcript is later supplied, until employee approval and rights checks are completed.

## Actual local review video and QA

- Source: cycle901_PROVISIONAL_PROOF_JAPANESE_REVIEW_ONLY.mp4, SHA-256 e23ac030112f1b96543b28a862afd0136146ca15f1a525e2242baa5a4ec5aac8.
- Local review output: cycle903_CAPTION_FOCUS_JAPANESE_REVIEW_ONLY.mp4, SHA-256 in local verification report; **not committed or uploaded to public GitHub**.
- Caption focus switches at frames 52, 119, 200, 283, 373, 454, 545, 628 (30 fps).
- H.264 1080x1920, 30fps, 691 frames / 23.033s; AAC 48kHz inherited bitstream identical to source (ADTS SHA-256 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9).
- All 691 caption frames changed (>5 sampled mean pixel delta); non-caption 95th-percentile delta <0.5, maximum <0.6 at quarter resolution. Full A/V decode PASS; local 15 unit tests PASS.
- The source video and caption text remain *review-only*, not approved public media. Independent Japanese ASR, naturalness, word alignment, source rights, smartphone hardware playback, employee signoff, original v33 parity and actual Actions billing **not verified**.
- GitHub CI tests source/policy and synthetic one-second A/V, **not** the private Japanese 23-second MP4.

## Local reproduction (private)

Requires Python 3.11+, Pillow, FFmpeg, ffprobe and Noto CJK fonts. Do not commit source footage, audio, transcript or private manifest.

    python -m unittest discover -s experiments/cycle903/tests -p 'test_*.py' -v
    python experiments/cycle903/caption_focus.py \
      --source /private/source.mp4 \
      --output /private/cycle903_REVIEW_ONLY.mp4 \
      --manifest /private/review_manifest.json \
      --report /private/verification.json

Private manifest must specify a supported genre, publication_approved:false, employee_approval:false, contains_private_data:false, exact source_sha256 and 8 caption pairs. The boolean only records the current operator's input assessment, **not a completed independent privacy audit**. The renderer rejects unknown genres, unpinned sources, missing privacy declarations, overwrites and invalid caption lengths.

## Research and reference

Accessed prior TikTok市場分析 and TikTok動画研究 summaries: first 1.5s hook, purposeful cuts, authentic UI, Before/After, readable Japanese captions, employee-reviewed manual posting. Full research task/chat transcripts unavailable. Directly inspected the user's ChatGPT×Excel時短術16コマ絵コンテ.png: 16 panels, 36 seconds, cinematic robot/person and real-app demonstration imagery. Original v33 MP4 not available for direct comparison this cycle. Main checked at 18e084c38db0dc55db7dfc0532b9451b1167f2aa, unmerged PR #274/#273/#272 reviewed, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, src/build_daily.py checked. Handoff explicitly cancels natural robot motion and requires approved image-first assets.

**Remaining gap:** This 8-scene UI-based 23-second review video does not match the reference's 16-shot cinematic variety or real software workflow. A local acoustic pause candidate does not establish Japanese pronunciation or semantic subtitle synchronization. Next cycle must independently transcribe and compare spoken Japanese, and verify caption timings before any approval. No merge, posting, paid service, public media upload or production delivery.
