#!/usr/bin/env python3
"""Review-only, source-matched removal of duplicate burned captions.

Restores an unobstructed, user-provided earlier local scene in a limited region
without touching audio. Never infers publication permission from possession.
The inputs must have the same timeline. Human approval is still required.
Reimplementation; not the original v33 engine.
"""
import argparse
import json
import subprocess
from pathlib import Path

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout

def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                           '-of', 'json', str(path)]))

def validate(source, clean, policy):
    a, b = probe(source), probe(clean)
    def video(meta):
        return next(s for s in meta['streams'] if s['codec_type'] == 'video')
    va, vb = video(a), video(b)
    for field in ('width', 'height', 'r_frame_rate'):
        if va[field] != vb[field]:
            raise ValueError(f'baseline mismatch: {field}')
    if abs(float(a['format']['duration']) - float(b['format']['duration'])) > 0.07:
        raise ValueError('source and clean reference must have matching duration')
    if not any(s['codec_type'] == 'audio' for s in a['streams']):
        raise ValueError('source audio missing')
    w, h = va['width'], va['height']
    x, y, cw, ch = (policy[k] for k in ('x', 'y', 'width', 'height'))
    if any(type(v) is not int for v in (x, y, cw, ch)) or min(x, y) < 0 or min(cw, ch) < 1 or x+cw>w or y+ch>h:
        raise ValueError('invalid replacement rectangle')
    start, end = policy['start_seconds'], policy['end_seconds']
    if not (isinstance(start, (int, float)) and isinstance(end, (int, float)) and 0 <= start < end <= float(a['format']['duration'])):
        raise ValueError('invalid replacement timeline')
    suppressed = policy['suppressed_cue_indices']
    if not suppressed or len(set(suppressed)) != len(suppressed) or any(not isinstance(i, int) or i < 1 for i in suppressed):
        raise ValueError('suppressed caption IDs must be unique positive integers')
    if policy.get('publication_approved') is not False or policy.get('asset_rights_verified') is not False:
        raise ValueError('review-only policy must fail closed')
    return {'fps': va['r_frame_rate'], 'width': w, 'height': h, 'duration': float(a['format']['duration']),
            'suppressed_cues': suppressed, 'rect': [x,y,cw,ch], 'time': [start,end]}

def render(source, clean, output, policy):
    if 'REVIEW_ONLY' not in Path(output).name:
        raise ValueError('output filename must contain REVIEW_ONLY')
    details = validate(source, clean, policy)
    x,y,w,h = details['rect']
    a,b = details['time']
    filt = (f'[1:v]crop={w}:{h}:{x}:{y}[unobstructed];'
            f"[0:v][unobstructed]overlay={x}:{y}:enable='between(t,{a},{b})':eof_action=pass[v]")
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(clean),
           '-filter_complex',filt,'-map','[v]','-map','0:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
           '-r','30','-c:a','copy','-movflags','+faststart',str(output)]
    run(cmd)
    details.update({'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
                    'source':str(source),'clean_reference':str(clean),'output':str(output),
                    'japanese_narration_semantics_verified':False,
                    'draft_srt_is_not_verified_transcript':True})
    return details

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--clean-reference',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--policy',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    policy=json.loads(args.policy.read_text(encoding='utf-8'))
    details=render(args.source,args.clean_reference,args.output,policy)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(details,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(details,ensure_ascii=False))

if __name__=='__main__':
    main()
