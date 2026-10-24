"""cycle819: rights-safe original desk/paper insert, 10-genre reusable renderer.

Only local private review media is used. GitHub CI generates a synthetic tone,
not Japanese speech. Never publish without employee approval.
"""
from __future__ import annotations
import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 30
START_FRAME = 540
FRAME_COUNT = 90
X, Y, WIDTH, HEIGHT = 125, 815, 820, 475
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRE_COLORS = {
    'ai_work': '#73CBFF', 'beauty': '#FF9EC4',
    'love_psychology': '#C3A2FF', 'money_saving': '#FFD475',
    'sales_business': '#5DE7C4', 'career': '#86B7FF',
    'health_life': '#B6E984', 'science': '#8DD9FF',
    'travel_food': '#FFBB8C', 'product_life': '#D8B0FF',
}

def check_genre(genre: str) -> str:
    if genre not in GENRE_COLORS:
        raise ValueError(f'Unknown genre: {genre}')
    if len(GENRE_COLORS) != 10:
        raise ValueError('Ten-genre contract changed')
    return GENRE_COLORS[genre]

def _font(path: str, size: int):
    return ImageFont.truetype(path, size)

def _base_image() -> Image.Image:
    h, w = HEIGHT, WIDTH
    yy, xx = np.mgrid[:h, :w]
    rng = np.random.default_rng(819)
    noise = rng.normal(0, 3.3, (h, w))
    spotlight = np.exp(-(((xx-385)/480)**2 + ((yy-180)/330)**2)) * 28
    grain = (np.sin(xx / 7.5 + np.sin(yy/36)) + np.sin(xx / 28)) * 2.8
    arr = np.empty((h, w, 3), dtype=np.uint8)
    for k, base in enumerate((23, 30, 35)):
        arr[:,:,k] = np.clip(base + spotlight * (1.05 - k*0.14) + grain + noise, 0, 255)
    img = Image.fromarray(arr, 'RGB').convert('RGBA')
    glow = Image.new('RGBA', (w,h))
    g = ImageDraw.Draw(glow,'RGBA')
    g.ellipse((-90,-160,390,220), fill=(231,171,97,44))
    g.ellipse((540,40,950,480), fill=(93,167,205,40))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(54)))
    d = ImageDraw.Draw(img,'RGBA')
    d.rounded_rectangle((40,47,600,462), radius=25, fill=(0,0,0,116))
    d.rounded_rectangle((32,36,590,450), radius=19, fill=(240,240,229,255))
    d.rounded_rectangle((32,36,590,450), radius=19, outline=(255,255,255,190), width=3)
    d.rectangle((69,93,557,96), fill=(201,207,204,255))
    d.text((69,54), '週次レビュー', font=_font(BOLD,25), fill=(36,51,62))
    d.text((395,59), '例示データ', font=_font(FONT,20), fill=(92,105,107))
    for i in range(5):
        gy = 153 + i*52
        d.line((91,gy,550,gy), fill=(196,204,201,190), width=2)
    d.line((92,147,92,368), fill=(99,111,117,190), width=2)
    d.line((92,368,550,368), fill=(99,111,117,190), width=2)
    for i in range(6):
        x = 108+i*83
        d.text((x-10,380), str(i+1), font=_font(FONT,20), fill=(87,98,102))
    d.text((77,415), '計画 → 実行 → 検証', font=_font(BOLD,25), fill=(45,59,66))
    d.rounded_rectangle((262,18,357,53), radius=9, fill=(22,27,30,150))
    d.rounded_rectangle((270,16,349,47), radius=7, fill=(177,191,191,255))
    d.rounded_rectangle((288,20,332,34), radius=6, fill=(71,83,88,255))
    d.line((687,315,790,448), fill=(0,0,0,155), width=20)
    d.line((680,306,786,440), fill=(180,189,195,255), width=14)
    d.line((680,306,786,440), fill=(78,101,111,255), width=5)
    d.rounded_rectangle((620,76,789,282), radius=14, fill=(0,0,0,115))
    d.rounded_rectangle((610,65,781,273), radius=10, fill=(251,232,157,255))
    d.polygon(((740,273),(781,231),(781,273)), fill=(219,197,124,255))
    d.text((628,103), '次の一手', font=_font(BOLD,30), fill=(42,55,63))
    d.line((628,150,758,150), fill=(105,104,81,155), width=2)
    d.text((628,174), '見直す', font=_font(BOLD,32), fill=(42,55,63))
    d.text((628,221), '→ 改善', font=_font(BOLD,29), fill=(42,55,63))
    return img

def render_frame(frame: int, genre: str='sales_business') -> Image.Image:
    if not 0 <= frame < FRAME_COUNT:
        raise ValueError('frame outside 0..89')
    accent = check_genre(genre)
    img = _base_image()
    d = ImageDraw.Draw(img, 'RGBA')
    points = [(108,342),(191,304),(274,322),(357,244),(440,217),(523,179)]
    progress = max(0.0, min(1.0, (frame-3)/53))*(len(points)-1)
    completed = int(progress)
    color = tuple(bytes.fromhex(accent.lstrip('#')))
    for i in range(min(completed,len(points)-1)):
        d.line((*points[i],*points[i+1]), fill=color+(255,), width=10, joint='curve')
    if completed < len(points)-1:
        p1,p2=points[completed],points[completed+1]
        frac=progress-completed
        endpoint=(int(p1[0]+(p2[0]-p1[0])*frac),int(p1[1]+(p2[1]-p1[1])*frac))
        d.line((*p1,*endpoint),fill=color+(255,),width=10)
    for i in range(min(completed+1,len(points))):
        x,y=points[i]
        d.ellipse((x-10,y-10,x+10,y+10),fill=(255,255,255,255),outline=color+(255,),width=4)
    if frame >= 56:
        alpha=min(255,(frame-56)*18)
        d.rounded_rectangle((325,112,555,157),radius=12,fill=(25,62,66,alpha))
        d.text((344,121),'変化を確認',font=_font(BOLD,25),fill=(255,255,255,alpha))
    zoom=1.0 + .015*frame/(FRAME_COUNT-1)
    if zoom>1:
        sw,sh=round(WIDTH/zoom),round(HEIGHT/zoom)
        x0=(WIDTH-sw)//2 + round(2*math.sin(frame/27))
        y0=(HEIGHT-sh)//2
        img=img.crop((x0,y0,x0+sw,y0+sh)).resize((WIDTH,HEIGHT),Image.Resampling.BICUBIC)
    return img.convert('RGB')

def probe(path: Path) -> dict:
    p=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def render(source: Path, output: Path, genre: str='sales_business', synthetic: bool=False) -> dict:
    check_genre(genre)
    if not source.is_file():
        raise FileNotFoundError(source)
    meta=probe(source)
    video=next(s for s in meta['streams'] if s['codec_type']=='video')
    audio=[s for s in meta['streams'] if s['codec_type']=='audio']
    if (video['width'],video['height'])!=(1080,1920) or video['avg_frame_rate']!='30/1' or not audio:
        raise ValueError('Requires 1080x1920 30fps source with audio')
    if float(meta['format']['duration']) < (START_FRAME+FRAME_COUNT)/FPS:
        raise ValueError('Source too short for 18-21s insert')
    output.parent.mkdir(parents=True,exist_ok=True)
    frames=output.parent/'frames819'
    frames.mkdir(exist_ok=True)
    for i in range(FRAME_COUNT):
        render_frame(i,genre).save(frames/f'{i:03}.png',compress_level=2)
    subprocess.run([
        'ffmpeg','-hide_banner','-loglevel','error','-y',
        '-i',str(source),'-framerate','30','-start_number','0','-i',str(frames/'%03d.png'),
        '-filter_complex',f"[1:v]setpts=PTS-STARTPTS+{START_FRAME/FPS}/TB[insert];[0:v][insert]overlay={X}:{Y}:eof_action=pass:enable='gte(t,18)*lt(t,21)',format=yuv420p[v]",
        '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-threads','2',
        '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)
    ],check=True)
    out=probe(output)
    ov=next(s for s in out['streams'] if s['codec_type']=='video')
    report={
        'cycle':819,'source':source.name,'output':output.name,'genre':genre,'genre_count':len(GENRE_COLORS),
        'insert_frames':FRAME_COUNT,'insert_start_s':18.0,'insert_end_s':21.0,
        'width':ov['width'],'height':ov['height'],'fps':ov['avg_frame_rate'],
        'output_duration_s':float(out['format']['duration']),
        'synthetic_source':synthetic,'asset_source':'original procedural illustration, no third-party media',
        'inherited_audio_preserved_as_aac_copy':True,
        'japanese_speech_semantic_alignment_verified':False,'asset_rights_verified':False,
        'phone_playback_verified':False,'publication_approved':False,'auto_post':False,
    }
    (output.parent/'qa819.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--genre',choices=sorted(GENRE_COLORS),default='sales_business')
    ap.add_argument('--synthetic',action='store_true')
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,a.synthetic),ensure_ascii=False))
