import json, subprocess, sys
p=sys.argv[1]
r=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
v=[s for s in r['streams'] if s['codec_type']=='video']
a=[s for s in r['streams'] if s['codec_type']=='audio']
assert len(v)==1 and v[0]['codec_name']=='h264' and (v[0]['width'],v[0]['height'])==(1080,1920)
assert abs(float(r['format']['duration'])-12)<0.1
assert not a, 'Unexpected audio: speech has not been approved or validated'
subprocess.run(['ffmpeg','-v','error','-i',p,'-f','null','-'],check=True)
print('PASS video 1080x1920 decode; FAIL publication: Japanese narration absent')
