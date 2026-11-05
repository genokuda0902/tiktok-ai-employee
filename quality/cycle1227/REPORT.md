# cycle1227 — evidence steps, review only

Previous cycle1226 added an opening hook. This cycle adds three timed Japanese evidence steps at 7, 9, and 11 seconds, ending at 14 seconds. The implementation is genre-neutral and does not load new assets.

Local command: `python render.py SOURCE.mp4 OUTPUT.mp4`.
Local tests: `python -m unittest -v test_render.py` — 3 passed.
Local MP4: 23.033333 seconds, H.264 1080x1920, AAC stream, 708155 bytes. FFmpeg full decode passed.
Original audio is copied, not newly generated. Japanese narration semantics, captions-to-audio sync, rights, and phone playback are NOT verified. Source review MP4 is not committed due to approval gate.
Reference v33 original and the full TikTok research chats are inaccessible. This is a reimplementation, not recovered v33 code.
Do not merge or post without human rights and quality approval.
