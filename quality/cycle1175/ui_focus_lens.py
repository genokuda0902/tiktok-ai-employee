#!/usr/bin/env python3
"""Review-only UI focus lens for pre-existing video; never generates fictitious UI data.

This reimplementation uses a live crop of the same source stream. It does not
claim that the underlying clip is a real-time screen recording. It does not
transcribe Japanese speech. Assets remain local and are not committed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
PALETTES = {'ai':'2BE2D2','business':'F0C171','money':'7ED6A1',
            'learning':'B4A2F8','health':'83DAC9','food':'FFC48D',
            'travel':'86CEFF','beauty':'F2A7D7','career':'F2D181','life':'A2D7AE'}
# Each focus rectangle must be manually reviewed against the input frame.
# x,y,w,h are coordinates of the real, already present UI, never fabricated text.
CUES = (
    (6.16, 6.96, (355, 343, 290, 54)),  # formula bar
    (6.96, 7.77, (230, 699, 340, 62)),  # fictional totals 46 / 29
    (7.77, 8.73, (540, 699, 255, 62)),  # human-review status
)
ZOOM_X, ZOOM_Y, ZOOM_W, ZOOM_H = 180, 807, 720, 170
CAPTION_SAFE_Y = 1270


def call(cmd):
    p=subprocess.run([str(x) for x in cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-2500:])
    return p.stdout


def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def probe(path):
    j=json.loads(call(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))
    v=next(s for s in j['streams'] if s['codec_type']=='video')
    a=next(s for s in j['streams'] if s['codec_type']=='audio')
    return {'duration':float(j['format']['duration']),'frames':int(v.get('nb_frames') or 0),
            'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],
            'video':v['codec_name'],'audio':a['codec_name'],
            'sample_rate':int(a['sample_rate']),'language':a.get('tags',{}).get('language','und')}


def adts_sha(path):
    return hashlib.sha256(call(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()


def validate(manifest,src):
    expected={'policy':POLICY,'asset_approval':'review_only_no_publication',
              'manual_post_only':True,'roi_reviewed':True,
              'caption_safe_y':CAPTION_SAFE_Y}
    if any(manifest.get(k)!=v for k,v in expected.items()):
        raise ValueError('Fail closed: approval, safe area, or source SHA mismatch')
    if manifest.get('source_sha256') != digest(src):
        raise ValueError('Source hash mismatch')
    if manifest.get('genre') not in PALETTES:
        raise ValueError('Unsupported genre')
    m=probe(src)
    if (m['width'],m['height'],m['fps'],m['video'],m['audio'],m['sample_rate']) != (1080,1920,'30/1','h264','aac',48000):
        raise ValueError('Source must be H264 1080x1920 30fps + AAC 48k')
    if m['duration'] < max(c[1] for c in CUES):
        raise ValueError('Source ends before focus cues')
    if ZOOM_Y+ZOOM_H >= CAPTION_SAFE_Y:
        raise ValueError('Lens overlaps subtitle safe area')
    for start,end,(x,y,w,h) in CUES:
        if start>=end or min(x,y,w,h)<0 or x+w>1080 or y+h>CAPTION_SAFE_Y:
            raise ValueError('Invalid focus cue geometry')
    return m


def graph(genre):
    """Crop the actual source video, highlight exact source coordinates, preserve captions."""
    accent='0x'+PALETTES[genre]
    g='[0:v]split=4[b][a0][a1][a2];'
    for i,(start,end,(x,y,w,h)) in enumerate(CUES):
        # The inset is a crop of the *same input video*, never a fake UI screenshot.
        g+=f'[a{i}]trim=start={start}:end={end},setpts=PTS-STARTPTS+{start}/TB,crop={w}:{h}:{x}:{y},scale={ZOOM_W}:{ZOOM_H}:flags=lanczos,format=yuv420p,drawbox=x=0:y=0:w=iw:h=ih:color={accent}@0.95:t=6[z{i}];'
        g+=f"[{'b' if i==0 else 'v'+str(i-1)}]drawbox=x={x}:y={y}:w={w}:h={h}:color={accent}@0.98:t=5:enable='gte(t,{start})*lt(t,{end})'[d{i}];"
        g+=f"[d{i}][z{i}]overlay=x={ZOOM_X}:y={ZOOM_Y}:enable='gte(t,{start})*lt(t,{end})':eof_action=pass:format=auto[v{i}];"
    return g+'[v2]format=yuv420p[v]'


def render(src,dst,manifest_path,report_path):
    src,dst,manifest_path,report_path=map(Path,(src,dst,manifest_path,report_path))
    if not src.is_file() or src.resolve()==dst.resolve():
        raise ValueError('Source missing or output would overwrite source')
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    before=validate(manifest,src)
    dst.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',src,'-filter_complex',graph(manifest['genre']),
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
         '-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-t',str(before['duration']),dst]
    call(cmd)
    call(['ffmpeg','-v','error','-xerror','-i',dst,'-f','null','-'])
    after=probe(dst)
    audio_same=adts_sha(src)==adts_sha(dst)
    passed=audio_same and before['frames']==after['frames'] and abs(before['duration']-after['duration'])<0.05
    result={'policy':POLICY,'source_sha256':digest(src),'output_sha256':digest(dst),
            'genre':manifest['genre'],'before':before,'after':after,'focus_cues':CUES,
            'subtitle_safe_y':CAPTION_SAFE_Y,'audio_adts_bit_identical':audio_same,
            'full_av_decode':True,'technical_pass':passed,
            'independent_japanese_asr':False,'caption_semantic_sync_verified':False,
            'smartphone_verified':False,'asset_rights_approved':False,
            'employee_approved':False,'publication_approved':False}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if not passed:
        dst.unlink(missing_ok=True)
        raise RuntimeError('Technical output failed validation')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for a in ('source','output','manifest','report'):p.add_argument('--'+a,required=True)
    x=p.parse_args()
    print(json.dumps(render(x.source,x.output,x.manifest,x.report),ensure_ascii=False,indent=2))
