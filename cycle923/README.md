# cycle923 — subtitle-safe editorial scene wipes (REVIEW ONLY)

Distinct from cycle922's single-scene cinematic paper rendering and parallel cycle922 speech timeline: this adds a nine-frame **directional wipe at each of seven existing scene cuts**, with a narrow color seam, while keeping the inherited caption and footer pixels below y=1460 unchanged at source-frame level. No invented business results, new media, TTS or ASR claims.

The renderer is reusable for **10 genre accents** (`ai_work`, `finance`, `health`, `travel`, `beauty`, `cooking`, `education`, `career`, `lifestyle`, `technology`); only the `ai_work` MP4 is produced in this cycle. Media is private and never checked into public GitHub. GitHub CI checks only pure-Python geometry, palette, and fail-closed policy. Local QA is separate and includes full MP4 decode, stream properties, audio ADTS hash equality, and visual/caption region comparisons.

## Local reproduction

```bash
python cycle923/src/scene_wipe.py \
  --source /private/cycle922_CINEMATIC_SAMPLE_PAPER_JP_HUMAN_REVIEW.mp4 \
  --output /private/cycle923_EDITORIAL_WIPES_JP_HUMAN_REVIEW.mp4 \
  --expected-source-sha 833a2a4f94aaa2ed454da179ec74fa9bd2d0b3972804be77f3a5b24a9819a515 \
  --report /private/cycle923_render.json
python -m unittest discover -s cycle923/tests -p 'test_*.py' -v
```

Requires local ffmpeg, OpenCV and NumPy for actual MP4 generation; CI tests require only Python stdlib. Source video and inherited audio are not licensed/approved for publication by this workflow. Do not auto-post, merge, contract for paid services, or assert v33 quality parity. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
