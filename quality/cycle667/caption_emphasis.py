"""Script-preserving Japanese semantic caption layout; no ASR/forced-alignment claims."""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Span:
    text: str
    emphasized: bool

def semantic_spans(script: str, term: str) -> list[Span]:
    if not script or not term or term not in script:
        raise ValueError("Highlight must occur in spoken script")
    before, after = script.split(term, 1)
    result = []
    if before:
        result.append(Span(before, False))
    result.append(Span(term, True))
    if after:
        result.append(Span(after, False))
    return result

def wrap_spans(spans: Sequence[Span], measure, max_width: float) -> list[list[Span]]:
    lines: list[list[Span]] = [[]]
    current = ""
    def add(text, emphasis):
        nonlocal current
        if not text:
            return
        if lines[-1] and lines[-1][-1].emphasized == emphasis:
            old = lines[-1][-1]
            lines[-1][-1] = Span(old.text + text, emphasis)
        else:
            lines[-1].append(Span(text, emphasis))
        current += text
    for span in spans:
        if span.emphasized:
            if measure(span.text) > max_width:
                raise ValueError("Emphasized phrase too wide")
            if current and measure(current + span.text) > max_width:
                lines.append([])
                current = ""
            add(span.text, True)
        else:
            for ch in span.text:
                if current and measure(current + ch) > max_width and ch not in "、。！？":
                    lines.append([])
                    current = ""
                add(ch, False)
    return [line for line in lines if line]

def contrast_ratio(rgb1, rgb2):
    def luminance(rgb):
        v = [((c / 255 + 0.055) / 1.055) ** 2.4 if c / 255 > 0.04045 else c / 255 / 12.92 for c in rgb]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = sorted((luminance(rgb1), luminance(rgb2)), reverse=True)
    return (a + 0.05) / (b + 0.05)
