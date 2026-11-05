"""Review-only FFmpeg checkpoint strip; no publication approval implied."""
from pathlib import Path

def checkpoint_filter(font_path: str, start: float = 1.0, end: float = 5.0) -> str:
    if not (0 <= start < end):
        raise ValueError("invalid checkpoint interval")
    if not font_path or "'" in font_path or ":" in font_path:
        raise ValueError("unsafe font path")
    window = f"between(t,{start:g},{end:g})"
    return (
        f"drawbox=x=85:y=1640:w=910:h=170:color=0x101b30@0.94:t=fill:enable='{window}',"
        f"drawbox=x=85:y=1640:w='910*min(max((t-{start:g})/{end-start:g},0),1)':h=10:"
        f"color=0x38bdf8:t=fill:enable='{window}',"
        f"drawtext=fontfile={font_path}:text='目的 → 条件 → 確認':fontcolor=white:"
        f"fontsize=54:x=(w-text_w)/2:y=1690:enable='{window}'"
    )
