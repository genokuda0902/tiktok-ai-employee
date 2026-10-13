# cycle551: evidence-accurate subtotal renderer (review only)

New in cycle551: the previous 16.0–18.6s animation could show changing numbers under the heading 合計. Now every intermediate number is explicitly labeled 途中経過, and 検算OK / 合計 appears only after all four terms have been revealed. Inputs are synthetic 120+150+200+250=720.

Reproduction (requires Pillow, ffmpeg, ffprobe, Noto Sans CJK font and a **rights-reviewed** prior MP4 with existing audio):

```sh
python quality/cycle551/cycle551_renderer.py --base prior_review.mp4 --output cycle551_review.mp4
python -m unittest discover -s quality/cycle551 -p 'test_cycle551.py' -v
```

Source media are not committed. The 1080x1920/30fps/20s renderer copies the previous audio without new Japanese narration; its semantic alignment and voice quality are **UNVERIFIED**. Ten-genre math contracts are unit-tested; only AI work efficiency was video-rendered. No confidential footage, automatic posting, merge or publication approval.
