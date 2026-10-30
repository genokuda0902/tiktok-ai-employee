# cycle1018 — complete Japanese prompt entry / REVIEW ONLY

Date: 2026-10-30 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Verified delta vs cycle1016
- At **8.94–11.31s**, the simulated AI-input screen had a visually incomplete prompt at some frames. This adds an original animated 3-line prompt card with all three complete Japanese instructions, text-fit checks, a typing cursor, and a progress bar.
- Text: 「この売上データを月別に集計して」「4〜6月の営業AとBを比較し」「表とグラフで要点をまとめて」.
- Clearly marked **再現画面・説明用**; not a real ChatGPT screen recording, real AI run, or actual narrated word alignment. Preserves lower captions, waveform, other scenes, and original audio.
- Common 10 genre IDs; only SHA-pinned local ai_work can render the real video. Other 9 genres fail closed. Synthetic CI is separately restricted to short A/V fixtures.

## Real private video and local verification
- Input cycle1016 MP4 SHA256: ba2b8937fd6343a12f5dd09fcfcef590d800fef73347b52662792ea72e5fa163.
- Output cycle1018 MP4 SHA256: 779db27ac4d0a0644d1d8f12d65a4766fafd0c6c6346b2eaa12e0d43795c5172.
- H264 1080x1920, 30fps, 691 frames, 23.033333s; AAC 48kHz jpn-tagged; full video+audio decode PASS.
- AAC ADTS SHA256 before/after: ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e (unchanged).
- Burned-in Japanese captions: eight inherited segments, no selectable subtitle track. 70/691 frames sampled: subtitle ROI y1280–1610 max mean pixel difference 0.525/255; insert ROI max 51.414/255. Image samples are not semantic speech verification.
- Local 12/12 unit tests PASS; 2-second synthetic A/V integration PASS. Real private MP4 is in the ChatGPT sandbox only, NOT in public GitHub or CI artifact.

## Research/reference and unverified gates
- Consulted accessible summaries of 「TikTok市場分析」「TikTok動画研究」 and directly inspected user's ChatGPT×Excel時短術16コマ絵コンテ.png (16 panels, about 36 seconds). Full original research chats and original v33 MP4 inaccessible.
- Current 8-scene 23s video still lacks reference visual diversity, cinematic imagery, and continuous real application operation; no v33 parity claim.
- NOT VERIFIED: independent Japanese ASR, narration-caption semantic/word-level sync, publication rights, smartphone playback, employee approval, retention, actual Actions billing. No posting.

## Repository safety
- Main at check: 18e084c38db0dc55db7dfc0532b9451b1167f2aa. Draft PR #419 stacks on open PR #417, parallel PR #418 untouched. No merge.
- Source: cycle1018/source/prompt_completeness.py; tests: cycle1018/tests/test_prompt_completeness.py; workflow: .github/workflows/cycle1018_review.yml.
- GitHub Actions tests synthetic 2-second media only, not private full MP4.
- No private media, storyboard, extracted narration, auto-post, or paid API contract.

## Next cycle
1. Highest priority: independent offline Japanese ASR or explicitly labeled human speech-caption verification, with fail-closed mismatch gate.
2. Improve image-first cinematic stills and genuine sanitized operation footage with approved assets; natural robot animation is out of scope.
3. Obtain phone playback, rights, and employee approval before any manual post.
