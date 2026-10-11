"""Standalone review-only kinetic comparison scene, 1080x1920/30fps."""
import argparse,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from contract import Scene,FRAMES,validate
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def txt(d,x,y,s,n=39,c='white',b=False):
    d.text((x,y),s,font=ImageFont.truetype(BOLD if b else FONT,n),fill=c)
def box(d,xy,fill,outline=None):
    d.rounded_rectangle(xy,radius=23,fill=fill,outline=outline,width=4)
def frame(s,stage):
    total=validate(s)
    if stage not in range(6):raise ValueError('Invalid stage')
    im=Image.new('RGB',(1080,1920),'#071b30');d=ImageDraw.Draw(im)
    for j in range(12):
        d.ellipse((500-j*42,90-j*42,1120+j*32,760+j*32),outline='#123b55',width=2)
    txt(d,62,90,'AI時短ラボ / SYNTHETIC DEMO',36,'#61e7f4',True)
    d.line((60,164,1020,164),fill='#286480',width=4)
    txt(d,60,248,'Before / After',83,'white',True)
    txt(d,60,371,'手作業 → 手順の標準化',45,'#c7e5f4',True)
    box(d,(50,490,1030,1405),'#0d2a42','#2b6484')
    for x,name,steps,accent,bg,visible in (
        (78,'BEFORE',s.before,'#ff9f9f','#4b2c3e',min(3,stage+1)),
        (562,'AFTER',s.after,'#74f5c7','#14504e',max(0,min(3,stage-1)))):
        box(d,(x+10,548,x+449,1360),'#031522')
        box(d,(x,530,x+437,1340),bg,accent)
        box(d,(x+22,555,x+415,645),accent)
        txt(d,x+45,568,name,50,'#061d2b',True)
        for i,item in enumerate(steps):
            y=698+i*197
            box(d,(x+20,y,x+415,y+140),'#18374b' if i<visible else '#132b3d',accent if i==visible-1 else None)
            if i<visible:
                box(d,(x+35,y+31,x+95,y+99),accent)
                txt(d,x+49,y+38,str(i+1),34,'#061d2b',True)
                txt(d,x+111,y+39,item,39,'white',True)
            else:txt(d,x+49,y+37,'···',38,'#466579')
    if stage>=2:
        d.ellipse((470,855,608,993),fill='#09263c',outline='#7fefff',width=6)
        d.line((496,924,572,924),fill='#7fefff',width=14)
        d.polygon(((566,893),(602,924),(566,955)),fill='#7fefff')
    box(d,(60,1445,1020,1605),'#087f77' if stage==5 else '#13445d','#61c6e1')
    caption=('違いを3つの工程で比較' if stage==0 else '同じ4件を式で検算' if stage==4
             else ' + '.join(map(str,s.values))+' = '+str(total) if stage==5 else '手順を一つずつ確認')
    txt(d,89,1490,caption,38,'white',True)
    txt(d,62,1640,'※ 作業時間の短縮効果は未測定',32,'#d6e8f3')
    txt(d,62,1715,'再現映像 / 架空データ / 投稿未承認',30,'#a8c9d8')
    d.line((60,1810,1020,1810),fill='#264f6b',width=9)
    d.line((60,1810,60+int(960*(stage+1)/6),1810),fill='#46e3db',width=9)
    return im
def render(out):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);clips=[]
        for i,n in enumerate(FRAMES):
            png=tmp/f'{i}.png';frame(Scene(),i).save(png)
            mp4=tmp/f'{i}.mp4';clips.append(mp4)
            subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-framerate','30','-i',str(png),
                            '-frames:v',str(n),'-c:v','libx264','-preset','ultrafast','-crf','22',
                            '-pix_fmt','yuv420p','-an',str(mp4)],check=True)
        f=tmp/'list.txt';f.write_text(''.join("file '"+str(p)+"'\n" for p in clips))
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0',
                        '-i',str(f),'-c','copy',str(out)],check=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True)
    render(p.parse_args().out)
