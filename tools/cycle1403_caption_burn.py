"""Cycle 1403: burn timed Japanese scene captions into an existing review MP4.
Requires ffmpeg with libass. Review-only, not speech-synchronized.
Usage: python tools/cycle1403_caption_burn.py input.mp4 captions.srt output.mp4
"""
import json
import subprocess
import sys
from pathlib import Path

def render(source: Path, captions: Path, target: Path) -> None:
    if not source.is_file() or not captions.is_file():
        raise FileNotFoundError("Source MP4 and approved caption file required")
    if captions.read_text(encoding="utf-8").count("-->") < 1:
        raise ValueError("No timed captions")
    vf = (
        f"subtitles='{captions.resolve()}':"
        "force_style='FontName=Noto Sans CJK JP,FontSize=18,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H00102030,Outline=2,MarginV=240',"
        "drawbox=x=80:y=1840:w=920:h=10:color=white@0.18:t=fill,"
        "drawbox=x=80:y=1840:w='min(920,46*t)':h=10:color=0x27d3c5:t=fill"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(source),
        "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(target)], check=True)

def verify(target: Path) -> dict:
    p = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams",
        "-show_format", "-of", "json", str(target)]))
    video = next(s for s in p["streams"] if s["codec_type"] == "video")
    assert (video["width"], video["height"]) == (1080, 1920)
    assert not any(s["codec_type"] == "audio" for s in p["streams"])
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(target), "-f", "null", "-"], check=True)
    return {"decode": "PASS", "burned_scene_captions": True,
            "japanese_narration": False, "speech_synced_captions": False,
            "publication_approved": False}

if __name__ == "__main__":
    render(*map(Path, sys.argv[1:4]))
    print(json.dumps(verify(Path(sys.argv[3]))))
