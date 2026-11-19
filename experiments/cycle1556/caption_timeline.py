"""Review-only caption timeline. No narration or publication approval is implied."""
from pathlib import Path
STEPS = [
    ("合計を出す", "合計セルを選択"),
    ("関数を入力", "=SUM(B2:B5)"),
    ("範囲を確認", "B2 から B5 を選択"),
    ("結果を表示", "合計 10,000 円"),
]
STEP_SECONDS = 3
def srt_timestamp(seconds):
    return f"00:{seconds // 60:02d}:{seconds % 60:02d},000"
def build_srt(steps=STEPS):
    blocks = []
    for i, (title, detail) in enumerate(steps):
        blocks.append(f"{i+1}\n{srt_timestamp(i*STEP_SECONDS)} --> {srt_timestamp((i+1)*STEP_SECONDS)}\n{title}。{detail}\n")
    return "\n".join(blocks)
def write_srt(path):
    Path(path).write_text(build_srt(), encoding="utf-8")
if __name__ == "__main__":
    write_srt(Path(__file__).with_name("captions_ja.srt"))
