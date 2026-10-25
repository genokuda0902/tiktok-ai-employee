#!/usr/bin/env bash
set -euo pipefail
mkdir -p cycle839/ci_out
python3 - <<'PY'
import wave, math, struct
silences=[(2.809875,3.705625),(5.855396,6.704687),(8.867312,9.723333),
          (12.177,13.008979),(15.447521,16.309708),(18.791187,19.659625),
          (21.782312,22.664333)]
with wave.open('cycle839/ci_out/synthetic_voice.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
    for i in range(1238400):
        t=i/48000
        silent=any(a<=t<b for a,b in silences)
        sample=0 if silent else int(0.25*32767*math.sin(2*math.pi*220*t))
        w.writeframesraw(struct.pack('<h',sample))
PY
ffmpeg -hide_banner -loglevel error -y -f lavfi -i 'testsrc2=size=360x640:rate=30' -frames:v 775 -c:v libx264 -preset ultrafast -pix_fmt yuv420p -an cycle839/ci_out/synthetic_video.mp4
python3 cycle839/pacing.py --input cycle839/ci_out/synthetic_video.mp4 --audio cycle839/ci_out/synthetic_voice.wav --output cycle839/ci_out/cycle839_SYNTHETIC_NOT_JAPANESE.mp4
python3 - <<'PY'
import json,subprocess
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-show_entries','stream=codec_type,nb_frames,duration,sample_rate','-of','json','cycle839/ci_out/cycle839_SYNTHETIC_NOT_JAPANESE.mp4']))
v=next(s for s in p['streams'] if s['codec_type']=='video')
a=next(s for s in p['streams'] if s['codec_type']=='audio')
assert int(v['nb_frames'])==691,p
assert 22.95<float(a['duration'])<23.05,p
assert abs(float(p['format']['duration'])-691/30)<0.04,p
print('Synthetic-only A/V smoke PASS; not Japanese; not publishable')
PY
