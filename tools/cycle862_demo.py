"""Cycle862: 10-genre reusable, fictional animated workflow demo. Offline PIL+FFmpeg only.
Full local renderer, tests, and verified MP4 are included in cycle862_review_package.zip.
"""
import math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
OVERLAY_FPS=10
BOUNDARIES=(0,99,177,255,342,429,519,597,691)
GENRE_ACCENTS={'ai_productivity':'#32D6C6','career':'#F2B75E','money':'#66D7B0','health':'#8BC4FF','learning':'#C4A7FF','beauty':'#F79DC2','travel':'#7ED5F0','food':'#FFAE7E','home':'#B5DB8B','business':'#73A8FF'}
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
STEPS=[
 ('全体の流れ','作業を選ぶ  →  見本  →  指示  →  確認','デモの流れを確認'),
 ('繰り返す作業を選択','毎朝の進捗共有メール','対象は架空の定型業務'),
 ('完成形を先に決める','件名：今週の進捗共有','結論 → 数字 → 次の行動'),
 ('AIへの指示を入力','社内向けの進捗メールを150字以内で。','結論を先に、丁寧な文体で。'),
 ('出力例を確認','今週の進捗を共有します。','未達項目は明日再確認します。'),
 ('1点だけ修正','結論を最初の1行に移動して。','変更前 → 変更後を比較'),
 ('再利用用テンプレート','相手：[対象]  目的：[内容]','条件：[長さ・文体]'),
 ('今日から実践','①選ぶ  ②確認する  ③保存する','小さな改善を積み重ねる'),
]
def frame_to_scene(t):
    frame=min(690,max(0,int(t*FPS)))
    return next(i for i in range(8) if BOUNDARIES[i]<=frame<BOUNDARIES[i+1])
def typed_length(text,progress):
    return max(0,min(len(text),int((progress-0.12)*1.5*len(text))))
def font(size,bold=False):
    return ImageFont.truetype(BOLD if bold else REG,size)
def draw_frame(t,genre='ai_productivity'):
    if genre not in GENRE_ACCENTS: raise ValueError('Unknown genre')
    i=frame_to_scene(t)
    start=BOUNDARIES[i]/FPS;end=BOUNDARIES[i+1]/FPS
    progress=min(1,max(0,(t-start)/(end-start)))
    accent=GENRE_ACCENTS[genre]
    im=Image.new('RGBA',(900,420),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((2,2,897,417),radius=27,fill=(10,27,42,249),outline=(92,137,153,255),width=3)
    d.rounded_rectangle((2,2,897,76),radius=27,fill=(25,49,67,255))
    d.rectangle((2,51,897,76),fill=(25,49,67,255))
    for x,c in ((36,'#FF766C'),(63,'#FFD15B'),(90,'#55D49A')):d.ellipse((x,28,x+15,43),fill=c)
    d.text((127,19),'WORKFLOW DEMO  /  架空の画面',font=font(28,True),fill=(235,245,248))
    d.rounded_rectangle((731,22,853,60),radius=14,fill=(34,78,83))
    d.text((752,24),f'{i+1:02d} / 08',font=font(22,True),fill=accent)
    title,body,foot=STEPS[i]
    d.text((36,91),title,font=font(37,True),fill=(243,248,251))
    d.rounded_rectangle((35,163,864,310),radius=22,fill=(241,247,250,255))
    d.rounded_rectangle((55,180,149,219),radius=12,fill=accent)
    d.text((72,181),'入力' if i in (1,3,5,6) else '表示',font=font(24,True),fill=(12,36,46))
    displayed=body[:max(1,typed_length(body,progress))]
    f=font(33,True)
    while d.textbbox((0,0),body,font=f)[2]>755 and f.size>22:f=font(f.size-1,True)
    d.text((58,232),displayed,font=f,fill=(18,44,62))
    if progress<0.92 and int(t*4)%2==0:
        cx=58+d.textbbox((0,0),displayed,font=f)[2]
        d.rounded_rectangle((min(835,cx+4),236,min(842,cx+10),277),radius=2,fill=accent)
    d.rounded_rectangle((35,331,864,383),radius=13,fill=(24,57,75,255))
    d.text((54,338),foot,font=font(26,True),fill=(219,245,241))
    d.rounded_rectangle((36,396,863,403),radius=3,fill=(65,92,105))
    if progress>0.01:d.rounded_rectangle((36,396,36+max(5,int(827*progress)),403),radius=3,fill=accent)
    return im
def render_overlay_frames(output,genre='ai_productivity'):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    count=math.ceil(691/FPS*OVERLAY_FPS)
    for j in range(count):draw_frame(j/OVERLAY_FPS,genre).save(output/f'overlay_{j:04d}.png',optimize=True)
    return count
def make_video(previous,overlay_dir,audio_output):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(previous),'-framerate',str(OVERLAY_FPS),'-i',str(Path(overlay_dir)/'overlay_%04d.png'),'-filter_complex','[0:v][1:v]overlay=90:800:shortest=1:format=auto,format=yuv420p[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-r','30','-frames:v','691','-c:a','copy','-movflags','+faststart',str(audio_output)],check=True)
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--previous',required=True);p.add_argument('--output',required=True);p.add_argument('--frames-dir',required=True);p.add_argument('--genre',default='ai_productivity')
    a=p.parse_args();render_overlay_frames(a.frames_dir,a.genre);make_video(a.previous,a.frames_dir,a.output)
