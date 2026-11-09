"""Self-contained review-only 5-scene video. No private assets or posting."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SCENES = [
    ("売上合計、まだ手計算？", "ExcelのSUM関数で3秒チェック"),
    ("架空の売上データ", "月曜 12,000円 / 火曜 18,000円 / 水曜 15,000円"),
    ("セルに式を入力", "＝SUM(B2:B4)"),
    ("合計が自動で出る", "45,000円"),
    ("実務では必ず確認", "参照範囲と数字をチェック"),
]
def render(out: Path, font_path: str):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    clips = []
    for i, (heading, body) in enumerate(SCENES):
        img = Image.new("RGB", (1080, 1920), "#0b1323")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, 52)
        draw.rounded_rectangle((70, 250, 1010, 1550), radius=32, fill="#18273d")
        draw.text((110, 360), heading, font=font, fill="white")
        draw.text((110, 660), body, font=ImageFont.truetype(font_path, 38), fill="#9ae8e0")
        draw.text((110, 1720), "REVIEW ONLY / 架空データ / 投稿未承認", font=ImageFont.truetype(font_path, 27), fill="#ffc7c7")
        png = out.parent / f"scene_{i}.png"
        clip = out.parent / f"scene_{i}.mp4"
        img.save(png)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", "3", "-i", str(png), "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(clip)], check=True)
        clips.append(clip)
    playlist = out.parent / "concat.txt"
    playlist.write_text("".join(f"file '{p.resolve()}'\n" for p in clips))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(playlist), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    return out

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--font", required=True)
    args = parser.parse_args()
    render(args.out, args.font)
