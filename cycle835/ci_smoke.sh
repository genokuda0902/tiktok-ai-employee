#!/usr/bin/env bash
set -euo pipefail
mkdir -p cycle835/ci_out
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i 'color=c=0x092b34:s=1080x1920:r=30:d=25.833333' \
  -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=25.833333' \
  -frames:v 775 -c:v libx264 -preset ultrafast -crf 36 \
  -c:a aac -b:a 64k -pix_fmt yuv420p cycle835/ci_out/source.mp4
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i 'testsrc2=s=1366x768:r=30:d=5.0' \
  -c:v libx264 -preset ultrafast -crf 35 -pix_fmt yuv420p \
  cycle835/ci_out/synthetic_gui.mp4
python cycle835/evidence_insert.py \
  --source cycle835/ci_out/source.mp4 \
  --capture cycle835/ci_out/synthetic_gui.mp4 \
  --manifest cycle835/fixture_manifest.json \
  --out cycle835/ci_out/cycle835_SYNTHETIC_TECHNICAL_ONLY.mp4
ffmpeg -hide_banner -loglevel error -xerror -i \
  cycle835/ci_out/cycle835_SYNTHETIC_TECHNICAL_ONLY.mp4 -f null -
python - <<'PY'
import json,subprocess
p='cycle835/ci_out/cycle835_SYNTHETIC_TECHNICAL_ONLY.mp4'
s=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
v=next(x for x in s['streams'] if x['codec_type']=='video')
a=next(x for x in s['streams'] if x['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],int(v['nb_frames']))==('h264',1080,1920,775)
assert (a['codec_name'],int(a['sample_rate']))==('aac',48000)
assert 25.8<float(s['format']['duration'])<25.9
print('SYNTHETIC CI AV PASS — no Japanese speech or private assets')
PY
