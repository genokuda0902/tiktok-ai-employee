import json,subprocess,sys
p=sys.argv[1]
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
s=meta['streams']; v=next(x for x in s if x['codec_type']=='video')
assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264')
assert v['r_frame_rate']=='30/1'
assert any(x['codec_type']=='audio' and x['codec_name']=='aac' for x in s)
assert any(x['codec_type']=='subtitle' for x in s)
assert float(meta['format']['duration'])>20
subprocess.run(['ffmpeg','-v','error','-i',p,'-f','null','-'],check=True)
print('PASS: video/audio/subtitle/full decode')
