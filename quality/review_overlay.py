"""Review-only overlay renderer. Never authorizes publication or supplies narration."""
import argparse
import json
import subprocess
from pathlib import Path

def overlay_filter(duration: float, font: str) -> str:
    if not 1 <= duration <= 120:
        raise ValueError("duration must be 1..120 seconds")
    if not Path(font).is_file():
        raise FileNotFoundError(font)
    # Top progress and end-card remain outside the central subtitle region.
    return (
        "drawbox=x=0:y=0:w=iw:h=18:color=0x1ed5d0@0.95:t=fill,"
        f"drawbox=x=0:y=0:w='min(iw,iw*t/{duration})':h=18:color=white:t=fill,"
        f"drawbox=x=0:y=1700:w=iw:h=220:color=0x101827@0.60:t=fill:enable='gte(t,{max(0,duration-3)})',"
        "drawtext=fontfile=" + font +
        ":text='保存してあとで試す':fontcolor=white:fontsize=52:"
        f"x=(w-text_w)/2:y=1780:enable='gte(t,{max(0,duration-3)})'"
    )

def probe(path: Path) -> dict:
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,width,height", "-of", "json", str(path)],
        check=True, capture_output=True, text=True)
    return json.loads(p.stdout)

def render(source: Path, target: Path, font: str) -> dict:
    if not source.is_file():
        raise FileNotFoundError(source)
    info = probe(source)
    duration = float(info["format"]["duration"])
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source), "-vf", overlay_filter(duration, font),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-an", str(target)], check=True)
    result = probe(target)
    video = next((s for s in result["streams"] if s["codec_type"] == "video"), None)
    if not video or (video["width"], video["height"]) != (1080, 1920):
        raise RuntimeError("review render must be 1080x1920")
    # Explicitly fail publication gate: this tool is intentionally silent.
    return {"path": str(target), "duration": float(result["format"]["duration"]),
            "publication_approved": False, "narration_verified": False}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("target", type=Path)
    p.add_argument("--font", default="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    a = p.parse_args()
    print(json.dumps(render(a.source, a.target, a.font), ensure_ascii=False))
