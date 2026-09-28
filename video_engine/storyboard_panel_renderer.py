from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Panel:
    index: int
    caption: str
    duration: float

DEFAULT_PANELS = (
    Panel(1, 'まだ手作業ですか？', 2.117),
    Panel(3, 'AIにデータを渡す', 2.117),
    Panel(4, 'あとは自動で分析', 2.117),
    Panel(5, '数秒で結果が完成', 2.117),
    Panel(8, '数時間が数分に', 2.117),
    Panel(11, '保存してあとで試して', 2.121),
)

def validate_panels(panels: Sequence[Panel], cols=3, rows=4):
    if not panels:
        raise ValueError('panels required')
    seen = set()
    for panel in panels:
        if not 1 <= panel.index <= cols * rows:
            raise ValueError('panel index out of range')
        if panel.index in seen:
            raise ValueError('duplicate panel')
        if not panel.caption.strip():
            raise ValueError('caption required')
        if panel.duration <= 0:
            raise ValueError('positive duration required')
        seen.add(panel.index)
    return True

def crop_box(width: int, height: int, index: int, cols=3, rows=4):
    if index < 1 or index > cols * rows:
        raise ValueError('panel index out of range')
    col = (index - 1) % cols
    row = (index - 1) // cols
    return (
        round(col * width / cols), round(row * height / rows),
        round((col + 1) * width / cols), round((row + 1) * height / rows),
    )
