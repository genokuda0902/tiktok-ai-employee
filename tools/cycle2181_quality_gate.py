# cycle2181 quality gate
# Run: python tools/cycle2181_quality_gate.py video.mp4
import json, subprocess, sys
p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height','-of','json',sys.argv[1]],capture_output=True,text=True,check=True)
s=json.loads(p.stdout)['streams']
v=next((x for x in s if x['codec_type']=='video'),None)
a=any(x['codec_type']=='audio' for x in s)
assert v and v['width']==1080 and v['height']==1920, 'invalid dimensions'
assert a, 'FAIL: Japanese narration/audio stream missing; publication prohibited'
print('Audio present; Japanese intelligibility and sync require separate verification')
