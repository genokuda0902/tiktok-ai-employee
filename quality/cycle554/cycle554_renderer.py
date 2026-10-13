#!/usr/bin/env python3
"""Cycle554 review-only genre-neutral proof UI. Reimplementation, synthetic data.
Requires Pillow, FFmpeg, Japanese Noto CJK fonts. No new TTS or auto-post.
"""
from __future__ import annotations
import argparse
import functools
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, SECONDS = 540, 960, 30, 20
START, END = 9.0, 12.0
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = ('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス',
          '転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')

@functools.lru_cache(maxsize=40)
def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def validate_proof(values, total, labels, genre, scene_start=START, scene_end=END):
    if genre not in GENRES: raise ValueError('unknown genre')
    if not isinstance(values, (list, tuple)) or not 1 <= len(values) <= 8:
        raise ValueError('need 1..8 values')
    if any(type(v) is not int or v < 0 for v in values):
        raise ValueError('synthetic counts must be nonnegative integers')
    if type(total) is not int or sum(values) != total:
        raise ValueError('false arithmetic claim')
    if len(labels) != len(values) or any(not isinstance(s,str) or not s or len(s)>10 for s in labels):
        raise ValueError('invalid labels')
    if not 0 <= scene_start < scene_end <= SECONDS or scene_end-scene_start > 5:
        raise ValueError('invalid timeline')
    return True

def center(d, pos, txt, size=24, color='#15263b', bold=False):
    d.text(pos, txt, anchor='mm', font=font(size,bold), fill=color)

def scene_frame(t, values=(120,150,200,250), labels=('1月','2月','3月','4月'),
                genre='AI・仕事効率化'):
    """Spreadsheet-like recreation; never actual Excel or LibreOffice footage."""
    validate_proof(values,sum(values),labels,genre)
    if not 0 <= t <= 3: raise ValueError('scene t outside 0..3')
    im=Image.new('RGB',(WIDTH,HEIGHT),'#081b2a')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((24,100,516,159),radius=12,fill='#123c4b',outline='#36d6c7',width=2)
    center(d,(270,128),'実操作風デモ｜式で検算',26,'white',True)
    center(d,(270,192),'売上データから、合計を確認',28,'white',True)
    d.rounded_rectangle((25,236,515,729),radius=13,fill='#f8fafc',outline='#8cc3c2',width=3)
    d.rounded_rectangle((27,238,513,280),radius=12,fill='#176d56')
    d.rectangle((27,263,513,283),fill='#176d56')
    center(d,(270,259),'月別売上データ  |  再現画面',20,'white',True)
    d.rectangle((39,296,501,347),fill='#e3ebef')
    center(d,(67,321),'fx',24,'#147d60',True)
    stage=0 if t < 1.0 else (1 if t < 2.05 else 2)
    formula='B2:B5 を選択' if stage==0 else '=SUM(B2:B5)'
    d.text((103,306),formula,font=font(22,True),fill='#18304a')
    xs=[43,94,245,487]; ys=[365,420,487,554,621,688]
    for r in range(5):
        for c in range(3):
            x0,x1=xs[c],xs[c+1];y0,y1=ys[r],ys[r+1]
            fill='#dce9ef' if r==0 else ('#eff5f7' if r%2 else 'white')
            d.rectangle((x0,y0,x1,y1),fill=fill,outline='#b7cbd1',width=1)
    center(d,(67,390),'#',20,'#5a6d7a',True)
    center(d,(167,390),'月',22,'#254358',True)
    center(d,(363,390),'売上',22,'#254358',True)
    for i,(label,value) in enumerate(zip(labels,values)):
        y=(ys[i+1]+ys[i+2])/2
        center(d,(67,y),str(i+2),18,'#61798a')
        center(d,(167,y),label,24,'#183449',True)
        center(d,(363,y),str(value),28,'#12384b',True)
    d.rectangle((94,688,487,727),fill='#e4f2ed',outline='#b7cbd1',width=1)
    center(d,(167,706),'合計',19,'#183449',True)
    center(d,(363,706),str(sum(values)) if stage==2 else '—',22,'#08795b',True)
    if stage==0:
        height=int(55+202*min(1,t/0.75))
        d.rectangle((246,421,486,421+height),outline='#0ca879',width=5)
        d.rounded_rectangle((70,753,470,813),radius=12,fill='#0d605c',outline='#6dffe1',width=2)
        center(d,(270,783),'① 4か月の数値を選択',26,'white',True)
    elif stage==1:
        d.rectangle((246,421,486,688),outline='#0ca879',width=5)
        d.rounded_rectangle((70,753,470,813),radius=12,fill='#0d605c',outline='#6dffe1',width=2)
        center(d,(270,783),'② SUM関数で合計',26,'white',True)
    else:
        d.rectangle((246,688,486,727),outline='#0ca879',width=4)
        d.rounded_rectangle((70,753,470,813),radius=12,fill='#08795b',outline='#d5f66c',width=3)
        center(d,(270,779),f'③ 検算結果：{sum(values)}',27,'white',True)
    d.text((27,847),'※数値・画面は架空の再現デモです',font=font(18),fill='#d7e8ed')
    d.text((27,910),'HUMAN REVIEW / NOT APPROVED',font=font(13),fill='#b6c8d7')
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def make(base, output):
    base,output=Path(base),Path(output)
    info=probe(base)
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'])!=(1080,1920) or abs(float(info['format']['duration'])-SECONDS)>.05:
        raise ValueError('baseline must be 1080x1920, 20s')
    if not any(s['codec_type']=='audio' for s in info['streams']):
        raise ValueError('baseline audio stream missing')
    output.parent.mkdir(parents=True,exist_ok=True)
    segment=output.parent/'scene_9_to_12.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{WIDTH}x{HEIGHT}',
         '-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p',str(segment)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(round((END-START)*FPS)):
            proc.stdin.write(scene_frame(n/FPS).tobytes())
    finally:
        proc.stdin.close()
    if proc.wait(): raise RuntimeError('scene encoder failed')
    fc=(f'[1:v]scale=1080:1920:flags=lanczos,setpts=PTS-STARTPTS+{START}/TB[scene];'
        f"[0:v][scene]overlay=eof_action=pass:shortest=0:enable='gte(t,{START})*lt(t,{END})',format=yuv420p[v]")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base),'-i',str(segment),
        '-filter_complex',fc,'-map','[v]','-map','0:a:0','-frames:v','600','-c:v','libx264','-preset','veryfast',
        '-crf','22','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)],check=True)
    meta=probe(output)
    vv=next(s for s in meta['streams'] if s['codec_type']=='video')
    if (vv['width'],vv['height'],int(vv['nb_frames']))!=(1080,1920,600):
        raise RuntimeError('failed frame gate')
    if abs(float(meta['format']['duration'])-20)>.05:
        raise RuntimeError('failed duration gate')
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args()
    print(make(args.base,args.output))
