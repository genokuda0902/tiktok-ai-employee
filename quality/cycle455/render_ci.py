#!/usr/bin/env python3
"""Zero-cost, synthetic-data Japanese narration CI proof. Never auto-publish."""
import hashlib, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from pydub import AudioSegment
ROOT=Path(__file__).resolve().parent
DUR=[1.7,2.2,2.7,2.9,2.6,2.7,2.7,2.5]
LINES=['集計、まだ手作業？','数字が変わると、また計算。','合計する範囲を選びます。','サム関数で、合計17。','2を4に変えてみると。','合計も、自動で19に。','AIには、目的と範囲を伝えよう。','保存して、試してみて。']
CAP=['毎日の集計、手で足してない？','数字が変わるたび、数え直すのは大変。','合計には、この数式を使います。','E2からE7を足すと、17。','数字を2から4に変えてみると…','合計も19に。自動で更新されます。','AIに聞くなら、範囲と目的を具体的に。','保存して、まずは練習用の表で試そう。']
TITLES=['毎日、手で集計？','BEFORE：毎回計算','E2:E7 を選択','=SUM(E2:E7)','2 → 4 に変更','AFTER：合計19','AIには目的と範囲を','保存して試そう']
VALUES=[3,2,4,1,5,2]
GENRES=['AI・仕事効率化','転職・キャリア','お金・家計','学習・資格','コミュニケーション','健康習慣','生産性','IT・デジタル','ビジネス','暮らしの工夫']
def run(*a):
 p=subprocess.run(list(map(str,a)),text=True,capture_output=True)
 if p.returncode:raise RuntimeError('COMMAND_FAILED '+p.stderr[-1200:])
 return p.stdout
def font(size):
 for path in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']:
  if Path(path).exists():return ImageFont.truetype(path,size)
 raise RuntimeError('JAPANESE_FONT_MISSING')
def textfit(draw,text,xy,width,initial,fill):
 size=initial
 while draw.textbbox((0,0),text,font=font(size))[2]>width and size>28:size-=2
 draw.text(xy,text,font=font(size),fill=fill)
def draw_slide(i,path):
 im=Image.new('RGB',(1080,1920),'#F5F8FC');d=ImageDraw.Draw(im)
 d.rectangle((0,0,1080,20),fill='#38D9C4')
 d.text((70,68),'WORKFLOW  /  JAPANESE VOICE',font=font(27),fill='#17253D')
 d.text((70,210),'EXCEL × AI',font=font(32),fill='#546CF0')
 textfit(d,TITLES[i],(70,285),935,75,'#122238')
 d.rounded_rectangle((65,535,1015,1325),radius=35,fill='white',outline='#DEE7F0',width=5)
 d.rounded_rectangle((65,535,1015,640),radius=35,fill='#122238')
 d.rectangle((65,605,1015,640),fill='#122238')
 d.text((115,559),'架空の集計シート / 実在データなし',font=font(30),fill='white')
 if i<6:
  vals=VALUES if i<5 else [3,4,4,1,5,2]
  if i==4:vals=[3,4,4,1,5,2]
  d.text((125,710),'成約件数  E2:E7',font=font(43),fill='#122238')
  for k,v in enumerate(vals):
   y=790+k*66
   d.rounded_rectangle((130,y,940,y+55),radius=8,fill='#F0F5FA' if k%2==0 else '#FAFBFD')
   d.text((160,y+5),f'E{k+2}',font=font(31),fill='#566A80')
   d.text((760,y+5),str(v),font=font(33),fill='#122238')
  d.rounded_rectangle((115,1210,965,1290),radius=16,fill='#C6F8DF')
  d.text((148,1225),'=SUM(E2:E7)   →   '+str(sum(vals)),font=font(37),fill='#122238')
 else:
  d.text((125,740),'AIへの質問例',font=font(44),fill='#122238')
  d.text((125,880),'「E2:E7 の合計を出す',font=font(40),fill='#122238')
  d.text((125,960),'数式を教えて」',font=font(40),fill='#122238')
  d.text((125,1170),'出力内容は必ず確認',font=font(30),fill='#566A80')
 d.rounded_rectangle((65,1440,1015,1615),radius=28,fill='#122238')
 textfit(d,CAP[i],(90,1500),895,46,'white')
 for k in range(8):
  d.rounded_rectangle((70+k*120,1690,166+k*120,1707),radius=6,fill='#38D9C4' if k<=i else '#DBE3ED')
 d.text((70,1770),'SYNTHETIC DATA  •  HUMAN REVIEW ONLY',font=font(25),fill='#64758C')
 im.save(path)
def main():
 assert abs(sum(DUR)-20)<.001 and sum(VALUES)==17
 ROOT.mkdir(parents=True,exist_ok=True)
 files=[]
 for i,secs in enumerate(DUR):
  p=ROOT/f'scene_{i:02}.png';draw_slide(i,p);files.append((p,secs))
 playlist=ROOT/'concat.txt'
 playlist.write_text(''.join(f"file '{p.resolve()}'\\nduration {secs:.8f}\\n" for p,secs in files)+f"file '{files[-1][0].resolve()}'\\n")
 # Replace escaped newlines only if this source was embedded through JS template.
 playlist.write_text(playlist.read_text().replace('\\n','\n'))
 video=ROOT/'silent.mp4'
 run('ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',playlist,'-vf','fps=30,format=yuv420p','-t','20','-c:v','libx264','-preset','veryfast','-crf','19',video)
 audio=AudioSegment.silent(duration=0,frame_rate=48000)
 for i,(line,secs) in enumerate(zip(LINES,DUR)):
  mp3=ROOT/f'voice_{i}.mp3'
  gTTS(text=line,lang='ja',slow=False).save(str(mp3))
  clip=AudioSegment.from_file(mp3).set_channels(1).set_frame_rate(48000)
  slot=int(secs*1000)
  if len(clip)>slot-80:
   ratio=len(clip)/(slot-80)
   if ratio>1.5:raise RuntimeError(f'TTS_TOO_LONG scene={i} ratio={ratio:.2f}')
   wav=ROOT/f'in_{i}.wav';faster=ROOT/f'out_{i}.wav'
   clip.export(wav,format='wav')
   run('ffmpeg','-y','-v','error','-i',wav,'-af',f'atempo={ratio:.5f}',faster)
   clip=AudioSegment.from_wav(faster)
  if len(clip)>slot:raise RuntimeError(f'TTS_OVERLAP scene={i}')
  audio+=clip+AudioSegment.silent(duration=slot-len(clip),frame_rate=48000)
 if not 19950<=len(audio)<=20050 or audio.rms<100:raise RuntimeError('VOICE_QA_FAILED')
 wav=ROOT/'japanese_voice.wav';audio.export(wav,format='wav')
 mp4=ROOT/'cycle455_JA_VOICE_HUMAN_REVIEW.mp4'
 run('ffmpeg','-y','-v','error','-i',video,'-i',wav,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-t','20','-movflags','+faststart',mp4)
 probe=json.loads(run('ffprobe','-v','error','-show_entries','stream=codec_name,codec_type,width,height,nb_frames,sample_rate:format=duration','-of','json',mp4))
 run('ffmpeg','-v','error','-i',mp4,'-f','null','-')
 v=next(s for s in probe['streams'] if s['codec_type']=='video')
 a=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264')
 assert a['codec_name']=='aac' and abs(float(probe['format']['duration'])-20)<.12
 qa={'cycle':455,'tts_engine':'gTTS Japanese','narration_generated':True,'audio_rms':audio.rms,'captions':'burned_in','resolution':'1080x1920','full_decode':'PASS','reference_equivalence':'NOT_VERIFIED','human_voice_quality':'NOT_REVIEWED','publication':'NOT_APPROVED','sha256':hashlib.sha256(mp4.read_bytes()).hexdigest(),'genres_configured':GENRES,'genres_rendered':1}
 (ROOT/'qa_ci.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 print(json.dumps(qa,ensure_ascii=False))
if __name__=='__main__':main()
