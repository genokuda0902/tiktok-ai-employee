"""cycle581: 10-genre reusable TikTok-safe caption compositor.

Requires Pillow, FFmpeg, Noto Sans CJK; no paid APIs or automatic posting.
Cue boundaries are measured from visible source subtitles, not speech recognition.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'assets' / 'cycle580.mp4'
OUTPUT = ROOT / 'output' / 'cycle581_SAFE_CAPTIONS_JA_HUMAN_REVIEW.mp4'
FPS, WIDTH, HEIGHT = 30, 1080, 1920
OVERLAY_Y = 1110
LAYER_H = HEIGHT - OVERLAY_Y
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
CUES = [
    (0, 39, ['これ、ただの'], 'ただの'),
    (39, 66, ['基板じゃない。'], '基板じゃない。'),
    (66, 132, ['ラズベリーパイ', 'ファイブ。'], 'ラズベリーパイ'),
    (132, 216, ['小さなパソコン', 'として、'], '小さなパソコン'),
    (216, 249, ['プログラミングや'], 'プログラミング'),
    (249, 282, ['電子工作に使える。'], '電子工作'),
    (282, 351, ['自分だけの', '仕組みを'], '自分だけの'),
    (351, 417, ['作りたい人は、', '保存してチェック。'], '保存してチェック。'),
    (417, 468, ['あとで試すなら、', '保存！'], '保存！'),
]
SAFE = {'left': 80, 'right': 900, 'top': 130, 'bottom': 1436}

def genres():
    return json.loads((ROOT / 'config/genres.json').read_text(encoding='utf-8'))['genres']

def rgb(hexstr):
    return tuple(bytes.fromhex(hexstr.lstrip('#')))

def caption_image(lines, highlight, accent, index):
    S = 2
    im = Image.new('RGBA', (WIDTH*S, LAYER_H*S), (0,0,0,0))
    d = ImageDraw.Draw(im)
    c = rgb(accent)
    for y in range(LAYER_H*S):
        absolute_y = OVERLAY_Y + y/S
        if absolute_y < 1160: alpha = 0
        elif absolute_y < 1310: alpha = int(245*(absolute_y-1160)/150)
        else: alpha = 255
        if alpha:
            d.line((0,y,WIDTH*S,y), fill=(4,13,28,alpha), width=1)
    d.rounded_rectangle((78*S,1218*S-OVERLAY_Y*S,882*S,1425*S-OVERLAY_Y*S),
                        radius=26*S,fill=(4,20,37,246),outline=(*c,130),width=2*S)
    d.rounded_rectangle((94*S,1240*S-OVERLAY_Y*S,102*S,1400*S-OVERLAY_Y*S),
                        radius=4*S,fill=(*c,255))
    base_size = 66 if len(lines)==1 else 58
    font = ImageFont.truetype(FONT_PATH,base_size*S)
    while max(d.textbbox((0,0),line,font=font)[2] for line in lines) > 725*S:
        base_size -= 2
        font = ImageFont.truetype(FONT_PATH,base_size*S)
    line_h = (base_size+14)*S
    top = (1296 if len(lines)==1 else 1252)*S - OVERLAY_Y*S
    for j,line in enumerate(lines):
        x,y = 124*S,top+j*line_h
        p=line.find(highlight)
        parts=[(line,False)] if p<0 else [(line[:p],False),(highlight,True),(line[p+len(highlight):],False)]
        for segment,active in parts:
            if not segment: continue
            d.text((x+2*S,y+3*S),segment,font=font,fill=(0,0,0,170))
            d.text((x,y),segment,font=font,fill=(*c,255) if active else (251,253,255,255))
            x+=d.textlength(segment,font=font)
    d.rounded_rectangle((110*S,1413*S-OVERLAY_Y*S,850*S,1419*S-OVERLAY_Y*S),
                        radius=3*S,fill=(55,76,91,210))
    d.rounded_rectangle((110*S,1413*S-OVERLAY_Y*S,(110+740*(index+1)/len(CUES))*S,1419*S-OVERLAY_Y*S),
                        radius=3*S,fill=(*c,255))
    return im.resize((WIDTH,LAYER_H),Image.Resampling.LANCZOS)

def build(source=SOURCE, output=OUTPUT, genre='雑学・科学'):
    source,output=Path(source),Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    gs=genres()
    if genre not in gs: raise ValueError('unknown genre: '+genre)
    out=ROOT/'work'/'cues'
    out.mkdir(parents=True,exist_ok=True)
    manifest=['ffconcat version 1.0']
    for i,(start,end,lines,highlight) in enumerate(CUES):
        p=out/('%02d.png'%i)
        caption_image(lines,highlight,gs[genre]['theme'],i).save(p)
        manifest.extend(["file '%s'"%p.as_posix(), 'duration %.9f'%((end-start)/FPS)])
    manifest.append("file '%s'"%(out/'08.png').as_posix())
    playlist=ROOT/'work'/'cues.ffconcat'
    playlist.write_text('\n'.join(manifest)+'\n')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-f','concat','-safe','0','-i',str(playlist),
         '-filter_complex','[0:v][1:v]overlay=0:%d:format=auto:shortest=1,format=yuv420p[v]'%OVERLAY_Y,
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
         '-r',str(FPS),'-frames:v','468','-pix_fmt','yuv420p','-c:a','copy',
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'output':str(output),'genre':genre,'cues':len(CUES),'safe':SAFE}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=SOURCE)
    p.add_argument('--output',type=Path,default=OUTPUT)
    p.add_argument('--genre',default='雑学・科学')
    a=p.parse_args()
    print(json.dumps(build(a.source,a.output,a.genre),ensure_ascii=False))
