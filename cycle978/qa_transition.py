#!/usr/bin/env python3
"""Synthetic-safe media QA; no ASR claims and no external uploads."""
import argparse
import hashlib
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
from repair_transition import probe, sha256, CAPTION_SAFE_Y


def capture_frame(path, index):
    p = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
                        '-vf', f'select=eq(n\\,{index})', '-vsync', '0',
                        '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', 'pipe:1'],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return Image.open(io.BytesIO(p.stdout)).convert('RGB')


def mean_diff(a,b,box):
    return sum(ImageStat.Stat(ImageChops.difference(a.crop(box), b.crop(box))).mean)/3


def aac_sha(path):
    p = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
                        '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', 'pipe:1'],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return hashlib.sha256(p.stdout).hexdigest()


def qa(source, output, start, end, anchor, *, full_decode=True):
    n1, src_meta = probe(source)
    n2, dst_meta = probe(output)
    if n1 != n2:
        raise AssertionError('Frame count mismatch')
    audio1, audio2 = aac_sha(source), aac_sha(output)
    if audio1 != audio2:
        raise AssertionError('AAC elementary stream changed')
    # Sample first/middle/last repaired frames and unaffected end scene.
    samples = sorted(set([0, max(0,start-1), start, (start+end)//2, end, anchor, n1-1]))
    subtitle_deltas=[]
    for f in samples:
        a,b=capture_frame(source,f),capture_frame(output,f)
        subtitle_deltas.append(mean_diff(a,b,(0,CAPTION_SAFE_Y,1080,1920)))
    if max(subtitle_deltas)>3.0:
        raise AssertionError('Caption protection region changed unexpectedly')
    # Check against an actual *later clean anchor* instead of an invented image.
    middle=(start+end)//2
    old, new, clean = capture_frame(source,middle),capture_frame(output,middle),capture_frame(source,anchor)
    upper=(0,0,1080,CAPTION_SAFE_Y)
    before,after=mean_diff(old,clean,upper),mean_diff(new,clean,upper)
    if before < 0.5:
        raise AssertionError('No visible original transition defect detected')
    if not after < before * 0.40:
        raise AssertionError(f'Ghost not sufficiently reduced: {before:.3f}->{after:.3f}')
    if full_decode:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror',
                        '-i',str(output),'-f','null','-'],check=True)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'source_frames':n1,'output_frames':n2,
            'duration_sec':float(dst_meta['format']['duration']),
            'video':dst_meta['streams'][0],
            'audio':next(s for s in dst_meta['streams'] if s['codec_type']=='audio'),
            'aac_sha256_unchanged':audio1==audio2,
            'max_sampled_caption_roi_mean_delta':round(max(subtitle_deltas),4),
            'transition_artwork_mean_delta_before':round(before,4),
            'transition_artwork_mean_delta_after':round(after,4),
            'ghost_reduction_pct':round(100*(1-after/before),2),
            'full_decode_pass':full_decode,
            'japanese_transcript_semantics_verified':False,
            'publication_approved':False}

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--start',type=int,default=522);p.add_argument('--end',type=int,default=530)
    p.add_argument('--anchor',type=int,default=532)
    p.add_argument('--report',required=True)
    a=p.parse_args(); result=qa(a.source,a.output,a.start,a.end,a.anchor)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
