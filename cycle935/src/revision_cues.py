"""Three-step original revision cue overlay; review only, no posting."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse

FPS=30
START=14.5
END=17.4
FRAME_COUNT=87
CANVAS=(1080,150)
POSITION_Y=850
SAFE_CAPTION_START_Y=1450
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_productivity':'#21d4c1','business':'#54b4ff',
 'finance':'#5bd4b0','education':'#ffd15c',
 'health':'#60d9ae','beauty':'#ff9bc5',
 'food':'#ffad65','travel':'#7ed5ff',
 'lifestyle':'#e0aaff','technology':'#5bd9ff'}
STEPS=[
 ('01','修正箇所を指定','例：冒頭の見出し'),
 ('02','直し方を指定','例：1行で短くする'),
 ('03','結果を見比べる','画面で読めるか確認')]

def smooth(x):
    x=max(0.0,min(1.0,x))
    return x*x*(3-2*x)

def stage_for_frame(n):
    if not 0<=n<FRAME_COUNT: raise ValueError('frame outside scene')
    return min(2,n//29)

def alpha_for_frame(n):
    phase=n%29
    return min(smooth(phase/5),smooth((29-phase)/5))

def draw_frame(n,genre='ai_productivity'):
    if genre not in GENRES: raise ValueError('Unknown genre: fail closed')
    idx=stage_for_frame(n)
    a=alpha_for_frame(n)
    img=Image.new('RGBA',CANVAS,(0,0,0,0))
    if a<=0:return img
    d=ImageDraw.Draw(img,'RGBA')
    x0,y0,x1,y1=130,10,950,140
    d.rounded_rectangle((x0,y0,x1,y1),radius=24,
        fill=(6,27,46,int(244*a)),
        outline=(255,255,255,int(85*a)),width=2)
    color=tuple(bytes.fromhex(GENRES[genre][1:]))
    d.rounded_rectangle((x0+18,y0+22,x0+106,y0+103),radius=17,
        fill=(*color,int(240*a)))
    fnum=ImageFont.truetype(BOLD,44)
    fmain=ImageFont.truetype(BOLD,41)
    fsub=ImageFont.truetype(FONT,25)
    d.text((x0+34,y0+32),STEPS[idx][0],font=fnum,fill=(5,22,36,int(255*a)))
    d.text((x0+128,y0+16),STEPS[idx][1],font=fmain,fill=(255,255,255,int(255*a)))
    d.text((x0+130,y0+77),STEPS[idx][2],font=fsub,fill=(211,229,240,int(255*a)))
    progress=smooth((n%29)/28)
    d.rounded_rectangle((x0+128,y0+117,x1-25,y0+122),radius=2,
        fill=(91,112,135,int(130*a)))
    d.rounded_rectangle((x0+128,y0+117,
        x0+128+int((x1-x0-153)*progress),y0+122),radius=2,
        fill=(*color,int(240*a)))
    return img

def export_frames(outdir:Path,genre='ai_productivity'):
    outdir.mkdir(parents=True,exist_ok=True)
    for n in range(FRAME_COUNT):
        draw_frame(n,genre).save(outdir/f'{n:03d}.png')
    return FRAME_COUNT

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--outdir',type=Path,required=True)
    p.add_argument('--genre',choices=list(GENRES),default='ai_productivity')
    args=p.parse_args()
    print(export_frames(args.outdir,args.genre))
