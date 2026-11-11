from pathlib import Path
import subprocess
OUT=Path(__file__).with_name('cycle1381_REVIEW_ONLY.mp4')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
filters=[]
for start,end,title,sub in [(0,2,'集計に10分？','毎日のExcel作業'),(2,4,'関数を入力','=SUM(B2-B5)'),(4,6,'合計を自動計算','12400 円'),(6,8,'作業を短縮','保存して試してみよう')]:
    e=f'between(t,{start},{end-0.001})'
    filters += [f"drawbox=x=80:y=370:w=560:h=480:color=0x14243c:t=fill:enable='{e}'",f"drawtext=fontfile={font}:text='{title}':fontsize=49:fontcolor=white:x=(w-text_w)/2:y=470:enable='{e}'",f"drawtext=fontfile={font}:text='{sub}':fontsize=34:fontcolor=0x7de3dc:x=(w-text_w)/2:y=590:enable='{e}'"]
filters += ["drawbox=x=65:y=1060:w=590:h=12:color=0x3a465a:t=fill", "drawbox=x=65:y=1060:w='min(590,590*t/8)':h=12:color=0x49dfcf:t=fill",f"drawtext=fontfile={font}:text='AI時短ラボ / REVIEW ONLY':fontsize=25:fontcolor=white:x=70:y=1120"]
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=0x091321:s=720x1280:r=24:d=8','-vf',','.join(filters),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(OUT)],check=True)
print(OUT)
