#!/usr/bin/env python3
"""Cycle630: original kinetic Japanese hook overlay on existing REVIEW_ONLY MP4.
Not a v33 reproduction. Uses an inherited, unapproved baseline only for private review.
The template is configurable for ten genres; only ai_work was rendered here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, HOOK_FRAMES = 540, 960, 30, 66
GENRE_HOOKS = {
    'ai_work': ('その集計、', 'まだ手作業？', '4件の数値を検算', '120 + 150 + 200 + 250', '720'),
    'beauty': ('その変化、', '根拠はある？', '写真と条件を比較', '加工・照明の違いを確認', '比較'),
    'relationships': ('その言葉、', '伝わってる？', '状況を整理して考える', '相手の気持ちは決めつけない', '確認'),
    'money': ('その数字、', '計算した？', '条件と金額を確認', '費用と期間を見直そう', '検算'),
    'sales_business': ('その提案、', '伝わってる？', '相手の課題を明確に', '数字は出典とセットで', '根拠'),
    'career': ('その選択、', '比較した？', '条件を並べて判断', '働き方は人によって違う', '比較'),
    'health_lifestyle': ('その習慣、', '続けられる？', '自分の条件を確認', '個別の健康判断ではありません', '確認'),
    'science_trivia': ('その話、', '確かめた？', '実験条件を確認', '出典と限界を示そう', '検証'),
    'travel_food': ('その旅先、', '比較した？', '移動と予算を確認', '価格・営業日は要確認', '比較'),
    'product_lifestyle': ('その買い物、', '比べてみた？', '用途と条件を整理', '価格は購入前に確認', '比較'),
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
RIGHTS='INHERITED_BASELINE_UNVERIFIED'
PUBLICATION='NOT_APPROVED'

def validate(genre='ai_work', rights=RIGHTS, publication=PUBLICATION):
    if genre not in GENRE_HOOKS:
        raise ValueError('unknown genre')
    if rights != RIGHTS or publication != PUBLICATION:
        raise ValueError('fail-closed: review-only unverified rights')
    fields=GENRE_HOOKS[genre]
    if len(fields)!=5 or any(not isinstance(s,str) or not s for s in fields):
        raise ValueError('incomplete hook')
    if any(len(s)>19 for s in fields[:3]) or len(fields[3])>26 or len(fields[4])>8:
        raise ValueError('hook would overflow safe area')
    return fields

def stage(frame):
    if type(frame) is not int or not 0<=frame<HOOK_FRAMES:
        raise ValueError('frame outside hook')
    return 'question' if frame < 17 else ('proof' if frame < 38 else 'result')

def font(size,bold=True):
    return ImageFont.truetype(BOLD if bold else FONT,size)

def rounded(draw, xy, fill, radius=17, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def composite_hook(base:Image.Image, frame:int, genre='ai_work'):
    first, second, explanation, equation, answer=validate(genre)
    if base.size != (W,H):
        raise ValueError('baseline size mismatch')
    st=stage(frame)
    t=frame/FPS
    zoom=1.0 + 0.035 * min(1,t/1.1)
    crop_w=int(W/zoom); crop_h=int(H/zoom)
    base=base.crop(((W-crop_w)//2,(H-crop_h)//2,(W+crop_w)//2,(H+crop_h)//2))
    base=base.resize((W,H),Image.Resampling.BICUBIC)
    overlay=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    rounded(d,(22,123,500,313),(3,16,32,255),24,(48,208,240,220),3)
    rounded(d,(34,137,189,170),(29,117,152,255),9)
    d.text((47,141),'4件の売上 / 架空例',font=font(19),fill=(246,254,255))
    d.text((44,185),first,font=font(43),fill=(248,252,255))
    d.text((44,241),second,font=font(44),fill=(255,218,91))
    wave=0.5+0.5*math.sin(t*8)
    d.ellipse((445,180,460,195),fill=(36,204,232,int(140+100*wave)))
    rounded(d,(22,628,500,925),(4,17,31,255),22)
    if st=='question':
        d.text((48,674),'4件の数字を、',font=font(30),fill=(234,247,252))
        d.text((48,727),'根拠つきで見せる。',font=font(28),fill=(73,223,229))
    if st in ('proof','result'):
        slide=max(0,int((1-min(1,(frame-17)/9))*85))
        rounded(d,(30,660+slide,496,742+slide),(5,32,55,239),17,(53,221,233,235),3)
        d.text((47,671+slide),explanation,font=font(25),fill=(219,249,252))
        d.text((46,709+slide),equation,font=font(24),fill=(247,250,254))
    if st=='result':
        alpha=min(255,int(255*(frame-38)/9))
        rounded(d,(31,748,494,842),(8,48,65,min(245,alpha+30)),20,(255,218,93,alpha),3)
        d.text((46,759),'検算結果',font=font(22),fill=(207,247,249,alpha))
        d.text((284,749),answer,font=font(59),fill=(255,221,108,alpha))
    d.text((31,858),'架空データ・操作再現｜公開未承認',font=font(17),fill=(217,235,242,220))
    return Image.alpha_composite(base.convert('RGBA'),overlay).convert('RGB')

def render(baseline:Path, output:Path, genre='ai_work'):
    validate(genre)
    output.parent.mkdir(parents=True,exist_ok=True)
    seg=output.parent/'hook630.segment.mp4'
    decode=['ffmpeg','-hide_banner','-loglevel','error','-i',str(baseline),'-map','0:v:0',
            '-frames:v',str(HOOK_FRAMES),'-vf',f'scale={W}:{H}:flags=lanczos',
            '-f','rawvideo','-pix_fmt','rgb24','-']
    enc=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264',
         '-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(seg)]
    p_in=subprocess.Popen(decode,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p_out=subprocess.Popen(enc,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(HOOK_FRAMES):
            raw=p_in.stdout.read(W*H*3)
            if len(raw)!=W*H*3:raise RuntimeError(f'baseline decode stopped at frame {i}')
            frame=Image.frombytes('RGB',(W,H),raw)
            p_out.stdin.write(composite_hook(frame,i,genre).tobytes())
        p_out.stdin.close()
        enc_err=p_out.stderr.read().decode()
        dec_err=p_in.stderr.read().decode()
        if p_out.wait() or p_in.wait():raise RuntimeError('ffmpeg error '+enc_err+' '+dec_err)
    except Exception:
        p_in.kill();p_out.kill();raise
    filt=(f'[0:v]trim=start_frame={HOOK_FRAMES},setpts=PTS-STARTPTS[v0];'
          f'[1:v]scale=1080:1920,setsar=1,setpts=PTS-STARTPTS[v1];'
          '[v1][v0]concat=n=2:v=1:a=0[v]')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(baseline),'-i',str(seg),
       '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
       '-crf','20','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(output)],check=True)
    seg.unlink(missing_ok=True)
    manifest={'cycle':630,'genre':genre,'rights':RIGHTS,'publication':PUBLICATION,
              'new_japanese_narration':False,'speech_caption_sync':'UNVERIFIED',
              'reference_v33_directly_compared':False,'hook_frames':HOOK_FRAMES,
              'new_hook':'question from frame 0, proof at frame 17, result at frame 38',
              'synthetic_demo':True,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    output.with_suffix('.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--baseline',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai_work');a=p.parse_args()
    print(json.dumps(render(Path(a.baseline),Path(a.output),a.genre),ensure_ascii=False))
