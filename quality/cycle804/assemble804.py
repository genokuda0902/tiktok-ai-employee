#!/usr/bin/env python3
"""Review-only 1080x1920 business slideshow from free Open JTalk narration.
Input: cycle803/assets/scene_01..08.png and cycle803/out/{voice_timing.json,cycle803_business_japanese.m4a}.
No paid services, merge, auto-publishing or personal data.
"""
import json, subprocess, sys
from pathlib import Path

GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business','career','health_life','science','travel_food','product_life')
CAPTIONS=[
 '仕事ができる人は、質問が違う。',
 'まず、目指すゴールを確認する。',
 '次に、今の数字を確かめる。',
 'そして、理想との差を一つに絞る。',
 '原因には、なぜを三回重ねる。',
 '対策は、今日できる行動に変える。',
 '結果を見て、また修正する。',
 '小さな改善が、強いチームをつくる。',
]
def run(*args): subprocess.run(list(args),check=True)
def build(root):
    root=Path(root);assets=root/'assets';out=root/'out';out.mkdir(parents=True,exist_ok=True)
    timing=json.loads((out/'voice_timing.json').read_text(encoding='utf-8'))
    audio=out/'cycle803_business_japanese.m4a';segments=timing['sentences']
    assert timing['genre']=='sales_business' and len(GENRES)==10
    assert len(segments)==len(CAPTIONS)==8 and audio.stat().st_size>10000
    clips=[];cues=[];current=0
    for i,s in enumerate(segments):
        assert s['text']==CAPTIONS[i],f'scene {i+1} narration mismatch'
        img=assets/f'scene_{i+1:02d}.png';assert img.is_file()
        frames=max(1,round(float(s['seconds'])*30));clip=out/f'clip_{i+1:02d}.mp4'
        vf="scale=1112:1978:flags=lanczos,crop=1080:1920:x='16+5*sin(n/42)':y='29+6*cos(n/54)',format=yuv420p"
        run('ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','30','-i',str(img),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(clip))
        cues.append({'scene':i+1,'start_frame':current,'end_frame':current+frames,'text':CAPTIONS[i]})
        current+=frames;clips.append(clip)
    manifest=out/'clips.txt';manifest.write_text(''.join(f"file '{p.resolve()}'\n" for p in clips))
    silent=out/'silent_business.mp4'
    run('ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(silent))
    final=out/'cycle804_BUSINESS_FRESH_JAPANESE_HUMAN_REVIEW.mp4'
    run('ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-shortest',str(final))
    run('ffmpeg','-v','error','-xerror','-i',str(final),'-f','null','-')
    (out/'captions_timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
    return final
if __name__=='__main__':
    print(build(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'cycle803'))
