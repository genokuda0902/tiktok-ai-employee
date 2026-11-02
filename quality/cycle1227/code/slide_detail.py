#!/usr/bin/env python3
"""Offline ROI slide-detail enhancer. Ten genres; preserves original AAC bytes."""
import argparse,hashlib,json,subprocess
from pathlib import Path
GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
FRAME_W,FRAME_H,FPS=1080,1920,30
DEFAULT_ROI=(64,480,952,720)
def run(args,binary=False):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode: raise RuntimeError(f'{args[0]} returned {p.returncode}: {p.stderr[-1400:].decode(errors="replace")}')
    return p.stdout if binary else p.stdout.decode()
def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))
def adts_hash(path):
    return hashlib.sha256(run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],True)).hexdigest()
def validate_roi(roi):
    if len(roi)!=4: raise ValueError('roi must be x,y,w,h')
    x,y,w,h=map(int,roi)
    if min(x,y)<0 or min(w,h)<8 or x+w>FRAME_W or y+h>FRAME_H or any(v%2 for v in (x,y,w,h)):
        raise ValueError('ROI outside 1080x1920 or not even-aligned')
    if y+h>1280: raise ValueError('ROI would encroach on narration/subtitle safe area')
    return x,y,w,h
def ffmpeg_filter(roi=DEFAULT_ROI,amount=0.6):
    x,y,w,h=validate_roi(roi)
    if not 0<=amount<=1.0: raise ValueError('sharpen amount outside safe range 0..1')
    return (f'[0:v]split=2[bg][cropin];'
            f'[cropin]crop={w}:{h}:{x}:{y},unsharp=5:5:{amount:.2f}:5:5:0[detail];'
            f'[bg][detail]overlay={x}:{y}:shortest=1:format=auto,format=yuv420p[v]')
def render(source,output,genre='ai',roi=DEFAULT_ROI,amount=.60,report=None):
    if genre not in GENRES: raise ValueError('unsupported genre')
    source,output=Path(source),Path(output)
    if not source.is_file() or source.resolve()==output.resolve(): raise ValueError('invalid source/output')
    info=probe(source)
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',FRAME_W,FRAME_H,'30/1','aac'):
        raise ValueError('requires H.264 1080x1920 30fps AAC')
    frames=int(v['nb_frames']);chapters=info['chapters']
    output.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-filter_complex',ffmpeg_filter(roi,amount),'-map','[v]','-map','0:a:0','-map_chapters','0',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-frames:v',str(frames),'-c:a','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart',str(output)])
    after=probe(output)
    ov=next(s for s in after['streams'] if s['codec_type']=='video')
    oa=next(s for s in after['streams'] if s['codec_type']=='audio')
    if (ov['width'],ov['height'],int(ov['nb_frames']))!=(FRAME_W,FRAME_H,frames):
        raise RuntimeError('frame/geometry changed')
    if len(after['chapters'])!=len(chapters) or oa['codec_name']!='aac':
        raise RuntimeError('chapters or audio missing')
    h1,h2=adts_hash(source),adts_hash(output)
    if h1!=h2: raise RuntimeError('AAC narration bitstream modified')
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(output),
         '-map','0:v:0','-map','0:a:0','-f','null','-'])
    qa={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'output_bytes':output.stat().st_size,'genre':genre,'roi':list(validate_roi(roi)),
        'sharpen_amount':amount,'frames':frames,'width':FRAME_W,'height':FRAME_H,
        'fps':FPS,'duration':float(after['format']['duration']),
        'chapters':len(after['chapters']),'japanese_aac_adts_sha256':h2,
        'aac_bitstream_identical':True,'full_av_decode':'PASS',
        'japanese_speech_transcription':'NOT VERIFIED',
        'subtitle_semantics_and_timing':'NOT VERIFIED',
        'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report: Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
    return qa
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report');p.add_argument('--genre',choices=GENRES,default='ai')
    p.add_argument('--amount',type=float,default=.60)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,amount=a.amount,report=a.report),ensure_ascii=False))
