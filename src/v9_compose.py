#!/usr/bin/env python3
from pathlib import Path
import subprocess,wave
O=Path('output'); frames=O/'v9_operation_frames'; op=O/'v9_operation.mp4'; final=O/'AI時短ラボ_01_v9.mp4'; voice=O/'narration.wav'; robot=Path('assets/robot/presenter.png')
for p in (frames,voice,robot):
 if not p.exists(): raise SystemExit(f'missing {p}')
subprocess.run(['ffmpeg','-y','-framerate','15','-i',str(frames/'%04d.jpg'),'-vf','fps=30','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(op)],check=True)
with wave.open(str(voice),'rb') as w: dur=w.getnframes()/w.getframerate()
# Split the still presenter stream because one filtered stream cannot feed two overlays.
fc=("[0:v]scale=1080:1920,setsar=1[base];"
    "[1:v]scale=1080:1920,setsar=1[op];"
    "[2:v]scale=650:-2,format=rgba,split=2[bot1][bot2];"
    "[base][bot1]overlay=x='215+18*sin(t*2.4)':y='430+12*cos(t*3)':enable='lt(t,5.5)'[a];"
    "[a][op]overlay=0:0:enable='between(t,5.5,21.5)'[b];"
    "[b][bot2]overlay=x='215+12*sin(t*2)':y='470+10*cos(t*2.8)':enable='gte(t,21.5)'[v]")
subprocess.run(['ffmpeg','-y','-f','lavfi','-i',f"color=c=0x07111f:s=1080x1920:r=30:d={dur:.3f}",'-i',str(op),'-loop','1','-i',str(robot),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','3:a','-t',f'{dur:.3f}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(final)],check=True)
print(final)
