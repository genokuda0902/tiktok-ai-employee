"""Reusable zero-cost UI data-change proof primitives for review-only TikTok renders.

This module only builds FFmpeg filter expressions. It does not publish, approve,
or access personal data. Values are synthetic demo data suitable for all genres.
"""


def dynamic_data_filter(scene_index: int, start_at: float) -> str:
    """Return a compact table/counter/chart state transition after ``start_at``."""
    rows_before = (5, 4, 6, 3, 5)[scene_index % 5]
    rows_after = (1, 1, 2, 1, 1)[scene_index % 5]
    before = (15, 12, 8, 3, 5)[scene_index % 5]
    after = (1, 1, 3, 1, 1)[scene_index % 5]
    s = max(float(start_at), 0.0)
    end = s + 0.75
    return (
        "drawbox=x=120:y=1115:w=840:h=250:color=black@0.80:t=fill:"
        f"enable='gte(t,{s:.3f})',"
        "drawtext=text='DATA CHANGE':fontcolor=white:fontsize=28:borderw=2:bordercolor=black:x=155:y=1140:"
        f"enable='gte(t,{s:.3f})',"
        f"drawtext=text='ROWS {rows_before} → {rows_after}':fontcolor=white:fontsize=34:borderw=2:bordercolor=black:x=155:y=1190:enable='gte(t,{s:.3f})',"
        f"drawtext=text='{before} → {after}':fontcolor=white:fontsize=52:borderw=2:bordercolor=black:x=690:y=1180:enable='gte(t,{s:.3f})',"
        "drawbox=x=155:y=1280:w=700:h=22:color=white@0.18:t=fill:"
        f"enable='gte(t,{s:.3f})',"
        "drawbox=x=155:y=1280:w='700*min(max((t-" + f"{s:.3f})/0.75,0),1)'" + ":h=22:color=white@0.95:t=fill:"
        f"enable='between(t,{s:.3f},{end:.3f})',"
        "drawbox=x=155:y=1280:w=700:h=22:color=white@0.95:t=fill:"
        f"enable='gte(t,{end:.3f})'"
    )
