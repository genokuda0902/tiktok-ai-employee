"""Review-only, genre-independent focus beats on pre-approved existing MP4.

Changes picture only; preserves Japanese AAC and optional subtitles by stream
copy. This does NOT verify speech, source rights, or publication approval.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

CAPTION_SAFE_Y = 1270

def validate(config):
    if config.get('review_only') is not True or config.get('publication_approved') is not False:
        raise ValueError('review-only fail-closed configuration required')
    if config.get('genre') is None or not isinstance(config['genre'], str):
        raise ValueError('genre required')
    beats = config.get('beats')
    if not isinstance(beats, list) or not 2 <= len(beats) <= 10:
        raise ValueError('2-10 focus beats required')
    last_end = -1.0
    for b in beats:
        if not all(k in b for k in ('start','end','x','y','w','h')):
            raise ValueError('incomplete beat')
        st,en=float(b['start']),float(b['end'])
        x,y,w,h=[int(b[k]) for k in ('x','y','w','h')]
        if st < 0 or en <= st or st < last_end:
            raise ValueError('beats must be ordered and nonoverlapping')
        if x < 0 or y < 0 or w < 40 or h < 40 or x+w > 1080 or y+h >= CAPTION_SAFE_Y:
            raise ValueError('focus region outside 1080x1920 safe upper picture')
        last_end=en
    return beats

def filtergraph(config):
    filters=[]
    for b in validate(config):
        start,end=float(b['start']),float(b['end'])
        x,y,w,h=[int(b[k]) for k in ('x','y','w','h')]
        enabled=f"between(t\\,{start:.3f}\\,{end:.3f})"
        filters.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0x22e6d1@0.95:t=7:enable='{enabled}'")
        filters.append(f"drawbox=x={x-1 if x>0 else x}:y={y+16}:w=9:h={h-32}:color=0xffffff@0.92:t=fill:enable='{enabled}'")
    return ','.join(filters)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):
            h.update(chunk)
    return h.hexdigest()

def render(source, output, config, expected_sha=None, preset='veryfast'):
    validate(config)
    if expected_sha and sha256(source)!=expected_sha:
        raise ValueError('input SHA256 mismatch: refusing unknown media')
    if Path(source).resolve()==Path(output).resolve():
        raise ValueError('never overwrite original source')
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-xerror','-y','-i',str(source),
         '-map','0:v:0','-map','0:a:0','-map','0:s?','-vf',filtergraph(config),
         '-c:v','libx264','-preset',preset,'-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-c:s','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'beats':len(config['beats']),'review_only':True,'publication_approved':False,
            'independent_asr':False,'command':' '.join(cmd)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--config',required=True)
    ap.add_argument('--expected-sha256')
    ap.add_argument('--report')
    args=ap.parse_args()
    config=json.loads(Path(args.config).read_text(encoding='utf-8'))
    report=render(args.source,args.output,config,args.expected_sha256)
    if args.report:
        Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='command'},ensure_ascii=False))

if __name__=='__main__':
    main()
