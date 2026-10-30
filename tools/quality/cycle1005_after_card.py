#!/usr/bin/env python3
"""Offline repair of duplicated Japanese AFTER text in scene 06 (review-only)."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = (1080, 1920)
FPS = 30
PATCH_BOX = (109, 934, 952, 1186)
CAPTION_TOP = 1325
GENRES = {
    'ai_work':'#23D5D0', 'business':'#E8BC4C', 'finance':'#A9DB48',
    'education':'#FFB766', 'health':'#B6DD56', 'travel':'#76BDF6',
    'cooking':'#7BABFF', 'lifestyle':'#F4A8E8',
    'technology':'#F0E04E', 'entertainment':'#C39FFF',
}
COPY = ('週次報告の「冒頭」だけ', '数字を残し、3行に要約')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def make_patch(genre='ai_work', font_path=FONT):
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    if not Path(font_path).is_file():
        raise FileNotFoundError('Japanese font missing')
    if PATCH_BOX[3] >= CAPTION_TOP:
        raise AssertionError('patch touches captions')
    im = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0,y0,x1,y1 = PATCH_BOX
    d.rounded_rectangle((x0,y0,x1,y1), radius=20, fill='#0B2634')
    d.rounded_rectangle((123,943,315,998), radius=12, fill=GENRES[genre])
    label_font = ImageFont.truetype(font_path, 31)
    main_font = ImageFont.truetype(font_path, 47)
    sub_font = ImageFont.truetype(font_path, 44)
    d.text((146,946), 'AFTER', font=label_font, fill='#061825')
    assert d.textbbox((0,0),COPY[0],font=main_font)[2] < x1-140
    assert d.textbbox((0,0),COPY[1],font=sub_font)[2] < x1-140
    d.text((128,1010), COPY[0], font=main_font, fill='#F5FBFF')
    d.text((128,1093), COPY[1], font=sub_font, fill=GENRES[genre])
    return im

def render(source, output, genre='ai_work', start=14.55, end=17.12,
           font_path=FONT):
    source,output = Path(source),Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    if source.resolve()==output.resolve(): raise ValueError('refuse source overwrite')
    if not (0 <= start < end): raise ValueError('invalid window')
    probe=subprocess.run(['ffprobe','-v','error','-select_streams','v:0',
        '-show_entries','stream=width,height,r_frame_rate', '-of','json',str(source)],
        capture_output=True,text=True,check=True)
    v=json.loads(probe.stdout)['streams'][0]
    if (v['width'],v['height'],v['r_frame_rate']) != (1080,1920,'30/1'):
        raise ValueError('expected 1080x1920 at 30fps')
    output.parent.mkdir(parents=True,exist_ok=True)
    patch=output.with_suffix('.patch.png')
    make_patch(genre,font_path).save(patch)
    filt=f"[0:v][1:v]overlay=0:0:format=auto:enable='between(t,{start},{end})'[v]"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-i',str(patch),'-filter_complex',filt,
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','17','-pix_fmt','yuv420p','-c:a','copy',
         '-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)]
    try:
        subprocess.run(cmd,check=True,timeout=240)
    finally:
        patch.unlink(missing_ok=True)
    return {'start':start,'end':end,'genre':genre,'copy':COPY,'patch_box':PATCH_BOX,
            'output':str(output),'publication':'NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--start',type=float,default=14.55)
    p.add_argument('--end',type=float,default=17.12)
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,args.start,args.end),ensure_ascii=False))
