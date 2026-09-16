#!/usr/bin/env python3
import json, subprocess, shlex, wave, math, struct
from pathlib import Path

OUT=Path('output'); AS=OUT/'v19_assets'; SC=OUT/'v19_scenes'; TMP=OUT/'v19_clips'
TMP.mkdir(parents=True,exist_ok=True)
plan=json.loads((OUT/'v19_plan.json').read_text())
hero_map={1:'01_robot_hook',2:'02_stressed_worker',3:'03_robot_solution',9:'09_before_after',11:'11_robot_cta',12:'12_device_next',13:'11_robot_cta',14:'14_city_message',16:'11_robot_cta'}

def pick(prefix):
    for ext in ('mp4','mov','webm','png','jpg','jpeg','webp'):
        fs=sorted(AS.glob(prefix+'*.'+ext))
        if fs:return fs[0]
    return None

def run(cmd):
    print('+',' '.join(shlex.quote(str(x)) for x in cmd)); subprocess.check_call([str(x) for x in cmd])

clips=[]
for s in plan['scenes']:
    i=s['id']; dur=float(s['duration']); clip=TMP/f'{i:02d}.mp4'
    src=pick(hero_map[i]) if i in hero_map else None
    if src is None:
        candidates=[SC/f'scene_{i:02d}.mp4',SC/f'scene_{i:02d}.webm',SC/f'scene_{i:02d}.png']
        src=next((p for p in candidates if p.exists()),None)
    if src is None: raise SystemExit(f'missing independent scene source {i}')
    if src.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}:
        vf="scale=1240:2205:force_original_aspect_ratio=increase,crop=1080:1920:x='(iw-ow)/2+18*sin(t*1.7)':y='(ih-oh)/2+12*cos(t*1.3)',zoompan=z='min(zoom+0.0008,1.08)':d=1:s=1080x1920:fps=30,format=yuv420p"
        run(['ffmpeg','-y','-loop','1','-i',src,'-t',str(dur),'-vf',vf,'-an','-c:v','libx264','-preset','medium','-crf','15',clip])
    else:
        vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p"
        run(['ffmpeg','-y','-i',src,'-t',str(dur),'-vf',vf,'-an','-c:v','libx264','-preset','medium','-crf','15',clip])
    clips.append(clip)

lst=TMP/'concat.txt'; lst.write_text('\n'.join("file '"+str(p.resolve()).replace("'","'\\''")+"'" for p in clips))
visual0=OUT/'v19_visual_raw.mp4'
run(['ffmpeg','-y','-f','concat','-safe','0','-i',lst,'-c:v','libx264','-preset','medium','-crf','15','-pix_fmt','yuv420p',visual0])

# TikTok-safe, short dynamic captions. Kept independent from hero art so generated assets never bake Japanese text.
captions=['これ、まだ手でやってるの？','コピペ地獄、終わらせます','ChatGPT × Excel','必要項目だけ指示','AIが一瞬で整理','表でそのまま出力','Excelへ貼り付け','グラフまで完成','手作業 → 一気に時短','要約・メール・分析にも','保存して明日使って','次は資料作成を時短','AI時短ラボ','AIで仕事をもっと自由に','毎日1つ仕事がラクに','また次の動画で']
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
filters=[]; t=0.0
for s,txt in zip(plan['scenes'],captions):
    d=float(s['duration']); start=t; end=t+d; safe=txt.replace("'","’").replace(':','\\:')
    filters.append("drawtext=fontfile=%s:text='%s':fontcolor=white:fontsize=58:borderw=5:bordercolor=black@0.85:box=1:boxcolor=black@0.34:boxborderw=22:x=(w-text_w)/2:y=h-360:enable='between(t,%.3f,%.3f)'"%(font,safe,start,end))
    t=end
visual=OUT/'v19_visual.mp4'
run(['ffmpeg','-y','-i',visual0,'-vf',','.join(filters),'-c:v','libx264','-preset','medium','-crf','15','-an',visual])

# Copyright-free procedural UI sound bed: subtle clicks at scene changes + low ambient tone.
sr=48000; total=max(36.0,t); wav=OUT/'v19_sfx.wav'; boundaries=[]; x=0
for s in plan['scenes'][:-1]: x+=float(s['duration']); boundaries.append(x)
with wave.open(str(wav),'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    for n in range(int(total*sr)):
        sec=n/sr; v=0.012*math.sin(2*math.pi*110*sec)+0.006*math.sin(2*math.pi*220*sec)
        for b in boundaries:
            dt=sec-b
            if 0<=dt<0.055: v += 0.11*math.exp(-55*dt)*math.sin(2*math.pi*1050*dt)
        w.writeframesraw(struct.pack('<h',max(-32767,min(32767,int(v*32767)))))

voice=OUT/'narration.wav'; final=OUT/'AI時短ラボ_01_v19.mp4'
if not voice.exists(): raise SystemExit('missing narration.wav')
run(['ffmpeg','-y','-i',visual,'-i',voice,'-i',wav,'-filter_complex','[1:a]volume=1.0[voice];[2:a]volume=0.45[sfx];[voice][sfx]amix=inputs=2:duration=longest:normalize=0[a]','-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',f'{t:.3f}',final])
print(final)
