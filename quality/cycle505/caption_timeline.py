#!/usr/bin/env python3
"""Review-only Japanese caption rhythm renderer. No voice synthesis or auto posting."""
from __future__ import annotations
import argparse, json, math, subprocess
from pathlib import Path

GENRES={'ai_work','gadgets','study','travel','cooking','beauty','home','fitness','history','business'}
W,H=1080,1920

def validate(data):
    if data.get('genre') not in GENRES: raise ValueError('unknown genre')
    if data.get('rights')!='original_procedural': raise ValueError('rights not approved')
    if data.get('publication')!='NOT_APPROVED' or data.get('human_review')!='HUMAN_REVIEW' or data.get('auto_post') is not False:
        raise ValueError('fail closed: publication not allowed')
    if data.get('narration_status')!='NOT_AVAILABLE': raise ValueError('narration cannot be certified here')
    clips=data.get('captions')
    if not isinstance(clips,list) or not 5<=len(clips)<=12: raise ValueError('caption count')
    previous=0.0
    for c in clips:
        if set(c)!={'start','end','text','tag'}: raise ValueError('invalid caption keys')
        s,e=c['start'],c['end']
        if not all(type(t) in (int,float) and math.isfinite(t) for t in (s,e)): raise ValueError('non-finite time')
        if not 0<=s<e<=20 or e-s<1 or abs(s-previous)>1e-7: raise ValueError('invalid caption time / gap / overlap')
        previous=e
        if not isinstance(c['text'],str) or not 2<=len(c['text'])<=24 or any(x in c['text'] for x in ['\n','{','}','\\']): raise ValueError('unsafe caption text')
        if c['tag'] not in ('HOOK','INPUT','ACTION','PROOF','RESULT','CTA'): raise ValueError('caption tag')
    if abs(clips[0]['start'])>1e-6 or abs(clips[-1]['end']-20)>1e-6: raise ValueError('full 20s coverage required')
    return clips

def ass_time(t):
    h=int(t//3600);m=int(t%3600//60);s=t%60
    return f'{h}:{m:02d}:{s:05.2f}'

def build_ass(data,path):
    clips=validate(data)
    header='''[Script Info]
Title: Review-only Japanese caption timing
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans CJK JP,54,&H00FFFFFF,&H0000FFFF,&H0010161C,&HD9081522,-1,0,0,0,100,100,0,0,3,4,0,2,90,190,410,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    rows=[]
    for c in clips:
        rows.append(f"Dialogue: 0,{ass_time(c['start'])},{ass_time(c['end'])},Default,,0,0,0,,{{\\fad(120,100)}}{c['text']}")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(header+'\n'.join(rows)+'\n',encoding='utf-8')

def probe(path):
    p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height:format=duration','-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def render(src,out,manifest,ass_path):
    validate(manifest)
    info=probe(src)
    v=next((s for s in info['streams'] if s['codec_type']=='video'),{})
    if (v.get('width'),v.get('height'))!=(W,H) or abs(float(info['format']['duration'])-20)>.08:
        raise ValueError('requires 1080x1920 / 20-second review source')
    if not any(s['codec_type']=='audio' for s in info['streams']): raise ValueError('source audio track missing')
    if src.resolve()==out.resolve(): raise ValueError('cannot overwrite input')
    build_ass(manifest,ass_path)
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(src),'-vf',f'ass={ass_path.as_posix()}',
         '-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
         '-pix_fmt','yuv420p','-r','30','-c:a','copy','-t','20','-movflags','+faststart',
         '-metadata','comment=HUMAN_REVIEW; NOT_APPROVED',str(out)]
    subprocess.run(cmd,check=True)
    return cmd

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--ass',type=Path,required=True)
    a=p.parse_args();m=json.loads(a.manifest.read_text(encoding='utf-8'));cmd=render(a.input,a.output,m,a.ass)
    print(json.dumps({'status':'REVIEW_ONLY','output':str(a.output),'captions':len(m['captions']),'command':cmd},ensure_ascii=False))
