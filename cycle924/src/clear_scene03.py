"""cycle924: caption-topic-aligned, readable report preview (scene03 only).

Reimplementation for human review; inherited private source MP4 must never be
uploaded to public GitHub. Does not verify Japanese speech transcript.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
NFRAMES = 691
START, END = 174, 261
SIZE = (1080, 1920)
EDIT_BOTTOM = 1390
CAPTION_START = 1450
STATUS = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# Original, synthetic, non-sensitive examples. Missing entries are NOT imputed.
GENRES = {
    "ai_work": ("月次レポート", "営業A", "営業B", ("4月", "12", "8"), ("5月", "16", "9"), ("6月", "—", "—")),
    "finance": ("家計メモ", "入金", "支出", ("1週", "12", "8"), ("2週", "16", "9"), ("3週", "—", "—")),
    "business": ("案件一覧", "提案", "確認", ("月", "12", "8"), ("火", "16", "9"), ("水", "—", "—")),
    "health": ("習慣の記録", "散歩", "睡眠メモ", ("月", "1", "8"), ("火", "1", "7"), ("水", "—", "—")),
    "education": ("学習記録", "学習分", "復習分", ("月", "12", "8"), ("火", "16", "9"), ("水", "—", "—")),
    "tech": ("検証メモ", "成功", "保留", ("A", "12", "8"), ("B", "16", "9"), ("C", "—", "—")),
    "lifestyle": ("予定メモ", "作業", "休憩", ("月", "12", "8"), ("火", "16", "9"), ("水", "—", "—")),
    "history": ("資料整理", "確認済", "未確認", ("資料A", "12", "8"), ("資料B", "16", "9"), ("資料C", "—", "—")),
    "travel": ("旅程メモ", "訪問", "移動", ("午前", "1", "2"), ("午後", "2", "1"), ("夜", "—", "—")),
    "productivity": ("作業ログ", "実行", "保留", ("月", "12", "8"), ("火", "16", "9"), ("水", "—", "—")),
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def beat(frame: int) -> int:
    if not START <= frame < END:
        raise ValueError("frame outside scene03")
    return min(2, (frame - START) // 29)

def validate(genre: str, output: Path, frames: int = NFRAMES) -> None:
    if genre not in GENRES:
        raise ValueError("unsupported genre")
    if not output.name.endswith("_REVIEW_ONLY.mp4"):
        raise ValueError("review-only output required")
    if frames != NFRAMES or not (0 < START < END <= frames):
        raise ValueError("unexpected geometry")
    if any("—" not in (v[5][1], v[5][2]) for v in GENRES.values()):
        raise ValueError("missing values must remain missing")

def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def draw_scene(frame: Image.Image, frame_index: int, genre: str = "ai_work") -> Image.Image:
    """Composite only the editorial image region; caption/footer y>=1450 untouched."""
    if not START <= frame_index < END:
        return frame
    if frame.size != SIZE:
        raise ValueError("1080x1920 expected")
    if genre not in GENRES:
        raise ValueError("unsupported genre")
    out = frame.copy().convert("RGB")
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay, "RGBA")
    # Opaque editorial panel suppresses unreadable, previously layered text.
    d.rounded_rectangle((48, 130, 1032, 1390), radius=38, fill=(5, 19, 37, 255), outline=(43, 188, 210, 255), width=4)
    d.rounded_rectangle((84, 166, 996, 322), radius=24, fill=(14, 56, 77, 255))
    d.text((112, 185), "完成形の見本を先に用意", font=font(54, True), fill=(255, 255, 255, 255))
    d.text((116, 268), "架空のサンプル / 数値は例示です", font=font(27), fill=(164, 224, 232, 255))
    active = beat(frame_index)
    labels = ("① 見本", "② 表にする", "③ 空欄確認")
    for i, label in enumerate(labels):
        x0 = 88 + i * 310
        d.rounded_rectangle((x0, 343, x0 + 292, 423), radius=20,
                            fill=(29, 177, 181, 255) if i == active else (24, 49, 65, 255),
                            outline=(65, 223, 228, 255) if i == active else (55, 85, 100, 255), width=3)
        d.text((x0 + 20, 360), label, font=font(32, True), fill=(255, 255, 255, 255))
    # Floating paper/report with layered depth and restrained motion.
    phase = (frame_index - START) / (END - START)
    dy = round(6 * math.sin(phase * 2 * math.pi))
    paper_top = 468 + dy
    d.rounded_rectangle((116, paper_top + 24, 980, 1142 + dy), radius=31, fill=(3, 12, 23, 185))
    d.rounded_rectangle((99, paper_top, 963, 1118 + dy), radius=30, fill=(243, 250, 252, 255))
    title, c1, c2, r1, r2, r3 = GENRES[genre]
    d.text((148, paper_top + 35), title, font=font(54, True), fill=(13, 40, 59, 255))
    d.text((150, paper_top + 118), "OUTPUT PREVIEW  /  DEMO", font=font(24, True), fill=(51, 110, 127, 255))
    cols = [149, 392, 642, 839]
    yy = paper_top + 205
    d.rounded_rectangle((135, yy, 927, yy + 94), radius=16, fill=(18, 78, 106, 255))
    for x, txt in zip(cols, ("期間", c1, c2, "状態")):
        d.text((x, yy + 20), txt, font=font(32, True), fill=(255, 255, 255, 255))
    for i, row in enumerate((r1, r2, r3)):
        y = yy + 113 + i * 105
        if i <= active:
            d.rounded_rectangle((135, y, 927, y + 96), radius=12,
                                fill=(234, 245, 249, 255) if i % 2 == 0 else (220, 239, 244, 255))
            values = (row[0], row[1], row[2], "要確認" if i == 2 else "確認済")
            for j, (x, val) in enumerate(zip(cols, values)):
                color = (184, 83, 18, 255) if i == 2 and j > 0 else (20, 56, 71, 255)
                d.text((x, y + 20), val, font=font(34, True), fill=color)
        else:
            d.rounded_rectangle((135, y, 927, y + 96), radius=12, fill=(232, 237, 240, 255))
            d.text((150, y + 22), "次の行を表示", font=font(30), fill=(132, 151, 161, 255))
    # Fixed, readable takeaway with explicit no-imputation rule.
    d.rounded_rectangle((112, 1184, 967, 1345), radius=25,
                        fill=(96, 49, 23, 255) if active == 2 else (12, 80, 103, 255),
                        outline=(244, 164, 75, 255) if active == 2 else (55, 207, 220, 255), width=3)
    d.text((145, 1201), "空欄は推測で埋めない" if active == 2 else "必要な項目を見える形に", font=font(49, True), fill=(255, 255, 255, 255))
    d.text((147, 1274), "未入力の値は、確認してから反映" if active == 2 else "出力例を先に決めてからAIへ指示", font=font(28), fill=(245, 229, 208, 255))
    # Crucially no overlay pixels below EDIT_BOTTOM.
    out.paste(overlay, (0, 0), overlay)
    return out

def render(source: Path, output: Path, report: Path, genre: str = "ai_work"):
    import cv2
    import numpy as np
    validate(genre, output)
    if not source.is_file():
        raise FileNotFoundError(source)
    cap = cv2.VideoCapture(str(source))
    props = [cap.get(p) for p in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FRAME_COUNT, cv2.CAP_PROP_FPS)]
    if tuple(map(int, props[:3])) != (1080, 1920, NFRAMES) or round(props[3]) != FPS:
        cap.release()
        raise ValueError(f"unexpected source {props}")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "pipe:0", "-i", str(source), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(output)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(NFRAMES):
            ok, fr = cap.read()
            if not ok:
                raise RuntimeError(f"early source EOF {i}")
            if START <= i < END:
                im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
                fr = cv2.cvtColor(np.asarray(draw_scene(im, i, genre)), cv2.COLOR_RGB2BGR)
            proc.stdin.write(fr.tobytes())
    finally:
        cap.release()
        if proc.stdin:
            proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg render failed")
    obj = {"cycle": 924, "genre": genre, "status": STATUS, "source_sha256": sha256(source), "output_sha256": sha256(output), "changed_scene": 3, "frame_range": [START, END-1], "improvement": "Replace cluttered chart with readable fictional report preview and three-step staged reveal", "caption_region": "Inherited lower band y>=1450 not deliberately edited; lossy reencode may change pixels", "japanese_asr": "NOT_VERIFIED", "reference_v33": "UNAVAILABLE", "publication_approved": False, "automatic_posting": False}
    report.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return obj

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--genre", choices=tuple(GENRES), default="ai_work")
    args = p.parse_args()
    print(json.dumps(render(args.source, args.output, args.report, args.genre), ensure_ascii=False))

if __name__ == "__main__":
    main()
