# cycle829 — reusable Japanese prompt template (REVIEW ONLY)

## New, non-repeated improvement
After cycle828's recommendation-to-action scene (16.150–19.383s), cycle829 improves **19.383–22.617s (97 frames)**, the next "save reusable instructions" scene. Replaces the prior static generic UI list with an original warm desk / paper notebook visual, three timed save/reuse states, gentle camera push-in, and a specific fictional Japanese prompt. Preserves the original scene title and 3-line subtitles, original 25.833-second Open JTalk narration, and all 775 frames. Ten genre palettes and nine unit tests; complete MP4 produced for ai_work only.

No actual app account, customer data, performance claim, real screenshot, external photo, unlicensed music or public posting. Source video is never committed; CI reconstructs it from the existing synthetic assets and offline Japanese narration.

## How to reproduce
\`\`\`bash
python -m unittest discover -s quality/cycle829 -p 'test_*.py' -v
python quality/cycle829/save829.py --source cycle828_AI_WORK_APPLY_ACTIONS_JAPANESE_REVIEW_ONLY.mp4 --output cycle829_AI_WORK_SAVE_REUSE_JAPANESE_REVIEW_ONLY.mp4 --genre ai_work --report qa829.json
ffmpeg -v error -xerror -i cycle829_AI_WORK_SAVE_REUSE_JAPANESE_REVIEW_ONLY.mp4 -f null -
\`\`\`

The CI workflow rebuilds the source via cycles 823/819/825/826/827/828 and then runs this exact cycle829 source and tests, checks H.264 1080×1920 30fps 775 frames + AAC 48kHz, source/target AAC packet identity, non-silent audio RMS, full decode, original script/caption parity 8 scenes/24 states, and saves a 7-day review-only MP4 artifact. The QA explicitly does **not** claim ASR transcription or word-level timing.

## Prior evidence and limitations
- Prior cycle828 final CI: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40141656228 (SUCCESS).
- Latest main inspected on 2026-10-25: 18e084c38db0dc55db7dfc0532b9451b1167f2aa; cycle829 stacks on unmerged PR #148, other open PRs not merged.
- TikTok市場分析 and TikTok動画研究: accessible past summaries indicate 0–1.5s hook, 15–25s short clips, visual demonstrations, short captions, safe area, human approval. Full historical task/chat bodies inaccessible.
- User's 16-panel AI時短ラボ storyboard inspected directly: robotic character, people, spreadsheet demo, vivid cinematic scenes and multiple cuts. Reference v33 original MP4 inaccessible, no direct comparison.
- Still unverified: audible Japanese pronunciation/semantics, exact word-level subtitle alignment, mobile playback, publication rights, employee approval, reference-quality equivalence.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No automatic publication, merge, paid services or contracts.

## Next
Independently inspect audible Japanese speech vs subtitles and on-device playback; then replace remaining generic UI scenes with rights-approved image-led or real workflow demonstrations. Do not repeat cycle829 save/reuse overlay.
