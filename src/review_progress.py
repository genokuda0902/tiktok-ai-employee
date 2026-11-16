"""Pure FFmpeg filter for a safe, time-based review progress indicator."""
def progress_filter(duration, width=720, height=1280):
    if duration <= 0 or width < 200 or height < 400:
        raise ValueError("invalid duration or canvas")
    x=int(width*.08); y=int(height*.955); w=width-2*x; h=max(5,round(height*.006))
    return (f"drawbox=x={x}:y={y}:w={w}:h={h}:color=white@0.25:t=fill,"
            f"drawbox=x={x}:y={y}:w='min({w},max(0,{w}*t/{duration:.6f}))':h={h}:color=0x22d3ee@0.95:t=fill")
