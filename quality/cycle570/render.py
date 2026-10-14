#!/usr/bin/env python3
"""Cycle570: 3s provenance-first prompt animation for a synthetic spreadsheet demo.

Reimplementation, not v33 source. Review-only; does not create speech or post.
The source MP4 must match the explicitly allowlisted cycle569 SHA-256.
"""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
START,END=6.0,9.0
VALUES=(120,150,200,250)
SOURCE_SHA='e09a62c458a7ef4f089cc7ebab7c793075b2dd338ce6066bea01c77e1914ae3c'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GATES=('rights_human_verified','japanese_narration_human_verified','voice_caption_semantic_sync_verified','employee_approved')

def gate(status):
    if status.get('auto_post') is not False: raise ValueError('auto-post must be false')
    if status.get('publication')=='APPROVED' and not all(status.get(k) is True for k in GATES):
        raise ValueError('publication requires all human gates')
    return True

def ease(x):
    x=max(0.0,min(1.0,x));return 1-(1-x)**3

def font(size,bold=False): return ImageFont.truetype(BOLD if bold else REG,size)

def draw_frame(t):
    """Render a distinct three-second explanation, no reference assets or real UI."""
    im=Image.new('RGB',(W,H),'#06172b'); d=ImageDraw.Draw(im)
    # Grid, subtle halo, and brand-independent frame.
    for x in range(0,W,90): d.line((x,0,x,H),fill='#10243c',width=2)
    for y in range(0,H,90): d.line((0,y,W,y),fill='#10243c',width=2)
    d.rounded_rectangle((55,105,1025,215),radius=30,fill='#0a3b4b',outline='#33d8d6',width=3)
    d.text((94,132),'STEP 02  /  入力の再現デモ',font=font(44,True),fill='#f3ffff')
    d.text((72,300),'数字から、答えまでの道筋',font=font(62,True),fill='white')
    d.text((75,395),'※架空データ／実際のサービス画面ではありません',font=font(32),fill='#8bb5c9')
    d.rounded_rectangle((60,505,1020,900),radius=36,fill='#102d44',outline='#267f91',width=3)
    d.text((100,545),'入力するデータ',font=font(46,True),fill='#e4fbff')
    for i,v in enumerate(VALUES):
        x=102+i*224; arrival=ease((t-i*.14)/.46)
        y=int(710+90*(1-arrival)); color='#0e6375' if arrival>.6 else '#174050'
        d.rounded_rectangle((x,y,x+194,y+135),radius=26,fill=color,outline='#3be7d6',width=3)
        d.text((x+22,y+14),f'{i+1}月',font=font(29),fill='#c4e6ec')
        d.text((x+24,y+52),str(v),font=font(55,True),fill='white')
    d.rounded_rectangle((60,985,1020,1470),radius=36,fill='#f5fbff',outline='#44dfdf',width=5)
    d.rounded_rectangle((60,985,1020,1060),radius=35,fill='#0d4a65')
    d.rectangle((60,1035,1020,1060),fill='#0d4a65')
    d.text((100,996),'AIへの指示文（操作の再現）',font=font(37,True),fill='white')
    prompt='4か月の売上を合計し、計算式と結果を表示して'
    shown=int(len(prompt)*ease((t-.55)/1.65))
    # 2-line text with stable semantic content, avoid fake AI completion claim.
    d.text((100,1120),'4か月の売上を合計し、',font=font(45,True),fill='#132d40') if shown>=12 else None
    if shown<12:
        d.text((100,1120),prompt[:shown],font=font(45,True),fill='#132d40')
    else:
        d.text((100,1200),prompt[12:shown],font=font(43,True),fill='#132d40')
    if int(t*3)%2==0 and t<2.3:
        d.rounded_rectangle((103,1325,115,1382),radius=4,fill='#14a9ad')
    ready=ease((t-1.9)/.8)
    d.rounded_rectangle((690,1350,980,1440),radius=24,fill='#168b87' if ready>.5 else '#7cabb2')
    d.text((756,1364),'入力完了' if ready>.5 else '入力中…',font=font(35,True),fill='white')
    d.rounded_rectangle((60,1540,1020,1710),radius=28,fill='#0b3a4c',outline='#33d6cd',width=3)
    d.text((105,1568),'次の画面で B2:B5 を選択',font=font(45,True),fill='#e7ffff')
    d.text((105,1636),'120 + 150 + 200 + 250 = 720',font=font(40,True),fill='#59e6d5')
    d.text((83,1780),'BGMのみ／日本語ナレーション未生成',font=font(30),fill='#9db6c5')
    d.text((83,1840),'HUMAN REVIEW  •  PUBLICATION NOT APPROVED',font=font(23),fill='#8297aa')
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height','-of','json',str(path)],text=True))

def render(source,output):
    source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    actual=hashlib.sha256(source.read_bytes()).hexdigest()
    if actual!=SOURCE_SHA:raise ValueError('baseline SHA not allowlisted: '+actual)
    meta=probe(source); v=next(s for s in meta['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'])!=(W,H) or abs(float(meta['format']['duration'])-20)>.1:raise ValueError('baseline format invalid')
    assert sum(VALUES)==720
    gate({'publication':'NOT_APPROVED','auto_post':False})
    output.parent.mkdir(parents=True,exist_ok=True)
    clip=output.parent/'replacement_6to9.mp4'
    p=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',str(clip)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for k in range(int((END-START)*FPS)):
            p.stdin.write(draw_frame(k/FPS).tobytes())
        p.stdin.close(); error=p.stderr.read().decode(); rc=p.wait()
        if rc:raise RuntimeError('replacement encode failed: '+error[-1500:])
    except Exception:
        if p.poll() is None:p.kill()
        raise
    # Trim source video only; keep original AAC and mov_text subtitle streams.
    filt='[0:v]trim=start=0:end=6,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start=9:end=20,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(clip),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-map','0:s:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30','-c:a','copy','-c:s','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,capture_output=True,text=True)
    data={'cycle':570,'previous_cycle':569,'baseline_sha256':actual,'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'new_scene_seconds':[6,9],'change':'Animated input provenance and explicit synthetic data, 3s reimplementation','narration':'ABSENT_BGM_ONLY','caption':'8 previous soft captions, 8 previous burned-in scene cues; scene text is not speech transcription','publication':'NOT_APPROVED','human_review':True,'auto_post':False,'cost_jpy':0,'source_rights':'synthetic and inherited review-only video; final rights unapproved'}
    (output.parent/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args();print(json.dumps(render(a.source,a.output),ensure_ascii=False,indent=2))
