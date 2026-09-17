#!/usr/bin/env python3
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
STORY=ROOT/'assets/v20/storyboard.jpg'
OUT=ROOT/'output/v20_motion'; OUT.mkdir(parents=True,exist_ok=True)
SCENES=OUT/'scenes'; SCENES.mkdir(exist_ok=True)
if not STORY.exists(): raise SystemExit('Missing assets/v20/storyboard.jpg')
# Ubuntu runner ships ImageMagick 6, where the CLI is `convert`.
W,H=600,1066
for i,(r,c) in enumerate([(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)],1):
    x=c*(W//2); y=r*(H//3); w=W//2; h=H//3
    subprocess.run(['convert',str(STORY),'-crop',f'{w}x{h}+{x}+{y}','+repage','-resize','1080x1920^','-gravity','center','-extent','1080x1920',str(SCENES/f's{i}.jpg')],check=True)
durs=[4,4,5,5,6,8]; clips=[]
for i,d in enumerate(durs,1):
    frames=d*30; src=SCENES/f's{i}.jpg'; dst=OUT/f'clip_{i}.mp4'
    if i%2:
        move=f"zoompan=z='min(zoom+0.0015,1.14)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    else:
        move=f"zoompan=z=1.12:x='min((iw-iw/zoom)*on/{frames},iw-iw/zoom)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    vf='scale=1200:2134:force_original_aspect_ratio=increase,crop=1200:2134,'+move+',format=yuv420p'
    subprocess.run(['ffmpeg','-y','-loop','1','-i',str(src),'-vf',vf,'-t',str(d),'-r','30','-an','-c:v','libx264','-crf','18',str(dst)],check=True); clips.append(dst)
lst=OUT/'concat.txt'; lst.write_text(''.join(f"file '{p.name}'\n" for p in clips))
visual=OUT/'visual.mp4'; subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','visual.mp4'],cwd=OUT,check=True)
srt=OUT/'captions.srt'; srt.write_text('''1\n00:00:00,000 --> 00:00:04,000\nそのExcelコピペ、まだ手作業？\n\n2\n00:00:04,000 --> 00:00:08,000\nバラバラな顧客情報も\n\n3\n00:00:08,000 --> 00:00:13,000\nChatGPTにそのまま貼って\n\n4\n00:00:13,000 --> 00:00:18,000\n氏名・電話・メール・日時を表にして\n\n5\n00:00:18,000 --> 00:00:24,000\n整理された表をExcelへ\n\n6\n00:00:24,000 --> 00:00:32,000\n明日使うなら、保存して試してみて。\n''',encoding='utf-8')
voice=ROOT/'output/narration.wav'
if not voice.exists(): raise SystemExit('Missing output/narration.wav')
final=OUT/'AI時短ラボ_01_v20_final.mp4'
style='FontName=Noto Sans CJK JP,FontSize=18,Alignment=2,MarginV=180,Outline=3,Shadow=1'
subprocess.run(['ffmpeg','-y','-i',str(visual),'-i',str(voice),'-vf',f"subtitles={srt}:force_style='{style}'",'-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-shortest',str(final)],check=True)
probe=subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=width,height,codec_name','-show_entries','format=duration,size','-of','json',str(final)],text=True)
(OUT/'report.json').write_text(probe,encoding='utf-8')
print(final)
