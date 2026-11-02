#!/usr/bin/env python3
"""Review-only, ten-genre image-area glow and per-chapter audio-presence QA.

A 2D light pass, NOT 3D animation, ASR, rights clearance, or v33 reproduction.
Private source videos must never be uploaded to public CI/artifacts.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import subprocess

from PIL import Image

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai', 'business', 'money', 'learning', 'health', 'food',
          'travel', 'beauty', 'career', 'life')


def run(args, capture=False):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                          stderr=subprocess.PIPE if capture else subprocess.DEVNULL)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    info = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                           '-of', 'json', str(path)], True).stdout)
    v = next(x for x in info['streams'] if x['codec_type'] == 'video')
    a = next(x for x in info['streams'] if x['codec_type'] == 'audio')
    if (v['codec_name'], int(v['width']), int(v['height']), v['avg_frame_rate']) != ('h264', 1080, 1920, '30/1'):
        raise ValueError('Expected H264 1080x1920 30fps')
    if (a['codec_name'], int(a['sample_rate'])) != ('aac', 48000):
        raise ValueError('Expected AAC 48kHz')
    return {'duration': float(info['format']['duration']), 'frames': int(v.get('nb_frames') or 0),
            'size_bytes': Path(path).stat().st_size}


def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
                               '-c:a', 'copy', '-f', 'adts', 'pipe:1'], True).stdout).hexdigest()


def validate_manifest(m, source):
    if (m.get('policy') != POLICY or m.get('asset_approval') != 'review_only_no_publication'
            or m.get('manual_post_only') is not True or m.get('genre') not in GENRES
            or m.get('source_sha256') != sha256(source)):
        raise ValueError('Fail closed: policy, genre or source hash')
    start, end = m['window']
    if not (0 <= start < end <= probe(source)['duration'] and end - start <= 2.0):
        raise ValueError('Unsafe glow window')
    edges = m['chapter_edges']
    if len(edges) < 2 or abs(edges[0]) > .001 or abs(edges[-1]-probe(source)['duration']) > .06 or any(b-a < .25 for a,b in zip(edges,edges[1:])):
        raise ValueError('Invalid chapter boundaries')


def create_glow(path, w=420, h=640):
    """Original vector-style translucent blue light; no external imagery."""
    im = Image.new('RGBA', (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            dx = (x-w/2)/(w*.24)
            dy = (y-h/2)/(h*.36)
            alpha = round(58*math.exp(-.5*(dx*dx+dy*dy)))
            px[x,y] = (146, 227, 255, alpha)
    im.save(path)


def chapter_audio_rms(path, edges):
    raw = run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
               '-ac','1','-ar','16000','-f','f32le','pipe:1'], True).stdout
    values = array('f'); values.frombytes(raw)
    out=[]
    for a,b in zip(edges,edges[1:]):
        s=values[int(a*16000):min(len(values),int(b*16000))]
        if not s:
            raise ValueError('Empty audio chapter')
        out.append(round(math.sqrt(sum(float(v)*v for v in s)/len(s)),6))
    return out


def render(source, output, manifest, report):
    source,output,manifest,report=map(Path,(source,output,manifest,report))
    if source.resolve()==output.resolve():
        raise ValueError('Source overwrite prohibited')
    m=json.loads(manifest.read_text(encoding='utf-8'))
    validate_manifest(m,source)
    output.parent.mkdir(parents=True,exist_ok=True)
    glow=output.with_suffix('.glow.png')
    create_glow(glow)
    start,end=m['window']
    # Top illustration only (y=470..1110); subtitle panel begins below y=1490.
    xexpr=f'-420+(t-{start})*1020'
    filt=f"[0:v][1:v]overlay=shortest=1:x='{xexpr}':y=470:enable='between(t,{start},{end})':eval=frame:format=auto[v]"
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-loop','1','-framerate','30','-i',str(glow),'-filter_complex',filt,
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','medium','-crf','21',
         '-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)])
    glow.unlink(missing_ok=True)
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    a,b=probe(source),probe(output)
    rms=chapter_audio_rms(output,m['chapter_edges'])
    passed=(a['frames']==b['frames'] and a['frames']>0 and abs(a['duration']-b['duration'])<.05
            and audio_sha(source)==audio_sha(output) and all(r>.005 for r in rms))
    result={'policy':POLICY,'genre':m['genre'],'source_sha256':sha256(source),
            'output_sha256':sha256(output),'before':a,'after':b,
            'audio_adts_bit_identical':audio_sha(source)==audio_sha(output),
            'chapter_audio_rms':rms,'chapter_audio_presence_pass':all(r>.005 for r in rms),
            'full_av_decode':True,'technical_pass':passed,
            'independent_japanese_asr_verified':False,'subtitle_semantic_timing_verified':False,
            'rights_approved':False,'publication_approved':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if not passed:
        output.unlink(missing_ok=True)
        raise RuntimeError('Technical QA failed; see report')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','report'):p.add_argument('--'+k,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False,indent=2))
