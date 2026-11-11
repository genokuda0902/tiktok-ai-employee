import json, subprocess
from pathlib import Path
p=Path(__file__).with_name('cycle1381_REVIEW_ONLY.mp4')
x=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
v=next(s for s in x['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==(720,1280)
assert 7.9<float(x['format']['duration'])<8.1
assert not any(s['codec_type']=='audio' for s in x['streams']), 'audio absent must not be claimed narration'
subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
print('PASS: video dimensions, duration, audio-truth, full decode')
