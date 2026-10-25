#!/usr/bin/env bash
set -euo pipefail
mkdir -p cycle834/ci_out
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i "color=c=0x08222d:s=1080x1920:r=30:d=25.833333" \
  -f lavfi -i "sine=frequency=440:sample_rate=48000:duration=25.833333" \
  -frames:v 775 -c:v libx264 -preset ultrafast -crf 36 \
  -c:a aac -b:a 64k -pix_fmt yuv420p \
  cycle834/ci_out/synthetic_source.mp4
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i "testsrc2=s=1366x768:r=30:d=4.2" \
  -c:v libx264 -preset ultrafast -crf 32 -pix_fmt yuv420p \
  cycle834/ci_out/synthetic_screen.mp4
python cycle834/screen_insert.py \
  --source cycle834/ci_out/synthetic_source.mp4 \
  --clip cycle834/ci_out/synthetic_screen.mp4 \
  --out cycle834/ci_out/cycle834_SYNTHETIC_CI_NOT_JAPANESE.mp4
ffmpeg -hide_banner -loglevel error -xerror \
  -i cycle834/ci_out/cycle834_SYNTHETIC_CI_NOT_JAPANESE.mp4 -f null -
python - <<'PY'
import json, subprocess
p='cycle834/ci_out/cycle834_SYNTHETIC_CI_NOT_JAPANESE.mp4'
s=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
v=next(x for x in s['streams'] if x['codec_type']=='video')
a=next(x for x in s['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264')
assert int(v['nb_frames'])==775
assert (a['codec_name'],int(a['sample_rate']))==('aac',48000)
assert 25.8<float(s['format']['duration'])<25.9
print('CI SYNTHETIC ONLY: video/audio decode and geometry PASS')
print('NOT a Japanese narration or reference-quality certification')
PY
