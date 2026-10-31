# cycle1143 — illustration-only clarity lift (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No publishing, merging, paid APIs, external image downloads, or private MP4 upload to GitHub.

## Distinct change from cycle1141

cycle1141 froze the caption card while moving upper artwork. cycle1143 applies a restrained gamma/contrast/saturation lift **only to the central illustration band y=370–1220**, feathered at both edges, leaving the Japanese caption card below y=1350 and top titles outside the effect. The same parameterized compositing code accepts 10 genre IDs. Actual MP4 is AI-workflow genre only.

No new imagery or voices were generated. The inherited AAC stream is copied bit-for-bit. This improves measured midtone brightness, but does not prove the original Japanese narration matches the displayed subtitles.

## Local QA

Run `python -m unittest discover -s quality/cycle1143/tests -v` and `python quality/cycle1143/code/ci_synthetic.py`. Synthetic CI uses only 1.5 seconds of FFmpeg-generated color bars and sine audio; it verifies H264/AAC, 1080×1920, 30fps, 45 frames, full decode, and unchanged AAC elementary stream.

The private 22.5-second completed MP4, actual before/after JPEG, 8-scene contact sheet, QA JSON and code are available in the downloadable local review package. They are not committed to GitHub.

## Research and limitations

Consulted available `TikTok市場分析` and `TikTok動画研究` summaries from the user's Library and previous cycle1141 README: immediate hook, intentional visual changes, clear Japanese subtitles, concrete examples, employee-reviewed manual publication. Prior summaries mention the user's `ChatGPT×Excel時短術16コマ絵コンテ.png`, but this cycle did not obtain or inspect the original v33 MP4. No claim of matching its visual quality.

**Not verified:** independent Japanese ASR and semantic/timing alignment, inherited audio's commercial rights, real phone playback, employee approval, actual GitHub Actions billing. No automatic posting.
