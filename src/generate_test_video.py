from pathlib import Path
import subprocess

OUT = Path("output")
OUT.mkdir(exist_ok=True)
video = OUT / "ai_jitan_lab_cloud_test.mp4"

# First cloud smoke test: proves GitHub Actions + FFmpeg can render a 9:16 MP4
# without requiring the user's Mac/Windows to stay awake.
cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi",
    "-i", "color=c=0x0b1020:s=1080x1920:d=6:r=30",
    "-vf",
    "drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:"
    "text='AI JITAN LAB':fontcolor=white:fontsize=82:"
    "x=(w-text_w)/2:y=(h-text_h)/2-90,"
    "drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:"
    "text='CLOUD TEST OK':fontcolor=white:fontsize=54:"
    "x=(w-text_w)/2:y=(h-text_h)/2+40",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    str(video)
]
subprocess.run(cmd, check=True)
print(f"Created: {video}")
