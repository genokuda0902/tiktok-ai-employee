# cycle1111 — Japanese caption safe-zone (review only)

## Change from cycle1109
cycle1109 localized English UI chrome. This cycle **reflows all eight Japanese captions** into a left-aligned two-line 1080x1920 safe-area card, reserving rightmost 180px and bottom 270px for potential app overlays. These are template-specific engineering margins, **not a verified TikTok UI specification**.

Original eight-scene timing, image artwork, and narration bitstream remain unchanged. No automatic posting, paid APIs, or merges.

## Reproduction
Install FFmpeg with libass and Noto Sans CJK (free, offline):
```bash
python cycle1111/code/safe_caption.py INPUT.mp4 OUTPUT.mp4 --genre ai_work
python -m unittest discover -s cycle1111/tests -v
```

## Actual local MP4 QA
22.5s, H.264/AAC, 1080x1920, 30fps, 675 frames; full audio/video decode PASS. Audio AAC bitstream SHA256 identical to source. Eight caption regions differ by 29.117–35.222/255 mean, central image regions max 0.922/255 mean (8 sampled frames). Local 9/9 tests PASS. Ten genre names are configured; actual video was verified for AI-work only.

**Full MP4 is shared privately in conversation, not publicly committed to GitHub.** CI renders and fully decodes synthetic 2s media only. No claim of independent Japanese ASR, semantic audio/subtitle match, source asset commercial rights, actual phone playback, retention impact, reference v33 equivalence, or employee approval.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**
