#!/usr/bin/env python3
"""Conservative, genre-agnostic pause trimming for 9:16 narrated image slides.

Cuts only the center of quiet spans, leaving >=0.30 s of silence, avoiding
chapter boundaries and the opening/closing. It never transcribes Japanese.
Output is review-only and must not be posted automatically.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

GENRE_IDS = ('ai_work','money','health','psychology','relationships','history','science','lifehacks','career','trivia')
FPS = 30

def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(path)]).stdout)

def detect_silences(source, threshold='-35dB', min_d=0.40):
    p = subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(source),'-vn','-af',f'silencedetect=noise={threshold}:d={min_d}','-f','null','-'],text=True,capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr[-2000:])
    starts=[]; result=[]
    for line in p.stderr.splitlines():
        a=re.search(r'silence_start: ([\d.]+)',line)
        if a: starts.append(float(a.group(1)))
        b=re.search(r'silence_end: ([\d.]+)',line)
        if b and starts:
            result.append((starts.pop(0),float(b.group(1))))
    return result

def plan_cuts(silences, chapters, duration, *, max_remove=0.133333, keep_quiet=0.30, guard=0.24):
    boundaries=[float(c['start_time']) for c in chapters]
    cuts=[]
    for start,end in silences:
        if start < 0.60 or end > duration-0.33: continue
        mid=(start+end)/2
        if any(abs(mid-b)<guard for b in boundaries): continue
        frames=int(round(min(max_remove,end-start-keep_quiet)*FPS))
        if frames < 3: continue
        removed=frames/FPS
        left=round((mid-removed/2)*FPS)/FPS
        right=left+removed
        if left<start+0.12 or right>end-0.12: continue
        cuts.append((round(left,6),round(right,6)))
    return cuts

def map_time(t,cuts):
    removed=0.0
    for a,b in cuts:
        if t>=b: removed+=b-a
        elif t>a: return a-removed
        else: break
    return t-removed

def keep_segments(duration,cuts):
    points=[0.0]+[z for a,b in cuts for z in (a,b)]+[duration]
    return [(points[i],points[i+1]) for i in range(0,len(points)-1,2)]

def write_metadata(chapters,cuts,duration,out):
    lines=[';FFMETADATA1']
    for c in chapters:
        st=round(map_time(float(c['start_time']),cuts)*1000)
        en=round(map_time(float(c['end_time']),cuts)*1000)
        if en<=st: continue
        title=c.get('tags',{}).get('title','chapter').replace('=','\\=').replace(';','\\;')
        lines.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={st}',f'END={en}',f'title={title}'])
    Path(out).write_text('\n'.join(lines)+'\n',encoding='utf-8')

def msfmt(t,webvtt=False):
    m=round(t*1000)
    h,m=divmod(m,3600000); mm,m=divmod(m,60000); ss,ms=divmod(m,1000)
    return f'{h:02}:{mm:02}:{ss:02}{"." if webvtt else ","}{ms:03}'

def retime_srt(source,out,cuts):
    txt=Path(source).read_text(encoding='utf-8-sig')
    def change(match):
        def sec(s):
            h,m,s=s.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
        a,b=match.group(1),match.group(2)
        return f'{msfmt(map_time(sec(a),cuts))} --> {msfmt(map_time(sec(b),cuts))}'
    pat=r'(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)'
    Path(out).write_text(re.sub(pat,change,txt),encoding='utf-8')

def render(source,out,chapters,cuts,duration,threads=4):
    meta=Path(out).with_suffix('.ffmetadata')
    write_metadata(chapters,cuts,duration,meta)
    segments=keep_segments(duration,cuts)
    filters=[];labels=[]
    for i,(start,end) in enumerate(segments):
        filters.extend([f'[0:v:0]trim=start={start:.6f}:end={end:.6f},setpts=PTS-STARTPTS[v{i}]',
                        f'[0:a:0]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS[a{i}]'])
        labels.append(f'[v{i}][a{i}]')
    filters.append(''.join(labels)+f'concat=n={len(segments)}:v=1:a=1[v][a]')
    cmd=['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-y','-i',str(source),'-f','ffmetadata','-i',str(meta),
         '-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-map_metadata','1','-map_chapters','1',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30','-threads',str(threads),
         '-c:a','aac','-b:a','192k','-ar','48000','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(out)]
    run(cmd)
    return cmd

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--srt');p.add_argument('--genre',choices=GENRE_IDS,default='ai_work')
    p.add_argument('--synthetic',action='store_true')
    a=p.parse_args(); src=Path(a.source);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    info=probe(src);duration=float(info['format']['duration']);chs=info.get('chapters',[])
    silences=detect_silences(src);cuts=plan_cuts(silences,chs,duration)
    if not cuts: raise RuntimeError('No safe cuts; leave source unchanged, do not claim improvement')
    render(src,out,chs,cuts,duration)
    if a.srt: retime_srt(a.srt,out.with_suffix('.srt'),cuts)
    new=probe(out);v=next(s for s in new['streams'] if s['codec_type']=='video');audio=next(s for s in new['streams'] if s['codec_type']=='audio')
    decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True)
    result={'genre':a.genre,'duration_before':duration,'duration_after':float(new['format']['duration']),
            'removed_seconds_planned':round(sum(b-a for a,b in cuts),6),'cuts':cuts,
            'video':v['codec_name'],'size':[v['width'],v['height']],'fps':v['r_frame_rate'],
            'audio':audio['codec_name'],'audio_rate':audio['sample_rate'],'audio_language':audio.get('tags',{}).get('language'),
            'chapters_before':len(chs),'chapters_after':len(new.get('chapters',[])),
            'embedded_subtitles':sum(s['codec_type']=='subtitle' for s in new['streams']),
            'full_decode':'PASS' if decoded.returncode==0 else 'FAIL','independent_asr':'NOT_DONE',
            'speech_text_sync':'NOT_VERIFIED','publication':'NOT_APPROVED','employee_approval':False,
            'rights':'NOT_VERIFIED','synthetic':a.synthetic}
    if result['full_decode']!='PASS' or result['size']!=[1080,1920] or result['fps']!='30/1': raise RuntimeError(str(result))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
