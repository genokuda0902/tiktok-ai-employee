"""cycle908 — deterministic, clearly fictional, mobile-legible animated comparison chart.

This renderer adds a short *review-only* data-to-chart visual to a pre-existing
Japanese-captioned video. It does not transcribe audio, approve rights or post.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

GENRES = ('ai_work','business','education','finance','health','lifestyle',
          'technology','travel','food','entertainment')
MONTHS = ('4月','5月','6月')
SAMPLE_A = (12,16,18)
SAMPLE_B = (8,9,12)
FPS = 30
FRAMES = 81
START = 10.9
PANEL_X, PANEL_Y = 90, 265
PANEL_W, PANEL_H = 900, 990
CAPTION_TOP = 1280
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'

def font(size, bold=False):
    from PIL import ImageFont
    paths = ['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else
             '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
             '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']
    for p in paths:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    raise RuntimeError('Noto Japanese font required for rendering')

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def run(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(str(args[:6])+': '+p.stderr[-2000:])
    return p.stdout

def validate(data):
    if data.get('genre') not in GENRES: raise ValueError('unknown genre')
    if data.get('synthetic') is not True: raise ValueError('must mark values synthetic')
    if data.get('publication_approved') is not False: raise ValueError('publication approval must be false')
    if data.get('employee_approved') is not False: raise ValueError('employee approval must be false')
    if data.get('asset_rights_approved') is not False: raise ValueError('rights must remain unapproved')
    if data.get('independent_asr_verified') is not False: raise ValueError('ASR must remain unverified')
    if data.get('automatic_posting') is not False: raise ValueError('no automatic posting')
    if not re.fullmatch(r'[a-f0-9]{64}',data.get('source_sha256','')): raise ValueError('source digest required')
    values=data.get('values')
    if not isinstance(values,dict) or set(values)!={'A','B'}: raise ValueError('two series required')
    for v in values.values():
        if not isinstance(v,list) or len(v)!=3 or any(type(n) is not int or n<0 or n>999 for n in v):
            raise ValueError('three nonnegative integer data points required')
    return True

def ease(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)

def axis_max(values):
    peak=max(max(v) for v in values.values())
    return max(20, ((peak+19)//20)*20)

def chart_heights(values,progress,max_height=315):
    m=axis_max(values)
    return {k:[round(n/m*max_height*ease(progress)) for n in nums] for k,nums in values.items()}

def draw_center(d, xy, txt, f, fill):
    x,y=xy; b=d.textbbox((0,0),txt,font=f)
    d.text((x-(b[2]-b[0])/2,y),txt,font=f,fill=fill)

def frame(data, i):
    if not 0<=i<FRAMES: raise ValueError('frame outside range')
    from PIL import Image, ImageDraw
    im=Image.new('RGBA',(PANEL_W,PANEL_H),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((4,4,PANEL_W-5,PANEL_H-5),radius=38,fill=(4,20,35,249),outline=(80,205,211,255),width=5)
    d.rounded_rectangle((26,26,874,164),radius=24,fill=(13,65,81,255))
    d.text((52,44),'数字からグラフへ',font=font(54,True),fill='white')
    d.text((55,111),'月別データを比較して可視化',font=font(29),fill=(182,225,230))
    d.rounded_rectangle((637,50,850,103),radius=14,fill=(138,56,40,255))
    draw_center(d,(743,58),'架空データ',font(29,True),'white')
    d.text((65,199),'営業A',font=font(35,True),fill=(86,229,220))
    d.rectangle((36,207,55,231),fill=(86,229,220))
    d.text((272,199),'営業B',font=font(35,True),fill=(255,186,99))
    d.rectangle((243,207,262,231),fill=(255,186,99))
    top,base=306,698
    for tick in range(5):
        val=axis_max(data['values'])*tick//4
        y=base-round(tick/4*315)
        d.line((100,y,820,y),fill=(50,78,93,255),width=2)
        d.text((48,y-17),str(val),font=font(23),fill=(156,180,195))
    p=ease((i-6)/53)
    h=chart_heights(data['values'],p)
    for idx,month in enumerate(MONTHS):
        group_x=151+idx*239
        for key,dx,color in (('A',0,(86,229,220,255)),('B',84,(255,186,99,255))):
            bh=h[key][idx];x=group_x+dx
            if bh: d.rounded_rectangle((x,base-bh,x+71,base),radius=9,fill=color)
            if i>=20:
                draw_center(d,(x+35,base-bh-46),str(data['values'][key][idx]),font(32,True),'white')
        draw_center(d,(group_x+77,724),month,font(34,True),(224,240,242))
    d.rounded_rectangle((36,794,864,894),radius=20,fill=(13,54,68,255))
    d.text((57,808),'3か月の合計',font=font(31,True),fill=(207,229,232))
    d.text((351,803),f"A {sum(data['values']['A'])}",font=font(47,True),fill=(86,229,220))
    d.text((607,803),f"B {sum(data['values']['B'])}",font=font(47,True),fill=(255,186,99))
    d.text((55,923),'※ 検証用サンプル。実際の業務実績ではありません',font=font(24),fill=(196,207,216))
    return im

def probe(path):
    p=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(s for s in p['streams'] if s['codec_type']=='video')
    a=next(s for s in p['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames'])) != ('h264',1080,1920,'30/1',691): raise ValueError('video spec mismatch')
    if (a['codec_name'],a['sample_rate']) != ('aac','48000'): raise ValueError('audio spec mismatch')
    return {'width':1080,'height':1920,'fps':30,'frames':691,'duration':float(p['format']['duration']),'audio':'aac/48000'}

def audio_digest(path,work):
    dest=Path(work)/(Path(path).stem+'.aac')
    run(['ffmpeg','-v','error','-y','-i',str(path),'-vn','-c:a','copy','-f','adts',str(dest)])
    return sha256(dest)

def render(source,output,manifest,work):
    source=Path(source).resolve();output=Path(output).resolve();work=Path(work).resolve()
    data=json.loads(Path(manifest).read_text(encoding='utf-8'));validate(data)
    if source==output or output.exists(): raise ValueError('output must not overwrite source')
    if sha256(source)!=data['source_sha256']: raise ValueError('source digest mismatch')
    probe(source)
    if PANEL_Y+PANEL_H>=CAPTION_TOP: raise AssertionError('caption region overlap')
    work.mkdir(parents=True,exist_ok=True);frames=work/'frames';frames.mkdir(exist_ok=True)
    for i in range(FRAMES): frame(data,i).save(frames/f'chart_{i:03d}.png')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate','30','-start_number','0','-i',str(frames/'chart_%03d.png'),
         '-filter_complex',f'[1:v]format=rgba,setpts=PTS+{START}/TB[chart];[0:v][chart]overlay={PANEL_X}:{PANEL_Y}:shortest=0:eof_action=pass:repeatlast=0:format=auto[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
         '-pix_fmt','yuv420p','-c:a','copy','-frames:v','691','-movflags','+faststart',str(output)]
    run(cmd)
    result=probe(output)
    run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
    if audio_digest(source,work)!=audio_digest(output,work): raise AssertionError('audio changed')
    return {'status':STATUS,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'audio_adts_identical':True,'full_decode_pass':True,'fictional_values':data['values'],
            'independent_japanese_asr':'UNAVAILABLE','semantic_caption_alignment':'NOT_VERIFIED',
            'rights_approved':False,'employee_approved':False,'publication_allowed':False,**result}

def publication_gate(_):
    raise PermissionError('PUBLICATION_NOT_APPROVED: independent ASR, rights, human review and device playback missing')

def main():
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','work','report'):p.add_argument('--'+k,required=True)
    a=p.parse_args();report=render(a.source,a.output,a.manifest,a.work)
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
