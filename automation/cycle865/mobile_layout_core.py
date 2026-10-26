"""Cycle865: reusable 10-genre mobile-readable browser-overlay rules.
Pure Python; no network calls, posting, payments or personal data.
"""
from dataclasses import dataclass

PALETTES = {
    "ai_productivity": "#28D7BE",
    "career": "#FFBB68",
    "money": "#82DBAA",
    "health": "#87CFFB",
    "learning": "#BEA7FF",
    "beauty": "#F4A4C5",
    "travel": "#78C6FA",
    "food": "#F6B778",
    "home": "#A5DC8E",
    "business": "#82A9FF",
}

@dataclass(frozen=True)
class MobileLayout:
    video_width: int = 1080
    video_height: int = 1920
    browser_width: int = 900
    browser_height: int = 960
    browser_x: int = 90
    browser_y: int = 350
    caption_top: int = 1360
    caption_bottom: int = 1505
    protected_bottom_start: int = 1600

    def validate(self):
        assert self.browser_width > 0 and self.browser_height > 0
        assert 0 <= self.browser_x <= self.video_width - self.browser_width
        assert 0 <= self.browser_y <= self.video_height - self.browser_height
        assert self.browser_y + self.browser_height < self.caption_top
        assert self.caption_top < self.caption_bottom < self.protected_bottom_start
        return True

def palette_for(genre: str) -> str:
    if genre not in PALETTES:
        raise ValueError("unsupported genre")
    return PALETTES[genre]

def completed_progress(tasks: list[bool]) -> dict:
    if len(tasks) != 4 or any(type(t) is not bool for t in tasks):
        raise ValueError("four synthetic boolean task states required")
    count = sum(tasks)
    return {"done": count, "total": 4, "pending": 4 - count, "percent": count * 25}

def report_text(progress: dict, conclusion_first: bool = False) -> str:
    summary = f"今週の進捗は4件中{progress['done']}件完了、達成率{progress['percent']}%です。"
    followup = f"未完了{progress['pending']}件は明日確認します。"
    return summary + "\n" + followup if conclusion_first else followup + "\n" + summary

def browser_area_growth_percent(previous_height: int = 450) -> float:
    if previous_height <= 0:
        raise ValueError("height must be positive")
    return round((MobileLayout().browser_height / previous_height - 1) * 100, 1)
