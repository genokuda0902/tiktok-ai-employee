from pathlib import Path
import subprocess

OUT=Path('output'); OUT.mkdir(exist_ok=True)
video=OUT/'ai_jitan_lab_excel_ai_v1.mp4'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
regular='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
# First complete-video visual prototype: dynamic vertical UI-demo style, no paid services.
filters=(
"drawbox=x=55:y=90:w=970:h=1740:color=0x111827:t=fill,"
"drawtext=fontfile=%s:text='AI時短ラボ':fontcolor=0x67e8f9:fontsize=48:x=80:y=125," % font+
"drawtext=fontfile=%s:text='そのコピペ、まだ手作業？':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=280:enable='between(t,0,4)'," % font+
"drawtext=fontfile=%s:text='長文 → 表\nAIなら数秒':fontcolor=0xfacc15:fontsize=82:line_spacing=24:x=(w-text_w)/2:y=560:enable='between(t,4,9)'," % font+
"drawbox=x=110:y=520:w=860:h=620:color=0x1f2937:t=fill:enable='between(t,9,17)',"
"drawtext=fontfile=%s:text='AIチャット':fontcolor=0x67e8f9:fontsize=44:x=150:y=560:enable='between(t,9,17)'," % font+
"drawtext=fontfile=%s:text='氏名・電話番号・メール・希望日時を\n表にまとめて':fontcolor=white:fontsize=46:line_spacing=20:x=150:y=680:enable='between(t,9,17)'," % regular+
"drawbox=x=110:y=470:w=860:h=820:color=white:t=fill:enable='between(t,17,26)',"
"drawtext=fontfile=%s:text='氏名   電話   メール   希望日時':fontcolor=0x111827:fontsize=39:x=145:y=535:enable='between(t,17,26)'," % font+
"drawtext=fontfile=%s:text='山田   090...  yamada...  10/1 14時\n佐藤   080...  satou...   10/2 10時':fontcolor=0x111827:fontsize=35:line_spacing=35:x=145:y=650:enable='between(t,17,26)'," % regular+
"drawtext=fontfile=%s:text='そのまま表計算へ貼り付け':fontcolor=0x22c55e:fontsize=54:x=(w-text_w)/2:y=1370:enable='between(t,17,26)'," % font+
"drawtext=fontfile=%s:text='面倒なコピペ作業を\n一気に減らせます':fontcolor=white:fontsize=72:line_spacing=25:x=(w-text_w)/2:y=620:enable='between(t,26,34)'," % font+
"drawtext=fontfile=%s:text='フォローしてAI時短術を保存':fontcolor=0xfacc15:fontsize=52:x=(w-text_w)/2:y=1040:enable='between(t,26,34)'" % font
)
cmd=['ffmpeg','-y','-f','lavfi','-i','color=c=0x070b14:s=1080x1920:d=34:r=30','-vf',filters,'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
subprocess.run(cmd,check=True)
print(video)
