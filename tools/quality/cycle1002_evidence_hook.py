#!/usr/bin/env python3
"""Review-only evidence-verified result hook and cue-level audio audit.

Never invent metrics: source rows must reconcile to both totals and displayed delta.
Audio review manifest is NOT independent ASR or semantic alignment certification.
No external uploads, no publishing, no automatic posting.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
FONT_CANDIDATES = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
                   '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                   '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
START, END = 0.30, 1.43

def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):
            h.update(part)
    return h.hexdigest()

def evidence_summary(evidence):
    if evidence.get('genre') not in GENRES:
        raise ValueError('genre is not in the ten-genre allowlist')
    if evidence.get('classification') != 'synthetic_example':
        raise ValueError('unverified real-world data cannot be displayed')
    a,b=evidence.get('left_series'),evidence.get('right_series')
    if not isinstance(a,list) or not isinstance(b,list) or len(a)!=len(b) or len(a)<2:
        raise ValueError('need paired source data')
    if any(type(v) is not int or v<0 or v>100000 for v in a+b):
        raise ValueError('source data must be safe nonnegative integers')
    left,right=sum(a),sum(b)
    if (left,right)!=(evidence.get('expected_left'),evidence.get('expected_right')):
        raise ValueError('expected totals do not match source data')
    if left-right!=evidence.get('expected_difference'):
        raise ValueError('expected difference does not reconcile')
    if left<=right:
        raise ValueError('this positive-difference badge requires left>right')
    return {'left':left,'right':right,'difference':left-right,'classification':'synthetic_example'}

def font(size):
    for p in FONT_CANDIDATES:
        if Path(p).is_file(): return ImageFont.truetype(p,size)
    raise FileNotFoundError('Noto CJK or fallback font required')

def make_badge(evidence, dest):
    stats=evidence_summary(evidence)
    im=Image.new('RGBA',(425,146),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((2,2,423,144),radius=24,fill=(8,37,56,241),outline=(42,221,200,245),width=3)
    d.rounded_rectangle((19,20,26,125),radius=3,fill=(36,226,198,255))
    d.text((44,15),'架空データの集計差',font=font(23),fill=(209,243,243,255))
    d.text((45,45),f"{stats['left']} − {stats['right']} =",font=font(29),fill=(242,250,251,255))
    d.text((287,39),f"+{stats['difference']}",font=font(51),fill=(54,236,207,255))
    d.text((46,110),'実データの成果ではありません',font=font(18),fill=(170,202,212,255))
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
    return stats

def parse_srt(srt_text):
    cues=[]
    pattern=re.compile(r'(\d\d):(\d\d):(\d\d)[,.](\d\d\d)')
    def seconds(s):
        m=pattern.fullmatch(s.strip())
        if not m: raise ValueError('bad SRT timestamp')
        h,mn,sec,ms=map(int,m.groups())
        return h*3600+mn*60+sec+ms/1000
    for block in re.split(r'\n\s*\n',srt_text.strip()):
        lines=block.splitlines()
        if not lines: continue
        if lines[0].strip().isdigit(): lines=lines[1:]
        if not lines or '-->' not in lines[0]: raise ValueError('bad SRT cue')
        a,b=lines[0].split('-->')
        st,en=seconds(a),seconds(b)
        if st<0 or en<=st or (cues and st<cues[-1]['end']-.002):
            raise ValueError('invalid or overlapping SRT cue')
        text='\n'.join(lines[1:]).strip()
        if not text: raise ValueError('empty SRT text')
        cues.append({'start':st,'end':en,'text':text,'independent_asr_verified':False})
    if not cues: raise ValueError('no SRT cues')
    return cues

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def validate_source(source):
    streams=probe(source)['streams']
    v=next((s for s in streams if s['codec_type']=='video'),None)
    a=next((s for s in streams if s['codec_type']=='audio'),None)
    s=next((s for s in streams if s['codec_type']=='subtitle'),None)
    if not v or (v['width'],v['height'],v['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('source must be 1080x1920/30fps')
    if not a or a.get('sample_rate')!='48000' or not s:
        raise ValueError('Japanese audio and subtitle tracks are required')

def render(source, output, evidence, badge_path, report, review_only=False):
    if not review_only: raise ValueError('human review only: publishing is prohibited')
    source,output,report=map(Path,(source,output,report))
    if not source.is_file() or source.resolve()==output.resolve(): raise ValueError('source/output invalid')
    validate_source(source)
    stats=make_badge(evidence,badge_path)
    output.parent.mkdir(parents=True,exist_ok=True)
    filtergraph=("[1:v]format=rgba,fade=t=in:st=0.30:d=0.18:alpha=1,"
                 "fade=t=out:st=1.22:d=0.21:alpha=1[badge];"
                 "[0:v][badge]overlay=x=620:y=160:enable='between(t,0.30,1.43)':"
                 "shortest=1:format=auto[v]")
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-loop','1','-framerate','30','-i',str(badge_path),
         '-filter_complex',filtergraph,'-map','[v]','-map','0:a:0','-map','0:s:0',
         '-c:v','libx264','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p',
         '-c:a','copy','-c:s','copy','-metadata:s:a:0','language=jpn',
         '-metadata:s:s:0','language=jpn','-movflags','+faststart',str(output)]
    run(cmd)
    payload={'source_sha256':sha256(source),'output_sha256':sha256(output),
             'genre':evidence['genre'],'evidence':stats,'badge_seconds':[START,END],
             'badge_xy':[620,160],'review_only':True,'publication_approved':False,
             'semantic_audio_caption_match':'NOT_VERIFIED'}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf8')
    return payload

def make_audio_review(source, srt, output_dir):
    """Produce private 8-cue WAV snippets for human transcription; no ASR claim."""
    validate_source(source)
    cues=parse_srt(Path(srt).read_text(encoding='utf8'))
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    for i,c in enumerate(cues,1):
        out=output_dir/f'cue_{i:02d}_PRIVATE_REVIEW.wav'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(c['start']),
             '-i',str(source),'-t',str(round(c['end']-c['start'],3)),
             '-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(out)])
        c['audio_file']=out.name
        c['human_transcription']=''
        c['meaning_matches_caption']=None
        c['timing_approved']=None
    manifest={'cues':cues,'independent_asr':'UNAVAILABLE',
              'human_review_complete':False,'publish_approved':False}
    (output_dir/'caption_audio_review.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--evidence',required=True);p.add_argument('--badge',required=True)
    p.add_argument('--report',required=True);p.add_argument('--review-only',action='store_true')
    p.add_argument('--srt');p.add_argument('--private-audio-review-dir')
    a=p.parse_args()
    data=json.loads(Path(a.evidence).read_text(encoding='utf8'))
    render(a.source,a.output,data,a.badge,a.report,a.review_only)
    if a.srt and a.private_audio_review_dir:
        make_audio_review(a.output,a.srt,a.private_audio_review_dir)
