#!/usr/bin/env python3
"""Fail-closed single-caption playback MP4 + optional SRT (PRIVATE REVIEW).

MP4 muxers may mark a sole mov_text subtitle as default even with
-disposition:s:0 0. Avoid duplicate captions by omitting that optional track
from the playback MP4, while preserving a separate Japanese SRT. The original
video has burned-in Japanese captions; encoded A/V are copied unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
PRIVATE_TESTED = ('ai_work',)


def run(args):
    p = subprocess.run([str(a) for a in args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError('command failed: ' + ' '.join(map(str,args)) + '\n' + p.stderr[-1500:])
    return p.stdout


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))


def streams(meta):
    s = meta['streams']
    if len(s) != 3 or [x['codec_type'] for x in s] != ['video','audio','subtitle']:
        raise ValueError('requires exactly one video, one audio and one selectable subtitle')
    v,a,sub = s
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate']) != ('h264',1080,1920,'30/1'):
        raise ValueError('unsupported video stream')
    if (a['codec_name'],a['sample_rate'],a.get('tags',{}).get('language')) != ('aac','48000','jpn'):
        raise ValueError('Japanese-tagged AAC 48kHz required (metadata is not speech proof)')
    if (sub['codec_name'],sub.get('tags',{}).get('language')) != ('mov_text','jpn'):
        raise ValueError('Japanese selectable mov_text required')
    return v,a,sub


def policy(genre, review_only, expected_sha, source, output):
    if genre not in GENRES or genre not in PRIVATE_TESTED:
        raise ValueError('unknown or unapproved genre: fail closed')
    if not review_only:
        raise ValueError('human review required; no release mode')
    if not re.fullmatch('[0-9a-fA-F]{64}',expected_sha):
        raise ValueError('pinned source SHA256 required')
    src, dst = Path(source).resolve(), Path(output).resolve()
    if src == dst or dst.exists():
        raise ValueError('cannot overwrite original or existing output')
    if sha256(src).lower() != expected_sha.lower():
        raise ValueError('source SHA256 mismatch')


def elementary_hashes(source, directory, name):
    paths = {}
    for kind,ext,opts in (
        ('video','h264',['-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264']),
        ('audio','aac',['-map','0:a:0','-c:a','copy','-f','adts']),
        ('subtitle','srt',['-map','0:s:0','-f','srt']),
    ):
        p = Path(directory)/(name+'.'+ext)
        run(['ffmpeg','-v','error','-y','-i',source,*opts,str(p)])
        paths[kind] = sha256(p)
        if kind == 'subtitle':
            paths['subtitle_cues'] = p.read_text(encoding='utf-8-sig').count('-->')
    return paths


def repair(source, output, report, expected_sha, genre='ai_work', review_only=False):
    policy(genre, review_only, expected_sha, source, output)
    before = probe(source)
    v0,a0,s0 = streams(before)
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    sidecar = Path(output).with_suffix('.srt')
    if sidecar.exists():
        raise ValueError('sidecar already exists; refusing overwrite')
    # FFmpeg MOV/MP4 can force the sole subtitle track to default even with
    # -disposition:s:0 0. Export that track as an optional SRT instead.
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
         '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
         '-c','copy','-disposition:v:0','default','-disposition:a:0','default',
         '-movflags','+faststart',output])
    run(['ffmpeg','-v','error','-y','-i',source,'-map','0:s:0','-f','srt',sidecar])
    after = probe(output)
    if len(after['streams']) != 2 or [x['codec_type'] for x in after['streams']] != ['video','audio']:
        raise AssertionError('unexpected subtitle stream in safe playback MP4')
    v,a = after['streams']
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate']) != ('h264',1080,1920,'30/1'):
        raise AssertionError('video format changed')
    if (a['codec_name'],a['sample_rate'],a.get('tags',{}).get('language')) != ('aac','48000','jpn'):
        raise AssertionError('audio format/language metadata changed')
    if abs(float(before['format']['duration'])-float(after['format']['duration'])) > 0.001:
        raise AssertionError('duration changed')
    for t in ('v','a'):
        run(['ffmpeg','-v','error','-xerror','-i',output,'-map',f'0:{t}:0','-f','null','-'])
    with tempfile.TemporaryDirectory() as tmp:
        hb = elementary_hashes(source,tmp,'before')
        # Playback MP4 has no subtitle; check A/V elementary streams separately.
        ha = {}
        for kind,ext,opts in (
            ('video','h264',['-map','0:v:0','-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264']),
            ('audio','aac',['-map','0:a:0','-c:a','copy','-f','adts']),
        ):
            p=Path(tmp)/('after.'+ext)
            run(['ffmpeg','-v','error','-y','-i',output,*opts,p])
            ha[kind]=sha256(p)
    if any(hb[k] != ha[k] for k in ('video','audio')):
        raise AssertionError('encoded video/audio changed')
    if sha256(sidecar) != hb['subtitle'] or hb['subtitle_cues'] < 1:
        raise AssertionError('SRT text not preserved')
    data = {
        'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
        'source_sha256':sha256(source),'output_sha256':sha256(output),
        'change':'avoid duplicate burned + auto-enabled soft captions: MP4 has baked captions only; optional SRT sidecar',
        'before_subtitle_default':s0['disposition'].get('default'),
        'after_mp4_subtitle_streams':0,'sidecar_srt_sha256':sha256(sidecar),
        'sidecar_cues':hb['subtitle_cues'],
        'duration_seconds':float(after['format']['duration']),
        'resolution':f"{v['width']}x{v['height']}",'fps':v['r_frame_rate'],
        'video_frames':int(v.get('nb_frames',0)),'audio_sample_rate':a['sample_rate'],
        'japanese_audio_tag':a['tags']['language'],
        'encoded_video_audio_equal':True,'video_audio_sha256':ha,
        'video_decode':'PASS','audio_decode':'PASS',
        'independent_japanese_asr':'NOT_AVAILABLE','caption_semantic_sync':'NOT_VERIFIED',
        'mobile_player_subtitle_behavior':'NOT_TESTED','publication_approved':False,
        'other_genres':'FAIL_CLOSED',
    }
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--report',required=True)
    p.add_argument('--expected-sha',required=True)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--review-only',action='store_true')
    a=p.parse_args()
    print(json.dumps(repair(a.source,a.output,a.report,a.expected_sha,a.genre,a.review_only),ensure_ascii=False))
