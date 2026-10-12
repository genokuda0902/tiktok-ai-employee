#!/usr/bin/env python3
"""cycle515: reusable first-1.5s proof-first motion; synthetic, review-only.
This is a new implementation, not recovered v33 code. Reference media is
never included. Caller must verify source rights. Output stays NOT_APPROVED.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1250,30
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES={'ai_work','beauty','relationship','money','sales','career','health','science','travel','products'}
def validate(m):
    if m.get('genre') not in GENRES: raise ValueError('unsupported genre')
    if m.get('rights')!='synthetic_local_review_only' or m.get('privacy_checked') is not True: raise ValueError('rights/privacy approval missing')
    if m.get('human_review')!='HUMAN_REVIEW' or m.get('publication')!='NOT_APPROVED' or m.get('auto_post') is not False: raise ValueError('fail-closed publication gate')
    nums=m.get('values')
    if not isinstance(nums,list) or len(nums)!=4 or any(type(n) is not int or n<0 or n>9999 for n in nums): raise ValueError('four bounded synthetic values required')
    if not isinstance(m.get('title'),str) or not 2<=len(m['title'])<=24: raise ValueError('short title required')
    if not isinstance(m.get('unit'),str) or len(m['unit'])>6: raise ValueError('invalid unit')
    return m
def font(sz,bold=True): return ImageFont.truetype(FONT if bold else REG,sz)
def smooth(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def frame(m,t):
    validate(m)
    im=Image.new('RGB',(540,625),'#071426');d=ImageDraw.Draw(im)
    for y in range(625):
        v=int(16+15*(y/625));d.line((0,y,540,y),fill=(7,20,v))
    d.rounded_rectangle((20,24,520,95),radius=20,fill='#123047',outline='#2c8496',width=2)
    d.text((38,41),'AI時短ラボ  /  架空データの実演',font=font(20),fill='#a9f7f0')
    d.text((25,115),m['title'],font=font(39),fill='#ffffff')
    d.text((26,172),'完成イメージを先に見せる',font=font(22),fill='#e6df87')
    d.rounded_rectangle((18,223,522,577),radius=24,fill='#f4fbff',outline='#53d9cb',width=3)
    d.rounded_rectangle((18,223,522,282),radius=20,fill='#0b726e')
    d.rectangle((18,257,522,282),fill='#0b726e')
    d.text((37,238),'4か月の売上 → グラフ',font=font(24),fill='#ffffff')
    nums=m['values'];peak=max(max(nums),1)
    for i,v in enumerate(nums):
        x=59+i*119;target=180*v/peak
        progress=smooth((t-0.12-i*.15)/.43)
        height=max(1,int(target*progress))
        d.rounded_rectangle((x,480-height,x+68,480),radius=7,fill='#0db6b0' if i==3 else '#2c9de0')
        if progress>.3: d.text((x+7,484),f'{i+1}月',font=font(16),fill='#29445a')
        if progress>.90: d.text((x,480-height-31),str(v),font=font(20),fill='#15364d')
    d.line((44,481,505,481),fill='#9db5c0',width=2)
    p=smooth((t-.68)/.55)
    d.rounded_rectangle((50,519,490,566),radius=10,fill='#d6f6ed')
    d.text((67,524),'合計',font=font(24),fill='#115d53')
    d.text((256,519),str(int(sum(nums)*p)),font=font(31),fill='#095a4d')
    if t>=.92:
        cx=395+int(65*smooth((t-.92)/.4));cy=492-int(24*smooth((t-.92)/.4))
        d.polygon([(cx,cy),(cx+12,cy+37),(cx+20,cy+26),(cx+33,cy+43),(cx+40,cy+38),(cx+27,cy+22),(cx+42,cy+19)],fill='#e7a84c',outline='#735b2e')
    d.text((30,591),'※ 架空の数値。実際のAI処理結果ではありません。',font=font(15,False),fill='#9fc7d2')
    return im
def run(cmd): subprocess.run(cmd,check=True)
def render(m,base,out,work):
    validate(m);base=Path(base);out=Path(out);work=Path(work);work.mkdir(parents=True,exist_ok=True)
    if not base.is_file():raise FileNotFoundError(base)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(base)]))
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'])!=(1080,1920):raise ValueError('base must be 1080x1920')
    if not any(s['codec_type']=='audio' for s in probe['streams']):raise ValueError('audio stream required; does not prove Japanese narration')
    duration=float(probe['format']['duration'])
    if not 19.95<=duration<=20.05:raise ValueError('20-second baseline required')
    frames=work/'frames';frames.mkdir(exist_ok=True)
    for i in range(45):frame(m,i/FPS).save(frames/f'{i:03d}.png')
    overlay=work/'hook.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','30','-i',str(frames/'%03d.png'),'-vf','scale=1080:1250:flags=lanczos,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20',str(overlay)])
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base),'-i',str(overlay),'-filter_complex',"[0:v][1:v]overlay=0:0:eof_action=pass:enable='lt(t,1.5)',format=yuv420p[v]",'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-r','30','-c:a','copy','-movflags','+faststart',str(out)])
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--base',required=True);p.add_argument('--out',required=True);p.add_argument('--work',required=True);a=p.parse_args()
    render(json.loads(Path(a.manifest).read_text()),a.base,a.out,a.work)
