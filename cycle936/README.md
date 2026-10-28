# cycle936 — cinematic background depth focus (HUMAN_REVIEW)

## Distinct change
Prior cycle935 added three revision cues to scene06. This cycle adds a 0.5-second optical focus pull and selective background blur to scene03 (5.8–8.7s). The original Japanese report is not zoomed, avoiding ghost-text artifacts from the rejected cycle933 zoom experiment. Ten genre blur presets, protected paper glyphs, and caption/header safe zones.

## Verified local MP4 (not uploaded to public GitHub)
- Output: cycle936_DEPTH_FOCUS_JP_HUMAN_REVIEW.mp4
- SHA256: d284c11692cde78af184c53175ac49723a2f20ef66f0a236865008f73bdfe0ad
- Source: private cycle935 MP4, SHA256 e066328ed65250fe4c7f1cbc2c0f6e072ba577fbc770437066a2e02b5de5d7d3
- 23.033s / 691 frames / H.264 1080x1920 30fps / AAC 48kHz
- Full A/V decode PASS; AAC ADTS bitstream identical to source
- 87 scene03 frames processed; header and burned captions preserved except recompression noise
- At 7.2s: background Laplacian variance 42.91 -> 1.46; report ROI 599.20 -> 581.74; report pixel MAE 1.07/255
- Local synthetic unit tests 10/10 PASS; all ten genre presets validated
- These metrics verify a blur effect, not human preference or reference-video parity

## Reproduce with free tools
Extract frames 174–260 (inclusive) from the private source, process with the script, then overlay starting at 5.8 seconds:

```sh
ffmpeg -i SOURCE_REVIEW.mp4 -vf "select='between(n,174,260)',setpts=N/30/TB" -vsync 0 -start_number 0 frames_in/%03d.png
python cycle936/src/depth_focus.py --srcdir frames_in --outdir frames_out --genre ai_productivity
ffmpeg -i SOURCE_REVIEW.mp4 -framerate 30 -start_number 0 -i frames_out/%03d.png -filter_complex '[1:v]format=rgba,setpts=PTS+5.8/TB[fg];[0:v][fg]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]' -map '[v]' -map 0:a:0 -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a copy -movflags +faststart OUTPUT_REVIEW.mp4
```

## Research context and limits
Prior TikTok market/video research supports a 1–1.5s hook, 15–25s duration, real operation demonstrations, Before/After and readable Japanese subtitles. User-provided v33 storyboard is known from prior research notes; the original reference MP4 is not available for direct comparison. This cycle addresses depth, not the still-open real-footage diversity gap.

Not verified: independent Japanese ASR and narration/caption meaning/timing, naturalness, v33 direct comparison, commercial use rights of inherited media, phone playback, employee approval, actual GitHub Actions charges. CI tests the synthetic code only, not the private MP4.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid service, or auto-post; employee approval required before manual publication.
