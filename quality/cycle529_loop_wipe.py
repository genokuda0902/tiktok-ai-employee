#!/usr/bin/env python3
"""Review-only, zero-cost spatial wipe to remove final-second crossfade ghosts.

Usage: python quality/cycle529_loop_wipe.py --source source.mp4 --output review.mp4
       --manifest manifest.json --qa qa.json
Requires ffmpeg, ffprobe, numpy, Pillow. No external calls or publishing.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

GENRES = (
    'AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
    '営業・ビジネス','転職・キャリア','健康・生活改善',
    '雑学・科学','旅行・グルメ','商品比較・暮らし',
)

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-1500:])
    return p.stdout

def validate_manifest(m):
    if m.get('genre') not in GENRES: raise ValueError('unknown genre')
    if m.get('rights')!='SYNTHETIC_OR_OWNER_APPROVED': raise ValueError('rights not cleared')
    if m.get('contains_private_data') is not False: raise ValueError('privacy gate failed')
    if m.get('publication')!='NOT_APPROVED' or m.get('review_status')!='HUMAN_REVIEW':
        raise ValueError('not review-only')
    if m.get('japanese_narration') not in ('NOT_GENERATED','GENERATED_UNVERIFIED'):
        raise ValueError('voice status missing')

def wipe_frame(closing,opening,progress):
    if closing.shape!=opening.shape or closing.ndim!=3: raise ValueError('geometry mismatch')
    if not 0<=progress<=1: raise ValueError('invalid progress')
    cut=round(closing.shape[1]*(1-progress))
    out=closing.copy()
    out[:,cut:,:]=opening[:,cut:,:]
    return out

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def snapshot(src,t,dst):
    run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(src),'-frames:v','1','-update','1',str(dst)])

def render(src,dst,manifest,qa):
    src,dst,qa=map(Path,(src,dst,qa))
    validate_manifest(manifest)
    if not src.is_file() or src.stat().st_size<10000: raise ValueError('source absent')
    info=probe(src)
    v=next((x for x in info['streams'] if x['codec_type']=='video'),None)
    a=next((x for x in info['streams'] if x['codec_type']=='audio'),None)
    if not v or not a or v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('H264/AAC required')
    if (v['width'],v['height'])!=(1080,1920) or abs(float(info['format']['duration'])-20)>.1:
        raise ValueError('1080x1920 20s required')
    dst.parent.mkdir(parents=True,exist_ok=True)
    opening,closing=dst.parent/'_open.png',dst.parent/'_close.png'
    snapshot(src,0,opening); snapshot(src,18.65,closing)
    a=np.asarray(Image.open(closing).convert('RGB'))
    b=np.asarray(Image.open(opening).convert('RGB'))
    tail=dst.parent/'_tail.mp4'
    proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
      '-s','1080x1920','-r','30','-i','-','-c:v','libx264','-preset','veryfast',
      '-crf','18','-pix_fmt','yuv420p',str(tail)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for k in range(30):
        progress=max(0.,min(1.,(k/30-.1)/.7))
        proc.stdin.write(wipe_frame(a,b,progress).tobytes())
    proc.stdin.close()
    err=proc.stderr.read().decode(errors='replace')
    if proc.wait(): raise RuntimeError('tail encoding failed '+err[-1000:])
    filt=('[0:v]trim=0:19,fps=30,setpts=PTS-STARTPTS[body];'
          '[1:v]fps=30,setpts=PTS-STARTPTS[tail];'
          '[body][tail]concat=n=2:v=1:a=0,format=yuv420p[out]')
    run(['ffmpeg','-v','error','-y','-i',str(src),'-i',str(tail),'-filter_complex',filt,
         '-map','[out]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','19','-r','30','-c:a','copy','-t','20','-movflags','+faststart',str(dst)])
    final=probe(dst)
    fv=next(x for x in final['streams'] if x['codec_type']=='video')
    fa=next(x for x in final['streams'] if x['codec_type']=='audio')
    def audio_md5(path):
        return run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).strip()
    checks={'video_h264':fv['codec_name']=='h264','audio_aac':fa['codec_name']=='aac',
            'vertical':(fv['width'],fv['height'])==(1080,1920),
            'duration':abs(float(final['format']['duration'])-20)<.05,
            'audio_unchanged':audio_md5(src)==audio_md5(dst)}
    report={'cycle':529,'checks':checks,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
            'japanese_narration':'NOT_GENERATED','narration_caption_sync':'NOT_VERIFIED',
            'captions':'INHERITED','review_status':'HUMAN_REVIEW','publication':'NOT_APPROVED'}
    qa.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not all(checks.values()): raise RuntimeError('technical QA failed '+str(checks))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('source','output','manifest','qa'): p.add_argument('--'+key,required=True)
    x=p.parse_args()
    print(json.dumps(render(x.source,x.output,json.loads(Path(x.manifest).read_text()),x.qa),ensure_ascii=False))
