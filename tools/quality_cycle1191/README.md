# Cycle1191: safe-area soft scene cuts (review only)

Distinct from cycle1189's UI save cursor: seven hard cuts are softened over six frames (~200ms) in the upper story region only. Narration captions/footer remain at original timecodes. The original AAC audio bitstream is copied, not synthesized or altered. Generic for ten genre IDs, but only AI/workflow has a completed private sample MP4.

Source cuts: frames 94, 168, 250, 330, 412, 499, 575, at 30fps. The first output attempt was truncated to 670 frames by ffmpeg -shortest; this was removed, and the final local 675-frame video fully decodes. This failure/recovery is documented to avoid repeating it.

Run locally: `python tools/quality_cycle1191/soft_scene_cut.py INPUT.mp4 OUTPUT.mp4 --genre ai`. Auto detection is available via `--auto-detect` but must be manually reviewed. Requires free ffmpeg, opencv-python-headless, numpy.

Local private source QA: 1080x1920, 30fps, 675 frames, 22.5s, H.264, AAC 48kHz. All seven first-frame cut jumps in story area reduced; mean reduction 89.7%. Sampled caption-region MAE max 1.615/255 due to re-encoding; no semantic ASR was performed. Audio stream hash equal. Full decode PASS. No reference v33 original, phone playback or commercial rights approval available.

CI uses a synthetic two-second sample, **not** the final private 22.5s video. No personal data, user footage, or third-party licensed material is committed. Human review only, publication NOT approved. No automatic posting, paid services or merging.
