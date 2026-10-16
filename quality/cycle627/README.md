# cycle627 — Verified-result animation (REVIEW ONLY)

Baseline: cycle626 four-cell selection, local MP4 SHA is recorded in the attached QA package. Main remains unchanged.

## Difference
Replace frames 126–185 (4.2–6.2s). Previous video temporarily showed a large intermediate numeric result (420) without explaining that the calculation was in progress. New segment displays '検算中…' without a numeric total, then displays all four source values (120,150,200,250), their formula =SUM(B2:B5), and final verified 720. Synthetic demo; not real ChatGPT/Excel screen capture.

## Reproduction
Requires Python 3, Pillow, FFmpeg and Noto CJK fonts. Download the separately shared baseline cycle626 MP4. From this directory:
```sh
python -m unittest -v test_verified_result_scene.py
python verified_result_scene.py --baseline /path/to/cycle626_four_cell_selection_REVIEW_ONLY.mp4 --output cycle627_verified_result_REVIEW_ONLY.mp4
ffmpeg -v error -i cycle627_verified_result_REVIEW_ONLY.mp4 -f null -
```
No user video, voice, private files, or copyrighted reference material is committed. Only original code and tests are committed.

## Release gates
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Existing BGM is inherited, not a new Japanese voice; voice-caption alignment is NOT verified. 10 genres share numeric-proof validation but only AI-work has an MP4. Reference storyboard inspected; original v33 and other reference MP4 raw-byte materialization was denied in this run. Do not merge, auto-post, or distribute for publication.
