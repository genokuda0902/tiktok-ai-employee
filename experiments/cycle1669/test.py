import json, subprocess, sys
p=sys.argv[1]
x=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
v=next(s for s in x['streams'] if s['codec_type']=='video')
a=next(s for s in x['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264')
assert a['codec_name']=='aac'
assert abs(float(x['format']['duration'])-25.6)<.2
assert not any(s['codec_type']=='subtitle' for s in x['streams'])
subprocess.run(['ffmpeg','-v','error','-xerror','-i',p,'-f','null','-'],check=True)
print('PASS')
