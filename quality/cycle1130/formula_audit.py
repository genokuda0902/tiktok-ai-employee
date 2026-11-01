#!/usr/bin/env python3
"""Review-only source-cell/formula consistency repair for ten genres.
The private manifest is authored from human-inspected evidence, NOT OCR.
No source video, audio, screenshot, private manifest or fonts are committed.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def run(args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(p.stderr.decode('utf8','replace')[-1800:])
    return p.stdout

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def audio_hash(p):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()

def inspect(p):
    j=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
    v=[s for s in j['streams'] if s['codec_type']=='video']
    a=[s for s in j['streams'] if s['codec_type']=='audio']
    subs=[s for s in j['streams'] if s['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or subs:raise ValueError('one video, one audio, no soft subtitles')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac' or a[0]['sample_rate']!='48000':raise ValueError('H264/AAC48 required')
    if (v[0]['width'],v[0]['height']) not in ((1080,1920),(540,960)) or v[0]['avg_frame_rate']!='30/1':raise ValueError('portrait 30fps required')
    return v[0]['width'],v[0]['height'],int(v[0]['nb_frames']),float(j['format']['duration'])

def validate(m,source_sha,frames):
    if set(m)!={'policy','asset_approval','source_sha256','genre','sheet','patch'}:raise ValueError('manifest keys')
    if m['policy']!=POLICY or m['asset_approval']!='private_review_only' or m['source_sha256']!=source_sha:raise ValueError('approval/source')
    if m['genre'] not in GENRES:raise ValueError('genre')
    s=m['sheet']
    if set(s)!={'columns','selected_cell','visible_formula','visible_total','other_total','incorrect_overlay'}:raise ValueError('sheet keys')
    cols=s['columns']
    if not isinstance(cols,dict) or len(cols)!=2 or any(not re.fullmatch('[A-Z]',k) for k in cols):raise ValueError('columns')
    if any(not isinstance(v,list) or not 2<=len(v)<=12 or any(type(n) is not int or abs(n)>999999 for n in v) for v in cols.values()):raise ValueError('source rows')
    if len({len(v) for v in cols.values()})!=1:raise ValueError('row count')
    sel=re.fullmatch(r'([A-Z])(\d+)',s['selected_cell'])
    form=re.fullmatch(r'=SUM\(([A-Z])(\d+):([A-Z])(\d+)\)',s['visible_formula'])
    if not sel or not form:raise ValueError('selection/formula')
    c,row=sel.group(1),int(sel.group(2))
    fc,start,ec,end=form.group(1),int(form.group(2)),form.group(3),int(form.group(4))
    if c not in cols or c!=fc or c!=ec or start!=2 or end!=len(cols[c])+1 or row!=end+1:raise ValueError('selected formula mismatch')
    if type(s['visible_total']) is not int or sum(cols[c])!=s['visible_total']:raise ValueError('total mismatch')
    other=[k for k in cols if k!=c]
    if len(other)!=1 or type(s['other_total']) is not int or sum(cols[other[0]])!=s['other_total']:raise ValueError('other total')
    if s['incorrect_overlay']==s['visible_formula'] or not re.fullmatch(r'=SUM\([A-Z]\d+:[A-Z]\d+\)',s['incorrect_overlay']):raise ValueError('not a safe correction')
    p=m['patch']
    if set(p)!={'start_frame','end_frame','bbox','text_origin'}:raise ValueError('patch keys')
    startf,endf=p['start_frame'],p['end_frame']
    if type(startf) is not int or type(endf) is not int or not 0<=startf<endf<=frames or endf-startf>90:raise ValueError('frame range')
    x0,y0,x1,y1=p['bbox'];x,y=p['text_origin']
    if not (0<=x0<x1<=1080 and 150<=y0<y1<=340 and x1-x0<=700 and y1-y0<=100 and x0<=x<=x1 and y0<=y<=y1):raise ValueError('patch geometry')
    return startf,endf

def make_overlay(m,width,height):
    scale=width/1080
    im=Image.new('RGBA',(width,height));d=ImageDraw.Draw(im)
    d.rectangle([round(v*scale) for v in m['patch']['bbox']],fill=(0,18,32,255))
    if not Path(FONT).is_file():raise FileNotFoundError('Noto CJK Bold font required')
    f=ImageFont.truetype(FONT,round(34*scale))
    x,y=m['patch']['text_origin']
    d.text((round(x*scale),round(y*scale)),'① 数式：'+m['sheet']['visible_formula'],font=f,fill=(246,248,255,255))
    return im

def render(source,output,manifest,report):
    source,output,manifest,report=map(lambda x:Path(x).resolve(),(source,output,manifest,report))
    if len({source,output,manifest,report})!=4 or output.exists() or report.exists():raise ValueError('unsafe overwrite')
    w,h,n,duration=inspect(source)
    m=json.loads(manifest.read_text(encoding='utf8'))
    start,end=validate(m,sha(source),n)
    output.parent.mkdir(parents=True,exist_ok=True)
    overlay=output.parent/'formula_overlay.private.png'
    if overlay.exists():raise ValueError('overlay exists')
    try:
        make_overlay(m,w,h).save(overlay)
        filt=f"[0:v][1:v]overlay=0:0:format=auto:enable='between(n,{start},{end-1})'[v]"
        run(['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-i',str(source),'-loop','1','-framerate','30','-i',str(overlay),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-frames:v',str(n),'-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
    finally:overlay.unlink(missing_ok=True)
    w2,h2,n2,d2=inspect(output)
    if (w,h,n)!=(w2,h2,n2) or abs(duration-d2)>.05:raise AssertionError('video regression')
    if audio_hash(source)!=audio_hash(output):raise AssertionError('AAC changed')
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-f','null','-','-map','0:a:0','-f','null','-'])
    qa={'policy':POLICY,'source_sha256':sha(source),'output_sha256':sha(output),'resolution':[w2,h2],'frames':n2,'duration':d2,'changed_frames':[start,end-1],'visible_formula':m['sheet']['visible_formula'],'selected_cell':m['sheet']['selected_cell'],'full_av_decode':'PASS','audio_adts_unchanged':True,'independent_japanese_asr':'NOT_VERIFIED','rights':'NOT_VERIFIED','phone_playback':'NOT_VERIFIED'}
    report.write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
    return qa

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('source','output','manifest','report'):ap.add_argument('--'+k,required=True)
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False))
