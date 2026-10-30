#!/usr/bin/env python3
"""Review-only three-beat, readable task scene; no external assets or upload.

The inherited video is PRIVATE and never belongs in the public repository.
Japanese audio and burned captions are preserved; this is not ASR.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

GENRES = {
    'ai_work': ('0x23d4c5', '繰り返し作業を見つける', ('データの集計', '転記・入力', '資料・報告')),
    'beauty': ('0xf0a6c4', '毎日の手間を見つける', ('情報の整理', '予約の確認', '記録の作成')),
    'romance_psychology': ('0xbca5f2', '迷いの原因を整理する', ('気持ちの記録', '考えの整理', '行動の振り返り')),
    'money_saving': ('0xeacb7c', '見直す支出を見つける', ('固定費の確認', '買い物の記録', '予算の振り返り')),
    'sales_business': ('0x72bcff', '仕事の手間を見つける', ('数字の集計', '顧客情報の整理', '報告書の作成')),
    'career': ('0x65d9df', '準備の手間を見つける', ('経験の棚卸し', '応募先の比較', '面接の準備')),
    'health_lifestyle': ('0x69dca8', '習慣の手間を見つける', ('予定の整理', '食事の記録', '睡眠の振り返り')),
    'science_trivia': ('0xc8b3ff', '疑問を3つに分ける', ('仮説を立てる', '根拠を探す', '結果を比べる')),
    'travel_food': ('0xffb06f', '旅の準備を整理する', ('行き先を決める', '移動を調べる', '持ち物を確認')),
    'product_comparison_lifestyle': ('0x6dc9fa', '選ぶ基準を整理する', ('予算を決める', '特徴を比べる', '条件を確認')),
}
DETAILS = ('まず、繰り返していることを整理', '3つの候補から1つ選んで試す')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def call(args, binary=False):
    p=subprocess.run([str(a) for a in args],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.stdout if binary else p.stdout.decode('utf-8')

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def probe(path):
    return json.loads(call(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def audio_hash(path):
    return hashlib.sha256(call(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()

def escape(s):
    if any(c in s for c in "\\:'%,\n"):
        raise ValueError('unsafe caption characters')
    return s

def filter_graph(genre, start, end):
    if genre not in GENRES:raise ValueError('unknown genre')
    if not 0 <= start < end:raise ValueError('bad time range')
    color,heading,cards=GENRES[genre]
    between=f'between(t,{start:.3f},{end:.3f})'
    f=[f"drawbox=x=42:y=205:w=996:h=1220:color=0x061825@0.94:t=fill:enable='{between}'",
       f"drawbox=x=74:y=254:w=12:h=122:color={color}@1:t=fill:enable='{between}'",
       f"drawtext=fontfile={FONT}:text='{escape(heading)}':fontsize=61:fontcolor=white:x=115:y=260:enable='{between}'",
       f"drawtext=fontfile={REG}:text='{DETAILS[0]}':fontsize=37:fontcolor=0xbcd1dc:x=115:y=355:enable='{between}'"]
    for i,(label,y) in enumerate(zip(cards,(490,740,990))):
        at=start+(0.18,0.86,1.54)[i]
        enabled=f'between(t,{at:.3f},{end:.3f})'
        f += [f"drawbox=x=106:y={y}:w=868:h=192:color=0x123447@0.97:t=fill:enable='{enabled}'",
              f"drawbox=x=106:y={y}:w=10:h=192:color={color}@1:t=fill:enable='{enabled}'",
              f"drawbox=x=138:y={y+37}:w=90:h=95:color=0x0b2634@1:t=fill:enable='{enabled}'",
              f"drawtext=fontfile={FONT}:text='{i+1:02d}':fontsize=52:fontcolor={color}:x=154:y={y+45}:enable='{enabled}'",
              f"drawtext=fontfile={FONT}:text='{escape(label)}':fontsize=62:fontcolor=white:x=266:y={y+51}:enable='{enabled}'"]
    f += [f"drawtext=fontfile={REG}:text='{DETAILS[1]}':fontsize=42:fontcolor={color}:x=115:y=1327:enable='{between}'"]
    return ','.join(f)

def render(source, output, report, genre, expected_source_sha, review_only=False, synthetic_ci=False):
    if not review_only:raise ValueError('HUMAN_REVIEW gate required')
    src,out,rep=map(lambda x:Path(x).resolve(),(source,output,report))
    if not src.is_file() or out.exists() or rep.exists() or src==out:raise ValueError('missing input or output exists')
    if len(expected_source_sha)!=64 or sha(src)!=expected_source_sha:raise ValueError('source SHA mismatch')
    info=probe(src);v=[s for s in info['streams'] if s['codec_type']=='video'];a=[s for s in info['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or len(info['streams'])!=2:raise ValueError('requires single A/V with no extra streams')
    if (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],a[0]['codec_name'],int(a[0]['sample_rate']))!=(1080,1920,'30/1','aac',48000):raise ValueError('invalid media spec')
    duration=float(info['format']['duration'])
    start,end=(0.10,1.85) if synthetic_ci else (2.90,5.80)
    if duration<end-.02:raise ValueError('video too short')
    out.parent.mkdir(parents=True,exist_ok=True);rep.parent.mkdir(parents=True,exist_ok=True)
    call(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',src,
          '-map','0:v:0','-map','0:a:0','-vf',filter_graph(genre,start,end),
          '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','2',
          '-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',out])
    call(['ffmpeg','-v','error','-xerror','-i',out,'-f','null','-'])
    fin=probe(out)
    av=audio_hash(src)==audio_hash(out)
    if not av:raise RuntimeError('audio bitstream changed')
    vv=next(x for x in fin['streams'] if x['codec_type']=='video')
    if vv['width']!=1080 or vv['height']!=1920 or vv['r_frame_rate']!='30/1':raise RuntimeError('video spec changed')
    data={'source_sha256':sha(src),'output_sha256':sha(out),'genre':genre,
          'duration_seconds':float(fin['format']['duration']),'frames':int(vv.get('nb_frames',0)),
          'video':'H.264 1080x1920 30fps','audio':'AAC 48kHz Japanese-tagged',
          'audio_bitstream_unchanged':av,'full_av_decode':'PASS',
          'change':'scene02 clutter replaced with three sequential high-contrast task cards',
          'change_window_seconds':[start,end], 'caption_safe_area_y_min':1490,
          'independent_japanese_asr':'NOT_PERFORMED', 'subtitle_semantics':'NOT_VERIFIED',
          'rights':'NOT_VERIFIED','publication':'NOT_APPROVED'}
    rep.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report',required=True);p.add_argument('--genre',choices=sorted(GENRES),default='ai_work')
    p.add_argument('--expected-source-sha',required=True);p.add_argument('--review-only',action='store_true')
    p.add_argument('--synthetic-ci',action='store_true');a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.report,a.genre,a.expected_source_sha,a.review_only,a.synthetic_ci),ensure_ascii=False))
