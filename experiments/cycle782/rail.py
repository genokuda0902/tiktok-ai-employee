"""Genre-neutral, review-only six-beat progress rail overlay."""
def overlay(beats):
    if not 3 <= len(beats) <= 10:
        raise ValueError("expected 3-10 beats")
    top, bottom, gap = 345, 1455, 14
    h = int((bottom-top-(len(beats)-1)*gap)/len(beats))
    filters = []
    for i, beat in enumerate(beats):
        y = top + i*(h+gap)
        filters.append(f"drawbox=x=24:y={y}:w=12:h={h}:color=0x7890a4@0.25:t=fill")
        filters.append(f"drawbox=x=24:y={y}:w=12:h={h}:color=0x37e6dd@0.92:t=fill:enable=gte(t\\,{beat['start']:.3f})")
    return ",".join(filters)
