"""Validate timed caption boundaries for a review-only video."""
import re
from pathlib import Path

def validate_srt(path, expected_seconds=12):
    text = Path(path).read_text(encoding="utf-8")
    ranges = re.findall(r"(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})", text)
    if not ranges:
        raise ValueError("no captions")
    def ms(t):
        h,m,s=t.replace(",",":").split(":")
        return ((int(h)*60+int(m))*60+int(s))*1000+int(t[-3:])
    previous=0
    for start,end in ranges:
        a,b=ms(start),ms(end)
        if a != previous or b <= a:
            raise ValueError("caption gap, overlap, or invalid interval")
        previous=b
    if previous != expected_seconds*1000:
        raise ValueError("caption coverage does not match video duration")
    return len(ranges)
