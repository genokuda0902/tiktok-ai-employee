#!/usr/bin/env bash
set -euo pipefail
mkdir -p cycle837/ci_out
ffmpeg -hide_banner -loglevel error -y -f lavfi -i 'color=c=0x0b2634:s=1080x1920:r=30:d=25.833333' -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=25.833333' -frames:v 775 -c:v libx264 -preset ultrafast -crf 38 -pix_fmt yuv420p -c:a aac -b:a 64k cycle837/ci_out/synthetic_source.mp4
printf '%s\n' '{"source_kind":"locally_rendered_ui","data_classification":"fictional","contains_personal_data":false,"review_only":true,"publication_approved":false,"service_connection":false}' > cycle837/ci_out/manifest.json
python cycle837/prompt_demo_insert.py --demo cycle837/ci_out/ui_demo.mp4 --source cycle837/ci_out/synthetic_source.mp4 --out cycle837/ci_out/cycle837_SYNTHETIC_TECHNICAL_ONLY.mp4 --manifest cycle837/ci_out/manifest.json
ffmpeg -hide_banner -loglevel error -xerror -i cycle837/ci_out/cycle837_SYNTHETIC_TECHNICAL_ONLY.mp4 -f null -
python - <<'PY'
import json,subprocess
p='cycle837/ci_out/cycle837_SYNTHETIC_TECHNICAL_ONLY.mp4'
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
v=next(x for x in d['streams'] if x['codec_type']=='video')
a=next(x for x in d['streams'] if x['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],int(v['nb_frames']))==('h264',1080,1920,775)
assert (a['codec_name'],int(a['sample_rate']))==('aac',48000)
assert abs(float(d['format']['duration'])-775/30)<.02
print('PASS: 10-genre source, synthetic AV 1080x1920/30fps/775f, AAC 48kHz; NOT JAPANESE REVIEW')
PY
