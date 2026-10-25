#!/usr/bin/env bash
set -euo pipefail
mkdir -p cycle836/ci_out
ffmpeg -hide_banner -loglevel error -y -f lavfi -i 'color=c=0x102d37:s=1080x1920:r=30:d=25.833333' -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=25.833333' -frames:v 775 -c:v libx264 -preset ultrafast -crf 37 -pix_fmt yuv420p -c:a aac -b:a 64k cycle836/ci_out/source.mp4
ffmpeg -hide_banner -loglevel error -y -f lavfi -i 'testsrc2=s=1366x768:r=30:d=5.0' -c:v libx264 -preset ultrafast -crf 36 -pix_fmt yuv420p cycle836/ci_out/capture.mp4
printf '%s\n' '{"source_kind":"synthetic_test_pattern","application":"synthetic_ffmpeg_fixture","data_classification":"fictional","contains_personal_data":false,"review_only":true,"publication_approved":false}' > cycle836/ci_out/manifest.json
python cycle836/writer_capture_insert.py --source cycle836/ci_out/source.mp4 --capture cycle836/ci_out/capture.mp4 --out cycle836/ci_out/cycle836_SYNTHETIC_TECHNICAL_ONLY.mp4 --manifest cycle836/ci_out/manifest.json --capture-start 1.5
ffmpeg -hide_banner -loglevel error -xerror -i cycle836/ci_out/cycle836_SYNTHETIC_TECHNICAL_ONLY.mp4 -f null -
python - <<'PY'
import json,subprocess
p='cycle836/ci_out/cycle836_SYNTHETIC_TECHNICAL_ONLY.mp4'
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
v=next(x for x in d['streams'] if x['codec_type']=='video')
a=next(x for x in d['streams'] if x['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],int(v['nb_frames']))==('h264',1080,1920,775)
assert (a['codec_name'],int(a['sample_rate']))==('aac',48000)
assert 25.8<float(d['format']['duration'])<25.9
print('SYNTHETIC TECHNICAL AV PASS; NOT JAPANESE OR PUBLISHABLE')
PY
