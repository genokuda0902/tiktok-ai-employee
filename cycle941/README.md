# cycle941 — template reuse, three micro-shots (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. A new distinct change from cycle940: scene07 (frames 522–586, 17.4–19.57 s) replaces the small static template with three distinct, large native-resolution views: save a prompt pattern, reuse it for three tasks, and verify manually. Inherited Japanese captions and AAC audio are preserved. Frames 587 onward retain the prior early unapproved outro, so scene08 narration is not paired with template imagery. All imagery is synthetic, fictional, and not an actual ChatGPT recording. This is a reimplementation, not original v33.

10 genre presets are included, but the full MP4 is rendered only for ai_work. All outputs remain private; do not commit media or confidential source. No automatic posting, no merge, no paid API, no release without employee approval.

Local reproduction with a privately authorized source, FFmpeg, Pillow, pytest, free Noto CJK fonts:

python cycle941/src/reuse_story.py --source /private/cycle940_FINISHED_EXAMPLE_FOCUS_REVIEW_ONLY.mp4 --output /private/cycle941_REUSE_STORY_REVIEW_ONLY.mp4 --tmp /private/cycle941_tmp --genre ai_work --expected-source-sha 4169c540bb354992a19705fb60fe4cb6da14fc4f857cb8c7d976b9667161c4de

python -m pytest -q cycle941/tests/test_reuse_story.py

CI tests source and synthetic frames, not the private actual MP4. Original v33 MP4, independent Japanese ASR/caption semantic sync, source publication rights, phone playback and employee approval remain unverified. Research: accessible summaries of TikTok市場分析 / TikTok動画研究 and user's 16-panel storyboard, not complete original chats.
