# cycle951 — fictional arithmetic-evidence clarity + fail-closed semantic QA

**2026-10-29 JST. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is a new review-only reimplementation; it is not original v33 source.

## Distinct change from cycle949 and concurrent PR #346
- cycle949 (PR #345) focused the camera on a Calc input cell and recalculated total. Concurrent cycle950 PR #346 animates a chapter badge.
- cycle951 fixes a different problem: during scene05 the Calc cell temporarily shows **28**, which could be mistaken for the final A-column total. A source-derived two-phase explanation clarifies **入力中：合計は未確定** and, after the final result appears, **A:12+16+18=46 / B:8+9+12=29**.
- No numeric claim is accepted unless it matches the explicit fictional arithmetic ledger; a mismatched total fails before render. Text is drawn only in a manually checked, moving left-panel blank region. Existing Japanese captions and audio are not rewritten.
- 10 genre labels supported in the fail-closed evidence validator; the visual placement is approved **only for the fictional AI-work review MP4**. Other genres require their own evidence and geometry review.
- New semantic_gate explicitly returns UNVERIFIED without an **independently obtained** Japanese ASR transcript. A copied script or audio-presence test cannot pass it. Even an exact text match does not authorize publication.

## Verified local review MP4 (private; NOT committed to public GitHub)
- Source cycle949 SHA256 a28f54e76e4fd54395d2003c0b403a63a5fdc3af9d86a3c4740811abdf66ab07.
- Output MP4 SHA256: 950b8d4d336cdb5f4ba4a774348e19c4f0dfc8bff98046e2eeeed2a9d2976c2d.
- H.264 1080x1920 30fps 691 frames / 23.033s; AAC 48kHz stereo.
- Full A/V decode PASS; source/output AAC elementary streams SHA256 equal 37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27.
- 691 frames compared at 1/8 resolution: subtitle-region max frame mean difference **0.2181 gray levels**; cue ROI mean difference **17.4222**; outside cue p95 **0.1305**.
- Local pytest **27 passed**. CI tests source and synthetic data only, not the private MP4.
- WebRTC VAD detected speech-like energy in 667/766 30ms windows (87.08%). This is **not** independent Japanese ASR or a subtitle meaning check.

## Local reproduction

~~~bash
python -m pytest -q cycle951/tests/test_evidence_consistency.py
python cycle951/src/evidence_consistency.py \
 --source /private/cycle949_ACTION_FOCUS_JP_REVIEW_ONLY.mp4 \
 --source-sha256 a28f54e76e4fd54395d2003c0b403a63a5fdc3af9d86a3c4740811abdf66ab07 \
 --output /private/cycle951_ARITHMETIC_EVIDENCE_JP_REVIEW_ONLY.mp4 \
 --qa /private/qa951.json
python cycle951/src/verify_review.py /private/cycle949_ACTION_FOCUS_JP_REVIEW_ONLY.mp4 \
 /private/cycle951_ARITHMETIC_EVIDENCE_JP_REVIEW_ONLY.mp4 /private/qa951_full.json
~~~

ffmpeg, ffprobe, Noto CJK fonts, pytest and optional numpy for the local verification script are required. No paid service or external media download is used.

## Research, reference and handoff
- Consulted available prior summaries of TikTok市場分析 / TikTok動画研究: immediate 1–1.5s hook, 15–25s, real UI, Before/After, readable Japanese subtitles, human approval. **Full original chat/task transcripts inaccessible.**
- Directly inspected user's Library ChatGPT×Excel時短術16コマ絵コンテ.png: 16 cuts/36s with 3D robot, person, real app-like visuals, transitions and CTA. **Original v33 MP4 not accessible**; no direct equivalence comparison.
- Read latest main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, open PR #345 and concurrent #346, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, src/build_daily.py (still silent). Original v33 generator remains missing.
- Current 8-scene, 23.033s graphic-heavy MP4 remains less cinematic than 16-panel reference; source media rights and employee approval unverified.
- Independent Japanese ASR transcript/semantic caption timing, smartphone playback, inherited rights, reference v33 parity and actual Actions billing remain **unverified**.

**No merge, posting, paid API, production delivery, or private video upload.** Employee-approved manual TikTok posting only after separate quality/rights clearance.
