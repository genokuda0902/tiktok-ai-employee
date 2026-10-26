# cycle868 — Japanese phrase-highlight captions (review only)

Difference from cycle866: unified subtitle surface across photographic and browser-demo scenes, with 24-beat per-character progressive highlighting. It is an **approximate visual effect**, not verified phoneme alignment.

Ten supported genre IDs match the existing cycle865 genre categories. Run locally: `cd review_cycles/cycle868 && python -m unittest -v test_caption_core.py`. The generated .ass requires FFmpeg libass and Noto Sans CJK JP. Video renderer and full MP4/QA are supplied as a separate review ZIP; **no media uploaded to GitHub**.

Local output: 1080x1920 H.264 30fps, 23.033s, 691 frames, inherited AAC 48kHz elementary stream bit-identical to cycle866. Full decode and 14 QA checks PASS locally. Source imagery is not newly generated; pixel fidelity above caption region PSNR 42.02–46.07dB in four samples.

Unverified: original reference-video parity, Japanese speech naturalness and phoneme/semantic alignment, physical mobile playback, source media rights, employee approval, Actions billing. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, no paid service, no auto-post.
