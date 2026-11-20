"""Review-only synthetic Japanese slides; no automatic publication."""
from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SIZE=(720,1280)
SCENES=[('入力に時間がかかる？','作業を3段階で整理'),('BEFORE','手入力で確認が必要'),('AFTER','関数で自動集計'),('最後は人が検算','数字の誤りを防ぐ')]
def make():
 assert Path(FONT).exists()
 clips=[]
 for i,(headline,detail) in enumerate(SCENES):
  im=Image.new('RGB',SIZE,(11,20,38));d=ImageDraw.Draw(im)
  d.rounded_rectangle((46,260,674,1010),radius=36,fill=(28,45,68))
  d.rectangle((46,260,60,1010),fill=(36,196,210))
  d.text((85,425),headline,font=ImageFont.truetype(FONT,48),fill='white')
  d.text((85,575),detail,font=ImageFont.truetype(FONT,32),fill=(206,233,242))
  d.text((85,915),f'{i+1} / {len(SCENES)}  REVIEW ONLY',font=ImageFont.truetype(FONT,32),fill=(118,203,215))
  p=ROOT/f'scene_{i}.png';im.save(p)
  clip=ROOT/f'scene_{i}.mp4'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','24','-i',str(p),'-t','3','-c:v','libx264','-pix_fmt','yuv420p','-r','24',str(clip)],check=True)
  clips.append(clip)
 playlist=ROOT/'concat.txt';playlist.write_text(''.join(f"file '{p.name}'\n" for p in clips))
 out=ROOT/'cycle1598_REVIEW_ONLY.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(playlist),'-c','copy','-movflags','+faststart',str(out)],check=True)
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
 videos=[s for s in meta['streams'] if s['codec_type']=='video']
 assert len(videos)==1 and (videos[0]['width'],videos[0]['height'])==SIZE
 assert not [s for s in meta['streams'] if s['codec_type']=='audio']
 (ROOT/'probe.json').write_text(json.dumps(meta,indent=2))
 (ROOT/'quality.json').write_text(json.dumps({'approved':False,'japanese_narration':False,'speech_synced_captions':False,'asset_type':'synthetic','publication':'BLOCKED'},indent=2))
 return out
if __name__=='__main__':print(make())
