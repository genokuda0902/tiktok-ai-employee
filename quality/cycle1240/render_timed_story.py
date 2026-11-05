"""Review-only timed story overlay. Requires an explicitly supplied approved source MP4."""
import argparse
from pathlib import Path
import subprocess

def render(source: Path, output: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    scenes=[(0,4,"BEFORE  手作業で計算"),(4,10,"ACTION  SUM関数を入力"),(10,15,"AFTER  合計300を確認"),(15,18,"公開前に内容を確認")]
    filters=[]
    for start,end,label in scenes:
        label=label.replace(":","\\:").replace("'","’")
        filters.extend([
            f"drawbox=x=55:y=1370:w=970:h=130:color=black@0.75:t=fill:enable='between(t,{start},{end})'",
            f"drawtext=fontfile={font}:text='{label}':fontsize=45:fontcolor=white:x=(w-text_w)/2:y=1405:enable='between(t,{start},{end})'"
        ])
    filters.append(f"drawtext=fontfile={font}:text='REVIEW ONLY':fontsize=28:fontcolor=yellow:x=70:y=80")
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(source),"-vf",",".join(filters),"-c:v","libx264","-preset","ultrafast","-crf","26","-c:a","copy","-movflags","+faststart",str(output)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(output),"-f","null","-"],check=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    render(args.input,args.output)
