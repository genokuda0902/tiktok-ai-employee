# cycle853: layered photo depth (review only)

This branch contains the **shared ten-genre motion core** and CI unit tests.
The actual Japanese-narrated 1080x1920 review MP4, photos, inherited AAC
narration and full Pillow/FFmpeg compositor are supplied only in the private
cycle853 review ZIP. They are **not** uploaded to this public repository.

## Distinct change from cycle852

- cycle852: uncropped source-safe photo, static foreground, pale editorial page.
- cycle853: blurred full-screen photographic backdrop moves by 16/12 pixels;
  a sharp, uncropped source-safe foreground photo moves independently by
  23/12 pixels. Titles and 24 burned Japanese subtitle beats stay fixed.
- Foreground source scale is capped at 1.12x. Decorative background can be
  upscaled only because it is strongly blurred.
- 8 scenes; 7 dissolves; 691 frames at 30fps (23.033s); audio stream reused
  from cycle852 and locally decoded PCM hash checked identical.

## Run core tests

```bash
PYTHONPATH=quality/cycle853 python -m unittest discover -s quality/cycle853 -p 'test_*.py' -v
```

CI tests **only this common core**. It does not generate the final MP4.
The local full compositor additionally runs source-asset and MP4 decode tests.

## Limitations / publication gate

The eight inherited photographs are 534–822 pixels wide, not independent
high-resolution source photos. Rights, model releases, narration pronunciation,
precise speech-caption alignment, reference-video comparison, smartphone
playback, actual retention impact and employee approval remain unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
No auto-posting, public media upload, paid services or merge is authorized.
