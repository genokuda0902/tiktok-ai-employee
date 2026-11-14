"""Self-contained review-only 12s portrait renderer. NOT original v33. No Japanese speech."""
from pathlib import Path
import argparse, subprocess
SCENES=[('毎日の集計、まだ手入力？','入力ミスを減らす'),('SUM関数で自動集計','数式を確認する'),('結果を必ず見直す','確認してから共有')]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def run(output: Path):
    output.parent.mkdir(parents=True,exist_ok=True)
    filters=[]
    for i,(head,sub) in enumerate(SCENES):
        start=i*4; end=start+4
        filters += [f"drawbox=x=75:y=260:w=930:h=1250:color=0x14243b:t=fill:enable='between(t,{start},{end})'",
                    f"drawbox=x=95:y={420+i*135}:w=890:h=85:color=0x237a89:t=fill:enable='between(t,{start},{end})'",
                    f"drawtext=fontfile={FONT}:text='{head}':fontsize=58:fontcolor=white:x=(w-text_w)/2:y=650:enable='between(t,{start},{end})'",
                    f"drawtext=fontfile={FONT}:text='{sub}':fontsize=42:fontcolor=white:x=(w-text_w)/2:y=1110:enable='between(t,{start},{end})'"]
    filters += [f"drawtext=fontfile={FONT}:text='REVIEW ONLY':fontsize=33:fontcolor=yellow:x=(w-text_w)/2:y=1770"]
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=0x07121f:s=1080x1920:r=24:d=12','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=12','-vf',','.join(filters),'-c:v','libx264','-preset','ultrafast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-t','12','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.output)
