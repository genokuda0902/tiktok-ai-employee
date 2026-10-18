def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3
