"""Reusable ten-genre visual cause/effect specification (cycle 673).

This is an illustration contract, not a GPIO execution claim.
Full offline PIL/ffmpeg renderer and reproducible MP4 are included in the
cycle673 downloadable source bundle; no publishing is performed here.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class CauseEffect:
    genre: str
    title: str
    command: str
    result: str
    disclaimer: str = "動作イメージ / 実機検証ではありません"

_PRESETS = {
    "science": ("FIRST PROJECT", "led = True", "LED ON"),
    "ai_tools": ("AI TOOL DEMO", "summary = True", "要約 完了"),
    "work": ("WORKFLOW DEMO", "done = True", "完了"),
    "money": ("BUDGET DEMO", "balanced = True", "確認 OK"),
    "health": ("HABIT DEMO", "logged = True", "記録 完了"),
    "history": ("TIMELINE DEMO", "opened = True", "年表 表示"),
    "language": ("LANGUAGE DEMO", "ready = True", "準備 OK"),
    "travel": ("TRAVEL DEMO", "route = True", "経路 表示"),
    "cooking": ("RECIPE DEMO", "scaled = True", "分量 計算"),
    "lifehacks": ("LIFEHACK DEMO", "applied = True", "設定 OK"),
}

def genres():
    return tuple(_PRESETS)

def storyboard(genre: str):
    if genre not in _PRESETS:
        raise ValueError("Unknown genre: " + genre)
    return CauseEffect(genre, *_PRESETS[genre])

def reveal_progress(t: float):
    """Text typing 0.12–0.75 s, then visual state transition 0.86–1.22 s."""
    typed = max(0.0, min(1.0, (t - 0.12) / 0.63))
    light = max(0.0, min(1.0, (t - 0.86) / 0.36))
    return typed, light

def validate(p: CauseEffect):
    assert p.disclaimer and "実機検証ではありません" in p.disclaimer
    assert p.command and p.result and p.title
    return True
