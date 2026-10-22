"""Ten-genre, review-only Japanese caption layout. No third-party assets."""
import re

GENRES = {
    'ai_work': '&H00DDF44E', 'romance': '&H00C086FF',
    'beauty': '&H00FFA6CB', 'money': '&H00A9E984',
    'trivia': '&H0073CBFF', 'gadgets': '&H00FFB87C',
    'health': '&H00D1E49B', 'sales': '&H007AB3F7',
    'travel': '&H00EFD975', 'mystery': '&H00FAA5BE',
}
CAPTIONS = (
    'Excel集計、まだ手作業？', '架空の4か月データを準備',
    '表をAIへ、グラフを依頼', 'AIがグラフを表示',
    '1月12万・2月15万', '3月20万・4月18万',
    '合計65万円、最後は人が確認', '保存して、あとで試そう',
)


def ms(value):
    m = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', value)
    if not m:
        raise ValueError('invalid SRT timestamp')
    h, minute, second, milli = map(int, m.groups())
    if minute >= 60 or second >= 60:
        raise ValueError('invalid SRT time')
    return ((h * 60 + minute) * 60 + second) * 1000 + milli


def parse_srt(raw):
    times = []
    for block in re.split(r'\n\s*\n', raw.strip().replace('\r\n', '\n')):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError('invalid SRT cue')
        parts = lines[1].split(' --> ')
        if len(parts) != 2:
            raise ValueError('invalid SRT range')
        a, b = ms(parts[0]), ms(parts[1])
        if a >= b:
            raise ValueError('empty cue')
        times.append((a, b))
    if len(times) != 8 or times[0][0] != 0 or not 27200 <= times[-1][1] <= 27400:
        raise ValueError('wrong cue count or duration')
    if any(a[1] != b[0] for a, b in zip(times, times[1:])):
        raise ValueError('gap/overlap in captions')
    return times


def ass_time(milliseconds):
    ticks = (milliseconds + 5) // 10
    h, rem = divmod(ticks, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f'{h}:{m:02}:{s:02}.{cs:02}'


def make_ass(cues, genre='ai_work'):
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    if len(cues) != 8 or any(len(t) > 20 for t in CAPTIONS):
        raise ValueError('invalid caption length/count')
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,54,&H00FFFFFF,ACCENT,&H0020190B,&H88091824,-1,0,0,0,100,100,0,0,3,16,0,2,70,70,235,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""".replace('ACCENT', GENRES[genre])
    return header + ''.join(
        f'Dialogue: 0,{ass_time(a)},{ass_time(b)},Caption,,0,0,0,,{caption}\n'
        for (a, b), caption in zip(cues, CAPTIONS))
