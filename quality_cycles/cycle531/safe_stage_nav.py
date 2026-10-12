#!/usr/bin/env python3
"""Cycle531 review-only: non-occluding, reusable stage navigation.

Reimplements the cycle530 ribbon in a measured footer-safe region using the
cycle529 pre-ribbon master, because burned-in text cannot be removed cleanly.
No private/uncleared sources, auto-publication, or Japanese speech claims.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = (
    'AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
    '営業・ビジネス','転職・キャリア','健康・生活改善',
    '雑学・科学','旅行・グルメ','商品比較・暮らし',
)
STAGES = ((2.5,5.0,'課題'),(5.0,10.0,'操作'),(10.0,15.0,'結果'),(15.0,17.5,'確認'))
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
# Prior ribbon used y=147..190, overlapping the spreadsheet header at t=12.
# Footer overlay occupies y=1604..1664, between story text and review watermark.
NAV_RECT=(70,1604,940,60)
UI_RECT=(0,90,1080,1510)
REVIEW_RECT=(60,1685,900,50)


def run(args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:
        raise RuntimeError('command failed: '+repr(args)+'\n'+p.stderr[-2500:])
    return p.stdout


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def intersects(a,b):
    x,y,w,h=a;u,v,p,q=b
    return x<u+p and x+w>u and y<v+q and y+h>v


def validate_stages(stages=STAGES):
    if len(stages)!=4:raise ValueError('exactly four stages required')
    previous=2.5
    for start,end,label in stages:
        if abs(start-previous)>1e-6 or end<=start or end>17.5 or not label or any(c in label for c in "':\\,;[]"):
            raise ValueError('invalid stage timeline')
        previous=end
    if previous!=17.5:raise ValueError('timeline must end at 17.5')


def validate_geometry(rect=NAV_RECT):
    x,y,w,h=rect
    if not (x>=60 and x+w<=1020 and y>=1550 and y+h<=1680):
        raise ValueError('navigation outside allowed footer')
    if intersects(rect,UI_RECT) or intersects(rect,REVIEW_RECT):
        raise ValueError('navigation obscures critical content or watermark')


def validate_manifest(m,source):
    if m.get('genre') not in GENRES:raise ValueError('genre not allowed')
    if m.get('rights')!='SYNTHETIC_OR_OWNER_APPROVED':raise ValueError('unapproved asset')
    if m.get('contains_private_data') is not False:raise ValueError('privacy gate')
    if m.get('review_status')!='HUMAN_REVIEW' or m.get('publication')!='NOT_APPROVED':
        raise ValueError('not review-only')
    if m.get('japanese_narration')!='NOT_GENERATED':raise ValueError('cannot claim narration')
    if m.get('source_sha256')!=sha(source):raise ValueError('source hash mismatch')
    if not Path(FONT).is_file():raise ValueError('Japanese font missing')
    validate_geometry();validate_stages()


def filtergraph(stages=STAGES):
    validate_stages(stages);validate_geometry()
    parts=[]
    for i,(start,end,label) in enumerate(stages):
        x=85+i*233
        active=f'between(t\\,{start}\\,{end})'
        during='between(t\\,2.5\\,17.5)'
        parts.append(f'drawtext=fontfile={FONT}:text={label}:fontcolor=0x8aa5b2:fontsize=28:x={x+66}:y=1605:enable={during}')
        parts.append(f'drawbox=x={x}:y=1647:w=206:h=8:color=0x274356:t=fill:enable={during}')
        parts.append(f'drawtext=fontfile={FONT}:text={label}:fontcolor=white:fontsize=28:x={x+66}:y=1605:enable={active}')
        parts.append(f'drawbox=x={x}:y=1647:w=206:h=8:color=0x37e0d6:t=fill:enable={active}')
    return ','.join(parts)+',format=yuv420p'


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def audio_md5(path):
    return run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).strip()


def render(source,out,manifest,qa_path):
    source,out,qa_path=map(Path,(source,out,qa_path))
    validate_manifest(manifest,source)
    inp=probe(source)
    v=next(x for x in inp['streams'] if x['codec_type']=='video')
    a=next(x for x in inp['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],a['codec_name'])!=('h264',1080,1920,'aac'):
        raise ValueError('source must be 1080x1920 H264/AAC')
    if abs(float(inp['format']['duration'])-20)>0.05:raise ValueError('source not 20 seconds')
    out.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-vf',filtergraph(),'-map','0:v:0','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-t','20','-movflags','+faststart',str(out)])
    pr=probe(out)
    v2=next(x for x in pr['streams'] if x['codec_type']=='video')
    a2=next(x for x in pr['streams'] if x['codec_type']=='audio')
    checks={
        'h264_aac':(v2['codec_name'],a2['codec_name'])==('h264','aac'),
        '1080x1920':(v2['width'],v2['height'])==(1080,1920),
        '20s':abs(float(pr['format']['duration'])-20)<0.05,
        '600_frames':int(v2.get('nb_frames',0))==600,
        '30fps':v2['avg_frame_rate']=='30/1',
        'audio_bitstream_unchanged':audio_md5(source)==audio_md5(out),
        'safe_geometry':not intersects(NAV_RECT,UI_RECT) and not intersects(NAV_RECT,REVIEW_RECT),
        'review_only':manifest['publication']=='NOT_APPROVED',
    }
    qa={
      'cycle':531,'source':source.name,'output':out.name,
      'change':'replace top-overlapping chapter ribbon with footer-safe stage navigation',
      'source_master':'cycle529 pre-ribbon master; cycle530 ribbon is baked into video',
      'stages':[{'start':s,'end':e,'label':l} for s,e,l in STAGES],
      'footer_rectangle':NAV_RECT,
      'japanese_narration':'NOT_GENERATED',
      'spoken_caption_sync':'NOT_VERIFIED',
      'visual_japanese_captions':'PRESERVED_FROM_SOURCE',
      'reference_storyboard':'ORIGINAL_IMAGE_INSPECTED',
      'reference_v33':'RAW_MP4_UNAVAILABLE',
      'research':'SUMMARY_AND_GENRE_PLAN_REVIEWED',
      'checks':checks,'sha256':sha(out),
      'review_status':'HUMAN_REVIEW','publication':'NOT_APPROVED',
    }
    qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not all(checks.values()):raise RuntimeError('QA failed: '+json.dumps(checks))
    return qa


def main():
    p=argparse.ArgumentParser()
    for arg in ['source','output','manifest','qa']:p.add_argument('--'+arg,required=True)
    args=p.parse_args()
    manifest=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    print(json.dumps(render(args.source,args.output,manifest,args.qa),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
