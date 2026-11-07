"""Zero-cost review-only Japanese captioned video. No external assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json
OUT=Path(__file__).resolve().parent
W,H=1080,1920
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('AIの回答、\nそのまま使う？','まず根拠を確かめる',3),('BEFORE','出典なしの回答を\nそのまま採用',3),('AFTER','出典・日付・条件を\n順番に確認',3),('最後は人が判断','確認してから使おう',3)]
def make_frame(i):
    title,sub,_=SCENES[i]; im=Image.new('RGB',(W,H),'#081525'); d=ImageDraw.Draw(im)
    d.rounded_rectangle((68,170,1012,1750),radius=48,fill='#14283b')
    d.rounded_rectangle((112,260,968,340),radius=18,fill='#1b5365')
    d.text((140,274),'AI WORKFLOW  /  REVIEW ONLY',font=ImageFont.truetype(REG,31),fill='white')
    f=ImageFont.truetype(FONT,74); g=ImageFont.truetype(REG,51)
    d.multiline_text((140,465),title,font=f,fill='#ffffff',spacing=30)
    d.multiline_text((140,850),sub,font=g,fill='#bdeaf0',spacing=28)
    for j in range(4): d.rounded_rectangle((135+j*207,1530,300+j*207,1548),radius=8,fill='#35dfd1' if j<=i else '#43596b')
    d.text((140,1600),f'{i+1:02d} / 04  •  社内レビュー用',font=ImageFont.truetype(REG,36),fill='#e4e9ed')
    im.save(OUT/f'scene{i}.png')
def render():
    for i in range(len(SCENES)):make_frame(i)
    args=['ffmpeg','-hide_banner','-loglevel','error','-y']
    for i,(_,_,sec) in enumerate(SCENES):args+=['-loop','1','-framerate','30','-t',str(sec),'-i',str(OUT/f'scene{i}.png')]
    filt=''.join(f'[{i}:v]scale=1080:1920,setsar=1,format=yuv420p[v{i}];' for i in range(4))+''.join(f'[v{i}]' for i in range(4))+'concat=n=4:v=1:a=0[out]'
    args+=['-filter_complex',filt,'-map','[out]','-c:v','libx264','-preset','ultrafast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'cycle1280_REVIEW_ONLY.mp4')]
    subprocess.run(args,check=True)
    (OUT/'captions.srt').write_text(''.join(f'{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{a.replace(chr(10)," ")}。{b.replace(chr(10)," ")}\n\n' for i,(a,b,_) in enumerate(SCENES)),encoding='utf8')
    (OUT/'manifest.json').write_text(json.dumps({'review_only':True,'posting_allowed':False,'narration_verified':False,'caption_sync_verified':False,'assets':'original PIL graphics'},ensure_ascii=False,indent=2))
if __name__=='__main__':render()
