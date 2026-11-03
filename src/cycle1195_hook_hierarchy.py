"""Review-only top hook hierarchy overlay; preserves caption-safe lower area."""
import argparse
import subprocess
from pathlib import Path

def filtergraph(font, title="AI仕事術", hook="今日から使える3つのコツ"):
    if not Path(font).is_file():
        raise FileNotFoundError(font)
    for text in (title, hook):
        if any(c in text for c in ":,'\\%\n"):
            raise ValueError("Unsupported drawtext punctuation")
        if len(text) > 24:
            raise ValueError("Headline too long")
    return (
        "drawbox=x=60:y=160:w=960:h=230:color=0x0a1428@0.88:t=fill,"
        "drawbox=x=60:y=160:w=12:h=230:color=0x46d7e9:t=fill,"
        f"drawtext=fontfile={font}:text='{title}':fontcolor=0x46d7e9:fontsize=44:x=98:y=185,"
        f"drawtext=fontfile={font}:text='{hook}':fontcolor=white:fontsize=51:x=98:y=255"
    )

def render(source, target, font, title, hook):
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    if Path(source).resolve() == Path(target).resolve():
        raise ValueError("Source and target must differ")
    vf = filtergraph(font, title, hook)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
                    "-vf",vf,"-c:v","libx264","-preset","ultrafast","-crf","19",
                    "-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source");p.add_argument("target");p.add_argument("--font",required=True)
    p.add_argument("--title",default="AI仕事術");p.add_argument("--hook",default="今日から使える3つのコツ")
    a=p.parse_args();render(a.source,a.target,a.font,a.title,a.hook)
