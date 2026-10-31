"""Synthetic-only CI smoke test: no private video or third-party assets."""
import json,math,subprocess,tempfile,wave,struct
from pathlib import Path
from speech_sync_accent import run,THEMES

with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp);wav=root/'tone.wav';src=root/'source.mp4';out=root/'result.mp4'
 with wave.open(str(wav),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000)
  f.writeframes(b''.join(struct.pack('<h',int(9000*math.sin(2*math.pi*220*i/16000)) if 4000<=i<18000 else 0) for i in range(32000)))
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
  '-f','lavfi','-i','color=c=0x051b27:s=1080x1920:r=30:d=2',
  '-i',str(wav),'-shortest','-c:v','libx264','-preset','ultrafast',
  '-pix_fmt','yuv420p','-c:a','aac',str(src)],check=True)
 result=run(src,out,'ai-work',preset='ultrafast')
 assert result['voice_energy_onsets'][0] is not None
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames',
  '-show_streams','-of','json',str(out)]))
 video=next(x for x in info['streams'] if x['codec_type']=='video')
 assert video['width']==1080 and video['height']==1920 and int(video['nb_read_frames'])==60
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
 print('Synthetic 60/60 frames + AAC decode PASS; 10 themes:',len(THEMES))
