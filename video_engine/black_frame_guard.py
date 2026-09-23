"""Fail-closed visual regression guard for image-slide delivery masters.

Zero-cost helper: parses FFmpeg blackdetect output and rejects accidental
long black segments before human review. It never posts or approves content.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_BLACK = re.compile(r"black_start:(?P<start>[0-9.]+)\s+black_end:(?P<end>[0-9.]+)\s+black_duration:(?P<duration>[0-9.]+)")

@dataclass(frozen=True)
class BlackSegment:
    start: float
    end: float
    duration: float


def parse_blackdetect(log_text: str) -> list[BlackSegment]:
    return [BlackSegment(float(m['start']), float(m['end']), float(m['duration'])) for m in _BLACK.finditer(log_text)]


def assert_no_long_black(log_text: str, *, max_seconds: float = 0.50) -> None:
    """Reject any detected black segment longer than max_seconds.

    A short transition may be intentional; sustained black frames are not
    acceptable for the image-slide route. Human rights/quality approval is
    still required after this technical check.
    """
    if max_seconds <= 0:
        raise ValueError('max_seconds must be positive')
    bad = [s for s in parse_blackdetect(log_text) if s.duration > max_seconds]
    if bad:
        worst = max(bad, key=lambda s: s.duration)
        raise ValueError(f'long black segment detected: {worst.start:.3f}-{worst.end:.3f}s ({worst.duration:.3f}s)')
