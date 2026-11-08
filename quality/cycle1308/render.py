"""Synthetic review-only Japanese spreadsheet walkthrough; no private assets."""
from pathlib import Path
import subprocess, json, sys
from PIL import Image, ImageDraw, ImageFont
SCENES=[('合計、手で計算してない？','4件の売上を一瞬で集計'),('STEP 1｜データを確認','12,000 / 8,000 / 15,000 / 5,000'),('STEP 2｜式を入力','=SUM(B2:B5)'),('STEP 3｜結果を確認','合計 40,000 円'),('最後に必ずチェック','範囲と元データを確認')]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def render(out):
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 font=ImageFont.truetype(FONT,64);small=ImageFont.truetype(FONT,38)
 frames=out.parent/'frames';frames.mkdir(exist_ok=True)
 for i,(headline,detail) in enumerate(SCENES):
  im=Image.new('RGB',(720,1280),'#0b1325');d=ImageDraw.Draw(im)
  d.rounded_rectangle((35,150,685,1090),radius=35,fill='#192a43')
  d.rounded_rectangle((60,230,660,385),radius=22,fill='#25466a')
  d.text((85,260),headline,font=font,fill='white')
  d.text((70,480),detail,font=small,fill='#ccecf5')
  for r,v in enumerate(['A       B','1  売上','2  12,000','3  8,000','4  15,000','5  5,000']):d.text((105,620+r*64),v,font=small,fill='#b8d4e8')
  d.rectangle((50,1160,50+int(620*(i+1)/len(SCENES)),1172),fill='#31d9c4')
  im.save(frames/f'{i:02d}.png')
 concat=out.parent/'concat.txt'
 concat.write_text(''.join(f"file '{(frames/f'{i:02d}.png').resolve()}'\nduration 3\n" for i in range(5))+f"file '{(frames/'04.png').resolve()}'\n")
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=24,scale=1080:1920:flags=lanczos,format=yuv420p','-t','15','-c:v','libx264','-preset','ultrafast','-crf','27','-movflags','+faststart','-an',str(out)],check=True)
 srt=''.join(f'{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{a}。{b}\n\n' for i,(a,b) in enumerate(SCENES))
 (out.parent/'captions.srt').write_text(srt,encoding='utf-8')
 (out.parent/'manifest.json').write_text(json.dumps({'review_only':True,'narration_verified':False,'caption_speech_synced':False,'asset_source':'synthetic only','publish_approved':False,'resolution':[1080,1920],'duration':15},ensure_ascii=False,indent=2))
if __name__=='__main__':render(sys.argv[1])
