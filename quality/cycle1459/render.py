"""Self-contained review-only silent render; not v33 or publishable."""
from pathlib import Path
import argparse,subprocess
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('毎日の集計、まだ手入力？','まず入力表を整理'),('SUM関数で自動集計','SUMで合計を表示'),('数字を照合して完了','確認してから共有')]
def render(output):
 output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 vf=['drawbox=x=80:y=370:w=920:h=1040:color=0x13243a:t=fill','drawbox=x=100:y=480:w=880:h=75:color=0x245d78:t=fill']
 for i,(heading,caption) in enumerate(SCENES):
  a,b=i*4,(i+1)*4
  vf += [f"drawtext=fontfile={FONT}:text='{heading}':fontsize=52:fontcolor=white:x=(w-text_w)/2:y=650:enable='between(t,{a},{b})'",f"drawtext=fontfile={FONT}:text='{caption}':fontsize=49:fontcolor=yellow:x=(w-text_w)/2:y=1170:enable='between(t,{a},{b})'"]
 vf += [f"drawtext=fontfile={FONT}:text='REVIEW ONLY / NO NARRATION':fontsize=30:fontcolor=white:x=(w-text_w)/2:y=1780"]
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=0x07121f:s=1080x1920:r=24:d=12','-vf',','.join(vf),'-an','-c:v','libx264','-preset','ultrafast','-crf','26','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True)
 return output
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);render(p.parse_args().output)
