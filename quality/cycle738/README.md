# cycle738: branded scene wipe (HUMAN REVIEW)
Improvement vs cycle737: seven opaque mint/navy left-to-right scene transitions, replacing abrupt scene cuts. We first tested a translucent soft wipe, but its caption ghosting was unacceptable. The opaque revision avoids superimposed Japanese text.
Source: cycle737 MP4 (14.3 seconds, 429 frames). Audio: stream copy, unchanged Japanese AAC. Output: 1080x1920, 30fps, H.264, 14.3 seconds.
To run: `python quality/cycle738/wipe.py input.mp4 output_HUMAN_REVIEW.mp4`.
Dependencies: Python 3, OpenCV, NumPy, ffmpeg.
To test: `PYTHONPATH=quality/cycle738 python -m unittest discover -s quality/cycle738 -p 'test_*.py'`.
For reuse across ten genres, change the cut frame numbers and theme colors to match each template.
Local QA: 12/12 checks; tests: 6/6. Source audio packet hash matched. MP4 exists as separate downloadable conversation artifact; it has NOT been committed to GitHub.
Limitations: no phone playback test, no human voice audit, no strict word-level caption synchronization, no source-asset rights audit, no employee approval. Manual posting only after approval. Do not merge or auto-publish.
