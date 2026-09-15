#!/usr/bin/env python3
from pathlib import Path
import subprocess,wave,json,math,struct
O=Path('output'); O.mkdir(exist_ok=True)
A=O/'narration.wav'; T=O/'narration_timing.json'; P=O/'v7_storyboard.json'; V=O/'AI時短ラボ_01_完成版.mp4'; S=O/'ui_sfx.wav'
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
with wave.open(str(A),'rb') as w:D=w.getnframes()/w.getframerate()
# UI sound design
sr=44100; buf=bytearray(int(sr*(D+.4))*2)
for c,hz in [(0.08,1180),(2.2,720),(6,980),(9,1180),(14,760),(17,1280),(21,900),(23,1380),(27,760)]:
 for j in range(int(.07*sr)):
  x=j/sr; v=math.sin(2*math.pi*hz*x)*math.exp(-45*x)*.13; i=(int(c*sr)+j)*2
  if i+1<len(buf): struct.pack_into('<h',buf,i,int(v*32767))
with wave.open(str(S),'wb') as w:w.setparams((1,2,sr,len(buf)//2,'NONE',''));w.writeframes(buf)
plan=json.loads(P.read_text(encoding='utf-8'))
f=["drawbox=x=0:y=0:w=1080:h=1920:color=0x050914:t=fill",
   "drawbox=x='-250+80*sin(t*.7)':y=120:w=760:h=760:color=0x082b48@0.35:t=fill",
   "drawbox=x='700+50*cos(t*.6)':y=520:w=520:h=700:color=0x351a66@0.28:t=fill",
   f"drawtext=fontfile={F}:text='AI時短ラボ':fontcolor=0x67e8f9:fontsize=31:x=54:y=64"]
# HOOK: character-like robot badge built from shapes + immediate proof
f += ["drawbox=x='70+10*sin(t*5)':y='250+8*cos(t*4)':w=270:h=300:color=0xf8fafc:t=fill:enable='between(t,0,2.2)'",
      "drawbox=x='105+10*sin(t*5)':y='290+8*cos(t*4)':w=200:h=125:color=0x101827:t=fill:enable='between(t,0,2.2)'",
      "drawbox=x='145+10*sin(t*5)':y='335+8*cos(t*4)':w=24:h=18:color=0x22d3ee:t=fill:enable='between(t,0,2.2)'",
      "drawbox=x='240+10*sin(t*5)':y='335+8*cos(t*4)':w=24:h=18:color=0x22d3ee:t=fill:enable='between(t,0,2.2)'",
      f"drawtext=fontfile={F}:text='そのコピペ':fontcolor=white:fontsize=80:x=390:y=260:enable='between(t,0,2.2)'",
      f"drawtext=fontfile={F}:text='AIなら一瞬':fontcolor=0xffe45e:fontsize=92:x=390:y=380:enable='between(t,.18,2.2)'",
      "drawbox=x=80:y=690:w=400:h=410:color=white:t=fill:enable='between(t,.35,2.2)'","drawbox=x=600:y=690:w=400:h=410:color=white:t=fill:enable='between(t,.55,2.2)'",
      f"drawtext=fontfile={F}:text='バラバラ文章':fontcolor=0xef4444:fontsize=40:x=145:y=735:enable='between(t,.35,2.2)'",f"drawtext=fontfile={R}:text='山田 090...':fontcolor=0x172033:fontsize=34:x=130:y=850:enable='between(t,.5,2.2)'",
      f"drawtext=fontfile={F}:text='Excel表 ✓':fontcolor=0x16a34a:fontsize=48:x=700:y=735:enable='between(t,.55,2.2)'",f"drawtext=fontfile={R}:text='氏名｜電話｜日時':fontcolor=0x172033:fontsize=31:x=650:y=850:enable='between(t,.7,2.2)'"]
# PAIN: desktop document, scanning highlight, small robot reaction
f += ["drawbox=x=55:y=210:w=970:h=1030:color=0xf8fafc:t=fill:enable='between(t,2.2,6)'","drawbox=x=55:y=210:w=970:h=90:color=0x334155:t=fill:enable='between(t,2.2,6)'",f"drawtext=fontfile={F}:text='問い合わせメモ.txt':fontcolor=white:fontsize=32:x=100:y=238:enable='between(t,2.2,6)'",
      f"drawtext=fontfile={R}:text='山田太郎様　090-0000-1111':fontcolor=0x172033:fontsize=39:x=110:y=430:enable='between(t,2.2,6)'",f"drawtext=fontfile={R}:text='yamada@example.com　10月1日14時':fontcolor=0x172033:fontsize=33:x=110:y=520:enable='between(t,2.4,6)'",
      f"drawtext=fontfile={R}:text='佐藤花子様　080-2222-3333':fontcolor=0x172033:fontsize=39:x=110:y=720:enable='between(t,2.7,6)'","drawbox=x=95:y='390+min(430,max(0,(t-2.2)*135))':w=880:h=72:color=0xffe45e@0.24:t=fill:enable='between(t,2.2,5.8)'",
      f"drawtext=fontfile={F}:text='1件ずつ移すの、やめます':fontcolor=0xff9f43:fontsize=52:x=(w-text_w)/2:y=1080:enable='between(t,3.8,6)'" ]
# DEMO: browser with address bar, chat bubbles, progressive prompt, cursor and punch-in label
f += ["drawbox=x=45:y=190:w=990:h=1110:color=0x111827:t=fill:enable='between(t,6,14)'","drawbox=x=45:y=190:w=990:h=105:color=0x1f2937:t=fill:enable='between(t,6,14)'","drawbox=x=160:y=218:w=720:h=52:color=0x374151:t=fill:enable='between(t,6,14)'",f"drawtext=fontfile={R}:text='chat.openai.com':fontcolor=0xd1d5db:fontsize=25:x=360:y=232:enable='between(t,6,14)'",
      f"drawtext=fontfile={F}:text='ChatGPTにそのまま貼る':fontcolor=0x67e8f9:fontsize=48:x=95:y=370:enable='between(t,6,14)'","drawbox=x=95:y=500:w=890:h=450:color=0x243247:t=fill:enable='between(t,6,14)'",
      f"drawtext=fontfile={R}:text='この文章から':fontcolor=white:fontsize=40:x=145:y=565:enable='between(t,6.2,14)'",f"drawtext=fontfile={R}:text='氏名・電話・メール・希望日時を':fontcolor=white:fontsize=37:x=145:y=660:enable='between(t,7.2,14)'",f"drawtext=fontfile={F}:text='表形式で出力して':fontcolor=0xffe45e:fontsize=57:x=145:y=770:enable='between(t,8.3,14)'",
      "drawbox=x='160+min(700,max(0,(t-6)*120))':y=865:w=5:h=55:color=white:t=fill:enable='between(t,6,11.8)'","drawbox=x=780:y=1030:w=165:h=90:color=0x10a37f:t=fill:enable='between(t,9.5,14)'",f"drawtext=fontfile={F}:text='送信':fontcolor=white:fontsize=35:x=820:y=1055:enable='between(t,9.5,14)'",
      f"drawtext=fontfile={F}:text='これだけ。':fontcolor=white:fontsize=70:x=(w-text_w)/2:y=1190:enable='between(t,11.2,14)'" ]
# PROOF: answer table + progressive rows + copy feedback
f += ["drawbox=x=45:y=200:w=990:h=1090:color=0xf8fafc:t=fill:enable='between(t,14,21)'",f"drawtext=fontfile={F}:text='AIが自動整理':fontcolor=0x10a37f:fontsize=58:x=95:y=300:enable='between(t,14,21)'","drawbox=x=85:y=455:w=910:h=110:color=0x2563eb:t=fill:enable='between(t,14,21)'",f"drawtext=fontfile={F}:text='氏名　　電話番号　　 希望日時':fontcolor=white:fontsize=36:x=120:y=490:enable='between(t,14,21)'",
      f"drawtext=fontfile={R}:text='山田太郎　090-0000-1111　10/1 14時':fontcolor=0x172033:fontsize=34:x=115:y=650:enable='between(t,14.5,21)'",f"drawtext=fontfile={R}:text='佐藤花子　080-2222-3333　10/2 10時':fontcolor=0x172033:fontsize=34:x=115:y=790:enable='between(t,15.3,21)'","drawbox=x=735:y=975:w=225:h=95:color=0xe2e8f0:t=fill:enable='between(t,16.2,21)'",f"drawtext=fontfile={F}:text='コピー':fontcolor=0x172033:fontsize=36:x=790:y=1002:enable='between(t,16.2,21)'",f"drawtext=fontfile={F}:text='コピー完了 ✓':fontcolor=0x16a34a:fontsize=58:x=(w-text_w)/2:y=1140:enable='between(t,17.5,21)'" ]
# PAYOFF: spreadsheet proof + kinetic confirmation
f += ["drawbox=x=40:y=195:w=1000:h=1110:color=0xf3f6f8:t=fill:enable='between(t,21,27)'","drawbox=x=40:y=195:w=1000:h=105:color=0x217346:t=fill:enable='between(t,21,27)'",f"drawtext=fontfile={F}:text='Excel　営業リスト.xlsx':fontcolor=white:fontsize=35:x=90:y=230:enable='between(t,21,27)'",f"drawtext=fontfile={F}:text='A　　 B　　　　 C　　　　 D':fontcolor=0x475569:fontsize=35:x=120:y=430:enable='between(t,21,27)'","drawbox=x=100:y=520:w=875:h=100:color=0x217346@0.18:t=fill:enable='between(t,21,27)'",f"drawtext=fontfile={F}:text='⌘V':fontcolor=0x217346:fontsize=110:x=(w-text_w)/2:y=800:enable='between(t,21.1,22.6)'",f"drawtext=fontfile={R}:text='山田太郎　090-0000-1111　10/1 14時':fontcolor=0x172033:fontsize=34:x=115:y=555:enable='between(t,22.5,27)'",f"drawtext=fontfile={R}:text='佐藤花子　080-2222-3333　10/2 10時':fontcolor=0x172033:fontsize=34:x=115:y=690:enable='between(t,23,27)'",f"drawtext=fontfile={F}:text='手入力 → 一括貼り付け':fontcolor=0x16a34a:fontsize=64:x=(w-text_w)/2:y=1060:enable='between(t,23.4,27)'" ]
# CTA: robot returns as visual anchor
cta=max(27,D-5.5)
f += [f"drawbox=x=100:y=380:w=880:h=760:color=0x101d31:t=fill:enable='gte(t,{cta})'",f"drawbox=x='140+8*sin(t*5)':y='510+7*cos(t*4)':w=250:h=280:color=0xf8fafc:t=fill:enable='gte(t,{cta})'",f"drawbox=x='175+8*sin(t*5)':y='550+7*cos(t*4)':w=180:h=115:color=0x101827:t=fill:enable='gte(t,{cta})'",f"drawtext=fontfile={F}:text='明日使うなら':fontcolor=white:fontsize=55:x=450:y=500:enable='gte(t,{cta})'",f"drawtext=fontfile={F}:text='保存':fontcolor=0xffe45e:fontsize=100:x=520:y=620:enable='gte(t,{cta})'",f"drawtext=fontfile={F}:text='次回：営業メールを10秒で作る':fontcolor=0x67e8f9:fontsize=42:x=(w-text_w)/2:y=950:enable='gte(t,{cta})'" ]
# phrase captions
for i,x in enumerate(json.loads(T.read_text(encoding='utf-8'))):
 a,b=x['start'],x['end']; txt=x['text'].replace("'","’").replace(':','\\:').replace(',','，'); sz=46 if len(txt)>20 else 57
 col='0xffe45e' if i in (0,4,len(json.loads(T.read_text()))-1) else 'white'
 f += [f"drawbox=x=60:y=1435:w=960:h=205:color=black@0.80:t=fill:enable='between(t,{a},{b})'",f"drawtext=fontfile={F}:text='{txt}':fontcolor={col}:fontsize={sz}:x=(w-text_w)/2:y=1495:enable='between(t,{a},{b})'"]
f += [f"drawbox=x=0:y=1878:w='min(1080,1080*t/{D:.3f})':h=9:color=0x38d9ff:t=fill"]
fg=','.join(f)
cmd=['ffmpeg','-y','-f','lavfi','-i',f'color=c=0x050914:s=1080x1920:r=30:d={D+.15:.3f}','-i',str(A),'-i',str(S),'-filter_complex',f"[0:v]{fg}[v];[1:a]volume=1[vo];[2:a]volume=.30[fx];[vo][fx]amix=inputs=2:duration=first:normalize=0[a]",'-map','[v]','-map','[a]','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(V)]
subprocess.run(cmd,check=True)
print(V)
