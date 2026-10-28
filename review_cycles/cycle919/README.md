# cycle919 — explicit correction instructions (review only)

**Change:** scene06, 14.5–17.4 s, frames 435–521. Replaces a generic instruction card with a 3-beat original vector animation: vague request → highlight ambiguity → explicit target, action and verification. Supports ten genre-specific presets without asserting invented results.

**Private MP4:** Generated and tested locally, not committed or uploaded. Source is the prior private cycle918 review video. Rendering only replaces the image region y=300–1459; existing header, Japanese burned captions and AAC bitstream are inherited. Use the locally supplied ZIP for full MP4 and local QA; CI checks the standalone renderer, synthetic frames, policy and layouts only.

**Local rendering:** python3 review_instruction.py --output /tmp/cycle919-frames. Compositing example: ffmpeg -i source.mp4 -framerate 30 -start_number 435 -i /tmp/cycle919-frames/frame_%04d.png -filter_complex "[1:v]setpts=PTS-STARTPTS+14.5/TB[patch];[0:v][patch]overlay=0:300:eof_action=pass:enable='between(n,435,521)'[v]" -map "[v]" -map 0:a:0 -c:v libx264 -pix_fmt yuv420p -r 30 -c:a copy output.mp4.

**Restrictions:** no automatic publication, merge, rights-unapproved assets, personal data, unsupported claims or payments. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Independent Japanese ASR, source rights, original v33 comparison, smartphone playback and employee approval remain outstanding.
