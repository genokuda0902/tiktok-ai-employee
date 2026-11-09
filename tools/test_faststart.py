import json, subprocess, sys
from pathlib import Path
p=Path(sys.argv[1]); data=p.read_bytes()
assert 0 < data.find(b'moov') < data.find(b'mdat'), 'moov must precede mdat'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
streams=probe['streams']; v=next(s for s in streams if s['codec_type']=='video')
assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264')
assert any(s['codec_type']=='audio' and s['codec_name']=='aac' for s in streams)
assert any(s['codec_type']=='subtitle' for s in streams)
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0','-f','null','-','-map','0:a:0','-f','null','-'],check=True)
print('PASS')
