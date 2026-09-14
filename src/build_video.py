#!/usr/bin/env python3
from pathlib import Path
import subprocess

out=Path('output'); out.mkdir(exist_ok=True)
audio=out/'narration.wav'; video=out/'AI時短ラボ_01_完成版.mp4'
if not audio.exists(): raise SystemExit('Missing narration')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
# Dynamic faceless TikTok v3: hook -> raw text -> AI prompt -> table -> spreadsheet -> CTA.
# UI is intentionally generic/illustrative, not a claim that this is the real ChatGPT interface.
f=[]
f += ["drawbox=x=0:y=0:w=1080:h=1920:color=0x07111f:t=fill"]
# top brand
f += [f"drawtext=fontfile={FONT}:text='AI時短ラボ':fontcolor=0x6ee7ff:fontsize=38:x=70:y=90"]
# scene 1 hook 0-3.5
f += ["drawbox=x=65:y=350:w=950:h=620:color=0x111f35:t=fill:enable='between(t,0,3.5)'",
      f"drawtext=fontfile={FONT}:text='そのExcelコピペ':fontcolor=white:fontsize=78:x=(w-text_w)/2:y=500:enable='between(t,0,3.5)'",
      f"drawtext=fontfile={FONT}:text='まだ手作業？':fontcolor=0xffe45e:fontsize=94:x=(w-text_w)/2:y=620:enable='between(t,0,3.5)'",
      f"drawtext=fontfile={REG}:text='3秒で Before → After':fontcolor=0x70f0b1:fontsize=48:x=(w-text_w)/2:y=800:enable='between(t,0,3.5)'"]
# scene 2 raw customer data 3.5-8
f += ["drawbox=x=70:y=300:w=940:h=980:color=0xf5f7fb:t=fill:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={FONT}:text='BEFORE  バラバラな文章':fontcolor=0xff5f6d:fontsize=48:x=110:y=350:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={REG}:text='山田太郎様  090-0000-1111':fontcolor=0x172033:fontsize=43:x=115:y=500:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={REG}:text='yamada@example.com':fontcolor=0x172033:fontsize=40:x=115:y=575:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={REG}:text='希望日時 10月1日 14時':fontcolor=0x172033:fontsize=43:x=115:y=650:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={REG}:text='佐藤花子様  080-2222-3333':fontcolor=0x172033:fontsize=43:x=115:y=800:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={REG}:text='satou@example.com':fontcolor=0x172033:fontsize=40:x=115:y=875:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={REG}:text='希望日時 10月2日 10時':fontcolor=0x172033:fontsize=43:x=115:y=950:enable='between(t,3.5,8)'",
      f"drawtext=fontfile={FONT}:text='これを1件ずつExcelへ…':fontcolor=0xffe45e:fontsize=52:x=(w-text_w)/2:y=1390:enable='between(t,3.5,8)'"]
# scene 3 AI prompt 8-15
f += ["drawbox=x=70:y=280:w=940:h=1050:color=0x101d31:t=fill:enable='between(t,8,15)'",
      f"drawtext=fontfile={FONT}:text='AIにこう頼むだけ':fontcolor=0x70f0b1:fontsize=62:x=110:y=340:enable='between(t,8,15)'",
      "drawbox=x=115:y=500:w=850:h=500:color=0x1d304b:t=fill:enable='between(t,8,15)'",
      f"drawtext=fontfile={REG}:text='氏名・電話番号・メール・希望日時を':fontcolor=white:fontsize=40:x=150:y=590:enable='between(t,8,15)'",
      f"drawtext=fontfile={REG}:text='抽出して、Excelに貼れる':fontcolor=white:fontsize=40:x=150:y=675:enable='between(t,8,15)'",
      f"drawtext=fontfile={FONT}:text='表形式':fontcolor=0xffe45e:fontsize=56:x=150:y=760:enable='between(t,8,15)'",
      f"drawtext=fontfile={REG}:text='で出力してください。':fontcolor=white:fontsize=40:x=370:y=775:enable='between(t,8,15)'",
      f"drawtext=fontfile={REG}:text='※画面はイメージ':fontcolor=white@0.55:fontsize=28:x=720:y=1260:enable='between(t,8,15)'"]
# scene 4 table 15-23
f += [f"drawtext=fontfile={FONT}:text='AFTER  一瞬で表に':fontcolor=0x70f0b1:fontsize=60:x=(w-text_w)/2:y=260:enable='between(t,15,23)'",
      "drawbox=x=55:y=430:w=970:h=700:color=0xf8fafc:t=fill:enable='between(t,15,23)'",
      "drawbox=x=55:y=430:w=970:h=120:color=0x1f6feb:t=fill:enable='between(t,15,23)'",
      f"drawtext=fontfile={FONT}:text='氏名      電話番号       希望日時':fontcolor=white:fontsize=39:x=105:y=465:enable='between(t,15,23)'",
      f"drawtext=fontfile={REG}:text='山田太郎   090-0000-1111   10/1 14時':fontcolor=0x172033:fontsize=36:x=90:y=650:enable='between(t,15,23)'",
      f"drawtext=fontfile={REG}:text='佐藤花子   080-2222-3333   10/2 10時':fontcolor=0x172033:fontsize=36:x=90:y=790:enable='between(t,15,23)'",
      f"drawtext=fontfile={FONT}:text='コピー':fontcolor=0x07111f:fontsize=45:x=450:y=1010:enable='between(t,15,23)'",
      f"drawtext=fontfile={FONT}:text='✓ 整理完了':fontcolor=0x70f0b1:fontsize=56:x=(w-text_w)/2:y=1330:enable='between(t,15,23)'"]
# scene 5 spreadsheet 23-30
f += [f"drawtext=fontfile={FONT}:text='Excel / スプレッドシートへ':fontcolor=white:fontsize=55:x=(w-text_w)/2:y=260:enable='between(t,23,30)'",
      "drawbox=x=55:y=440:w=970:h=720:color=0xffffff:t=fill:enable='between(t,23,30)'",
      "drawgrid=w=240:h=120:t=2:c=0xcbd5e1:enable='between(t,23,30)'",
      f"drawtext=fontfile={FONT}:text='貼り付けるだけ':fontcolor=0xffe45e:fontsize=82:x=(w-text_w)/2:y=1300:enable='between(t,23,30)'",
      f"drawtext=fontfile={REG}:text='面倒なコピペ作業を一気に減らす':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=1430:enable='between(t,23,30)'"]
# scene 6 CTA 30+
f += ["drawbox=x=90:y=470:w=900:h=650:color=0x101d31:t=fill:enable='gte(t,30)'",
      f"drawtext=fontfile={FONT}:text='明日から使うなら':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=590:enable='gte(t,30)'",
      f"drawtext=fontfile={FONT}:text='保存して試してみて':fontcolor=0xffe45e:fontsize=72:x=(w-text_w)/2:y=720:enable='gte(t,30)'",
      f"drawtext=fontfile={REG}:text='AI × 仕事術を毎日更新':fontcolor=0x70f0b1:fontsize=45:x=(w-text_w)/2:y=900:enable='gte(t,30)'"]
# progress bar adds constant motion
f += ["drawbox=x=0:y=1870:w='1080*t/35':h=12:color=0x38d9ff:t=fill"]
fg=','.join(f)
cmd=['ffmpeg','-y','-f','lavfi','-i','color=c=0x07111f:s=1080x1920:r=30','-i',str(audio),'-vf',fg,'-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','44100','-shortest','-movflags','+faststart',str(video)]
subprocess.run(cmd,check=True)
print(video)
