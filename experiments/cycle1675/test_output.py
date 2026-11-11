import json,subprocess,sys
p=sys.argv[1]
def run(args):return subprocess.check_output(args,text=True)
data=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height','-of','json',p]))
streams=data['streams']
assert any(s.get('codec_name')=='h264' and s.get('width')==1080 and s.get('height')==1920 for s in streams)
assert any(s.get('codec_name')=='aac' for s in streams)
subprocess.run(['ffmpeg','-v','error','-i',p,'-f','null','-'],check=True)
print('PASS: video, audio, resolution, full decode')
