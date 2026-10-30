#!/usr/bin/env python3
"""Review-only 8-cue progress rail + signal-only audio timing audit.

No ASR, no publishing, no uploads. User media remains local.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

GENRES = {
    'ai_work':'0x28ddc6', 'beauty':'0xf39cbb',
    'romance_psychology':'0xb5a0fa', 'money_saving':'0xe9c665',
    'sales_business':'0x64bbff', 'career':'0x5fd9df',
    'health_lifestyle':'0x62dca2', 'science_trivia':'0xdea8ff',
    'travel_food':'0xffad63', 'product_comparison_lifestyle':'0x68c9f7'
}

def run(args, binary=False):
    p = subprocess.run([str(x) for x in args], capture_output=True, check=True)
    return p.stdout if binary else p.stdout.decode('utf-8')

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def parse_srt(path):
    text=Path(path).read_text(encoding='utf-8-sig').strip()
    blocks=re.split(r'\n\s*\n',text)
    cues=[]
    def stamp(x):
        m=re.fullmatch(r'(\d\d):(\d\d):(\d\d),(\d{3})',x.strip())
        if not m:raise ValueError('invalid SRT timestamp')
        h,mi,s,ms=map(int,m.groups())
        if mi>=60 or s>=60:raise ValueError('invalid SRT time')
        return h*3600+mi*60+s+ms/1000
    for i,b in enumerate(blocks,1):
        lines=b.strip().splitlines()
        if len(lines)<3 or lines[0].strip()!=str(i):raise ValueError('SRT cue numbering')
        a=re.fullmatch(r'(.+?)\s*-->\s*(.+)',lines[1])
        if not a:raise ValueError('SRT cue arrow')
        start,end=stamp(a.group(1)),stamp(a.group(2))
        if end<=start or (cues and start<cues[-1]['end']-0.001):raise ValueError('overlap or negative cue')
        if not any(s.strip() for s in lines[2:]):raise ValueError('empty cue')
        cues.append({'start':start,'end':end,'text':' '.join(lines[2:])})
    if not cues:raise ValueError('empty SRT')
    return cues

def rail_filter(cues, genre):
    if genre not in GENRES:raise ValueError('unsupported genre')
    if len(cues)>10:raise ValueError('too many cues')
    w=112 if len(cues)==8 else int(960/len(cues)-8)
    step=121 if len(cues)==8 else int(960/len(cues))
    x0=56
    filters=[]
    for i,c in enumerate(cues):
        x=x0+step*i
        filters.append(f'drawbox=x={x}:y=136:w={w}:h=16:color=0x132d40@0.90:t=fill')
        filters.append(f"drawbox=x={x}:y=136:w={w}:h=16:color={GENRES[genre]}@0.90:t=fill:enable='gte(t,{c['start']:.3f})'")
        filters.append(f"drawbox=x={x}:y=132:w={w}:h=24:color=white@0.85:t=2:enable='between(t,{c['start']:.3f},{c['end']-0.001:.3f})'")
    return ','.join(filters)

def audio_audit(path,cues):
    raw=run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-vn','-ar','16000','-ac','1','-f','f32le','-'],True)
    a=array('f');a.frombytes(raw)
    def rms(start,end):
        lo=max(0,min(len(a),round(start*16000)))
        hi=max(lo,min(len(a),round(end*16000)))
        if hi==lo:return 0.0
        return round(math.sqrt(sum(x*x for x in a[lo:hi])/(hi-lo)),6)
    return {'kind':'MIXED_AUDIO_RMS_ONLY_NOT_SPEECH_RECOGNITION',
            'cues':[{'index':i+1,'start':c['start'],'end':c['end'],
                     'caption':c['text'],'signal_rms':rms(c['start'],c['end']),
                     'boundary_before_rms':rms(c['start']-.15,c['start']),
                     'boundary_after_rms':rms(c['start'],c['start']+.15),
                     'speech_text_match':'NOT_VERIFIED','speech_timing_match':'NOT_VERIFIED'}
                    for i,c in enumerate(cues)]}

def render(source,srt,output,report,genre,review_only,synthetic_ci=False):
    if not review_only:raise ValueError('review-only gate required')
    src,out,rep=Path(source).resolve(),Path(output).resolve(),Path(report).resolve()
    if not src.is_file() or out.exists() or rep.exists() or src==out:raise ValueError('source missing or destination exists')
    cues=parse_srt(srt)
    if len(cues)!=(2 if synthetic_ci else 8):raise ValueError('wrong cue count')
    info=probe(src);v=[x for x in info['streams'] if x['codec_type']=='video'];a=[x for x in info['streams'] if x['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or any(x['codec_type']=='subtitle' for x in info['streams']):raise ValueError('one A/V and no selectable subtitles required')
    if (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],a[0]['codec_name'],int(a[0]['sample_rate']))!=(1080,1920,'30/1','aac',48000):raise ValueError('wrong media spec')
    duration=float(info['format']['duration'])
    if abs(cues[-1]['end']-duration)>.05:raise ValueError('SRT duration mismatch')
    out.parent.mkdir(parents=True,exist_ok=True);rep.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',src,
         '-map','0:v:0','-map','0:a:0','-vf',rail_filter(cues,genre),
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','2',
         '-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',out])
    run(['ffmpeg','-v','error','-xerror','-i',out,'-f','null','-'])
    final=probe(out)
    vv=next(x for x in final['streams'] if x['codec_type']=='video')
    aa=next(x for x in final['streams'] if x['codec_type']=='audio')
    if vv['width']!=1080 or vv['height']!=1920 or aa['codec_name']!='aac':raise RuntimeError('output spec failed')
    def audio_hash(p):
        return hashlib.sha256(run(['ffmpeg','-v','error','-i',p,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()
    preserved=audio_hash(src)==audio_hash(out)
    if not preserved:raise RuntimeError('AAC bitstream modified')
    audit=audio_audit(out,cues)
    data={'source_sha256':sha(src),'output_sha256':sha(out),'genre':genre,
          'duration':float(final['format']['duration']),'resolution':[1080,1920],
          'fps':'30/1','audio':'AAC 48000 Hz Japanese-tagged',
          'audio_bitstream_unchanged':preserved,'cue_count':len(cues),
          'visual_change':'8-stage thin progress rail at y132-156; no new external assets',
          'audio_boundary_audit':audit,'full_av_decode':'PASS',
          'japanese_asr':'NOT_AVAILABLE','speech_caption_semantics':'NOT_VERIFIED',
          'publication':'NOT_APPROVED'}
    rep.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--srt',required=True)
    p.add_argument('--output',required=True);p.add_argument('--report',required=True)
    p.add_argument('--genre',choices=sorted(GENRES),default='ai_work')
    p.add_argument('--review-only',action='store_true');p.add_argument('--synthetic-ci',action='store_true')
    a=p.parse_args();print(json.dumps(render(a.source,a.srt,a.output,a.report,a.genre,a.review_only,a.synthetic_ci),ensure_ascii=False)[:800])
