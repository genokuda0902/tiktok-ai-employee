#!/usr/bin/env bash
set -euo pipefail
# Entirely synthetic technical smoke; NEVER uses or uploads Japanese review media.
FILTER=$(PYTHONPATH=. python3 -c 'from cycle841.motion_review import filtergraph; print(filtergraph())')
mkdir -p /tmp/cycle841
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i 'testsrc2=size=1080x1920:rate=30:duration=3.4' \
  -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=3.4' \
  -map 0:v -map 1:a -c:v libx264 -preset ultrafast -crf 34 -c:a aac \
  -shortest /tmp/cycle841/synthetic_input.mp4
ffmpeg -hide_banner -loglevel error -y -i /tmp/cycle841/synthetic_input.mp4 \
  -filter_complex "$FILTER" -map '[v]' -map '0:a:0' \
  -c:v libx264 -preset ultrafast -crf 34 -pix_fmt yuv420p -c:a copy \
  /tmp/cycle841/synthetic_output.mp4
ffmpeg -v error -xerror -i /tmp/cycle841/synthetic_output.mp4 -f null -
python3 - <<'PY'
import json, subprocess
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json','/tmp/cycle841/synthetic_output.mp4']))
assert any(s['codec_type']=='audio' for s in p['streams'])
assert next(s for s in p['streams'] if s['codec_type']=='video')['nb_frames']=='102'
print('SYNTHETIC_CI_PASS: 102 frames + AAC audio + full decode')
PY
