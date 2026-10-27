"""Offline pause-aware Japanese subtitle retiming; no ASR, network, or posting.

This component only suppresses inherited caption display during measured silent
intervals. It does not verify Japanese pronunciation or semantic correctness.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from pathlib import Path
import re

GENRES = ('AI時短', '雑学', '料理', '美容', 'お金', '健康', '旅行', '商品', 'ストーリー', '仕事術')
DURATION = 23.033333

@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str


def parse_time(s: str) -> float:
    h, m, sec = s.split(':')
    return int(h) * 3600 + int(m) * 60 + float(sec)


def ass_time(t: float) -> str:
    centis = max(0, round(t * 100))
    return f'{centis // 360000}:{centis // 6000 % 60:02d}:{centis // 100 % 60:02d}.{centis % 100:02d}'


def parse_ass(source: str) -> tuple[str, list[Caption]]:
    head, sep, tail = source.partition('[Events]')
    if not sep:
        raise ValueError('missing ASS events')
    lines = tail.splitlines()
    events = []
    for line in lines:
        if line.startswith('Dialogue:'):
            parts = line[len('Dialogue:'):].strip().split(',', 9)
            if len(parts) != 10:
                raise ValueError('invalid ASS dialogue')
            events.append(Caption(parse_time(parts[1]), parse_time(parts[2]), parts[9]))
    if not events:
        raise ValueError('no captions')
    return head + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n', events


def parse_silences(log: str, duration: float) -> list[tuple[float, float]]:
    starts = [float(v) for v in re.findall(r'silence_start:\s*([0-9.]+)', log)]
    ends = [float(v) for v in re.findall(r'silence_end:\s*([0-9.]+)', log)]
    if len(starts) != len(ends):
        raise ValueError('unpaired silence intervals')
    ranges = sorted((max(0., s), min(duration, e)) for s, e in zip(starts, ends))
    if any(e <= s or (i and s < ranges[i-1][1]) for i, (s, e) in enumerate(ranges)):
        raise ValueError('invalid silence intervals')
    return ranges


def voice_ranges(silences: list[tuple[float, float]], duration: float, lead: float = .045, tail: float = .07) -> list[tuple[float, float]]:
    voice, prev = [], 0.
    for s, e in silences:
        if s > prev:
            voice.append((max(0., prev - lead), min(duration, s + tail)))
        prev = e
    if prev < duration:
        voice.append((max(0., prev - lead), duration))
    merged = []
    for s, e in voice:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def retime(events: list[Caption], silences: list[tuple[float, float]], duration: float, min_visible: float = .14) -> list[Caption]:
    active = voice_ranges(silences, duration)
    result = []
    for event in events:
        if not 0 <= event.start < event.end <= duration + .05:
            raise ValueError('caption out of bounds')
        for s, e in active:
            start, end = max(event.start, s), min(event.end, e)
            if end - start >= min_visible:
                result.append(replace(event, start=start, end=end))
    return result


def overlap_duration(events: list[Caption], ranges: list[tuple[float, float]]) -> float:
    return sum(max(0., min(c.end, e) - max(c.start, s)) for c in events for s, e in ranges)


def write_ass(path: Path, header: str, events: list[Caption]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [header]
    for e in events:
        text = r'{\fad(35,45)}' + e.text
        lines.append(f'Dialogue: 0,{ass_time(e.start)},{ass_time(e.end)},JP,,0,0,0,,{text}\n')
    path.write_text(''.join(lines), encoding='utf-8')


def build(source_ass: Path, silence_log: Path, destination_ass: Path, duration: float = DURATION) -> dict:
    header, original = parse_ass(Path(source_ass).read_text(encoding='utf-8'))
    silences = parse_silences(Path(silence_log).read_text(encoding='utf-8'), duration)
    updated = retime(original, silences, duration)
    if not updated:
        raise ValueError('retiming would remove all captions')
    write_ass(destination_ass, header, updated)
    return {'original_intervals': len(original), 'retimed_intervals': len(updated),
            'silence_intervals': len(silences), 'original_silence_overlap_seconds': round(overlap_duration(original, silences), 3),
            'new_silence_overlap_seconds': round(overlap_duration(updated, silences), 3),
            'caption_text_preserved': all(any(c.text == o.text for c in updated) for o in original),
            'genre_templates': list(GENRES), 'semantic_asr_verified': False}
