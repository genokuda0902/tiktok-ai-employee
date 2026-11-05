"""Review-only audio QA overlay, never a substitute for synced subtitles."""
import subprocess
from pathlib import Path

def render_review(input_mp4, output_mp4, font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    source, target = Path(input_mp4), Path(output_mp4)
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        "drawbox=x=80:y=1380:w=920:h=180:color=black@0.85:t=fill:enable='between(t,2,8)',"
        f"drawtext=fontfile={font}:text='音声品質をチェック':fontcolor=white:fontsize=52:x=120:y=1410:enable='between(t,2,8)',"
        f"drawtext=fontfile={font}:text='日本語の発話と字幕同期は未確認':fontcolor=yellow:fontsize=36:x=120:y=1490:enable='between(t,2,8)'"
    )
    cmd = ["ffmpeg", "-y", "-i", str(source), "-vf", vf, "-map", "0:v:0", "-map", "0:a:0",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(target)]
    subprocess.run(cmd, check=True)
    return target
