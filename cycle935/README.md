# cycle935 — 3-step revision cue / HUMAN_REVIEW

This is a distinct visual quality iteration. The prior **cycle933** sharpened scene03 Japanese paper text; parallel **cycle934** revised the opening hook. This change instead adds **three sequential, original editorial labels** to the empty gap between the Before and After cards in scene06 (14.5–17.4 seconds). The overlay never touches the bottom subtitle band. It emphasizes *where to revise → how to revise → compare the result*.

## Local MP4 QA (not uploaded to public GitHub)

- Source: cycle933 local private MP4, **not** cycle934 (no parallel work merged)
- Result: `cycle935_REVISION_CUES_JP_HUMAN_REVIEW.mp4`
- SHA256: `e066328ed65250fe4c7f1cbc2c0f6e072ba577fbc770437066a2e02b5de5d7d3`
- H.264, 1080×1920, 30fps, 691 frames, 23.033s; AAC 48kHz
- Full audio/video decode PASS; original audio ADTS bitstream SHA256 unchanged
- 87 overlay frames prepared (three stage-start frames fully transparent)
- Sample subtitle band MAE max 0.62 / 255; off-scene MAE max 1.25 / 255 (recompression)
- 11/11 local synthetic tests PASS; 10 genre configurations validated
- No fabricated business results, no third-party imagery, no private media committed
- CI tests synthetic renderer only, **not** full private MP4

## Reproduce without paid services

Install Pillow and Noto CJK fonts; run:
```sh
python cycle935/src/revision_cues.py --outdir /tmp/cycle935-overlays
ffmpeg -i SOURCE_REVIEW.mp4 -framerate 30 -start_number 0 -i /tmp/cycle935-overlays/%03d.png \
  -filter_complex '[1:v]format=rgba,setpts=PTS+14.5/TB[ov];[0:v][ov]overlay=x=0:y=850:shortest=0:eof_action=pass:format=auto[v]' \
  -map '[v]' -map 0:a:0 -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a copy -movflags +faststart OUTPUT_REVIEW.mp4
```

Research context: hook 0–1.5s, 15–25s duration, operation demo, Before/After and safe captions; 16-panel v33 storyboard summary reviewed, original v33 MP4 unavailable. No claim of reference parity.

**Not verified:** independent Japanese ASR / subtitle meaning and timing, human pronunciation QA, reference video comparison, inherited source rights, phone hardware playback, employee approval or actual Actions charges.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Never auto-post, merge, pay, or claim publication readiness. Manual posting only after employee approval.
