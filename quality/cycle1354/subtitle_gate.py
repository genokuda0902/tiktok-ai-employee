"""Fail-closed checks for timed Japanese subtitles (review-only)."""
from pathlib import Path
import re

def validate_srt(path: str, expected_scenes: int = 4) -> bool:
    text = Path(path).read_text(encoding="utf-8-sig")
    blocks = [x.strip() for x in re.split(r"\n\s*\n", text) if x.strip()]
    if len(blocks) != expected_scenes:
        return False
    previous_end = -1
    for index, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3 or lines[0] != str(index):
            return False
        match = re.fullmatch(r"(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})", lines[1])
        if not match or not any(re.search(r"[ぁ-んァ-ン一-龥]", x) for x in lines[2:]):
            return False
        values = [int(x) for x in match.groups()]
        start = ((values[0]*60+values[1])*60+values[2])*1000+values[3]
        end = ((values[4]*60+values[5])*60+values[6])*1000+values[7]
        if start < previous_end or end <= start:
            return False
        previous_end = end
    return True
