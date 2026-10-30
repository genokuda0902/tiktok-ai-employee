#!/usr/bin/env python3
"""Chapter-aware micro-dip between still-image scenes. Review only; FFmpeg/stdlib."""
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path

GENRES = ('ai_work','money','career','psychology','health','beauty','food','travel','learning','lifestyle')

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError(f"command failed ({p.returncode}): {cmd[0]}\n{p.stderr[-2500:]}")
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))

def chapter_cuts(info,duration):
    return sorted({round(float(c['start_time']),3) for c in info.get('chapters',[])
                   if .25<float(c['start_time'])<duration-.25})

def brightness_expr(cuts,strength=.12,window=.133):
    if not (0<strength<=.2 and .067<=window<=.2):
        raise ValueError('unsafe transition parameters')
    if not cuts: return '0'
    terms=[f'max(0\\,1-abs(t-{t:.3f})/{window:.3f})' for t in cuts]
    expr=terms[0]
    for term in terms[1:]: expr=f'max({expr}\\,{term})'
    return f'-{strength:.3f}*{expr}'

def inspect(info):
    v=next((s for s in info['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    if not v or not a: raise ValueError('video and audio required')
    if (v['width'],v['height'],v['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('requires 1080x1920 30fps')
    if a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
        raise ValueError('requires AAC 48kHz')
    return v,a

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()

def render(source,output,genre='ai_work',strength=.12,window=.133,preset='veryfast',crf=19):
    if genre not in GENRES: raise ValueError('unknown genre')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('ffmpeg and ffprobe required')
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve(): raise ValueError('source overwrite prohibited')
    old=probe(source);inspect(old)
    duration=float(old['format']['duration'])
    cuts=chapter_cuts(old,duration)
    if not cuts: raise ValueError('no chapter cuts; refuse no-op')
    filt=f"eq=brightness='{brightness_expr(cuts,strength,window)}':eval=frame"
    output.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
         '-vf',filt,'-c:v','libx264','-preset',preset,'-crf',str(crf),
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)])
    new=probe(output);inspect(new)
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(output),
         '-map','0:v:0','-map','0:a:0','-f','null','-'])
    frames=int(run(['ffprobe','-v','error','-select_streams','v:0','-count_frames',
        '-show_entries','stream=nb_read_frames','-of','default=noprint_wrappers=1:nokey=1',str(output)]).strip())
    if frames!=round(duration*30): raise RuntimeError('frame count changed')
    if len(new['chapters'])!=len(old['chapters']): raise RuntimeError('chapters changed')
    if abs(float(new['format']['duration'])-duration)>.04: raise RuntimeError('duration changed')
    if any(s['codec_type']=='subtitle' for s in new['streams']):
        raise RuntimeError('duplicate selectable subtitle track')
    return {'cycle':1013,'genre':genre,'duration_s':duration,'frames':frames,
        'size':[1080,1920],'fps':30,'audio':'AAC 48kHz stream copy',
        'chapters':len(new['chapters']),'cut_count':len(cuts),'cut_times':cuts,
        'method':'8-frame chapter-boundary micro-dip without ghosted text',
        'full_decode':'PASS','sha256':sha256(output),'bytes':output.stat().st_size,
        'independent_asr':'NOT_DONE','speech_caption_sync':'NOT_VERIFIED',
        'rights':'NOT_VERIFIED','publication':'NOT_APPROVED','employee_approval':False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--strength',type=float,default=.12)
    p.add_argument('--window',type=float,default=.133)
    p.add_argument('--preset',default='veryfast')
    p.add_argument('--crf',type=int,default=19)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,a.strength,a.window,a.preset,a.crf),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
