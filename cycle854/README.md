# cycle854 — original cinematic task-focus, 10 genres (REVIEW ONLY)

Stacked on **unmerged Draft PR #194**. This is an **original reimplementation**, not recovered v33 source. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Delta from cycle853

- Replace scene 02 picture region only, **frames 89–169** (2.967–5.667 s, 81/691 frames) with an original cinematic photo-backed, three-beat glass checklist. The beat progression highlights `集計・入力` → `資料の作成` → `定型メール` as *illustrative task categories*, not claims of actual employee tasks or AI output.
- Keep the inherited source photo behind the card (subtle ≤4.5% Ken Burns), and protect the source Japanese headline and burned-in captions **outside** rectangle x=86..994, y=476..1234.
- Preserve inherited Japanese AAC bitstream without decoding/re-encoding. Local source/output ADTS SHA256 both `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- Local real video `1080×1920`, `30fps`, `691 frames`, `23.033s`; source SHA256 `80563f1b8d31aaf909581447fa81bb282039aece9bdb189c4c1e02ce003f1009`; output SHA256 `654c88cb891df36df512e29a4c6cfe9bf5978db20df77982c32293a2a1c6c1a0`. Full AV decode passed. 10 unit tests passed.
- Genre palettes for all ten supported genres; unknown genre, missing source, overwrite and invalid source-policy manifest fail closed. GitHub CI tests with *synthetic* sound and color; it does not contain the private Japanese MP4.

## Local reproduction

```bash
python cycle854/scene2_workflow_focus.py \
  --source /private/cycle853_REAL_WRITER_EVIDENCE_REVEAL_JAPANESE_REVIEW_ONLY.mp4 \
  --output /private/cycle854_CINEMATIC_WORKFLOW_FOCUS_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest /private/source_manifest.private.json --report /private/qa854.json
PYTHONPATH=cycle854 python -m unittest discover -s cycle854 -p 'test_*.py' -v
```

Manifest must contain `POLICY` exactly plus pinned `source_sha256`; no media is committed. Local review MP4 shared only via ChatGPT sandbox, **not** GitHub.

## Research and provenance

- Consulted accessible summaries of `TikTok市場分析` / `TikTok動画研究`: first-second hook, purposeful short scenes, demonstrative UI, Before/After, Japanese caption readability and manual posting after employee review. Original chat/task bodies unavailable.
- Directly inspected user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 visual panels, 36-second storyboard); original reference v33 MP4 inaccessible this cycle. No claim of reference-equivalent quality. Storyboard human emotion, cinematic photography and rich 16-panel composition remain gaps.
- Reviewed main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, open PRs (including #194 and parallel #195), `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md` and prior code. No merges.
- **Not independently verified:** Japanese spoken text/naturalness and word-level caption alignment, inherited media public-use rights, smartphone playback, employee approval, actual Actions billing. No paid API, publishing, external media upload or automatic posting.