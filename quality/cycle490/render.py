"""Cycle490 reproducible 20s synthetic UI proof. REVIEW ONLY, no user assets."""
import argparse, json, math, subprocess, tempfile, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=540,960,30
ENDS=[0,1.5,4,6.5,9.5,12.5,15.5,18,20]
VALUES=[120,150,200,250]
TITLES=['まだ手作業？','毎回の集計が大変','AIに依頼する手順','指示を入力','数式で検算','グラフに変換','Before / After','保存して試そう']
CAPTIONS=['4か月の売上、手で足してない？','コピーと集計に手間がかかる','元データと依頼内容を明確に','合計とグラフを作ってと指示','SUM関数で合計を確かめる','同じ4つの数字からグラフ作成','作業手順を短く整理する例','あとで試せるよう保存']
NARRATION=['四か月の売上、手で足していませんか。','毎回のコピーや集計、時間がかかりますよね。','まず元データと、やりたいことを整理します。','合計を出してグラフにして、と入力します。','四つの数字を足すと、合計は七百二十です。','同じデータからグラフも作れます。','手順を見直すだけでも、作業は変わります。','あとで試せるように、保存しておきましょう。']
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def check():
    assert len(TITLES)==len(CAPTIONS)==len(NARRATION)==8
    assert sum(VALUES)==720 and ENDS[-1]==20
    assert all(ENDS[i]<ENDS[i+1] for i in range(8))
def f(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def label(d,x,y,s,n=26,c='white',b=False):d.text((x,y),s,font=f(n,b),fill=c)
def box(d,xy,c='#1a3952'):d.rounded_rectangle(xy,radius=15,fill=c)
def index(t):return next((i for i in range(8) if ENDS[i]<=t<ENDS[i+1]),7)
def frame(t):
    k=index(t);p=max(0,min(1,(t-ENDS[k])/(ENDS[k+1]-ENDS[k])))
    im=Image.new('RGB',(W,H),'#081827');d=ImageDraw.Draw(im)
    d.ellipse((-130,120,170,480),outline='#19405a',width=3)
    d.ellipse((360,430,720,800),outline='#195064',width=3)
    label(d,35,35,'AI時短ラボ  /  DEMO',22,'#74e5f9',True)
    label(d,34,98,TITLES[k],41,'white',True)
    box(d,(25,190,515,728),'#10263b')
    label(d,48,216,'架空の売上データ・再現映像',20,'#b3dce8')
    if k in (0,5):
        label(d,52,284,'月別売上 / 架空データ',28,'white',True)
        for j,v in enumerate(VALUES):
            x=65+117*j;hh=int((v/250)*275*min(1,p*1.8))
            box(d,(x,620-hh,x+75,620),'#42c3ee' if j<3 else '#55e8b7')
            label(d,x+10,640,str(v),23,'white',True)
        if k==0:label(d,65,683,'合計 720' if p>.82 else '計算中…',31,'#ffdf86',True)
    elif k==1:
        for j,s in enumerate(['① データを開く','② コピーする','③ 手で合計する']):
            y=310+j*112;box(d,(50,y,492,y+84));label(d,73,y+21,s,29,'white',True)
        label(d,85,685,'手順を減らせる？',27,'#ffdf86',True)
    elif k==2:
        for j,s in enumerate(['元データ','やりたいこと','検算できる結果']):
            y=285+j*125;box(d,(64,y,475,y+86));label(d,110,y+20,s,29,'white',True)
            if j<2:label(d,245,y+90,'↓',27,'#ffdf86',True)
    elif k==3:
        box(d,(48,295,492,625),'#e9f6f7');label(d,73,319,'指示入力 / 再現UI',22,'#19485a',True)
        for j,s in enumerate(['この4か月の売上を','合計して検算し、','グラフ用の表にして。']):
            if p>(j+1)/4:label(d,69,386+j*66,s,29,'#1a3850',True)
        box(d,(328,564,464,613),'#197fc4');label(d,356,577,'送信',22,'white',True)
    elif k==4:
        label(d,55,274,'月      売上',27,'#a8e6f6',True)
        for j,v in enumerate(VALUES):
            y=327+j*62;box(d,(56,y,473,y+53));label(d,80,y+9,f'{j+1}月      {v}',28,'white',True)
        label(d,57,605,'= SUM(B2:B5)',28,'#80ebcb',True)
        label(d,58,668,'結果 720' if p>.82 else '検算中…',30,'#ffe08a',True)
    elif k==6:
        box(d,(45,290,257,654),'#493039');box(d,(268,290,494,654),'#19483d')
        label(d,63,313,'BEFORE',25,'#ffbaba',True);label(d,290,313,'AFTER',25,'#aaf9d2',True)
        for j,s in enumerate(['手動集計','手動転記','検算に時間']):label(d,58,407+j*70,s,21)
        for j,s in enumerate(['指示を整理','合計を確認','グラフ作成']):label(d,281,407+j*70,s,21)
        label(d,85,685,'※効果時間は未測定',20,'#ffdf86')
    else:
        label(d,90,320,'今日の手順を',40,'white',True)
        label(d,90,395,'あとで試そう',40,'#ffdf86',True)
        box(d,(100,530,440,629),'#167ac4');label(d,194,553,'保存',38,'white',True)
        label(d,83,685,'実際の操作録画ではありません',19,'#c4dbe5')
    box(d,(24,759,516,842),'#07111f')
    label(d,39,783,CAPTIONS[k],24,'white',True)
    box(d,(31,864,509,870),'#24465c')
    box(d,(31,864,31+int(478*t/20),870),'#52d7f6')
    label(d,34,894,'REVIEW ONLY / 投稿未承認',18,'#b5c9d7')
    return im
def srt_time(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
def srt(path,lines):
    Path(path).write_text(''.join(f'{i+1}\n{srt_time(ENDS[i])} --> {srt_time(ENDS[i+1])}\n{line}\n\n' for i,line in enumerate(lines)),encoding='utf8')
def sound(path):
    sr=44100
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        import struct
        b=bytearray()
        for i in range(20*sr):
            t=i/sr;v=0.
            for j,start in enumerate(ENDS[:-1]):
                dt=t-start
                if 0<=dt<.14:v+=.07*math.sin(2*math.pi*(420+35*j)*dt)*math.exp(-23*dt)
            b+=struct.pack('<h',round(max(-1,min(1,v))*32767))
        w.writeframes(b)
def render(out,voice=None,manifest=None):
    check();out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    if bool(voice)!=bool(manifest):raise ValueError('voice and manifest must be supplied together')
    if voice:
        m=json.loads(Path(manifest).read_text(encoding='utf8'))
        if m.get('script')!=NARRATION or m.get('scene_ends')!=ENDS or not m.get('measured_segments_fit'):
            raise ValueError('voice verification gate failed')
    with tempfile.TemporaryDirectory() as tmp:
        wav=Path(tmp)/'sfx.wav';sound(wav)
        cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(wav)]
        if voice:cmd+=['-i',str(voice)]
        cmd+=['-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p']
        if voice:cmd+=['-filter_complex','[1:a][2:a]amix=inputs=2:duration=first:weights=0.45 1[a]','-map','0:v:0','-map','[a]']
        else:cmd+=['-map','0:v:0','-map','1:a:0']
        cmd+=['-c:a','aac','-t','20','-movflags','+faststart',str(out)]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for i in range(600):p.stdin.write(frame(i/30).tobytes())
            p.stdin.close();err=p.stderr.read();rc=p.wait()
        except Exception:p.kill();p.wait();raise
        if rc:raise RuntimeError(err.decode(errors='replace')[-1000:])
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    srt(out.with_suffix('.srt'),NARRATION if voice else CAPTIONS)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
    v=next(x for x in probe['streams'] if x['codec_type']=='video')
    a=next(x for x in probe['streams'] if x['codec_type']=='audio')
    assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264') and a['codec_name']=='aac'
    result={'full_decode':'PASS','frames':int(v['nb_frames']),'duration':float(probe['format']['duration']),'narration':'KOKORO_NEW_SEGMENT_CHECKED' if voice else 'NOT_GENERATED_SFX_ONLY','captions':'VOICE_SCRIPT_SEGMENT_SYNC' if voice else 'SCENE_DESCRIPTIONS_NOT_TRANSCRIPT','rights':'SYNTHETIC_LOCAL_ONLY','publication':'NOT_APPROVED','quality':'HUMAN_REVIEW'}
    out.with_suffix('.qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--voice');p.add_argument('--manifest');a=p.parse_args()
    print(json.dumps(render(a.output,a.voice,a.manifest),ensure_ascii=False))
