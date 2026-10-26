# cycle874 — Japanese sentence-paced subtitles (draft)

Improvement from cycle873: 24 rapid phrase captions are regrouped into 8 complete, two-line captions. The Japanese narration text is unchanged, mean caption dwell grows from 0.853 s to 2.560 s (3.0×), and each line is limited to 16 characters. Narration timing is inherited from cycle873; **phoneme-level synchronization is not verified**.

The local MP4 is 1080×1920, H.264 30fps, AAC 48kHz, 691 frames / 23.033 s, and is provided in the cycle874 review ZIP, not stored in GitHub. Local technical QA: 20/20; local pytest: 17/17. GitHub CI only tests the shared caption logic.

Run: `python -m unittest discover -s cycle874 -p 'test_*.py'`. To reproduce the MP4, use the separate local ZIP with slides, local synthetic browser demo, inherited audio, FFmpeg and renderer. No external AI service, automatic posting, paid service, or merge is authorized. Assets and narration rights, subjective voice quality, reference comparison, smartphone playback and employee approval remain **UNVERIFIED**. Publication status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
