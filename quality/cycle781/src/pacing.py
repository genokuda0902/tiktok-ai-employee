#!/usr/bin/env python3
"""Genre-neutral, review-only dead-air trim and Japanese caption remapping.

Zero-cost FFmpeg. Does not transcribe speech or approve media for publication.
Input media and audio stay local; only code/tests/manifests may be committed.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from pathlib import Path

GENRES=('ai_productivity','trivia','cooking','beauty','finance','wellness','travel','product_demo','story','business')

def run(args):
    return subprocess.run(args,check=True,text=True,capture_output=True)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate:stream_tags=language','-of','json',str(path)]).stdout)

def silence_windows(path,noise='-40dB',min_duration=.5):
    p=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-map','0:a:0','-af',f'silencedetect=noise={noise}:d={min_duration}','-f','null','-'],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-2000:])
    starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',p.stderr)]
    ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',p.stderr)]
    if len(starts)!=len(ends):raise ValueError('unmatched silence boundaries')
    return list(zip(starts,ends))

def validate(m,source,silences):
    if m.get('genre_id') not in GENRES:raise ValueError('unknown genre')
    for key,expected in [('quality_approved',False),('publication_approved',False),('publish_mode','employee_manual_only'),('speech_transcript_verified',False),('source_rights','unverified_review_only'),('audio_rights','unverified_review_only')]:
        if m.get(key)!=expected:raise ValueError(f'review-only safety gate: {key}')
    if m.get('source_sha256')!=sha256(source):raise ValueError('input SHA256 mismatch')
    if m.get('caption_kind')!='scene_summary_not_verbatim_transcript':raise ValueError('cannot claim transcript')
    p=probe(source);duration=float(p['format']['duration']);cuts=m['cuts'];cues=m['cues']
    if not cuts or len(cuts)>30:raise ValueError('bad cut count')
    prev=0
    for a,b in cuts:
        a=float(a);b=float(b)
        if not (prev<=a<b<=duration and .10<=b-a<=.85):raise ValueError('invalid cut')
        if not any(s+.10<=a and b<=e-.10 for s,e in silences):
            raise ValueError(f'cut {a}-{b} not safely inside measured silence')
        prev=b
    prev=0
    for c in cues:
        a=float(c['start']);b=float(c['end']);label=c['caption']
        if not (prev<=a<b<=duration) or not (4<=len(label)<=30):raise ValueError('invalid caption')
        if any(a<x<b or a<y<b for x,y in cuts):raise ValueError('cut intersects caption')
        prev=b
    if not any(s['codec_type']=='audio' for s in p['streams']):raise ValueError('missing audio')
    if not any(s['codec_type']=='video' for s in p['streams']):raise ValueError('missing video')
    return duration

def remap(t,cuts):
    t=float(t)
    if any(a<t<b for a,b in cuts):raise ValueError('time lies inside removed cut')
    return round(t-sum(b-a for a,b in cuts if b<=t),3)

def stamp(sec):
    ms=round(sec*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'

def write_srt(cues,cuts,out):
    lines=[]
    for i,c in enumerate(cues,1):
        a,b=remap(c['start'],cuts),remap(c['end'],cuts)
        lines.extend([str(i),f'{stamp(a)} --> {stamp(b)}',c['caption'],''])
    Path(out).write_text('\n'.join(lines)+'\n',encoding='utf-8')

def segments(cuts,duration):
    pts=[0.0]
    for a,b in cuts:pts.extend([a,b])
    pts.append(duration)
    return [(pts[i],pts[i+1]) for i in range(0,len(pts)-1,2)]

def ffmpeg_graph(cuts,duration):
    parts=[];links=[]
    for i,(a,b) in enumerate(segments(cuts,duration)):
        parts.extend([f'[0:v:0]trim=start={a:.6f}:end={b:.6f},setpts=PTS-STARTPTS[v{i}]',
                      f'[0:a:0]atrim=start={a:.6f}:end={b:.6f},asetpts=PTS-STARTPTS[a{i}]'])
        links.append(f'[v{i}][a{i}]')
    parts.append(''.join(links)+f'concat=n={len(links)}:v=1:a=1[v][a]')
    return ';'.join(parts)

def render(source,manifest,out,qa_dir,preset='veryfast'):
    source=Path(source);out=Path(out);qa_dir=Path(qa_dir)
    out.parent.mkdir(parents=True,exist_ok=True);qa_dir.mkdir(parents=True,exist_ok=True)
    m=json.loads(Path(manifest).read_text(encoding='utf-8'))
    silences=silence_windows(source)
    duration=validate(m,source,silences)
    cuts=[tuple(map(float,x)) for x in m['cuts']]
    srt=qa_dir/'cycle781_timed_scene_summaries.srt';write_srt(m['cues'],cuts,srt)
    temp=out.with_name('cycle781_intermediate.mp4')
    graph=ffmpeg_graph(cuts,duration)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-filter_complex',graph,
         '-map','[v]','-map','[a]','-c:v','libx264','-preset',preset,'-crf','19',
         '-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000',
         '-movflags','+faststart',str(temp)]
    run(cmd)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(temp),'-i',str(srt),
         '-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text',
         '-metadata:s:s:0','language=jpn','-disposition:s:0','0','-movflags','+faststart',str(out)])
    temp.unlink()
    info=probe(out)
    actual=float(info['format']['duration']);expected=duration-sum(b-a for a,b in cuts)
    if abs(actual-expected)>.13:raise ValueError(f'bad duration {actual} expected {expected}')
    result={'cycle':781,'input_sha256':sha256(source),'output_sha256':sha256(out),
            'input_duration':duration,'output_duration':actual,'removed_seconds':round(duration-actual,3),
            'cuts':cuts,'detected_silence_windows':silences,'caption_count':len(m['cues']),
            'output_streams':info['streams'],'review_only':True,'rights_verified':False,
            'narration_language_content_verified':False,'speech_transcript_verified':False,
            'employee_approval':False,'publication_approved':False}
    (qa_dir/'render_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for a in ['source','manifest','output','qa']:p.add_argument('--'+a,required=True)
    a=p.parse_args();print(json.dumps(render(a.source,a.manifest,a.output,a.qa),ensure_ascii=False,indent=2))
