"""Cycle700 reusable Japanese caption contract (no network or posting)."""
from __future__ import annotations
SCENE_FRAMES=(60,60,60,60,60,60,54,54)
FPS=30
SIZE=(1080,1920)
CAPTION_BAND=(1300,1530)
GENRE_COLORS={
    "ai_work":"#42E4D7","beauty":"#FF92C9","love_psychology":"#FFB3D4",
    "saving":"#86E7A9","sales_business":"#65D0F9","career":"#A9BDFF",
    "health":"#80E7C1","science":"#4BE7D6","travel_food":"#FFC477",
    "product_comparison":"#C4ACFF",
}
CAPTIONS=(
    ("これ、実は小さなパソコン。","基板１枚に機能がぎゅっと。"),
    ("手のひらサイズなのに、","中身は本格的なパソコン。"),
    ("画面と入力機器をつなげば、","操作できるようになる。"),
    ("電源・画面・入力の３つ。","つないで準備を整えよう。"),
    ("LEDを光らせることも。","電子工作の第一歩に。"),
    ("入力された情報を処理して、","結果を出力する。"),
    ("最初は１行のコードから。","小さな成功を積み重ねよう。"),
    ("今日の３ステップを復習。","保存して、あとで試そう。"),
)
def scene_at(frame:int)->int:
    """Map 0-based frame to 0-based scene without off-by-one errors."""
    if not 0 <= frame < sum(SCENE_FRAMES):
        raise ValueError("frame outside video")
    offset=0
    for scene,count in enumerate(SCENE_FRAMES):
        if frame < offset+count:
            return scene
        offset+=count
    raise AssertionError("unreachable")
def validate()->bool:
    assert len(CAPTIONS)==len(SCENE_FRAMES)==8
    assert all(len(pair)==2 and all(line.strip() for line in pair) for pair in CAPTIONS)
    assert len(GENRE_COLORS)==10
    assert sum(SCENE_FRAMES)==468
    assert 1200<=CAPTION_BAND[0]<CAPTION_BAND[1]<=1536
    return True
# These are explanatory scene captions, NOT verified speech transcription.
# Source AAC narration remains unchanged; rights/approval must be reviewed.
