# cycle1539 review-only caption safe-area
Uses an existing **approved** MP4 and Japanese SRT. Does not synthesize narration.
```bash
python render.py input.mp4 captions_ja.srt review.mp4
python -m unittest discover -s . -p 'test_*.py' -v
ffmpeg -v error -xerror -i review.mp4 -f null -
```
Changes: 1080x1920 upscaled encode; dark 960x230 caption contrast panel; burned-in Japanese subtitles; preserve AAC and mov_text selectable subtitle. Output resolution is upscale, NOT additional source detail.
Local sample: 12s H.264/AAC/mov_text; decode PASS; 3 local checks PASS. Original sample source is NOT committed. Japanese spoken narration absent; effects-only AAC. No rights approval, no phone playback, no posting.
Reference v33 original unavailable; not equivalent. Do not merge or post without approval.
