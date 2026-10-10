#!/usr/bin/env python3
"""Cycle482 zero-cost Japanese-voice video proof. NOT APPROVED for posting."""
import json, math, wave, subprocess, shutil, hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).resolve().parent
O=P/'output';O.mkdir(exist_ok=True)
W,H=1080,1920
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
DATA=[
('AIに貼る前に','3秒だけ確認。','便利さと安全性、両方守る。','エーアイに貼る前に、三秒だけ確認。便利さと安全性、両方守ろう。'),
('個人情報は','入ってない？','氏名・電話番号・顧客情報を確認。','一つ目。個人情報は入っていない？氏名や電話番号、顧客情報を確認。'),
('数字の根拠は','確かめた？','AIの計算結果は必ず検算。','二つ目。数字の根拠は確かめた？エーアイの計算結果は必ず検算。'),
('指示は','具体的？','目的・条件・出力形式を伝える。','三つ目。指示は具体的？目的、条件、出力形式を伝えよう。'),
('速さだけでなく','確認まで。','入力前・出力後の二段階チェック。','速さだけじゃない。入力前と出力後、二段階のチェックが大切。'),
('今日から使える','AIの3原則','情報・根拠・指示を見直そう。','情報、根拠、指示。この三つを意識して、今日から使ってみよう。')]
def draw_slide(i,phase):
 im=Image.new('RGB',(W,H),(12,28,49));d=ImageDraw.Draw(im)
 for y in range(H):
  c=int(23*max(0,1-abs(y-390)/1150))
  d.line((0,y,W,y),fill=(12+c//2,28+c,49+c))
 for x in range(64,1080,103):d.line((x,0,x,1650),fill=(31,58,75),width=1)
 d.rounded_rectangle((62,83,410,148),radius=28,fill=(26,92,100))
 def t(x,y,s,size,color='#f8fcff',bold=False):
  d.text((x,y),s,font=ImageFont.truetype(B if bold else F,size,index=0),fill=color)
 t(90,98,'AI  ×  WORK SMART',27,'#b7ffeb',True)
 a,b,sub,_=DATA[i]
 t(63,290,a,84,bold=True);t(63,407,b,84,bold=True);t(65,565,sub,36,color='#c5e3ee')
 d.rounded_rectangle((62,692,1018,1410),radius=45,fill=(25,47,69),outline=(91,146,165),width=3)
 t(111,744,'QUALITY GATE  /  3 CHECKS',32,'#aefce8',True)
 labels=['01   個人情報','02   数字の根拠','03   指示の明確さ']
 details=['氏名・連絡先を外す','合計・件数を検算','目的・条件・形式を明示']
 for n in range(3):
  y=840+n*150
  active=(i-1==n or (i>=4 and n==(i-4)%3) or (i==0 and n==0))
  d.rounded_rectangle((101,y,976,y+129),radius=22,fill=(37,104,105) if active else (35,60,81),outline=(96,244,210) if active and phase else (65,100,118),width=5 if active and phase else 2)
  t(132,y+15,labels[n],41,bold=True)
  t(133,y+78,details[n],30,'#c1d9e1')
 d.rounded_rectangle((81,1498,999,1625),radius=27,fill=(26,93,103))
 t(111,1531,'CHECK  →  VERIFY  →  USE',38,'#d7fff2',True)
 if phase:
  d.rounded_rectangle((82,1643,1000,1710),radius=22,fill=(60,131,129))
  t(168,1651,'POINT ✓  安全 × 正確 × 明確',36,bold=True)
 d.rounded_rectangle((58,1743,1022,1837),radius=25,fill=(5,13,26))
 t(104,1761,[a+' '+b for a,b,*_ in DATA][i],38,bold=True)
 d.rounded_rectangle((70,1860,1010,1876),radius=7,fill=(51,79,99))
 d.rounded_rectangle((70,1860,70+int(940*(i+(phase+1)/2)/6),1876),radius=7,fill=(99,239,204))
 path=O/f'frame_{i:02d}_{phase}.png';im.save(path);return path
def voice(i):
 import glob
 dictionary='/var/lib/mecab/dic/open-jtalk/naist-jdic'
 models=glob.glob('/usr/share/hts-voice/**/*.htsvoice',recursive=True)
 if not shutil.which('open_jtalk') or not Path(dictionary).is_dir() or not models:raise RuntimeError('Open JTalk dictionary/voice missing')
 path=O/f'voice_{i}.wav'
 p=subprocess.run(['open_jtalk','-x',dictionary,'-m',models[0],'-r','1.14','-ow',str(path)],input=DATA[i][3]+'\n',text=True,capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr)
 with wave.open(str(path)) as w:
  duration=w.getnframes()/w.getframerate()
 if duration<1:raise RuntimeError('Japanese narration too short')
 return path,duration
def main():
 paths=[draw_slide(i,p) for i in range(6) for p in (0,1)]
 aud=[voice(i) for i in range(6)]
 ds=[math.ceil(max(3,d+.45)*30)/30 for _,d in aud]
 # create aligned 48k mono s16 PCM audio
 pieces=[]
 for (p,_),d in zip(aud,ds):
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar','48000','-ac','1','-f','s16le','-'])
  a=np.frombuffer(raw,dtype='<i2').copy()
  target=int(round(d*48000))
  pieces.append(np.pad(a[:target],(0,max(0,target-len(a)))))
 audio=O/'voice_aligned.wav'
 with wave.open(str(audio),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000)
  w.writeframes(np.concatenate(pieces).astype('<i2').tobytes())
 manifest=O/'slides.txt'
 with manifest.open('w') as f:
  for i,d in enumerate(ds):
   for phase in (0,1):
    f.write("file '"+paths[i*2+phase].name+"'\nduration "+str(d/2)+"\n")
  f.write("file '"+paths[-1].name+"'\n")
 out=O/'cycle482_NATIVE_JAPANESE_HUMAN_REVIEW.mp4'
 subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(manifest),'-i',str(audio),'-t',str(sum(ds)),'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20','-c:a','aac','-b:a','160k','-movflags','+faststart',str(out)],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
 decode=subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,text=True)
 v=next(s for s in probe['streams'] if s['codec_type']=='video')
 a=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert v['width']==1080 and v['height']==1920 and a['codec_name']=='aac' and decode.returncode==0
 qa={'cycle':482,'narration':'OPEN_JTALK_JAPANESE_SYNTHESIZED_HUMAN_LISTENING_PENDING','scene_aligned':True,'word_level_sync':'NOT_VERIFIED','scenes':6,'duration':float(probe['format']['duration']),'frames':int(v['nb_frames']),'resolution':[1080,1920],'codec':v['codec_name'],'audio_codec':a['codec_name'],'full_decode':'PASS','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'rights':'ORIGINAL_GRAPHICS','approval':'HUMAN_REVIEW','publication':'NOT_APPROVED','cost_jpy':0}
 (O/'qa_ci.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 print(json.dumps(qa,ensure_ascii=False))
if __name__=='__main__':main()
