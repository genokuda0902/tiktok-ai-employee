"""Review-only image-first renderer; no narration, never publish."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1080, 1920
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES = [('AIの答え、\nそのまま使う？','まず確認する3つのこと'),('① 出典を確認','情報の根拠を開いて確かめる'),('② 日付を確認','古い情報を見落とさない'),('③ 人が最終判断','確認してから使う')]

def make_image(i, title, sub):
    im = Image.new('RGB', (W,H), (9,19,37))
    d = ImageDraw.Draw(im)
    for y in range(0,H,4):
        d.line((0,y,W,y), fill=(9+int(10*y/H),19+int(15*y/H),37+int(24*y/H)),width=4)
    d.rounded_rectangle((80,250,1000,1630),radius=56,fill=(20,39,65),outline=(61,135,171),width=5)
    d.rounded_rectangle((135,370,945,800),radius=34,fill=(34,65,91))
    d.text((145,300),'AI × WORKFLOW',font=ImageFont.truetype(BOLD,45),fill='#65e2dc')
    for j,line in enumerate(title.split('\n')):
        d.text((160,430+j*125),line,font=ImageFont.truetype(BOLD,72),fill='white')
    d.text((145,920),sub,font=ImageFont.truetype(FONT,44),fill='#d4e7ef')
    for k in range(4):
        x=160+k*185
        d.rounded_rectangle((x,1150,x+150,1167),radius=8,fill='#66d9d2' if k<=i else '#486078')
    d.text((145,1490),'REVIEW ONLY  •  NOT FOR POSTING',font=ImageFont.truetype(FONT,28),fill='#b0c5d1')
    p=ROOT/f'scene{i}.png'
    im.save(p)
    return p

def render():
    clips=[]
    for i,(title,sub) in enumerate(SCENES):
        png=make_image(i,title,sub)
        clip=ROOT/f'clip{i}.mp4'
        vf="zoompan=z='min(zoom+0.00025,1.06)':d=120:s=1080x1920:fps=30,format=yuv420p"
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-i',str(png),'-vf',vf,'-frames:v','120','-c:v','libx264','-preset','ultrafast','-crf','26','-pix_fmt','yuv420p',str(clip)],check=True)
        clips.append(clip)
    lst=ROOT/'concat.txt'
    lst.write_text(''.join(f"file '{p.name}'\n" for p in clips))
    out=ROOT/'cycle1283_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(out)],check=True)
    (ROOT/'captions.srt').write_text(''.join(f'{i+1}\n00:00:{i*4:02d},000 --> 00:00:{(i+1)*4:02d},000\n{a.replace(chr(10)," ")}。{b}\n\n' for i,(a,b) in enumerate(SCENES)),encoding='utf-8')
    return out

if __name__=='__main__':
    print(render())
