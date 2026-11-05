# Cycle 1229 (2026-11-05 JST)
Prior: cycle1228 soft boundary fades. New: three time-gated Japanese visual labels at 4-6.8, 9-11.8, 15-17.8 seconds, located in lower-third safe zone. These are NOT verified speech-synchronized subtitles.
Local demo: 23.033333 s, 1080x1920 H.264, AAC copied from cycle1228, ffmpeg decode PASS, 4 local tests PASS. New narration NOT generated; Japanese speech content unverified. Reference v33 original unavailable. Asset provenance and posting approval unverified; REVIEW_ONLY, PUBLICATION_NOT_APPROVED.
Reproduce: python src/cycle1229_safe_captions.py input.mp4 output.mp4
Tests: python -m unittest discover -s tests -p 'test_cycle1229_safe_captions.py' -v
Do not merge or publish without human approval.
