"""Local-only A/V verification for cycle951. Do not upload private source media."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np


def run(*args):
    return subprocess.run(list(args), check=True, capture_output=True).stdout


def adts_hash(p: Path):
    data = run('ffmpeg','-hide_banner','-loglevel','error','-i',str(p),
               '-map','0:a:0','-c:a','copy','-f','adts','pipe:1')
    return hashlib.sha256(data).hexdigest()


def frames_gray(p: Path, w=135, h=240):
    data = run('ffmpeg','-hide_banner','-loglevel','error','-i',str(p),
               '-map','0:v:0','-vf',f'scale={w}:{h},format=gray',
               '-f','rawvideo','-pix_fmt','gray','pipe:1')
    arr = np.frombuffer(data, dtype=np.uint8)
    assert arr.size == 691*w*h, (arr.size, 691*w*h)
    return arr.reshape(691,h,w)


def verify(source: Path, output: Path, report: Path):
    ah1,ah2=adts_hash(source),adts_hash(output)
    if ah1!=ah2: raise RuntimeError('audio elementary stream mismatch')
    a,b=frames_gray(source),frames_gray(output)
    diff=np.abs(a.astype(np.int16)-b.astype(np.int16))
    # 1/8 sampling. Protected subtitle area from y1490 onward.
    subtitle=diff[:,187:235,:].mean(axis=(1,2))
    # Rendered cue occupies x76..446, y1085..1215 only, between 11.75..14.35.
    focus=diff[352:431,135:153,9:56].mean(axis=(1,2))
    outside=np.concatenate([diff[:350],diff[435:]],axis=0).mean(axis=(1,2))
    result={
      'source_adts_sha256':ah1,'output_adts_sha256':ah2,'adts_identical':True,
      'frames_compared':691,'sampling':'1/8 gray frame, 135x240',
      'subtitle_y_min':1490,'subtitle_region_mean_max':round(float(subtitle.max()),4),
      'subtitle_region_mean_p95':round(float(np.percentile(subtitle,95)),4),
      'cue_roi_mean':round(float(focus.mean()),4),
      'outside_cue_mean_p95':round(float(np.percentile(outside,95)),4),
      'semantic_asr_status':'UNVERIFIED: no independently obtained Japanese transcript',
      'phone_playback':'UNVERIFIED',
      'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    }
    if result['subtitle_region_mean_max']>3:
        raise RuntimeError('caption-region reencoding difference exceeds 3 gray levels')
    if result['cue_roi_mean']<2:
        raise RuntimeError('visual cue did not materially change')
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


if __name__=='__main__':
    print(json.dumps(verify(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])),indent=2))
