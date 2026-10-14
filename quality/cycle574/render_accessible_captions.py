#!/usr/bin/env python3
"""cycle574: genre-neutral burned-in caption compositor for review-only MP4.

The baseline video is not uploaded to GitHub. This renderer is a reimplementation,
not the missing original v33 renderer. It never generates or claims Japanese TTS.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

BASELINE_SHA256 = 'd581e69deef8e81e5a6cdd9f957095ed829cc552df16e325fd604d0a8a49ab93'
GENRES = ('ai_productivity', 'beauty', 'relationships', 'finance', 'sales',
          'career', 'wellness', 'science', 'travel_food', 'product_comparison')
CUES = (
    (0.0, 2.0, '4か月の架空売上を確認'),
    (2.0, 4.0, '120＋150＋200＋250'),
    (4.0, 6.0, '検算結果は 720'),
    (6.0, 9.0, '数字を入力し、集計を指示（再現）'),
    (9.0, 12.0, 'B2:B5 を選択 → SUM 関数'),
    (12.0, 16.0, '表とグラフの4本の数値を照合'),
    (16.0, 18.5, '手入力と関数を比較（再現）'),
    (18.5, 20.0, '保存して、後で検算'),
)

def validate_cues(cues=CUES, duration=20.0):
    if not cues:
        raise ValueError('At least one caption required')
    last = 0.0
    for start, end, caption in cues:
        if abs(start-last) > 0.001 or end-start < 1.0 or end > duration + 0.001:
            raise ValueError('Captions must be continuous and readable >=1s')
        if not caption or len(caption) > 30 or '\n' in caption:
            raise ValueError('Caption must be concise single-line Japanese')
        last = end
    if abs(last-duration) > 0.001:
        raise ValueError('Captions must cover full duration')
    return True

def approval_gate(metadata):
    if metadata.get('publication') != 'NOT_APPROVED' or metadata.get('auto_post') is not False:
        raise ValueError('No automatic publishing or approval')
    if metadata.get('narration') != 'ABSENT' or metadata.get('voice_semantic_sync') != 'UNVERIFIED':
        raise ValueError('Do not claim Japanese narration or speech sync')
    if metadata.get('rights') != 'INHERITED_ASSETS_UNVERIFIED':
        raise ValueError('Inherited assets must remain unapproved')
    return True

def timestamp(t):
    ms = round(t*1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def ass_timestamp(t):
    cs = round(t*100)
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f'{h}:{m:02}:{s:02}.{cs:02}'

def write_captions(folder, cues=CUES):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    validate_cues(cues)
    srt = '\n\n'.join(f'{i}\n{timestamp(a)} --> {timestamp(b)}\n{c}' for i,(a,b,c) in enumerate(cues,1))+'\n'
    (folder/'captions.srt').write_text(srt,encoding='utf-8')
    head = '''[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Caption,Noto Sans CJK JP,48,&H00FFFFFF,&H00FFFFFF,&H00101923,&H9906131E,-1,0,0,0,100,100,0,0,3,5,0,2,54,54,150,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
    body = ''.join(f'Dialogue: 0,{ass_timestamp(a)},{ass_timestamp(b)},Caption,,0,0,0,,{c}\n' for a,b,c in cues)
    (folder/'captions.ass').write_text(head+body,encoding='utf-8')
    return srt

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=index,codec_type,codec_name,width,height,r_frame_rate:format=duration','-of','json',str(path)],text=True))

def render(source, output, genre='ai_productivity'):
    if genre not in GENRES: raise ValueError('Unknown genre')
    source=Path(source); output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    if sha != BASELINE_SHA256: raise ValueError('Pinned source mismatch; refuse unexpected inherited media')
    src=probe(source)
    video=next((x for x in src['streams'] if x['codec_type']=='video'),None)
    audio=next((x for x in src['streams'] if x['codec_type']=='audio'),None)
    if video is None or audio is None or (video['width'],video['height'],video['r_frame_rate'])!=(1080,1920,'30/1') or abs(float(src['format']['duration'])-20)>.05:
        raise ValueError('Source must be 20s 1080x1920 30fps with audio')
    metadata={'cycle':574,'genre':genre,'baseline_sha256':sha,'narration':'ABSENT','voice_semantic_sync':'UNVERIFIED','rights':'INHERITED_ASSETS_UNVERIFIED','publication':'NOT_APPROVED','auto_post':False,'cost_jpy':0}
    approval_gate(metadata)
    write_captions(output.parent)
    ass_path=output.parent/'captions.ass'
    srt_path=output.parent/'captions.srt'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(srt_path),'-vf',f'ass={ass_path}:fontsdir=/usr/share/fonts/opentype/noto','-map','0:v:0','-map','0:a:0','-map','1:s:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30','-c:a','copy','-c:s','mov_text','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,capture_output=True,text=True)
    info=probe(output)
    if abs(float(info['format']['duration'])-20)>.05 or not {'video','audio','subtitle'}.issubset({s['codec_type'] for s in info['streams']}):
        raise RuntimeError('Output QA failed')
    metadata.update({'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'cue_count':len(CUES),'min_cue_seconds':min(b-a for a,b,_ in CUES),'output_probe':info,'command':cmd,'reference_storyboard':'VIEWED','reference_v33':'RAW_ACCESS_DENIED'})
    (output.parent/'manifest.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    return metadata

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--genre',default='ai_productivity')
    a=ap.parse_args();print(json.dumps(render(a.source,a.output,a.genre),ensure_ascii=False,indent=2))
