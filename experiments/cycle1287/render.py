"""Synthetic review-only TikTok demo. Requires Pillow, FFmpeg, Noto CJK fonts."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

OUT = Path("output/cycle1287")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES = [
    ("AIの回答、そのまま使う？", "まずは出典を確認", "SOURCE"),
    ("いつの情報かチェック", "更新日が古い場合も", "DATE"),
    ("数字は元資料と照合", "見落としを防ぐ", "VERIFY"),
    ("最後は人が判断する", "AIは補助ツール", "REVIEW"),
]

def render():
    for i, (heading, subtitle, tag) in enumerate(SCENES):
        im = Image.new("RGB", (720, 1280), (9, 18, 36))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((45,130,675,1100), radius=35, fill=(20,38,65), outline=(53,112,158), width=3)
        d.rounded_rectangle((82,190,638,272), radius=18, fill=(23,91,126))
        d.text((108,205), tag, font=ImageFont.truetype(BOLD,37), fill="white")
        d.text((82,365), heading, font=ImageFont.truetype(BOLD,38), fill="white")
        d.rounded_rectangle((85,555,635,850), radius=22, fill=(29,53,78))
        for j, item in enumerate(["情報の出典", "更新された日付", "数字の根拠"]):
            y=600+j*80
            d.ellipse((112,y,146,y+34), fill=(44,186,172) if j<=i else (90,110,129))
            d.text((168,y-5), item, font=ImageFont.truetype(FONT,31), fill="white")
        d.rounded_rectangle((75,948,645,1050), radius=18, fill=(4,11,25))
        d.text((96,963), subtitle, font=ImageFont.truetype(BOLD,31), fill="white")
        d.text((70,1160), f"REVIEW ONLY  •  {i+1}/4", font=ImageFont.truetype(FONT,23), fill=(153,194,211))
        im.save(OUT / f"frame{i}.png")
    with (OUT / "concat.txt").open("w") as f:
        for i in range(4):
            f.write(f"file 'frame{i}.png'\\nduration 3\\n".replace("\\n", "\n"))
        f.write("file 'frame3.png'\n")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(OUT/"concat.txt"),"-t","12","-vf","fps=24,format=yuv420p","-c:v","libx264","-preset","veryfast","-movflags","+faststart","-an",str(OUT/"cycle1287_REVIEW_ONLY.mp4")], check=True)

if __name__ == "__main__":
    render()
