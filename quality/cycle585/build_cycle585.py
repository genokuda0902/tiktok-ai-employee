"""Repair subtitles clipped by takeaway cards in a 1080x1920 TikTok slide video.
Visual cue timestamps are inherited from cycle581; no audio alignment is asserted.
"""
from __future__ import annotations
import argparse, json, os, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'assets/cycle583.mp4'
OUTPUT=ROOT/'output/cycle585_REPAIRED_CAPTIONS_HUMAN_REVIEW.mp4'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
WIDTH,HEIGHT,FPS,FRAMES=1080,1920,30,468
OVERLAY_Y,OVERLAY_H=1070,160
CUES=[
 (0,39,'これ、ただの'),
 (39,66,'基板じゃない。'),
 (66,132,'ラズベリーパイ ファイブ。'),
 (132,216,'小さなパソコンとして、'),
 (216,249,'プログラミングや'),
 (249,282,'電子工作に使える。'),
 (282,351,'自分だけの仕組みを'),
 (351,417,'作りたい人は、保存してチェック。'),
 (417,468,'あとで試すなら、保存！'),
]

def genres():
    return json.loads((ROOT/'config/genres.json').read_text(encoding='utf8'))['genres']

def validate_cues():
    assert len(genres())==10
    last=0
    for start,end,txt in CUES:
        assert start==last and end>start and txt
        last=end
    assert last==FRAMES
    return True

def rgb(s):
    return tuple(bytes.fromhex(s.removeprefix('#')))

def subtitle_card(index,genre='雑学・科学'):
    validate_cues()
    if genre not in genres(): raise ValueError('unknown genre')
    if not 0<=index<len(CUES): raise ValueError('bad cue')
    accent=rgb(genres()[genre]['theme'])
    text=CUES[index][2]
    S=2; w,h=WIDTH*S,OVERLAY_H*S
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    d=ImageDraw.Draw(im,'RGBA')
    for y in range(h):
        opacity=min(255,int(255*y/(30*S)))
        d.line((0,y,w,y),fill=(3,13,29,opacity),width=1)
    d.rounded_rectangle((54*S,46*S,928*S,153*S),radius=25*S,
                        fill=(7,25,43,255),outline=(*accent,255),width=3*S)
    d.rounded_rectangle((74*S,62*S,83*S,135*S),radius=4*S,fill=(*accent,255))
    font_size=55
    font=ImageFont.truetype(FONT,font_size*S)
    while d.textbbox((0,0),text,font=font)[2]>785*S:
        font_size-=2
        font=ImageFont.truetype(FONT,font_size*S)
    assert font_size>=34,'caption too long'
    bbox=d.textbbox((0,0),text,font=font)
    y=(46+int((107-(bbox[3]-bbox[1])/S)/2)-bbox[1]/S)*S
    d.text((114*S,y+2*S),text,font=font,fill=(0,0,0,255))
    d.text((112*S,y),text,font=font,fill=(251,253,255,255))
    d.rounded_rectangle((115*S,144*S,(115+min(775,775*(index+1)/len(CUES)))*S,148*S),
                        radius=2*S,fill=(*accent,255))
    return im.resize((WIDTH,OVERLAY_H),Image.Resampling.LANCZOS)

def build(source=SOURCE,output=OUTPUT,genre='雑学・科学'):
    validate_cues()
    source,output=Path(source),Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    if genre not in genres(): raise ValueError('unknown genre')
    work=ROOT/'work';seq=work/'frames';cards=work/'cards'
    seq.mkdir(parents=True,exist_ok=True);cards.mkdir(parents=True,exist_ok=True)
    for i,(start,end,_) in enumerate(CUES):
        img=cards/f'cue_{i:02d}.png'
        subtitle_card(i,genre).save(img,compress_level=1)
        for frame in range(start,end):
            link=seq/f'{frame:04d}.png'
            if link.exists() or link.is_symlink():link.unlink()
            link.symlink_to(os.path.relpath(img,seq))
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-i',str(source),'-framerate',str(FPS),'-start_number','0',
         '-i',str(seq/'%04d.png'),'-filter_complex',
         f'[0:v][1:v]overlay=0:{OVERLAY_Y}:format=auto:shortest=1,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast',
         '-threads','2','-crf','18','-r',str(FPS),'-frames:v',str(FRAMES),
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=SOURCE)
    p.add_argument('--output',type=Path,default=OUTPUT)
    p.add_argument('--genre',default='雑学・科学')
    args=p.parse_args()
    print(build(args.source,args.output,args.genre))
