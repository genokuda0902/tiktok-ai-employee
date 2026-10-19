def meter_history(levels, frame, count=16):
    if count < 1 or frame < 0 or frame >= len(levels):
        raise ValueError('invalid frame')
    return [float(levels[max(0, frame - count + 1 + i)]) for i in range(count)]
