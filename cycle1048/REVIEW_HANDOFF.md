# cycle1048 — Before/After evidence montage (private review only)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. This is a reimplementation, not the original v33. Do not post, merge, or distribute without rights and employee approval.

## Change from cycle1046

The previous cycle1046 decluttered the task-list scene (2.9–5.8s). This cycle replaces **only frames 609–672 (20.300–22.433s)** with a split BEFORE/AFTER demonstration: old repeated task → AI prompt → manual Calc check. The montage uses screenshots extracted solely from the private source MP4, not newly recorded operations. It explicitly labels fictional data, simulated UI, and unmeasured time savings. The existing 8 Japanese burned captions below y1460 and original AAC track remain unchanged.

## Reproduction (private media must remain outside GitHub)

Source: private cycle1046 MP4 SHA256 0208046ebc210ceb4bfda0ede5005a46cf888510cb7c8326d1f3fb10be5cbbbe.

Install offline FFmpeg, Noto CJK fonts, Python Pillow; for independent all-frame QA install OpenCV and NumPy.

Run:

    python -m unittest discover -s cycle1048/tests -p 'test_*.py' -v
    python cycle1048/source/before_after.py --source /PRIVATE/cycle1046.mp4 --source-sha 0208046ebc210ceb4bfda0ede5005a46cf888510cb7c8326d1f3fb10be5cbbbe --output /PRIVATE/cycle1048_REVIEW_ONLY.mp4 --review-only --report /PRIVATE/render_report.json
    python cycle1048/source/verify_video.py /PRIVATE/cycle1046.mp4 /PRIVATE/cycle1048_REVIEW_ONLY.mp4 /PRIVATE/qa.json

Do not commit source/finished MP4, screenshots, WAV, private manifest or other unapproved media. All ten genre color configurations are testable without private assets; **only ai_work has a permitted local review source**, the other nine fail closed.

## Verified private local output (2026-10-31 JST)

Output SHA256 edfd43e7248a15dc3628e23fc7ab3f2e84b9875c1d8922a03bdc250a17cd411a.
H.264 1080x1920 30fps, 691 frames / 23.033333s; AAC 48kHz, ADTS audio payload unchanged (ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e).
Full video/audio decode PASS, 9/9 local unit tests PASS. Protected subtitle ROI maximum MAE 0.5926/255 across 691 frames; unchanged upper-picture maximum MAE 0.729/255; changed upper-picture mean MAE 63.1882/255 across 64 frames. Audio signal mean -19.3dB, peak -3.3dB. These are technical checks, **not independent Japanese transcription, pronunciation, or semantic caption synchronization**.

## Research and provenance

Accessible summaries of the previous 「TikTok市場分析」 and 「TikTok動画研究」 favor 1–1.5s hooks, 15–25s videos, purposeful cuts, true UI, Before/After, readable captions, and human review. The user's 16-panel/36s storyboard was opened directly in Library. Its cinematic 3D robot, people and UI are still far beyond this 8-scene/23s implementation. Full original research chat transcripts and original v33 MP4 were not accessible. PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md require image-first, rights approval, and human posting; natural animated robot is out of scope.

GitHub Actions only tests the generic source and **synthetic one-second A/V**; the full private MP4 is not in CI. Speech-to-caption meaning, v33 visual comparison, rights, smartphone playback, employee approval, retention and actual Actions charges remain unverified. No paid service, no automatic posting, no merge.
