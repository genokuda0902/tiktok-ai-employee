#!/usr/bin/env python3
"""Offline review-only loudness repair for approved synthetic TikTok MP4s.

This does not synthesize Japanese speech. It does not approve publishing.
The source MP4 is supplied separately, never uploaded to GitHub.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし',
)
TARGET_I = -20.0
TARGET_TP = -2.0
TARGET_LRA = 7.0


def run(cmd, *, check=True):
    return subprocess.run(cmd, text=True, capture_output=True, check=check)


def parse_loudnorm(stderr):
    blocks = re.findall(r'\{\s*"input_i".*?\}', stderr, flags=re.S)
    if not blocks:
        raise RuntimeError('loudnorm measurement JSON absent')
    result = json.loads(blocks[-1])
    for field in ('input_i', 'input_tp', 'input_lra', 'input_thresh', 'target_offset'):
        if field not in result or result[field] in ('inf', '-inf', 'nan'):
            raise RuntimeError(f'loudnorm measurement invalid: {field}')
    return result


def probe(path):
    r = run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    return json.loads(r.stdout)


def check_input(path, manifest):
    if not path.is_file() or path.stat().st_size < 1024:
        raise ValueError('source MP4 missing')
    if manifest.get('genre') not in GENRES:
        raise ValueError('unknown genre')
    if manifest.get('rights') != 'SYNTHETIC_OR_OWNER_APPROVED':
        raise ValueError('rights not explicitly cleared')
    if manifest.get('contains_private_data') is not False:
        raise ValueError('privacy must be explicitly cleared')
    if manifest.get('publication') != 'NOT_APPROVED':
        raise ValueError('publication state must be NOT_APPROVED')
    if manifest.get('review_status') != 'HUMAN_REVIEW':
        raise ValueError('review status must be HUMAN_REVIEW')
    streams = probe(path)['streams']
    v = next((s for s in streams if s['codec_type'] == 'video'), None)
    a = next((s for s in streams if s['codec_type'] == 'audio'), None)
    if not v or not a or v['codec_name'] != 'h264' or a['codec_name'] != 'aac':
        raise ValueError('expected H.264 video and AAC audio')
    if (v.get('width'), v.get('height')) != (1080,1920):
        raise ValueError('expected vertical 1080x1920')
    if abs(float(v.get('duration', probe(path)['format']['duration']))-20.0) > 0.08:
        raise ValueError('expected 20 s review MP4')


def measure(path):
    cmd=['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af',
         f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json',
         '-f','null','-']
    r=run(cmd)
    return parse_loudnorm(r.stderr)


def video_md5(path):
    r=run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
           '-c:v','copy','-f','md5','-'])
    return r.stdout.strip()


def normalize(src, dst, manifest, qa_path):
    src, dst, qa_path = Path(src),Path(dst),Path(qa_path)
    check_input(src,manifest)
    before=measure(src)
    args=(f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:'
          f'measured_I={before["input_i"]}:measured_TP={before["input_tp"]}:'
          f'measured_LRA={before["input_lra"]}:measured_thresh={before["input_thresh"]}:'
          f'offset={before["target_offset"]}:linear=true:print_format=json')
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd=['ffmpeg','-y','-hide_banner','-nostats','-i',str(src),
         '-map','0:v:0','-map','0:a:0','-c:v','copy',
         '-af',args,'-ar','44100','-c:a','aac','-b:a','192k',
         '-movflags','+faststart',str(dst)]
    r=run(cmd)
    if not dst.exists() or dst.stat().st_size<10000:
        raise RuntimeError('render output missing')
    after=measure(dst)
    pre_md5, post_md5=video_md5(src),video_md5(dst)
    i, tp=float(after['input_i']),float(after['input_tp'])
    checks={
        'loudness_in_target': -22.0 <= i <= -18.0,
        'true_peak_safe': tp <= -1.5,
        'audible_gain_at_least_10_lu': i-float(before['input_i']) >= 10.0,
        'video_bitstream_unchanged': pre_md5 == post_md5,
        'rights_cleared': manifest['rights']=='SYNTHETIC_OR_OWNER_APPROVED',
        'publication_not_approved': manifest['publication']=='NOT_APPROVED',
    }
    qa={
        'cycle':'528','before_integrated_lufs':float(before['input_i']),
        'after_integrated_lufs':i,'before_true_peak_dbtp':float(before['input_tp']),
        'after_true_peak_dbtp':tp,'video_md5_before':pre_md5,
        'video_md5_after':post_md5,'checks':checks,
        'japanese_narration':'NOT_GENERATED',
        'voice_caption_sync':'NOT_VERIFIED',
        'captions':'INHERITED_FROM_CYCLE527_NOT_CHANGED',
        'review_status':'HUMAN_REVIEW','publication':'NOT_APPROVED',
        'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
        'commands':{'normalize':cmd},
    }
    qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not all(checks.values()):
        raise RuntimeError('fail-closed audio QA: '+str(checks))
    return qa


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True)
    p.add_argument('--qa',required=True)
    a=p.parse_args()
    manifest=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    qa=normalize(a.source,a.output,manifest,a.qa)
    print(json.dumps({k:v for k,v in qa.items() if k not in ('commands',)},ensure_ascii=False,indent=2))


if __name__=='__main__': main()
