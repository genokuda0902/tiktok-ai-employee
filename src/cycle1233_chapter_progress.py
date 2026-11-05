"""Review-only chapter timeline overlay for 10 genres. Does not certify speech/subtitle sync."""
def chapter_at(t: float) -> str:
    if t < 0: raise ValueError("negative timestamp")
    return "導入" if t < 7 else ("確認ポイント" if t < 16 else "まとめ")

def progress(t: float, duration: float) -> float:
    if duration <= 0: raise ValueError("duration must be positive")
    return max(0.0, min(1.0, t / duration))

def ffmpeg_filter(duration: float = 23.033) -> str:
    if duration <= 0: raise ValueError("duration must be positive")
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    return (
        "drawbox=x=80:y=1770:w=920:h=8:color=white@0.25:t=fill,"
        f"drawbox=x=80:y=1770:w='920*min(t/{duration},1)':h=8:color=0x4ee6c2@0.95:t=fill,"
        f"drawtext=fontfile={font}:text='導入':fontcolor=white:fontsize=27:x=85:y=1800:enable='between(t,0,7)',"
        f"drawtext=fontfile={font}:text='確認ポイント':fontcolor=white:fontsize=27:x=85:y=1800:enable='between(t,7,16)',"
        f"drawtext=fontfile={font}:text='まとめ':fontcolor=white:fontsize=27:x=85:y=1800:enable='gte(t,16)'"
    )
