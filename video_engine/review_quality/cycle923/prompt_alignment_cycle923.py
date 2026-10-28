"""Cycle923: original, fictional prompt-example overlay aligned to the scene-04 caption.

Source: a local private review-only MP4. Does not transcribe speech, post,
copy private media to GitHub, or claim a real ChatGPT interaction.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
FRAME_COUNT = 691
START, END = 261, 348  # scene04, 8.700s--11.600s
SCENE_BOUNDS = (0, 87, 174, 261, 348, 435, 522, 588, 691)
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRES = ('ai_work','finance','business','health','education','tech',
          'lifestyle','history','travel','productivity')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# Genre-specific data is original, generic, and fictional. No private or live metrics.
EXAMPLES = {
 'ai_work': ('3か月の売上を整理', '未入力は推測で埋めない', '表と要点を3つ'),
 'finance': ('架空の支出を分類', '欠損値は未入力のまま', '費目別の表を作る'),
 'business': ('架空の施策を比較', '根拠がない数値は使わない', '比較表と注意点'),
 'health': ('一般的な習慣を整理', '診断や治療の断定はしない', '確認項目を箇条書き'),
 'education': ('学習計画を整理', '理解度を決めつけない', '3ステップで説明'),
 'tech': ('機能の違いを比較', '未確認の仕様は明記', '表と検証手順'),
 'lifestyle': ('一日の予定を整理', '未確定の予定は仮置き', '時間順の一覧'),
 'history': ('出来事を時系列化', '出典不明は未確認とする', '年表と出典欄'),
 'travel': ('架空の行程を整理', '移動時間は推測しない', '時系列の行程表'),
 'productivity': ('作業を3つに分解', '実測していない効果は断定しない', '実行チェック表'),
}
LABELS = ('目的', '条件', '出力')


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()


def validate(genre: str, output: str, frame_count: int=FRAME_COUNT) -> None:
    if genre not in GENRES: raise ValueError('unsupported genre')
    if not output.endswith('_REVIEW_ONLY.mp4'): raise ValueError('review-only filename required')
    if frame_count != FRAME_COUNT: raise ValueError('unexpected frame count')
    if not (0 < START < END <= frame_count): raise ValueError('invalid scene bounds')


def beat(frame_index: int) -> int:
    """Three sequential editorial beats inside the existing 2.9-second scene."""
    if not START <= frame_index < END: raise ValueError('not scene04')
    return min(2, (frame_index-START)//29)


def prompt_text(genre: str) -> tuple[str, str, str]:
    if genre not in EXAMPLES: raise ValueError('unknown genre')
    return EXAMPLES[genre]


def draw_overlay(frame, frame_index: int, genre: str):
    """Only modifies y=145..1370; leaves inherited subtitle pixels y>=1490 intact."""
    import cv2
    import numpy as np
    if not START <= frame_index < END: return frame
    h,w=frame.shape[:2]
    if (w,h)!=(1080,1920): raise ValueError('unexpected geometry')
    # Original in-memory scene has no approved real-person footage. Overlay is original UI.
    # Color gradient is contained within the active top scene, not the caption band.
    canvas=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    draw=ImageDraw.Draw(canvas,'RGBA')
    draw.rounded_rectangle((58,145,1022,1382),radius=40,fill=(4,17,35,252),outline=(47,210,223,255),width=5)
    draw.rounded_rectangle((90,178,990,304),radius=22,fill=(14,55,80,255))
    draw.text((123,190),'AIへの指示を具体化',font=ImageFont.truetype(BOLD,57),fill=(248,253,255,255))
    draw.text((126,265),'入力例（架空）・実際の操作画面ではありません',font=ImageFont.truetype(FONT,23),fill=(159,216,226,255))
    examples=prompt_text(genre)
    current=beat(frame_index)
    for i,(label,example) in enumerate(zip(LABELS,examples)):
        y=360+i*292
        active=i<=current
        draw.rounded_rectangle((95,y,985,y+244),radius=28,fill=(12,60,82,255) if active else (18,35,52,255),outline=(59,229,211,255) if active else (58,76,92,255),width=5 if i==current else 2)
        draw.rounded_rectangle((125,y+26,283,y+95),radius=16,fill=(36,180,169,255) if active else (43,67,82,255))
        draw.text((150,y+30),f'{i+1}  {label}',font=ImageFont.truetype(BOLD,36),fill=(255,255,255,255))
        if active:
            draw.text((127,y+125),example,font=ImageFont.truetype(BOLD,49),fill=(255,255,255,255))
        else:
            draw.text((127,y+128),'次のポイント',font=ImageFont.truetype(FONT,43),fill=(120,143,157,255))
    # High-contrast takeaway reinforces, rather than replaces, the existing burned subtitle.
    draw.rounded_rectangle((112,1264,965,1352),radius=20,fill=(9,110,130,255))
    draw.text((145,1273),'目的 → 条件 → 出力 を明確に',font=ImageFont.truetype(BOLD,40),fill=(255,255,255,255))
    return cv2.cvtColor(np.asarray(canvas.convert('RGB')),cv2.COLOR_RGB2BGR)


def render(source: Path, output: Path, report_path: Path, genre: str='ai_work'):
    import cv2
    validate(genre,output.name)
    if not source.is_file(): raise FileNotFoundError(source)
    cap=cv2.VideoCapture(str(source))
    w,h,n,fps=[cap.get(x) for x in (cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FRAME_HEIGHT,cv2.CAP_PROP_FRAME_COUNT,cv2.CAP_PROP_FPS)]
    if (int(w),int(h),int(n),round(fps))!=(1080,1920,FRAME_COUNT,FPS):
        cap.release();raise ValueError(f'unexpected source geometry {(w,h,n,fps)}')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
         '-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(FRAME_COUNT):
            ok,frame=cap.read()
            if not ok: raise RuntimeError(f'early decode at frame {i}')
            if START<=i<END: frame=draw_overlay(frame,i,genre)
            p.stdin.write(frame.tobytes())
    finally:
        cap.release()
        if p.stdin: p.stdin.close()
    if p.wait()!=0: raise RuntimeError('ffmpeg encode failed')
    report={
      'cycle':923,'genre':genre,'status':STATUS,
      'source_sha256':sha256(source),'output_sha256':sha256(output),
      'changed_scene':4,'changed_frame_range':[START,END-1],
      'change':'Replace mismatched chart in scene04 with a 3-beat fictional purpose/condition/output prompt UI',
      'caption_region':'original video retained y>=1490; lossy reencode may change pixels',
      'spoken_japanese_semantic_alignment':'NOT_VERIFIED_NO_INDEPENDENT_ASR',
      'reference_v33_mp4':'NOT_AVAILABLE', 'employee_approved':False,'auto_post':False,
    }
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    ap.add_argument('--genre',choices=GENRES,default='ai_work')
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.output,a.report,a.genre),ensure_ascii=False))
if __name__=='__main__': main()
