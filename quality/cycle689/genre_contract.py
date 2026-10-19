"""Cycle689 reusable 10-genre / Japanese caption contract. No publication actions."""
GENRES = ("ai_work", "beauty", "love_psychology", "saving", "sales_business",
          "career", "health", "science", "travel_food", "product_comparison")
WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_LINES = (
 ("これ、ただの基板じゃ", "ありません。"),
 ("小さくても、", "パソコンとして動きます。"),
 ("モニターにつなげば、", "画面で操作できます。"),
 ("電源と周辺機器を", "つないで、準備します。"),
 ("LEDを光らせる", "工作にも使えます。"),
 ("入力して、処理して、", "結果を出す。"),
 ("最初は、小さな作品から", "始めましょう。"),
 ("保存して、", "あとで試そう。"),
)

def validate_timeline(timeline):
    if len(timeline) != 8:
        raise ValueError("eight scenes required")
    end = 0.0
    for i, scene in enumerate(timeline):
        if scene["scene"] != i + 1 or abs(scene["start"] - end) > .02:
            raise ValueError("gap or wrong scene order")
        end = scene["end"]
        if round((scene["end"] - scene["start"]) * FPS) <= 0:
            raise ValueError("zero-length scene")
        if i < 7 and "".join(CAPTION_LINES[i]) != scene["spoken_text"]:
            raise ValueError("caption script mismatch")
        if i == 7 and scene["spoken_text"]:
            raise ValueError("CTA must be silent")
    if abs(end - 15.6) > .02:
        raise ValueError("unexpected duration")
    return True
