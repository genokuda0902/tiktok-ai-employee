"""Review-only 3-scene Japanese storyboard. Requires Pillow and ffmpeg."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SCENES = [
    ("01 / PROBLEM", "AIの回答、そのまま使う？", "確認せずに貼るとミスが残る"),
    ("02 / ACTION", "3つだけチェック", "数字・出典・個人情報"),
    ("03 / RESULT", "最後は人が判断", "便利さと正確さを両立する"),
]
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def render(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    clips = []
    for i, (eyebrow, title, body) in enumerate(SCENES):
        im = Image.new("RGB", (1080, 1920), "#081525")
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((68, 280, 1012, 1590), radius=45, fill="#10283c")
        d.rounded_rectangle((105, 360, 975, 372), radius=6, fill="#35dbbd")
        d.text((110, 455), eyebrow, font=ImageFont.truetype(FONT, 40), fill="#35dbbd")
        d.text((110, 620), title, font=ImageFont.truetype(FONT, 62), fill="white")
        d.text((110, 810), body, font=ImageFont.truetype(FONT, 41), fill="#cbd5e1")
        for j in range(3):
            d.rounded_rectangle((110+j*295, 1320, 375+j*295, 1336), radius=7, fill="#35dbbd" if j <= i else "#40566b")
        d.text((110, 1470), "REVIEW ONLY  /  未承認・投稿禁止", font=ImageFont.truetype(FONT, 27), fill="#a3b4c5")
        png = out / f"scene{i}.png"
        im.save(png)
        clip = out / f"clip{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(png), "-t", "5", "-vf", "scale=1080:1920,format=yuv420p", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24", "-r", "30", str(clip)], check=True)
        clips.append(clip)
    (out / "concat.txt").write_text("".join(f"file '{p.name}'\n" for p in clips))
    video = out / "cycle1266_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(out / "concat.txt"), "-c", "copy", "-movflags", "+faststart", str(video)], check=True)
    def ts(s): return f"00:00:{s:02d},000"
    (out / "captions.srt").write_text("".join(f"{i+1}\n{ts(i*5)} --> {ts((i+1)*5)}\n{title}\n\n" for i, (_, title, _) in enumerate(SCENES)), encoding="utf8")
    return video

if __name__ == "__main__":
    print(render(Path("output/cycle1266")))
