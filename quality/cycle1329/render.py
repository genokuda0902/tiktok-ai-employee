"""Review-only, synthetic 4-scene MP4; no narration and not publishable."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

def render(out: Path):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    font = next(p for p in ["/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"] if Path(p).exists())
    scenes = [("売上集計、まだ手作業？", "3ステップで確認"), ("STEP 1", "集計する範囲を選ぶ"), ("STEP 2", "=SUM(B2:B5) を入力"), ("STEP 3", "合計を確認して完了")]
    for i, (heading, sub) in enumerate(scenes):
        im = Image.new("RGB", (720, 1280), "#0b1424")
        d = ImageDraw.Draw(im)
        f = lambda n: ImageFont.truetype(font, n)
        d.rounded_rectangle((45, 180, 675, 1030), radius=24, fill="#17263a")
        d.text((72, 70), "EXCEL / 仕事効率化", font=f(32), fill="#6ee7db")
        d.text((72, 245), heading, font=f(44), fill="white")
        for j, (name, value) in enumerate([("商品A", "120"), ("商品B", "180"), ("商品C", "250"), ("商品D", "150")]):
            y = 390 + j * 96
            d.rounded_rectangle((85, y, 635, y + 78), radius=8, fill="#26405b" if j == i % 4 else "#1d3148")
            d.text((110, y + 14), name, font=f(30), fill="white")
            d.text((490, y + 14), value, font=f(30), fill="#bce5ff")
        d.text((80, 850), sub, font=f(32), fill="#ffdf90")
        d.rectangle((70, 1100, 650, 1114), fill="#30465d")
        d.rectangle((70, 1100, 70 + (i + 1) * 145, 1114), fill="#6ee7db")
        d.text((70, 1160), "架空データ / レビュー専用", font=f(24), fill="#9daec2")
        im.save(out.parent / f"frame{i}.png")
    manifest = out.parent / "concat.txt"
    manifest.write_text("".join(f"file 'frame{i}.png'\\nduration 3\\n" for i in range(4)) + "file 'frame3.png'\\n".replace("\\n", "\n").replace("duration 3\\n", "duration 3\n"), encoding="utf-8")
    # Normalize escaped manifest sequences.
    manifest.write_text(manifest.read_text().replace("\\n", "\n"), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(manifest), "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22", "-movflags", "+faststart", str(out)], check=True)
    return out

if __name__ == "__main__":
    render(Path("cycle1329_REVIEW_ONLY.mp4"))
