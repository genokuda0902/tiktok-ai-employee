"""Mobile-safe Japanese ASS subtitle sizing for 10 genres (internal review only).

The module never changes wording/timing and does not claim speech recognition.
"""
from pathlib import Path
import re

TARGET_FONT = 71
MIN_FONT = 66
MAX_INNER_WIDTH = 930
OUTLINE_PX = 4
GENRES = ('ai_productivity', 'beauty', 'romance_psychology', 'money_saving',
          'sales_business', 'career', 'health_lifestyle', 'trivia_science',
          'travel_food', 'product_lifestyle')

def text_without_ass_tags(value):
    return re.sub(r'\{[^}]*\}', '', value).replace('\\N', '\n')

def select_font_size(lines, measure, max_size=TARGET_FONT,
                     min_size=MIN_FONT, available=MAX_INNER_WIDTH):
    if not lines or not any(line.strip() for line in lines):
        raise ValueError('empty subtitle')
    for size in range(max_size, min_size - 1, -1):
        if max(measure(line, size) for line in lines) + 2 * OUTLINE_PX <= available:
            return size
    raise ValueError('caption overflows safe card even at minimum font')

def upgrade_ass(source, target, measure, genre='ai_productivity'):
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    src = Path(source).read_text(encoding='utf-8')
    result, decisions = [], []
    for line in src.splitlines():
        if not line.startswith('Dialogue:'):
            result.append(line)
            continue
        parts = line.split(',', 9)
        if len(parts) != 10:
            raise ValueError('malformed ASS dialogue')
        readable = text_without_ass_tags(parts[9])
        size = select_font_size(readable.split('\n'), measure)
        parts[9] = '{\\fs%d}' % size + parts[9]
        result.append(','.join(parts))
        decisions.append({'start': parts[1], 'end': parts[2],
                          'font_size': size, 'text': readable})
    if len(decisions) != 24:
        raise ValueError('expected 24 inherited caption cues')
    Path(target).write_text('\n'.join(result) + '\n', encoding='utf-8')
    return decisions

def validate_reading_groups(decisions):
    """Group identical contiguous karaoke subcues as one full sentence."""
    def seconds(t):
        h, m, s = t.split(':')
        return int(h)*3600 + int(m)*60 + float(s)
    groups = []
    for d in decisions:
        if groups and groups[-1]['text'] == d['text'] and abs(seconds(d['start']) - groups[-1]['end']) < .021:
            groups[-1]['end'] = seconds(d['end'])
        else:
            groups.append({'text': d['text'], 'start': seconds(d['start']), 'end': seconds(d['end'])})
    for g in groups:
        g['chars_per_second'] = round(len(g['text'].replace('\n', ''))/(g['end']-g['start']), 2)
    return groups
