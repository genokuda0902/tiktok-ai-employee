# cycle910 — evidence wipe / private review only

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, posting, paid API, private media upload, or claim of reference-equivalent quality.

## Research / source provenance
- Accessible summaries of TikTok市場分析 / TikTok動画研究: hook in first 1–1.5 seconds, clear visual proof, Before/After, readable Japanese captions, manual employee approval. Original full research chats unavailable.
- Directly opened user's ChatGPT×Excel時短術16コマ絵コンテ.png (16 panels, human/robot cinematography, spreadsheet and graph, 36s). Original v33 MP4 not available for direct comparison.
- Read PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md and reviewed latest main and open PR #283 cycle908 and parallel #284 cycle909. Source is mounted private cycle908 review MP4, not cycle909; **no direct cycle909 video comparison**.

## Change vs cycle908
- Scene08 frames 588–690 (19.6–23.033s): replaces abstract Before/After workflow cards with a legible **fictional 4–6月 input table A12/16/18, B8/9/12 → existing animated chart**; totals A46/B29 are internally consistent. Animated left-to-right reveal, no time-saving performance claims.
- 10 reusable genre palettes/labels. Uses inherited local MP4 frames and native drawing only; no external photos, logo downloads, or personal information. Subtitle band untouched by overlay; inherited Japanese AAC copied bit-for-bit.
- Local tests and private technical QA are separate from CI: GitHub runs dependency-free policy tests only and **does not test the full private Japanese MP4**.

## Reproduce locally (do not publish)
Requires free ffmpeg, Pillow and a Japanese Noto CJK font.

\`\`\`bash
python -m unittest discover -s review_cycles/cycle910 -p 'test_*.py' -v
python review_cycles/cycle910/evidence_wipe.py --source /private/cycle908_REVIEW_ONLY.mp4 --source-sha256 VERIFIED_SOURCE_SHA256 --output /private/cycle910_EVIDENCE_WIPE_JAPANESE_REVIEW_ONLY.mp4 --frames-dir /private/overlays --report /private/render_report.json
\`\`\`

## Local verification
- Baseline cycle908 SHA256 d811aba20df5c2ef4a43742868035af60f494dc99c10651458da5ac4f5ae25ef.
- Output 1080×1920, 30fps, 691 frames/23.033s, H.264/AAC48kHz, full A/V decode PASS; ADTS AAC SHA256 source/output 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9.
- 103/103 changed frames detected at 1/4-resolution; protected subtitle area y≥1490 not drawn over, but re-encode pixel differences remain (max MAE 1.773 at quarter-resolution).
- Local 12 tests PASS, stdlib CI 12 tests PASS locally. ASR / Japanese speech-caption meaning and timing, rights, mobile playback, employee approval, v33 parity, actual Actions billing unverified.

**Do not publish** until rights and content are independently reviewed and employee approval is recorded; employee manual posting only.
