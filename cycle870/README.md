# cycle870 — cinematic generated photo insert (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No automatic posting, merging, paid API, or external media upload.

## Distinct change vs cycle868

Scene 07 (frames **510–587**, 17.000–19.600 s) now shows a newly generated **photorealistic still** of hands at a laptop with a warm/cool twilight cinematic look. A slow 5.5% digital push-in and a single restrained 3-step Japanese glass panel replace the previous 2D illustrated laptop. The image is synthetic, **not real camera footage**. Ten genre presets share the same photo-motion renderer; only `ai_work` has been rendered to a private full MP4. Original 691-frame Japanese voice track and caption strip are inherited unchanged. This is a reimplementation, **not v33 recovery**.

## Provenance and reproducibility

Private source review video: `cycle868_ORIGINAL_ILLUSTRATED_CLOSER_JAPANESE_REVIEW_ONLY.mp4`, SHA256 `315b13067f0ec0518da7bb85837658be7f3b81bbbd41c12eae66d4b3f57dcee4`.

Private image: generated specifically for this review with OpenAI image generation on 2026-10-26; no identifiable faces or brand/logo requested. The image is not uploaded to this public repository. Publication rights of **all inherited materials** and final user approval remain pending. Source image is **941×1672** and slightly upscaled in the 1080×1358 scene insert; do not claim native 1080 source resolution.

Install local free requirements `pip install pillow`; requires `ffmpeg`/`ffprobe` and installed Noto CJK font. Run tests:

```bash
PYTHONPATH=cycle870 python -m unittest discover -s cycle870 -p 'test_*.py' -v
```

To render, supply your **private** source MP4 and image and write a private JSON manifest with exactly `REVIEW_POLICY` from `cinematic_photo_insert.py`, plus `source_sha256` and `photo_sha256`. Then:

```bash
python cycle870/cinematic_photo_insert.py --source /PRIVATE/cycle868.mp4 --photo /PRIVATE/generated.png --output /PRIVATE/cycle870.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/render_report.json
```

## Verification scope and limits

Check H.264 1080×1920 30fps, 691 frames, AAC48k, full A/V decode, audio elementary stream bit identity, all-frame protected subtitle strip and unchanged outside-scene regions. **CI only executes synthetic tests and synthetic AV**, never private voice/image. Original v33 MP4 and full `TikTok市場分析`/`TikTok動画研究` chats were inaccessible; prior summaries and the user 16-panel storyboard context were consulted. Japanese ASR semantic timing, voice naturalness, device playback, reference parity, inherited media rights, staff approval and actual GitHub Actions billing are **not verified**. Do not publish.