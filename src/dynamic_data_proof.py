"""Reusable zero-cost UI state-transition proof for review-only TikTok renders.

Builds FFmpeg filter expressions only. Synthetic values are used so the primitive
can be reused across genres without personal data, paid assets, or result claims.
"""


def dynamic_data_filter(scene_index: int, start_at: float) -> str:
    """Animate spreadsheet selection, row reduction, countdown and chart updates."""
    rows_before = (5, 4, 6, 3, 5)[scene_index % 5]
    rows_after = (1, 1, 2, 1, 1)[scene_index % 5]
    before = (15, 12, 8, 3, 5)[scene_index % 5]
    after = (1, 1, 3, 1, 1)[scene_index % 5]
    s = max(float(start_at), 0.0)
    select_at = s + 0.10
    click_at = s + 0.24
    update_at = s + 0.38
    step = 0.16
    row_end = update_at + step * 4
    counter_end = update_at + 0.80
    done_at = max(row_end, counter_end)
    parts = [
        "drawbox=x=120:y=1030:w=840:h=370:color=black@0.84:t=fill:" + f"enable='gte(t,{s:.3f})'",
        "drawtext=text='LIVE DATA':fontcolor=white:fontsize=28:borderw=2:bordercolor=black:x=155:y=1050:" + f"enable='gte(t,{s:.3f})'",
        f"drawtext=text='ROWS {rows_before} → {rows_after}':fontcolor=white:fontsize=32:borderw=2:bordercolor=black:x=155:y=1094:enable='gte(t,{s:.3f})'",
        f"drawbox=x=155:y=1145:w=360:h=30:color=white@0.18:t=fill:enable='gte(t,{s:.3f})'",
        f"drawtext=text='TASK':fontcolor=white:fontsize=18:x=170:y=1150:enable='gte(t,{s:.3f})'",
        f"drawtext=text='STATUS':fontcolor=white:fontsize=18:x=365:y=1150:enable='gte(t,{s:.3f})'",
        f"drawbox=x=350:y=1145:w=2:h=170:color=white@0.24:t=fill:enable='gte(t,{s:.3f})'",
        # Selection border appears before the click, then flashes to prove input causality.
        f"drawbox=x=155:y=1178:w=360:h=22:color=white@0.95:t=2:enable='between(t,{select_at:.3f},{update_at:.3f})'",
        f"drawbox=x=500:y=1183:w=10:h=10:color=white@0.95:t=fill:enable='between(t,{click_at:.3f},{update_at:.3f})'",
        f"drawtext=text='SELECT':fontcolor=white:fontsize=15:x=535:y=1180:enable='between(t,{select_at:.3f},{click_at:.3f})'",
        f"drawtext=text='CLICK':fontcolor=white:fontsize=15:x=535:y=1180:enable='between(t,{click_at:.3f},{update_at:.3f})'",
    ]
    # Five spreadsheet rows disappear only after the click/update event.
    for row in range(5):
        y = 1178 + row * 28
        hide_at = update_at + step * (row + 1)
        enable = f"gte(t,{s:.3f})" if row == 0 else f"between(t,{s:.3f},{hide_at:.3f})"
        parts.append(f"drawbox=x=155:y={y}:w=360:h=22:color=white@0.10:t=fill:enable='{enable}'")
        parts.append(f"drawbox=x=155:y={y + 21}:w=360:h=1:color=white@0.18:t=fill:enable='{enable}'")
    parts.extend([
        f"drawtext=text='PROCESS':fontcolor=white:fontsize=17:x=170:y=1180:enable='between(t,{update_at:.3f},{done_at:.3f})'",
        f"drawtext=text='DONE':fontcolor=white:fontsize=17:x=380:y=1180:enable='gte(t,{done_at:.3f})'",
        f"drawbox=x=360:y=1178:w=125:h=22:color=white@0.18:t=fill:enable='gte(t,{done_at:.3f})'",
    ])
    # Countdown starts after the click so displayed data and chart motion share one cause.
    span = max(before - after, 1)
    for n in range(before, after - 1, -1):
        idx = before - n
        t0 = update_at + 0.80 * idx / span
        t1 = update_at + 0.80 * (idx + 1) / span
        enable = f"between(t,{t0:.3f},{t1:.3f})" if n != after else f"gte(t,{t0:.3f})"
        parts.append(f"drawtext=text='{n}':fontcolor=white:fontsize=58:borderw=2:bordercolor=black:x=735:y=1090:enable='{enable}'")
    # Three chart bars update independently after the same click event.
    for i, target in enumerate((0.92, 0.66, 0.38)):
        y = 1275 + i * 28
        delay = update_at + 0.10 * i
        parts.append(f"drawbox=x=545:y={y}:w=315:h=16:color=white@0.16:t=fill:enable='gte(t,{s:.3f})'")
        parts.append(f"drawbox=x=545:y={y}:w='315*{target:.2f}*min(max((t-{delay:.3f})/0.70,0),1)':h=16:color=white@0.92:t=fill:enable='gte(t,{delay:.3f})'")
    parts.append(f"drawtext=text='UPDATED':fontcolor=white:fontsize=24:borderw=2:bordercolor=black:x=155:y=1360:enable='gte(t,{done_at:.3f})'")
    return ','.join(parts)
