# Genre-independent portrait editor v1

Status: **rendering foundation, NOT a universal high-quality video generator or publish-ready system**. `build.py` is committed source. Actual visual tests were run in two genres (`ai_work`, `cooking`) on 2026-09-18: both 6.0 s, 720x1280, 3 scenes, silent visual tests. Neither proves visual quality or post readiness. Assets/videos are not in GitHub.

## Dependencies
Python 3, Pillow, ffmpeg and ffprobe; NotoSansCJK-Bold at `/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc` if using titles. Run: `python build.py --config /path/to/genre/config.json`.

## Configuration example
```json
{
  "genre":"cooking",
  "mode":"visual_test",
  "asset_approval":"approved",
  "output":"visual_test.mp4",
  "scenes":[
    {"type":"image","asset":"opening.jpg","seconds":2.0},
    {"type":"video","asset":"demo.mp4","seconds":5.0},
    {"type":"image","asset":"ending.jpg","seconds":2.0}
  ]
}
```
Assets resolve relative to config file. `mode: visual_test` is the only mode permitting missing narration. For a release candidate add a real, licensed `narration` file with duration matching sum of scene durations (within 0.6 s) and change `mode` to `review`. `asset_approval` is a human assertion, not automatic clearance. The engine refuses non-portrait assets, mismatched image canvas, video non-9:16, absent narration for non-test mode, missing files and short source clips. It creates `*_qa.json` including checksum and human review gates. Video audio is stripped per scene; narration must be supplied as a separate synchronized track. No claims of automatic speech/visual alignment.

## Creative direction and safety
Native 9:16 images only; no face zoom, center crop, or black-bar workaround. Full-frame hero composition must be designed before rendering. Hook -> proof/demo -> conclusion/CTA. Use only original/approved images, fictional non-identifiable example data, and separately licensed narration/music. Do not upload confidential screenshots, reference video bytes, or client information to GitHub. Inspect frame 0, every scene midpoint, last frame, and phone-size preview; check TikTok UI safe zone, text accuracy, content rights, substantiation of numeric claims and audio sync. Human approval before publishing. No automatic trend discovery, asset generation, narration generation, distribution, or TikTok posting in v1.

## Verified test outputs (session-local only)
- AI-work visual test: 720x1280, 6.0 s, 3 scenes, silent, SHA256 `01f7998324bac8c3e97c5b83b42baf0479c11ac75821d1e9e7e28f51f5201f11`.
- Cooking visual test: 720x1280, 6.0 s, 3 scenes, silent, SHA256 `df14a149fb67f54868008c3aa663feaa10d099984ce7ee77b827ee3a6b0369db`.

## Next release gates
1. Integrate a properly licensed, portrait-first visual asset generation/selection service and approved genre-specific storyboards.
2. Add synchronized narration generation and per-scene timing, music rights management and manual editorial checks.
3. Make automated scene contact sheets and safe-zone checks; test real image/video footage in 3+ genres, not only flat mockups.
4. Persist approved media in durable storage and test clean-environment reproducibility; GitHub contains source and docs only.
