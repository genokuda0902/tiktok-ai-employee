#!/usr/bin/env python3
"""Offline 8-chapter micro-zoom for 1080x1920 slide video.
Only central slide panel is modified. Narration/subtitle/footer untouched.
No crossfades between different slides; no external services.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

W,H,FPS=1080,1920,30
X,Y,PW,PH=52,430,824,694
ZOOM_MAX=1.018
GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')

def run(args,binary=False):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr[-1400:].decode(errors='replace'))
    return p.stdout if binary else p.stdout.decode()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))

def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],True)).hexdigest()

def chapter_frames(chapters,total):
    starts=sorted(set(max(0,min(total-1,round(float(c['start_time'])*FPS))) for c in chapters))
    if not starts or starts[0]!=0: starts.insert(0,0)
    return starts+[total]

def zoom_expression(bounds,max_zoom=ZOOM_MAX):
    if not 1.0<=max_zoom<=1.05: raise ValueError('max_zoom out of range')
    if bounds[0]!=0 or any(b<=a for a,b in zip(bounds,bounds[1:])): raise ValueError('invalid chapter frames')
    expr='1'
    for a,b in reversed(list(zip(bounds,bounds[1:]))):
        length=max(1,b-a-1)
        u=f'min(1,max(0,(on-{a})/{length}))'
        ease=f'({u}*{u}*(3-2*{u}))'
        local=f'(1+{max_zoom-1:.6f}*{ease})'
        expr=f'if(lt(on,{b}),{local},{expr})'
    return expr

def filtergraph(bounds,max_zoom=ZOOM_MAX):
    z=zoom_expression(bounds,max_zoom)
    return (f'[0:v]split=2[base][panel];'
            f'[panel]crop={PW}:{PH}:{X}:{Y},'
            f"zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
            f'd=1:s={PW}x{PH}:fps={FPS},format=yuv420p[zoom];'
            f'[base][zoom]overlay={X}:{Y}:shortest=0:eof_action=repeat:format=auto,'
            f'format=yuv420p[v]')

def render(source,output,genre='ai',max_zoom=ZOOM_MAX,report=None):
    if genre not in GENRES: raise ValueError('unsupported genre')
    source,output=Path(source),Path(output)
    if not source.is_file() or source.resolve()==output.resolve(): raise ValueError('bad input/output')
    meta=probe(source)
    v=next(s for s in meta['streams'] if s['codec_type']=='video')
    a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],a['codec_name'])!=(W,H,'30/1','h264','aac'):
        raise ValueError('expected 1080x1920 30fps H264/AAC')
    frames=int(v['nb_frames'])
    chapters=meta.get('chapters',[])
    bounds=chapter_frames(chapters,frames)
    output.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-filter_complex',filtergraph(bounds,max_zoom),'-map','[v]','-map','0:a:0',
         '-map_chapters','0','-c:v','libx264','-preset','veryfast','-crf','18',
         '-pix_fmt','yuv420p','-frames:v',str(frames),'-c:a','copy',
         '-movflags','+faststart',str(output)])
    out=probe(output)
    ov=next(s for s in out['streams'] if s['codec_type']=='video')
    if (ov['width'],ov['height'],int(ov['nb_frames']))!=(W,H,frames): raise RuntimeError('frame geometry mismatch')
    if len(out.get('chapters',[]))!=len(chapters): raise RuntimeError('chapter count mismatch')
    original_audio,new_audio=audio_sha(source),audio_sha(output)
    if original_audio!=new_audio: raise RuntimeError('AAC changed')
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    result={'genre':genre,'frames':frames,'resolution':[W,H],'fps':FPS,
            'duration_s':float(out['format']['duration']),'chapters':len(chapters),
            'chapter_frames':bounds,'max_zoom':max_zoom,'zoom_area':[X,Y,PW,PH],
            'audio_bitstream_identical':True,'full_av_decode':'PASS',
            'subtitle_meaning_asr':'NOT VERIFIED','rights':'NOT VERIFIED',
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report: Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',default='ai',choices=GENRES)
    p.add_argument('--zoom',type=float,default=ZOOM_MAX)
    p.add_argument('--report')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,a.zoom,a.report),ensure_ascii=False,indent=2))
