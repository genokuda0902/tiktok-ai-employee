# Cycle895 — Native Japanese document proof
Previous cycle893 improved voice-priority audio. This cycle improves scene03 (6.20–8.85s) by rebuilding a sample weekly-report card as **native 1080×1920 text**, progressively highlighting its three rows. No external imagery, personal data, paid service, or auto-posting.

Use Python/Pillow and Noto Sans CJK:
python experiments/cycle895/src/native_document_reveal.py --output overlays
python -m unittest discover -s experiments/cycle895/tests -v

The review MP4 is generated locally by compositing the 3 PNG states over the original cycle893 video (FFmpeg). The original MP4 is not committed. The original AAC bitstream and burned-in subtitles are retained. Local technical QA 11/11 PASS, local unit tests 6/6 PASS; the CI checks renderer tests only. Independent Japanese ASR semantic validation, v33 original, rights, smartphone playback, employee approval: UNVERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Manual posting only after approval.
