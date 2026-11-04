import json, subprocess, sys
from pathlib import Path
p=Path(sys.argv[1]); assert p.is_file() and p.stat().st_size > 100_000
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
v=next(s for s in info['streams'] if s['codec_type']=='video')
a=next(s for s in info['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name']) == (1080,1920,'h264')
assert a['codec_name']=='aac'
assert 20 < float(info['format']['duration']) < 25
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True)
print('PASS')
