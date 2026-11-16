"""Review-only reproducible five-scene renderer. Requires Pillow, ffmpeg and Noto CJK."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SCENES = [
    ("AIの指示で変わる", "依頼は具体的に"),
    ("目的を伝える", "誰に何を届ける？"),
    ("形式を指定", "3項目・表形式など"),
    ("最後は人が確認", "数字と出典をチェック"),
    ("保存して試す", "小さな業務から改善"),
]
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def render(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    clips = []
    for i, (heading, subtitle) in enumerate(SCENES):
        image = Image.new("RGB", (720, 1280), (8, 18, 34))
        d = ImageDraw.Draw(image)
        d.rounded_rectangle((38, 115, 682, 1115), radius=35, fill=(21, 41, 66))
        d.text((75, 174), f"AI 仕事術   /   {i+1:02d}", font=ImageFont.truetype(FONT, 29), fill=(87, 228, 219))
        d.text((72, 385), heading, font=ImageFont.truetype(FONT, 49), fill="white")
        d.rounded_rectangle((63, 812, 657, 958), radius=22, fill=(0, 9, 22))
        d.text((80, 860), subtitle, font=ImageFont.truetype(FONT, 34), fill="white")
        d.rounded_rectangle((72, 1050, 648, 1061), radius=5, fill=(67, 86, 107))
        d.rounded_rectangle((72, 1050, 72+int(576*(i+1)/len(SCENES)), 1061), radius=5, fill=(87, 228, 219))
        d.text((70, 1170), "REVIEW ONLY  |  日本語音声未検証", font=ImageFont.truetype(FONT, 22), fill=(181, 198, 215))
        png = directory / f"frame{i}.png"
        image.save(png)
        clip = directory / f"clip{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "24", "-i", str(png), "-t", "2.5", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip)], check=True)
        clips.append(clip)
    listing = directory / "concat.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in clips), encoding="utf-8")
    out = directory / "cycle1496_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    def stamp(t):
        return f"00:00:{int(t):02d},{round((t%1)*1000):03d}"
    (directory / "captions.srt").write_text("".join(f"{i+1}\n{stamp(i*2.5)} --> {stamp((i+1)*2.5)}\n{s}\n\n" for i, (_, s) in enumerate(SCENES)), encoding="utf-8")
    return out

if __name__ == "__main__":
    print(render(Path(__file__).resolve().parent))
