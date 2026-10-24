# cycle811: Remove action-card text ghosting (REVIEW ONLY)

Previous cycle810's scene 6 showed overlapping old and new text around 16 seconds. This is a visual defect, not a speech-quality claim. The fix replaces the action-card rectangle with a **fully opaque** 850×600 card at (115,730), frames 445–538 only; the rest of the video and Japanese subtitle panel remain unchanged. Three action rows are staged without overlap. All ten genres use the same validated layout.

Source media: prior private-review cycle810 MP4; do **not** commit/upload inherited voice, images, or resulting MP4 to public GitHub. CI uses a wholly synthetic color+tone input. No auto-post, merge, or release. This is a reimplementation, not recovered v33 code.

Research provenance: Prior summaries of TikTok市場分析 and TikTok動画研究 were consulted, but full task/chat transcripts remain unavailable. User-supplied 16-panel ChatGPT×Excel storyboard was inspected directly; original v33 MP4 was unavailable. Compared to the storyboard, this output still lacks cinematic/photographic imagery and genuine Excel operation footage. It is not approved for posting.

Run locally with free Pillow and FFmpeg:

```
PYTHONPATH=quality/cycle811 python -m unittest discover -s quality/cycle811 -p 'test_*.py' -v
python quality/cycle811/action_panel.py --source cycle810_RESULT_GROWTH_REVIEW_ONLY.mp4 --output cycle811_REVIEW_ONLY.mp4
ffmpeg -v error -xerror -i cycle811_REVIEW_ONLY.mp4 -f null -
```

Unverified: independent Japanese ASR, speech naturalness, semantic caption sync, source rights, smartphone playback, employee approval and direct v33 video comparison. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
