# cycle929 — Scene keyword ribbon (review-only)

This cycle improves editorial information hierarchy with a discreet, animated eight-scene keyword ribbon. The existing narration and burnt-in captions remain untouched. This is distinct from cycle928's audio-amplitude-driven header meter. The ribbon is scene-timed, **not word-level ASR synced**, and does not prove narration/caption semantic consistency.

## Reproduce

Requires Python, Pillow, FFmpeg and a separately obtained private source MP4:

```
python cycle929/src/keyword_ribbon.py --source /private/cycle928.mp4 --output /private/cycle929.mp4 --genre ai_work --expected-source-sha <sha256>
python -m unittest discover -s cycle929/tests -p 'test_*.py' -v
```

Ten genre accent palettes are supported; only ai_work was fully rendered as MP4. The private source and completed MP4 are not committed. Local MP4 verification: 691 frames, H.264 1080×1920 30fps, 23.033 seconds, AAC 48kHz bitstream preserved; eight scene badges present; caption/header regions unchanged within re-encoding tolerance. 14/14 local QA, 12/12 unit tests. Source SHA256: `13f43b925201f65425623c2e730007ab4bebe3e6ff37edc668286c5c58d9a0a9`; output SHA256: `7fe622488252605a4e2dbf23d2c28f66b325ee4addb460a2ba549d7251145342`.

## Restrictions

No auto-posting, no paid API, no merging. Commercial rights to inherited source material, original reference v33 direct comparison, independent Japanese ASR, phone playback, Actions actual billing and employee approval remain unverified. CI tests only source code and synthetic images, **not the completed MP4**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Employee approval before manual posting.
