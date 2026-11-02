#!/usr/bin/env python3
"""Review-only, source-hash-gated content-area scene wipes for ten genres.

Never publishes or uploads media. Transitions affect the central image only; header,
chapter rail, Japanese burned-in subtitles, and original AAC elementary stream stay.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
FPS = 30

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"command failed: {cmd[0]} {p.stderr[-1600:]}")
    return p.stdout

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def probe(path):
    d=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=[s for s in d['streams'] if s['codec_type']=='video']
    a=[s for s in d['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or any(s['codec_type']=='subtitle' for s in d['streams']):
        raise ValueError('requires one video, one audio and no subtitle tracks')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac' or a[0]['sample_rate']!='48000' or a[0].get('tags',{}).get('language')!='jpn':
        raise ValueError('H264/AAC 48kHz jpn required')
    if v[0]['width']!=1080 or v[0]['height']!=1920 or v[0]['avg_frame_rate']!='30/1':
        raise ValueError('1080x1920 30fps required')
    return {'frames':int(v[0]['nb_frames']),'duration':float(d['format']['duration']), 'width':1080,'height':1920}

def validate(m, actual_sha, spec):
    if set(m)!={'policy','asset_approval','source_sha256','genre','roi','cut_frames','transition_frames'}:
        raise ValueError('unknown or missing manifest keys')
    if m['policy']!=POLICY or m['asset_approval']!='private_review_only' or m['source_sha256']!=actual_sha:
        raise ValueError('source approval/hash mismatch')
    if m['genre'] not in GENRES:raise ValueError('unknown genre')
    roi=m['roi']
    if not isinstance(roi,dict) or set(roi)!={'x','y','width','height'} or any(type(v)!=int for v in roi.values()):
        raise ValueError('invalid ROI')
    if not (roi['x']>=0 and roi['x']+roi['width']<=1080 and roi['y']>=160 and roi['y']+roi['height']<=1200 and roi['width']>=500 and roi['height']>=300):
        raise ValueError('ROI must be inside audited central visual area, not subtitles')
    cuts=m['cut_frames']; n=m['transition_frames']
    if type(n)!=int or not (5<=n<=10):raise ValueError('unsafe transition length')
    if not isinstance(cuts,list) or not (1<=len(cuts)<=10) or any(type(c)!=int for c in cuts):
        raise ValueError('cut frames invalid')
    if cuts!=sorted(set(cuts)) or cuts[0]<30 or cuts[-1]+n>=spec['frames'] or any(b-a<30 for a,b in zip(cuts,cuts[1:])):
        raise ValueError('cuts must be ordered, distinct and separated')
    return cuts,n,roi

def still(video, t, roi, dest):
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',f'{t:.6f}','-i',str(video),'-frames:v','1',
         '-vf',f'crop={roi["width"]}:{roi["height"]}:{roi["x"]}:{roi["y"]}',str(dest)])

def cut_mae(before,after):
    a=Image.open(before).convert('RGB').resize((160,160));b=Image.open(after).convert('RGB').resize((160,160))
    return sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3

def wipe_alpha(width, progress, feather=32):
    """Old-scene opacity: left is revealed new scene, right stays old scene.

    The transition is a spatial wipe rather than an overlapping dissolve:
    only a narrow feather contains blended pixels, keeping UI text legible.
    """
    if not (0 <= progress <= 1) or feather < 1:raise ValueError('invalid wipe')
    boundary=round(width*progress)
    return [max(0,min(255,round((x-boundary+feather/2)/feather*255))) for x in range(width)]

def render(source,output,manifest,report):
    source=Path(source);output=Path(output);spec=probe(source)
    cuts,n,roi=validate(manifest,sha256(source),spec)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='scene_wipe_') as tmp:
        inputs=[];filters=[];measured=[]
        for i,frame in enumerate(cuts,1):
            old=Path(tmp)/f'previous_{i}.png';new=Path(tmp)/f'new_{i}.png'
            still(source,(frame-1)/FPS,roi,old)
            still(source,frame/FPS,roi,new)
            contrast=cut_mae(old,new)
            if contrast<8:raise ValueError(f'cut {frame} has no independently verified scene change ({contrast:.2f})')
            measured.append(round(contrast,3))
            prev=Image.open(old).convert('RGBA')
            for k in range(n):
                progress=(k+1)/n
                alphas=wipe_alpha(roi['width'],progress)
                # Repeat the same 1D opacity mask down all rows; no image-wide
                # text ghosting, just a 32px moving soft seam.
                mask=Image.frombytes('L',(roi['width'],roi['height']),bytes(alphas)*roi['height'])
                pane=prev.copy();pane.putalpha(mask)
                pane.save(Path(tmp)/f'wipe_{i}_{k:02d}.png',compress_level=1)
            inputs.extend(['-framerate','30','-start_number','0','-i',str(Path(tmp)/f'wipe_{i}_%02d.png')])
            filters.append(f'[{i}:v]format=rgba,setpts=PTS-STARTPTS+{frame/FPS:.6f}/TB[t{i}]')
        prior='[0:v]'
        for i in range(1,len(cuts)+1):
            nxt=f'[v{i}]'
            filters.append(f'{prior}[t{i}]overlay=x={roi["x"]}:y={roi["y"]}:eof_action=pass:repeatlast=0:shortest=0:format=auto{nxt}')
            prior=nxt
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),*inputs,
             '-filter_complex',';'.join(filters),'-map',prior,'-map','0:a:0',
             '-frames:v',str(spec['frames']),'-c:v','libx264','-preset','veryfast','-crf','17',
             '-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn',
             '-movflags','+faststart',str(output)]
        run(cmd)
    dest=probe(output)
    if dest['frames']!=spec['frames'] or abs(dest['duration']-spec['duration'])>.04:raise RuntimeError('frame count/duration mismatch')
    run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
    result={'source_sha256':sha256(source),'output_sha256':sha256(output),'frames':dest['frames'],
            'duration':dest['duration'],'resolution':[1080,1920],'fps':30,'cut_frames':cuts,
            'transition_frames':n,'transition_seconds':n/FPS,'cut_content_mae':measured,
            'roi':roi,'transition_style':'left-to-right content-only spatial wipe, 32px feather',
            'audio':'AAC jpn 48kHz stream-copied','caption_area':'not overlaid; video re-encoded',
            'review_only':True,'asr_semantics':'NOT_VERIFIED','real_phone':'NOT_VERIFIED'}
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True);p.add_argument('--report',required=True)
    a=p.parse_args();m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    print(json.dumps(render(a.source,a.output,m,a.report),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
