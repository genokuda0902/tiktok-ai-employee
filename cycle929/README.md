# cycle929 — integrated human-review story (private video)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Reimplementation; not original v33. No automatic posting, publication, merge, or paid services.

## Difference from prior unmerged work
- cycle928 PR #311: three-beat first-scene hook, based on cycle926.
- cycle927 PR #310: review gate on scene05, not present in the private cycle928 PR #311 MP4.
- **cycle929**: on top of the actual cycle928 PR #311 private MP4, rebuilds scene05 (87 frames, 11.6–14.5s) as an explicit three-stage unapproved verification gate, and scene08 (82 frames, 20.3–23.033s) as a clear one-task habit + **未承認** employee-manual-post-only reminder. Preserves all 691 frames of inherited Japanese captions in y>=1460 and the AAC bitstream. Distinct from cycle925's CTA: this is a status-safe verification narrative in the last scene, not a generic follow button. No approval is fabricated.
- 10 genre presets, one AI-work full MP4 tested. Does not integrate parallel PR #312 audio meter.

## Local private reproduction
Install Pillow==11.3.0, Noto CJK fonts and ffmpeg. Use only a rights-reviewed private source file, not repo content:

~~~bash
python cycle929/src/integrated_review_story.py \
  --source /private/cycle928_ANIMATED_HERO_JP_REVIEW_ONLY.mp4 \
  --expected-source-sha 9a05a5e6fec5c878409cac60e7769867237701ded0736240ebca65f762693b88 \
  --output /private/cycle929_INTEGRATED_HUMAN_REVIEW_ONLY.mp4 \
  --workdir /private/cycle929-work --genre ai_work
python -m unittest discover -s cycle929/tests -p 'test_*.py' -v
~~~

Local output SHA256: 1c538feccafd1d9d3339449a549e91c42b1e2415f0adb21b9adeac6ca85c7a1b; H.264 1080×1920 30fps 691 frames/23.033s, inherited AAC 48kHz bitstream identical. Local full decode and technical QA PASS; 12 tests PASS. Private MP4 is shared only in ChatGPT conversation, NOT committed or uploaded to public GitHub. CI tests synthetic rendering, NOT this private MP4.

## Reference and remaining gates
Original user storyboard ChatGPT×Excel時短術16コマ絵コンテ.png directly inspected (16 panels, 36s). Accessible past TikTok市場分析 / TikTok動画研究 summaries consulted; original full transcripts and original v33 MP4 unavailable. This 8-scene/23s synthetic tutorial does not match original cinematic 3D robot/human footage or genuine Excel/ChatGPT operation. Japanese spoken words, naturalness and semantic/word-level caption sync, rights, smartphone playback, employee approval and actual Actions billing remain unverified. No merge, paid contract, public upload or posting.
