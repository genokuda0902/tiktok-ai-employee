"""Reusable zero-cost UI state-transition proof for review-only TikTok renders.

Builds FFmpeg filter expressions only. Synthetic values are used so the primitive
can be reused across genres without personal data, paid assets, or result claims.
"""


def dynamic_data_filter(scene_index: int, start_at: float) -> str:
    """Animate table-row removal, a countdown counter, and three result bars."""
    rows_before = (5, 4, 6, 3, 5)[scene_index % 5]
    rows_after = (1, 1, 2, 1, 1)[scene_index % 5]
    before = (15, 12, 8, 3, 5)[scene_index % 5]
    after = (1, 1, 3, 1, 1)[scene_index % 5]
    s = max(float(start_at), 0.0)
    step = 0.16
    row_end = s + step * 4
    counter_end = s + 0.80
    parts = [
        "drawbox=x=120:y=1050:w=840:h=330:color=black@0.82:t=fill:" + f"enable='gte(t,{s:.3f})'",
        "drawtext=text='LIVE DATA':fontcolor=white:fontsize=28:borderw=2:bordercolor=black:x=155:y=1072:" + f"enable='gte(t,{s:.3f})'",
        f"drawtext=text='ROWS {rows_before} → {rows_after}':fontcolor=white:fontsize=32:borderw=2:bordercolor=black:x=155:y=1118:enable='gte(t,{s:.3f})'",
    ]
    # Five visible table rows disappear one-by-one; the final row remains.
    for row in range(5):
        y = 1170 + row * 28
        hide_at = s + step * (row + 1)
        if row == 0:
            enable = f"gte(t,{s:.3f})"
        else:
            enable = f"between(t,{s:.3f},{hide_at:.3f})"
        parts.append(
            f"drawbox=x=155:y={y}:w=300:h=18:color=white@0.72:t=fill:enable='{enable}'"
        )
    # A real countdown changes displayed value across timed intervals.
    span = max(before - after, 1)
    for n in range(before, after - 1, -1):
        idx = before - n
        t0 = s + 0.80 * idx / span
        t1 = s + 0.80 * (idx + 1) / span
        enable = f"between(t,{t0:.3f},{t1:.3f})" if n != after else f"gte(t,{t0:.3f})"
        parts.append(
            f"drawtext=text='{n}':fontcolor=white:fontsize=58:borderw=2:bordercolor=black:x=735:y=1110:enable='{enable}'"
        )
    # Three bars animate independently to avoid a single generic progress-bar look.
    for i, target in enumerate((0.92, 0.66, 0.38)):
        y = 1265 + i * 28
        delay = s + 0.10 * i
        parts.append(
            f"drawbox=x=500:y={y}:w=360:h=16:color=white@0.16:t=fill:enable='gte(t,{s:.3f})'"
        )
        parts.append(
            f"drawbox=x=500:y={y}:w='360*{target:.2f}*min(max((t-{delay:.3f})/0.70,0),1)':h=16:color=white@0.92:t=fill:enable='gte(t,{delay:.3f})'"
        )
    parts.append(
        f"drawtext=text='UPDATED':fontcolor=white:fontsize=24:borderw=2:bordercolor=black:x=155:y=1340:enable='gte(t,{max(row_end,counter_end):.3f})'"
    )
    return ','.join(parts)
