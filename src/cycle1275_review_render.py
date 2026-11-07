"""Review-only 1080p scene renderer; original synthetic visuals, no external assets."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SCENES = [
    ("AIの回答、\nそのまま送ってない？", "その1クリックが手戻りになる"),
    ("改善前", "「これ、いい感じにまとめて」"),
    ("改善後", "目的・対象・形式を指定する"),
    ("最後は人が確認", "事実・数字・個人情報をチェック"),
]
W, H, FPS, SECONDS = 1080, 1920, 30, 3

def render(output: Path):
    output.mkdir(parents=True, exist_ok=True)
    font = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    clips = []
    for i, (title, subtitle) in enumerate(SCENES):
        im = Image.new("RGB", (W, H), (8, 16, 33))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((58, 115, 1022, 1805), radius=48, fill=(18, 33, 57))
        d.text((110, 420), title, font=ImageFont.truetype(font, 72), fill="white", spacing=24)
        d.text((110, 940), subtitle, font=ImageFont.truetype(font, 39), fill=(200, 235, 244))
        d.text((110, 1660), f"REVIEW ONLY   {i+1}/4", font=ImageFont.truetype(font, 30), fill=(95, 195, 200))
        png = output / f"scene{i}.png"
        mp4 = output / f"clip{i}.mp4"
        im.save(png)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-t", str(SECONDS), "-vf", "zoompan=z='min(zoom+0.0004,1.035)':d=1:s=1080x1920:fps=30,format=yuv420p", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(mp4)], check=True)
        clips.append(mp4)
    concat = output / "concat.txt"
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in clips))
    result = output / "review_only.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(result)], check=True)
    return result

if __name__ == "__main__":
    render(Path("output/cycle1275"))
