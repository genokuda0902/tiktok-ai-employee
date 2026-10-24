# cycle818 | Japanese-first editorial cleanup (REVIEW ONLY)

Date: 2026-10-24 JST. Draft PR #129, based on parallel PR #128 (unmerged). main checked at 18e084c38db0dc55db7dfc0532b9451b1167f2aa.

## Distinct improvement
cycle817 (root-cause animation, PR #127) retained English scene headings, "BUSINESS / FIELD NOTES", and two lines of English production/debug labels in all 8 scenes. cycle818 replaces the top metadata, eight section headings, and debug footer with Japanese labels; it preserves the primary Japanese headlines, 8-scene content, and inherited AAC stream. This is a localization and editorial clarity improvement, **not** a claim of cinematic v33 equivalence. It does not repeat PR #128's audio loudness or source-image re-rendering.

## Reproduction with local approved assets
Requires free Python Pillow, FFmpeg, Noto Sans CJK. Source is a locally approved 1080x1920, 30fps video with audio. Do not commit private source video or inherited audio.

    PYTHONPATH=quality/cycle818 python -m unittest discover -s quality/cycle818 -p 'test_*.py' -v
    python quality/cycle818/localize.py --source /private/review817.mp4 --output /private/review818.mp4 --genre sales_business

The script validates 10 genre names/colors, creates eight opaque localized overlays, muxes the output with audio stream copy, and writes qa818.json. Other genres are configuration-ready but not individually rendered as complete videos.

## Local evidence
- Tests 7/7 PASS.
- MP4 1080x1920, H.264 30fps, 718 frames, 23.933333s; AAC 48kHz mono.
- Full audio/video decode PASS.
- Input/output AAC packet MD5 both 8d0baabf50866471846346e7159046e2.
- Output SHA256: 2fb8c40ae869e67844951dc7a17d8b8952faae01a820b3697799cb60b86b3a9f.
- At 0.5s, changed header/scene-label mean pixel difference 9.91, content 1.24, footer 14.13; difference includes lossy video re-encode.
- Actual private MP4 is only in the ChatGPT conversation sandbox, NOT a GitHub artifact. CI artifact is a separate synthetic tone-only MP4.
- Japanese speech content and word-level caption alignment NOT independently verified. Rights, real-device playback and employee approval NOT verified.

## Research & reference access
- Past TikTok市場分析 and TikTok動画研究 summaries were consulted; full transcripts inaccessible.
- User 16-panel ChatGPT×Excel storyboard available via conversation file search; it shows cinematic robot/office, live UI demo, Before/After and CTA. Do not re-use confidential robot assets.
- Original v33 MP4 unavailable in this runtime. GitHub recovery record documents SHA256 b190414f6e3e191cea184d80e28ca7a3404d37a3f212eb94964f95b7674ea712 and 31.553333s / 512x910, but no direct frame comparison was possible.

## Next priority
1. Independently check Japanese voice vs caption meaning with licensed offline ASR/word alignment or human reviewer.
2. Recover approved source stills for PR #128's clean-source renderer; avoid repeated MP4 re-encoding.
3. Improve actual image-first visual storytelling, check source rights, v33 comparison and smartphone playback.
4. No posting, merging, charging, or employee delivery without approval. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
