import json,subprocess,sys
p=sys.argv[1]
s=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',p]))['streams']
assert s[0]['width']==1080 and s[0]['height']==1920
assert any(x['codec_name']=='aac' for x in s)
subprocess.run(['ffmpeg','-v','error','-i',p,'-f','null','-'],check=True)
