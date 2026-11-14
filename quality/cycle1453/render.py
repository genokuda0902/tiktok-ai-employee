"""Review-only opener overlay; requires approved, captioned source MP4."""
from pathlib import Path
import subprocess, json, sys

def render(source: Path, output: Path):
    if not source.is_file():
        raise FileNotFoundError("Approved source required; never substitute private footage")
    output.parent.mkdir(parents=True, exist_ok=True)
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    vf=("drawbox=x=65:y=180:w=950:h=110:color=0x16324a@0.92:t=fill:enable='between(t,0,2)',"
        "drawtext=fontfile="+font+":text='手入力を減らす3ステップ':fontcolor=white:fontsize=51:x=(w-text_w)/2:y=205:enable='between(t,0,2)'")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",vf,
                    "-map","0:v:0","-map","0:s?","-c:v","libx264","-preset","ultrafast",
                    "-crf","24","-c:s","mov_text","-movflags","+faststart",str(output)],check=True)
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
                    "stream=codec_type,codec_name,width,height:format=duration","-of","json",str(output)]))
    assert any(s.get("width")==1080 and s.get("height")==1920 for s in probe["streams"])
    assert any(s["codec_type"]=="subtitle" for s in probe["streams"])
    subprocess.run(["ffmpeg","-v","error","-i",str(output),"-f","null","-"],check=True)
    return probe

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: render.py APPROVED_SOURCE.mp4 REVIEW_ONLY.mp4")
    print(json.dumps(render(Path(sys.argv[1]),Path(sys.argv[2])),ensure_ascii=False))
