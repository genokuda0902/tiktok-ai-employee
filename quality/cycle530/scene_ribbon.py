#!/usr/bin/env python3
"""Cycle530: 10-genre reusable scene-stage ribbon, review-only.

Adds a time-coded chapter guide under the masthead. Original audio is copied.
No Japanese TTS or speech-caption synchronization is claimed. No publication.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし',
)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
STAGES = ((2.5, 5.0, '課題'), (5.0, 10.0, '操作'),
          (10.0, 15.0, '結果'), (15.0, 17.5, '確認'))


def command(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'command failed ({r.returncode}): {r.stderr[-3000:]}')
    return r.stdout


def validate_manifest(m, source):
    if m.get('genre') not in GENRES:
        raise ValueError('genre not in 10-genre contract')
    if m.get('rights') != 'SYNTHETIC_OR_OWNER_APPROVED':
        raise ValueError('rights not cleared')
    if m.get('contains_private_data') is not False:
        raise ValueError('privacy not cleared')
    if m.get('review_status') != 'HUMAN_REVIEW' or m.get('publication') != 'NOT_APPROVED':
        raise ValueError('unapproved publication state')
    if m.get('japanese_narration') != 'NOT_GENERATED':
        raise ValueError('narration status must be explicit')
    if hashlib.sha256(Path(source).read_bytes()).hexdigest() != m.get('source_sha256'):
        raise ValueError('source SHA256 mismatch')
    if not Path(FONT).is_file():
        raise ValueError('Noto Sans CJK font unavailable')


def make_filter(stages=STAGES):
    if len(stages) != 4:
        raise ValueError('expected four stages')
    previous = -1
    parts = []
    for idx, (start, end, label) in enumerate(stages):
        if start < previous or end <= start or end > 20 or not label or ':' in label:
            raise ValueError('invalid stage contract')
        previous = end
        x = 77 + idx * 235
        parts.append(f'drawbox=x={x}:y=182:w=215:h=8:color=0x22495c@0.95:t=fill:enable=between(t\\,2.5\\,17.5)')
        parts.append(f'drawtext=fontfile={FONT}:text={label}:fontcolor=0x91aebc:fontsize=26:x={x+73}:y=147:enable=between(t\\,2.5\\,17.5)')
        parts.append(f'drawbox=x={x}:y=182:w=215:h=8:color=0x3de7e5:t=fill:enable=between(t\\,{start}\\,{end})')
        parts.append(f'drawtext=fontfile={FONT}:text={label}:fontcolor=white:fontsize=26:x={x+73}:y=147:enable=between(t\\,{start}\\,{end})')
    return ','.join(parts) + ',format=yuv420p'


def probe(path):
    return json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def audio_md5(path):
    return command(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).strip()


def render(source, dest, manifest, qa_path):
    source, dest, qa_path = map(Path, (source,dest,qa_path))
    validate_manifest(manifest, source)
    data=probe(source)
    v=next(x for x in data['streams'] if x['codec_type']=='video')
    a=next(x for x in data['streams'] if x['codec_type']=='audio')
    if (v['width'],v['height'],v['codec_name'],a['codec_name']) != (1080,1920,'h264','aac'):
        raise ValueError('expected 1080x1920 H.264/AAC')
    if abs(float(data['format']['duration'])-20)>0.05:
        raise ValueError('expected 20s input')
    dest.parent.mkdir(parents=True,exist_ok=True)
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
          '-vf',make_filter(),'-map','0:v:0','-map','0:a:0',
          '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
          '-c:a','copy','-t','20','-movflags','+faststart',str(dest)]
    command(args)
    data=probe(dest)
    v=next(x for x in data['streams'] if x['codec_type']=='video')
    a=next(x for x in data['streams'] if x['codec_type']=='audio')
    checks={
        'h264_aac': v['codec_name']=='h264' and a['codec_name']=='aac',
        '1080x1920': (v['width'],v['height'])==(1080,1920),
        'duration_20s': abs(float(data['format']['duration'])-20)<=0.05,
        '30fps': v['avg_frame_rate']=='30/1',
        '600_frames': int(v.get('nb_frames',-1))==600,
        'audio_bitstream_preserved': audio_md5(source)==audio_md5(dest),
        'review_only': manifest['review_status']=='HUMAN_REVIEW' and manifest['publication']=='NOT_APPROVED',
    }
    qa={
      'cycle':530, 'source':source.name, 'output':dest.name,
      'change':'four-stage navigation ribbon at y=147..190 during 2.5..17.5s',
      'stages':[{'start':s,'end':e,'label':label} for s,e,label in STAGES],
      'reference_storyboard':'VISUALLY_INSPECTED',
      'reference_v33_video':'RAW_BYTES_UNAVAILABLE',
      'market_research':'SUMMARY_ONLY',
      'japanese_narration':'NOT_GENERATED',
      'speech_caption_sync':'NOT_VERIFIED',
      'captions':'PREVIOUS_JAPANESE_EXPLANATORY_TEXT_PRESERVED',
      'checks':checks, 'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
      'publication':'NOT_APPROVED', 'review_status':'HUMAN_REVIEW',
    }
    qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not all(checks.values()):
        raise RuntimeError('QA failed: '+json.dumps(checks))
    return qa


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True)
    p.add_argument('--qa',required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(Path(a.manifest).read_text(encoding='utf-8')),a.qa),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
