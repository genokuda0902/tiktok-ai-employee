import json,subprocess,sys
p=sys.argv[1]
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
v=next(x for x in d['streams'] if x['codec_type']=='video')
a=next(x for x in d['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264')
assert a['codec_name']=='aac'
assert float(d['format']['duration'])>20
subprocess.run(['ffmpeg','-v','error','-xerror','-i',p,'-f','null','-'],check=True)
print('PASS')
