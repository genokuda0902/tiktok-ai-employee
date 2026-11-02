# cycle1134 — proportional evidence bars (REVIEW ONLY)

Previous cycle1132 added three original non-musical SFX cues. This independent cycle adds **animated proportionally accurate micro-bars** to the existing, fictional spreadsheet proof cards in scene 06 (14.30–17.30s), without covering numerical values or burned-in Japanese captions. Values are verified against the 3 fictional month rows: A=12+16+18=46, B=8+9+12=29, total=75. Bars share the same 75 denominator, fill sequentially, and do not claim business performance. The video is NOT approved for publication.

The engine is reusable across ten genres (ai, business, money, learning, health, food, travel, beauty, career, life), but requires an audited, genre-specific private manifest with exact source SHA, row-level numeric evidence, scene timestamps and an upper-content ROI. Fail-closed source policy prevents use of unapproved source material. The fixed bar geometry targets this specific three-card review layout; other genre layouts require audited ROI/layout adaptation, not blind reuse. The source video, private manifest and real MP4 are NOT committed.

Run locally with Pillow>=10,<12, FFmpeg and FFprobe:

    python quality/cycle1134/proof_share_bars.py --source /private/cycle1132.mp4 --output /private/cycle1134.mp4 --manifest /private/manifest.json --report /private/qa1134.json
    python -m unittest discover -s quality/cycle1134 -p 'test_*.py' -v

Manifest fields: policy=HUMAN_REVIEW/PUBLICATION_NOT_APPROVED, asset_approval=private_review_only, source_sha256, genre, scene_start, scene_end, values (A,B,total), monthly_rows (source pairs), roi (x,y,width,height). Source is H264 1080x1920/30fps and AAC Japanese 48kHz. The source audio is **stream copied** (bit-identical AAC); video is re-encoded, so pixels outside ROI may have small compression differences. Synthetic-media CI is separate from real-MP4 local QA.

Research summaries consulted: hook in first 1.5s, short purposeful scenes, real evidence, Before/After, legible Japanese captions and manual approval. User 16-panel storyboard directly inspected: robot/person, ChatGPT/Excel, graph, Before/After, CTA, 36s. Current 8-scene/23s review video still differs substantially. Full research transcripts and original v33 MP4 not available. Japanese independent ASR/caption semantic sync, rights, smartphone playback and employee approval are NOT verified. Never merge, post or distribute without approval.
