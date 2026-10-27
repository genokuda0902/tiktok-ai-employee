# cycle906 | Collision-safe save flow (REVIEW ONLY)

- Baseline: mounted cycle905 private MP4. Previous cycle905 improved scene06 NG/OK teaching.
- Unique change: scene07 (17.4–20.3s) now uses a native, collision-checked three-step save flow: name → purpose/conditions/format → human check.
- Avoids inherited scene07 overlapping captions/labels; overlays 87 RGBA frames at x=0, y=300 on 1080x1920/30fps video. 10 genres have separate synthetic text.
- No real UI, personal identifiers, claims, account access, or posting. The UI explicitly says it is fictional.
- Local MP4 (not stored in public GitHub): 23.033s, H.264 1080x1920, AAC 48kHz, 691 frames, inherited Japanese voice/subtitles unchanged. Technical QA 14/14; unit tests 7/7.
- To render the synthetic overlays: `python experiments/cycle906/save_flow_readable.py --genre ai_work --output /tmp/cycle906-frames`
- To overlay on an **authorized local baseline** (do not commit source media): FFmpeg overlay input setpts offset 17.4s, x=0 y=300, audio stream copy. The original baseline is not bundled because its commercial rights remain unverified.
- CI tests only geometry and synthetic frame generation. The completed private MP4 and Japanese glyphs are tested locally, not in CI.
- Independent ASR, reference v33 original, source asset rights, smartphone hardware playback, and employee approval remain unverified.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, no automatic posting, no paid service.
