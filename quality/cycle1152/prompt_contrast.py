#!/usr/bin/env python3
"""Review-only, ten-genre simultaneous before/after prompt clarity card.

Source video and generated overlays remain local. No posting, upload, or approval.
This is a new reimplementation, not the original v33 engine.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES={'ai':'#38d9d1','business':'#6dd1f5','money':'#e8c16b','learning':'#9abaff',
'health':'#75d5a7','food':'#efb97e','travel':'#80c8e8','beauty':'#efafd2',
'career':'#a2a5ff','life':'#a7dfb0'}
W,H,FPS=1080,1920,30
PANEL=(64,354,1016,1068)
CAPTION_TOP=1280
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def probe(path):
    j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(x for x in j['streams'] if x['codec_type']=='video')
    a=next(x for x in j['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['avg_frame_rate']) != ('h264',W,H,'30/1'):
        raise ValueError('Expected 1080x1920 H264 30fps')
    if (a['codec_name'],int(a['sample_rate']))!=('aac',48000):
        raise ValueError('Expected AAC 48kHz')
    return float(j['format']['duration']),int(v.get('nb_frames') or round(float(j['format']['duration'])*FPS))

def validate(m,source,duration):
    if m.get('policy')!=POLICY or m.get('asset_approval')!='review_only_no_publication' or m.get('manual_post_only') is not True:
        raise ValueError('Fail closed: publication and approval policy')
    if m.get('source_sha256')!=sha256(source):raise ValueError('Source hash mismatch')
    if m.get('genre') not in GENRES:raise ValueError('Unknown genre')
    t=m.get('window')
    if not isinstance(t,list) or len(t)!=2 or any(type(x) not in (int,float) for x in t):raise ValueError('Invalid window')
    a,b=t
    if not (0.1<=a<b<=duration-0.1 and b-a>=1.1):raise ValueError('Window invalid or too short')
    if PANEL[3]>=CAPTION_TOP:raise ValueError('Caption protected zone overlap')
    return float(a),float(b)

def font(size,bold=True):return ImageFont.truetype(FONT if bold else REG,size)

def draw_overlay(m,out):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    x0,y0,x1,y1=PANEL;accent=GENRES[m['genre']]
    d.rounded_rectangle((x0,y0,x1,y1),radius=28,fill=(4,19,37,250),outline=(90,131,149,255),width=3)
    d.rounded_rectangle((x0+14,y0+15,x1-14,y0+96),radius=16,fill=(6,52,66,255))
    d.text((x0+40,y0+25),'指示を具体化すると、何が変わる？',font=font(39),fill='white')
    left=(x0+22,y0+120,530,y1-28);right=(550,y0+120,x1-22,y1-28)
    d.rounded_rectangle(left,radius=21,fill=(34,43,60,255),outline=(136,147,161,255),width=3)
    d.rounded_rectangle(right,radius=21,fill=(9,54,64,255),outline=accent,width=5)
    d.rounded_rectangle((left[0]+17,left[1]+18,left[2]-17,left[1]+94),radius=12,fill=(71,76,91,255))
    d.rounded_rectangle((right[0]+17,right[1]+18,right[2]-17,right[1]+94),radius=12,fill=(13,105,113,255))
    d.text((left[0]+33,left[1]+24),'BEFORE',font=font(38),fill='white')
    d.text((right[0]+33,right[1]+24),'AFTER',font=font(38),fill='white')
    d.text((left[0]+26,left[1]+145),'「集計して」',font=font(41),fill='white')
    d.text((left[0]+26,left[1]+240),'何を？',font=font(39),fill='#ccd5df')
    d.text((left[0]+26,left[1]+305),'どのデータ？',font=font(37),fill='#ccd5df')
    d.text((left[0]+26,left[1]+370),'どんな形？',font=font(37),fill='#ccd5df')
    for i,(label,desc) in enumerate([('目的','月別売上を集計'),('条件','元データと照合'),('形式','表と要点で出力')]):
        yy=right[1]+132+i*135
        d.rounded_rectangle((right[0]+18,yy,right[2]-18,yy+114),radius=13,fill=(9,71,82,255))
        d.text((right[0]+31,yy+8),label,font=font(28),fill=accent)
        d.text((right[0]+31,yy+47),desc,font=font(31),fill='white')
    # Opaque footer masks the inherited sequential BEFORE/AFTER panel (y=1070..1218).
    # Without this, both panels are visible and text appears duplicated.
    d.rounded_rectangle((64,1070,1016,1218),radius=20,fill=(4,19,37,255),outline=accent,width=3)
    d.text((96,1096),'POINT  目的・条件・形式をセットで伝える',font=font(32),fill='white')
    d.text((96,1153),'架空例／出力結果は必ず人が確認',font=font(26,False),fill='#d1e1e5')
    im.save(out)
    return PANEL

def render(source,output,manifest,workdir):
    source,output,manifest,workdir=map(Path,(source,output,manifest,workdir))
    if source.resolve()==output.resolve():raise ValueError('Refuse source overwrite')
    m=json.loads(manifest.read_text(encoding='utf-8'))
    duration,frames=probe(source);start,end=validate(m,source,duration)
    workdir.mkdir(parents=True,exist_ok=True)
    overlay=workdir/'private_prompt_contrast_overlay.png';draw_overlay(m,overlay)
    fade=min(.22,(end-start)/5)
    vf=(f'[1:v]format=rgba,fade=t=in:st={start}:d={fade}:alpha=1,'
        f'fade=t=out:st={end-fade}:d={fade}:alpha=1[ov];'
        '[0:v][ov]overlay=x=0:y=0:format=auto:shortest=1[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-loop','1','-framerate','30','-i',str(overlay),'-filter_complex',vf,
         '-map','[v]','-map','0:a:0','-map_metadata','0','-c:v','libx264',
         '-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-threads','4',
         '-c:a','copy','-t',f'{duration:.6f}','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    od,of=probe(output)
    if abs(od-duration)>.05 or of!=frames:raise RuntimeError(f'Frame/duration mismatch {of}/{frames}, {od}/{duration}')
    report={'policy':POLICY,'source_sha256':sha256(source),'output_sha256':sha256(output),
        'frames':of,'duration':od,'window':[start,end],'genre':m['genre'],
        'caption_protection':'Overlay alpha zero below y=1218; captions y>=1280 unchanged',
        'meaning_alignment':'NOT_VERIFIED_BY_ASR','publication_approved':False}
    (workdir/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--workdir',required=True)
    a=p.parse_args();print(json.dumps(render(a.source,a.output,a.manifest,a.workdir),ensure_ascii=False,indent=2))
