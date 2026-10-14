# cycle579 | Japanese CG disclosure footer (HUMAN_REVIEW)
Previous cycle578 mastered the audio. This cycle changes the visual footer: English VISUAL NOTE -> 学びメモ, adds CGイメージ and a Japanese source-transparency disclosure, while preserving the hero and burned-in subtitles. 10 genres share one renderer.

Requirements: Python 3, Pillow, ffmpeg, Noto Sans CJK font. Put the cycle578 MP4 at `quality/cycle579/assets/cycle578.mp4` or pass `--source`.
Run: `python quality/cycle579/build_cycle579.py --source /path/to/cycle578.mp4`
Tests: `python -m unittest discover -s quality/cycle579/tests -v`
Output: `quality/cycle579/output/cycle579_JA_TRUST_FOOTER_HUMAN_REVIEW.mp4`.

The source MP4 is intentionally not committed due to binary size and inherited media-rights uncertainty. Reproducible assets and real MP4 are provided separately in the conversation artifact ZIP. No approval to publish, no automated posting, no paid services, no merge. Narration language/naturalness and word-level caption sync require human review.
