"""Cycle790: repair ghosted text transitions using opaque, frame-exact wipes.

REVIEW ONLY. The script cannot approve source rights or publish anything.
Uses only local source video, Pillow and FFmpeg. Works for any genre.
"""
import argparse
import hashlib
import io
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

FPS = 30
W, H = 1080, 1920

def validate(cfg):
    if cfg.get('mode') != 'review_only' or cfg.get('publication_approved') is not False or cfg.get('rights_reviewed') is not False:
        raise ValueError('Fail closed: human review and rights flags required')
    if cfg.get('canvas') != [W, H] or cfg.get('fps') != FPS:
        raise ValueError('Expected 1080x1920, 30fps')
    fixes = cfg.get('fixes', [])
    if not 1 <= len(fixes) <= 10:
        raise ValueError('Expected 1..10 fixes')
    last = -1
    for f in fixes:
        start, end = f['first_frame'], f['last_frame']
        if not (isinstance(start, int) and isinstance(end, int) and 0 <= start < end < 750):
            raise ValueError('Invalid frame range')
        if start <= last or end-start > 30:
            raise ValueError('Overlapping or too-long repair')
        if not (0 <= f['before_at'] < start/FPS < end/FPS < f['after_at'] <= 25):
            raise ValueError('Clean reference frames must bracket repair')
        last = end
    return True

def still(source, at):
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-ss',str(at),'-i',str(source),'-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1']
    data = subprocess.check_output(cmd)
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size != (W,H):
        raise ValueError('Source frame dimensions differ from contract')
    return im

def wipe_frame(before, after, progress):
    """Never alpha-blend different scenes: opaque wipe prevents doubled letters."""
    p = max(0.0, min(1.0, progress))
    if p <= 0: return before.copy()
    if p >= 1: return after.copy()
    eased = p*p*(3-2*p)
    x = int(W*eased)
    out = before.copy()
    out.paste(after.crop((0,0,x,H)),(0,0))
    draw = ImageDraw.Draw(out)
    draw.rectangle((max(0,x-3),0,min(W-1,x+3),H), fill=(30,205,201))
    return out

def make_patch(source, cfg, directory):
    patches=[]
    for i,f in enumerate(cfg['fixes']):
        a=still(source,f['before_at']);b=still(source,f['after_at'])
        folder=Path(directory)/f'fix{i}';folder.mkdir(parents=True)
        start,end=f['first_frame'],f['last_frame']
        n=end-start+1
        for j in range(n):
            p=(j/(n-1)-.25)/.50
            wipe_frame(a,b,p).save(folder/f'{j:03d}.png',compress_level=1)
        patches.append((folder,start,end))
    return patches

def render(source, dest, config, report):
    source=Path(source);dest=Path(dest);cfg=json.loads(Path(config).read_text(encoding='utf-8'))
    validate(cfg)
    if not source.is_file():raise FileNotFoundError(source)
    dest.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        patches=make_patch(source,cfg,td)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
        for folder,_,_ in patches:
            cmd += ['-framerate',str(FPS),'-i',str(folder/'%03d.png')]
        filters=[];prior='0:v'
        for i,(_,start,end) in enumerate(patches):
            filters.append(f'[{i+1}:v]setpts=PTS+{start}/{FPS}/TB,format=rgba[p{i}]')
            filters.append(f"[{prior}][p{i}]overlay=shortest=0:eof_action=pass:repeatlast=0:enable='between(n,{start},{end})'[v{i}]")
            prior=f'v{i}'
        cmd += ['-filter_complex',';'.join(filters),'-map',f'[{prior}]','-map','0:a:0',
                '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
                '-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(dest)]
        run=subprocess.run(cmd,capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stderr[-4000:])
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,nb_frames:format=duration','-of','json',str(dest)]))
    video=next(x for x in info['streams'] if x['codec_type']=='video')
    audio=next(x for x in info['streams'] if x['codec_type']=='audio')
    if (video['width'],video['height'],video['codec_name'],audio['codec_name'])!=(W,H,'h264','aac'):
        raise RuntimeError('Output format mismatch')
    result={'cycle':790,'status':'HUMAN_REVIEW','publication_approved':False,'rights_reviewed':False,
            'input':str(source),'output':str(dest),'fixes':cfg['fixes'],'duration':float(info['format']['duration']),
            'frames':int(video.get('nb_frames',0)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
            'note':'Opaque wipe replaces ghosted multi-scene transition without altering source AAC packets'}
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('input','output','config','report'):ap.add_argument('--'+name,required=True)
    a=ap.parse_args()
    print(json.dumps(render(a.input,a.output,a.config,a.report),ensure_ascii=False))
