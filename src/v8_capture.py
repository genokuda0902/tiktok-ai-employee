#!/usr/bin/env python3
from pathlib import Path
import subprocess
O=Path('output'); O.mkdir(exist_ok=True)
out=O/'operation_demo.mp4'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# A self-contained screen-demo capture. No external service login or brand UI scraping.
filters=[
"drawbox=x=35:y=90:w=1010:h=1660:color=0xf8fafc:t=fill",
"drawbox=x=35:y=90:w=1010:h=105:color=0x202938:t=fill",
f"drawtext=fontfile={font}:text='AI Assistant — 操作デモ':fontcolor=white:fontsize=34:x=90:y=122",
"drawbox=x=95:y=330:w=890:h=520:color=0xe9eef5:t=fill",
f"drawtext=fontfile={font}:text='この顧客情報から':fontcolor=0x111827:fontsize=45:x=145:y=410:enable='gte(t,0.3)'",
f"drawtext=fontfile={font}:text='氏名・電話・メール・希望日時を':fontcolor=0x111827:fontsize=39:x=145:y=510:enable='gte(t,1.0)'",
f"drawtext=fontfile={font}:text='表にして':fontcolor=0x2563eb:fontsize=64:x=145:y=620:enable='gte(t,1.8)'",
"drawbox=x=760:y=735:w=170:h=82:color=0x2563eb:t=fill",
f"drawtext=fontfile={font}:text='送信':fontcolor=white:fontsize=34:x=810:y=758",
"drawbox=x='150+min(720,max(0,(t-0.3)*145))':y=700:w=6:h=62:color=0x111827:t=fill:enable='between(t,0.3,5.0)'",
f"drawtext=fontfile={font}:text='生成中…':fontcolor=0x64748b:fontsize=38:x=100:y=930:enable='between(t,4.5,6.2)'",
"drawbox=x=95:y=900:w=890:h=600:color=white:t=fill:enable='gte(t,6.0)'",
"drawbox=x=115:y=980:w=850:h=95:color=0x2563eb:t=fill:enable='gte(t,6.0)'",
f"drawtext=fontfile={font}:text='氏名　　電話番号　　　希望日時':fontcolor=white:fontsize=33:x=150:y=1007:enable='gte(t,6.0)'",
f"drawtext=fontfile={font}:text='山田太郎　090-0000-1111　10/1 14時':fontcolor=0x111827:fontsize=31:x=140:y=1140:enable='gte(t,6.6)'",
f"drawtext=fontfile={font}:text='佐藤花子　080-2222-3333　10/2 10時':fontcolor=0x111827:fontsize=31:x=140:y=1260:enable='gte(t,7.3)'",
"drawbox=x=735:y=1390:w=210:h=80:color=0x10a37f:t=fill:enable='gte(t,8.0)'",
f"drawtext=fontfile={font}:text='コピー ✓':fontcolor=white:fontsize=31:x=770:y=1414:enable='gte(t,8.0)'"
]
cmd=['ffmpeg','-y','-f','lavfi','-i','color=c=0x0b1020:s=1080x1920:r=30:d=10','-vf',','.join(filters),'-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p','-an',str(out)]
subprocess.run(cmd,check=True)
print(out)
