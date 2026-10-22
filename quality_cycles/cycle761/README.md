# Cycle 761 — original editorial scale slides

This branch builds on cycle760. Local output: 14.314s H.264/AAC, 1080x1920, 429 frames, 16 Japanese caption cues. Two fully original vector slides replace 2.033–3.900s: compact board -> highlighted CPU/MEMORY/I/O. Previous AAC packets are preserved exactly through a second muxing pass.

The committed render_final.py is the same reusable video muxer that generated the deliverable. The two generated PNG slides, full artwork generator, original input MP4, QA and full reproducible assets are in the delivered ZIP (not in this Git repository). CI generates synthetic stand-in PNGs/audio to exercise rendering and audio packet preservation; CI does NOT certify the actual final MP4, Japanese voice naturalness, or third-party rights.

10 genres share this time-bound overlay + frame-count-detection path. HUMAN_REVIEW; publication not approved. No merge, payment, or auto-post.
