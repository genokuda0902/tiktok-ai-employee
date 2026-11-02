#!/usr/bin/env python3
"""Review-only cleanup of an unnecessary waveform HUD; preserve Japanese captions and AAC.

Reimplementation, not v33 original. 10-genre configurable, offline and fail-closed.
The source file is supplied locally; never upload confidential media to GitHub.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
ACCENTS = {'ai':'32D8D0','business':'F0BE70','money':'70D89C',
           'learning':'B3A2FF','health':'83DAC9','food':'FFC48D',
           'travel':'86CEFF','beauty':'F2A7D7','career':'F2D181','life':'A2D7AE'}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CAPTION_SAFE_BOTTOM = 1708
CLEAN_ROI = (48, 1710, 984, 180)


def cmd(args):
    p = subprocess.run([str(x) for x in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('ffmpeg/ffprobe failed: '+p.stderr.decode(errors='replace')[-1800:])
    return p.stdout


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def info(path):
    j=json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))
    v=next(x for x in j['streams'] if x['codec_type']=='video')
    a=next(x for x in j['streams'] if x['codec_type']=='audio')
    return {'duration':float(j['format']['duration']),'frames':int(v.get('nb_frames',0)),
            'width':int(v['width']),'height':int(v['height']), 'fps':v['avg_frame_rate'],
            'vcodec':v['codec_name'],'acodec':a['codec_name'],
            'sample_rate':int(a['sample_rate']),'language':a.get('tags',{}).get('language','und')}


def audio_digest(path):
    return hashlib.sha256(cmd(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()


def validate(manifest,source):
    if (manifest.get('policy')!=POLICY or manifest.get('asset_approval')!='review_only_no_publication'
            or manifest.get('manual_post_only') is not True or manifest.get('roi_reviewed') is not True):
        raise ValueError('Fail closed: human review and ROI approval required')
    if manifest.get('source_sha256')!=digest(source):
        raise ValueError('Fail closed: source SHA-256 mismatch')
    if manifest.get('genre') not in ACCENTS:
        raise ValueError('Unsupported genre')
    if manifest.get('caption_safe_bottom')!=CAPTION_SAFE_BOTTOM:
        raise ValueError('Unreviewed caption boundary')
    if CLEAN_ROI[1] < CAPTION_SAFE_BOTTOM:
        raise ValueError('Overlap with protected captions')
    i=info(source)
    if (i['width'],i['height'],i['fps'],i['vcodec'],i['acodec'],i['sample_rate']) != (1080,1920,'30/1','h264','aac',48000):
        raise ValueError('Unsupported source format')
    if i['duration']<2.0:
        raise ValueError('Source too short')
    return i


def filtergraph(genre,duration):
    if genre not in ACCENTS: raise ValueError('Unsupported genre')
    if not (2 <= duration <= 120): raise ValueError('Invalid duration')
    color=ACCENTS[genre]
    x,y,w,h=CLEAN_ROI
    # Waveform was a distracting diagnostic UI. Replace only the reviewed bottom band.
    base=(f'[0:v]drawbox=x={x}:y={y}:w={w}:h={h}:color=0x02091B@1:t=fill,'
          f'drawtext=fontfile={FONT}:text=AI時短ラボ:fontcolor=0xD8E8F0:fontsize=29:x=90:y=1764,'
          f'drawtext=fontfile={FONT}:text=レビュー用:fontcolor=0xA7B8CA:fontsize=24:x=850:y=1767,'
          f'drawbox=x=90:y=1833:w=900:h=4:color=0x1B314B@1:t=fill,'
          f'drawbox=x=90:y=1833:w=20:h=4:color=0x{color}@1:t=fill[base];')
    # A restrained moving progress indicator, unlike the original busy audio waveform.
    return (base+f'color=c=0x{color}:s=14x14:r=30:d={duration:.6f}[dot];'
            f'[base][dot]overlay=x=90+886*t/{duration:.6f}:y=1828:eval=frame:shortest=1:format=auto,'
            f'format=yuv420p[v]')


def render(source,output,manifest_path,report_path):
    source,output,manifest_path,report_path=map(Path,(source,output,manifest_path,report_path))
    if not source.is_file() or source.resolve()==output.resolve(): raise ValueError('Missing source or same output path')
    m=json.loads(manifest_path.read_text(encoding='utf-8'))
    before=validate(m,source)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-filter_complex',filtergraph(m['genre'],before['duration']),
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
         '-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',
         '-t',f"{before['duration']:.6f}",output])
    cmd(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    after=info(output)
    same_audio=audio_digest(source)==audio_digest(output)
    passed=(same_audio and before['frames']==after['frames'] and
            abs(before['duration']-after['duration'])<0.05)
    result={'policy':POLICY,'genre':m['genre'],'source_sha256':digest(source),
            'output_sha256':digest(output),'source':before,'output':after,
            'roi':CLEAN_ROI,'protected_caption_bottom':CAPTION_SAFE_BOTTOM,
            'audio_bit_identical':same_audio,'full_av_decode':True,'technical_pass':passed,
            'independent_japanese_asr':False,'subtitle_semantics_timing_verified':False,
            'smartphone_playback_verified':False,'rights_approved':False,
            'employee_approved':False,'publication_approved':False}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if not passed:
        output.unlink(missing_ok=True)
        raise RuntimeError('Technical QA failed: output removed')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for a in ('source','output','manifest','report'): ap.add_argument('--'+a,required=True)
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.manifest,args.report),ensure_ascii=False,indent=2))
