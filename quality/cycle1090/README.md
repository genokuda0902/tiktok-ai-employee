# cycle1090 — topic-continuous evidence-linked final CTA (REVIEW ONLY)

## Why this change
Previous cycle1088 ended with a generic habit-tracker checklist, disconnected from the earlier Excel calculation. This cycle replaces **scene08, frames 609–690 (20.300–23.033s)** with an evidence-linked preview extracted at 16.7s from the same source MP4, a staged 3-step reuse checklist, and the truthful fictional total **46 + 29 = 75**. The original Japanese narration and bottom subtitle are retained. The earlier scene05/06 animations are untouched.

## Local evidence (not uploaded to GitHub)
- Input: cycle1088 MP4 SHA256 f88f92cd900a8968088e03bea1f17730db67ac0853c54e6705458cab70551ca1
- Output: cycle1090 MP4 SHA256 0a0a653ac06a96a5445b3af138ad5018642b913096ff12123f080d3b78b694e7
- H.264 1080×1920 30fps, 691 frames / 23.033s; AAC 48kHz audio stream copied; full decode PASS.
- Audio ADTS SHA256 same for before/after: 76801539a721f7d968b5a8bf725fd056ab00de5a74bd09caf50112993c4aa2f8
- Bottom subtitle y>=1490 max per-frame mean difference (270x480 comparison): 0.2877 / 255. Changed scene mean difference 52.8371 / 255.
- 8 unit tests PASS, local synthetic 23s A/V smoke PASS. CI uses synthetic media; real MP4 is tested locally only.
- Japanese speech transcription, speech-caption semantic alignment, smartphone playback, asset rights and employee approval **NOT VERIFIED**.

## How to reproduce privately
Run from repository root with ffmpeg, Pillow, Noto CJK font:

    PYTHONPATH=. python -m quality.cycle1090.topic_continuity_cta --source /private/cycle1088.mp4 --source-sha f88f92cd900a8968088e03bea1f17730db67ac0853c54e6705458cab70551ca1 --manifest quality/cycle1090/synthetic_manifest.json --out /private/cycle1090.mp4

CI:

    PYTHONPATH=. /usr/bin/python3 -m unittest quality.cycle1090.test_topic_continuity_cta -v
    PYTHONPATH=. /usr/bin/python3 -m quality.cycle1090.topic_continuity_cta --smoke

The shared layout, 10 color presets, topic/step labels and preview crop/time are manifest-driven. Each other genre requires its own **approved, topic-relevant, sanitized source preview** and new human review; this cycle verifies only the AI-work completed MP4.

Research: prior TikTok市場分析/TikTok動画研究 summaries favor a first-1.5s hook, real operation proof, clear before/after, readable captions and manual posting. User 16-panel storyboard described ~36s with more cinematic scene variety. Original v33 MP4 **was recovered and directly inspected** from the user's Library this cycle: SHA256 b190414f6e3e191cea184d80e28ca7a3404d37a3f212eb94964f95b7674ea712, 31.553s, H.264 512x910, AAC 44.1kHz. Sampled reference frames at 1/4/8/12/16/20/24/28/31s: realistic person/robot shots around 4s and 31s, otherwise stepwise AI prompt / analysis / spreadsheet / before-after / reuse UI. Current cycle1090 is 23.033s, 1080x1920, 8 scenes and still lacks reference's photorealistic cinematic person/robot cut diversity and its ~8.52s extra runtime. User storyboard 16 panels (~36s) is a separate visual reference, directly inspected this cycle. Full original research chat texts remain inaccessible; this is **reimplementation**, not v33 reproduction.

Rights status is unverified; synthetic media and source audio remain private. Do not merge automatically, auto-post, or claim publication approval. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

Next: independent Japanese ASR for all 8 subtitle segments (especially 20.300s onward), then actual phone playback and rights/employee review. Do not treat signal presence or AAC equality as transcription verification.
