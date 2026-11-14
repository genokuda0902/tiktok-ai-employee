# cycle1452 review-only burn-in captions
Requires approved local source video (not committed). Run: python render.py --source SOURCE.mp4 --captions captions.srt --output review.mp4
Test: python -m unittest -v test_render
Locally validated: 1080x1920 H.264 13.5s, mov_text subtitle, no audio, full FFmpeg decode PASS; 2 unit tests PASS. Local MP4 SHA256 270f71fc818d51a6b644a791277b89470cc53167d80e4ecd719e71ff6f0d26e1. Original source video is not committed and GitHub-only reproduction is not possible. Never publish without rights, privacy and employee approval. Difference from cycle1451: burned-in captions visible even when player ignores optional subtitle track. Japanese narration remains absent. Reference v33 not directly available; no quality equivalence claimed.
