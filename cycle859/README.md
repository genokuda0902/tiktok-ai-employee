# cycle859 | Review-only time-progress bar

**Difference:** adds a 12-pixel watch-progress bar that fills continuously across 691 frames / 23.033s; unlike cycle858 PR #204's six beat-aligned detail crops, this change preserves the 8 original slide images and 24 Japanese subtitle states.

The code supports 10 genre colors. It copies the audio stream from a private source MP4 and never uploads, posts, purchases, merges, or publishes the original media. Private Japanese source media and completed review MP4 are intentionally not committed to GitHub.

Run local tests: `python -m unittest discover -s cycle859 -p 'test_progress_core.py' -v`

Run on an approved local review file: `python cycle859/render_progress.py --source SOURCE.mp4 --output REVIEW.mp4 --genre ai_work`

Source reference: cycle857 photo route (6 inherited AI photos + 2 original vector illustrations). This does **not** solve the 8 independently produced high-resolution photo goal. No claim of retention gain, reference-video parity, human-approved Japanese pronunciation/subtitle semantics, asset rights, phone playback, or employee approval. CI synthetic smoke is not a substitute for finished-MP4 local QA.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Manual posting only after employee approval.
