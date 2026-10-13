#!/usr/bin/env python3
"""Cycle553 review-only result-first hook. Reimplementation, synthetic values only.

Usage: python cycle553_renderer.py --base cycle552.mp4 --output cycle553.mp4
Requires Pillow and FFmpeg. Does not create speech, publish, or authorize assets.
"""
import argparse, functools, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,SECONDS=540,960,30,20
HOOK=2.4
VALUES=(120,150,200,250)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

@functools.lru_cache(maxsize=32)
def font(n): return ImageFont.truetype(FONT,n)

def ease(x):
    x=max(0,min(1,x));return 1-(1-x)**3

def valid_scene(values, claim, headline):
    if not values or len(values)>8 or any(type(v)!=int or v<0 for v in values):
        raise ValueError('approved demo requires 1..8 nonnegative integer values')
    if sum(values)!=claim: raise ValueError('false claim: result does not equal input sum')
    if not headline or len(headline)>22: raise ValueError('headline too long')
    return True

def center(draw,xy,txt,size,fill,stroke=0,sc='#071222'):
    draw.text(xy,txt,font=font(size),anchor='mm',fill=fill,stroke_width=stroke,stroke_fill=sc)

def render_frame(t, values=VALUES, headline='この集計、まだ手入力？'):
    valid_scene(values,sum(values),headline)
    im=Image.new('RGB',(W,H),'#061427');d=ImageDraw.Draw(im)
    # Graphic language: bold outlined text, cyan and yellow evidence, not borrowed footage.
    for i in range(12):
        x=(i*89+int(15*t))%W; d.line((x,0,x-110,H),fill='#102a47',width=2)
    d.rounded_rectangle((26,66,514,124),radius=16,fill='#0c3854',outline='#30dcf2',width=3)
    center(d,(270,95),'AI時短ラボ  |  20秒で実演',23,'#e6faff')
    # Result is shown from frame 0: actual synthetic values, no fake time savings.
    d.rounded_rectangle((25,160,515,520),radius=22,fill='#0b253d',outline='#3ca2cc',width=3)
    center(d,(270,199),'4か月の売上をグラフ化',29,'white')
    base=451
    for i,v in enumerate(values):
        x=77+i*110; height=round(164*v/max(values))
        # Intro chart grows rapidly, but completed value is labelled only after its bar settles.
        progress=ease(t/.35)
        h=int(height*progress)
        if h>1: d.rounded_rectangle((x,base-h,x+62,base),radius=7,fill='#22d3de')
        if progress>=.99: center(d,(x+31,base-h-22),str(v),23,'#ffffff')
        center(d,(x+31,base+23),f'{i+1}月',20,'#e5f5fa')
    d.rounded_rectangle((96,530,444,614),radius=19,fill='#066c63',outline='#9bffe7',width=3)
    center(d,(270,558),'検算後の合計',21,'#c8fff5')
    center(d,(270,590),str(sum(values)),39,'white',2)
    # Kinetic headline uses the reference's high-contrast hierarchy, not its copyrighted frames.
    y=int(685+20*(1-ease(t/.28)))
    center(d,(270,y),headline,40,'#ffffff',3,'#091a28')
    if t>=.8:
        a=ease((t-.8)/.22)
        d.rounded_rectangle((30,738,510,845),radius=18,fill='#102b44',outline='#f8d347',width=3)
        center(d,(270,773),'Excel  →  AI補助  →  グラフ',26,'#f9dc56')
        center(d,(270,817),'入力 → 集計 → 人が検算',24,'white')
    else:
        center(d,(270,799),'最初に「完成結果」を見せる',24,'#ffe06c')
    d.text((27,881),'※数値・操作は架空のデモです',font=font(18),fill='#e0e8f0')
    d.text((27,924),'HUMAN REVIEW / PUBLICATION NOT APPROVED',font=font(12),fill='#b6c8d7')
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def make(base,output):
    base,output=Path(base),Path(output)
    info=probe(base); v=next(s for s in info['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'])!=(1080,1920) or abs(float(info['format']['duration'])-SECONDS)>.1:
        raise ValueError('invalid baseline resolution/duration')
    if not any(s['codec_type']=='audio' for s in info['streams']):raise ValueError('baseline audio missing')
    output.parent.mkdir(parents=True,exist_ok=True)
    segment=output.parent/'cycle553_hook_segment.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p',str(segment)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for frame in range(round(HOOK*FPS)):
        p.stdin.write(render_frame(frame/FPS).tobytes())
    # Reverse first nine frames to make the final frame match the first frame.
    for frame in range(9):
        p.stdin.write(render_frame((8-frame)/FPS).tobytes())
    p.stdin.close()
    if p.wait()!=0:raise RuntimeError('segment encoding failed')
    # Re-use first 0.3s of new hook at the very end for a visual loop.
    fc=('[1:v]scale=1080:1920:flags=lanczos,split=2[head][tail];'
        '[head]trim=start=0:duration=2.4,setpts=PTS-STARTPTS[h];'
        '[tail]trim=start=2.4:duration=0.3,setpts=PTS-STARTPTS+19.7/TB[l];'
        "[0:v][h]overlay=eof_action=pass:shortest=0:enable='lt(t,2.4)'[v0];"
        "[v0][l]overlay=eof_action=pass:shortest=0:enable='gte(t,19.7)',format=yuv420p[v]")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base),'-i',str(segment),'-filter_complex',fc,'-map','[v]','-map','0:a:0','-frames:v','600','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)],check=True)
    m=probe(output); vv=next(s for s in m['streams'] if s['codec_type']=='video')
    if (vv['width'],vv['height'],int(vv.get('nb_frames',0)))!=(1080,1920,600):raise RuntimeError('frame gate failed')
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();print(make(a.base,a.output))
