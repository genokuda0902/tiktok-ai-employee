"""Free Japanese gTTS recovery test; voice required, no fake success."""
import json,subprocess,sys
from pathlib import Path
from gtts import gTTS
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
OUT=ROOT/'out';OUT.mkdir(exist_ok=True)
def call(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-800:])
 return p.stdout
paths=[]
for i,sc in enumerate(DATA['scenes']):
 duration=sc['seconds'];wav=OUT/f'{i:02d}.wav'
 if not sc['voice']:
  call(['ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t',str(duration),str(wav)])
 else:
  mp3=OUT/f'{i:02d}.mp3';gTTS(sc['voice'],lang='ja').save(str(mp3))
  dur=float(json.loads(call(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(mp3)]))['format']['duration'])
  rate=max(1.,dur/(duration-.12))
  if rate>1.45:raise RuntimeError(f'Scene {i}: speech {dur:.2f}s exceeds slot {duration}s (rate {rate:.2f})')
  call(['ffmpeg','-y','-v','error','-i',str(mp3),'-af',f'atempo={rate:.4f},apad,atrim=duration={duration}','-ar','48000','-ac','1',str(wav)])
 paths.append(wav)
(OUT/'concat.txt').write_text(''.join("file '"+str(x.resolve())+"'\\n" for x in paths))
call(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c:a','pcm_s16le',str(OUT/'narration.wav')])
duration=float(json.loads(call(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(OUT/'narration.wav')]))['format']['duration'])
if abs(duration-20)>0.2:raise RuntimeError(f'Audio length wrong: {duration}')
print(json.dumps({'status':'VOICE_GENERATED_NEEDS_HUMAN_LISTENING','duration':duration,'lang':'ja','scenes':len(paths)},ensure_ascii=False))
