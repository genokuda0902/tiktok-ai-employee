# Cycle486 review-only quality iteration

- Local preview: 20.166667 seconds, 1080x1920, H.264 30fps, AAC 44.1kHz.
- Synthetic sales values: 120, 150, 200, 250; total 720.
- Changes from cycle485: seven new UI shots showing source rows, formula, verification, chart result, Before/After and CTA.
- Preserve source animated 0-1.5s and 12-14s; all other visuals are drawn by Pillow. No copied logos or private imagery.
- Source audio is bitstream-copied from a separately supplied review-only MP4. Japanese speech and semantic caption sync are **not independently verified**. The labels are **not** a speech transcript.
- Original v33 source is not recovered. Do not publish, merge or distribute confidential material.
- Local reproduce with authorized source:
  `python quality/cycle486/render_cycle486.py --source /path/to/approved_prior_review.mp4 --out /tmp/cycle486_review.mp4`
- Test: `python -m unittest discover -s tests -p 'test_cycle486_storyboard.py' -v` and `python -m unittest discover -s tests -p 'test_cycle486_renderer.py' -v`.
- Dependencies: Python 3.11, Pillow, ffmpeg/ffprobe, NotoSansCJK fonts.
- CI validates code and scene gates; CI **does not** prove Japanese voice content, synchronization or v33-equivalent visual quality.
- Final status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; manual posting only after employee approval.
