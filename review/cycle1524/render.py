"""Review-only timed-caption overlay; no synthetic narration claims."""
import subprocess, json, sys
from pathlib import Path
SOURCE=Path(sys.argv[1]); OUTPUT=Path(sys.argv[2]); FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CAPTIONS=[('合計を手計算していませんか？',0,2),('セルにSUM関数を入力',2,4),('結果をすぐ確認',4,6),('最後に数値を検算',6,8)]
def validate(captions):
    assert captions and captions[0][1]==0
    assert all(a<b and (i==0 or a==captions[i-1][2]) for i,(_,a,b) in enumerate(captions))
    assert captions[-1][2]==8
validate(CAPTIONS)
filters=[]
for i,(caption,start,end) in enumerate(CAPTIONS):
    txt=OUTPUT.parent/f'caption_{i}.txt';txt.write_text(caption,encoding='utf-8')
    filters.append(f"drawbox=x=32:y=1030:w=656:h=132:color=black@0.82:t=fill:enable='between(t,{start},{end-0.001})'")
    filters.append(f"drawtext=fontfile={FONT}:textfile={txt}:fontcolor=white:fontsize=35:x=(w-text_w)/2:y=1072:enable='between(t,{start},{end-0.001})'")
subprocess.run(['ffmpeg','-y','-v','error','-i',str(SOURCE),'-vf',','.join(filters),'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(OUTPUT)],check=True)
print(json.dumps({'status':'REVIEW_ONLY','narration_verified':False,'caption_timing':CAPTIONS},ensure_ascii=False))
