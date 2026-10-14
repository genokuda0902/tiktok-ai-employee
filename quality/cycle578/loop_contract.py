"""Genre-neutral CTA -> hook loop contract (review only)."""
GENRES = ("ai_productivity","beauty","relationships","finance","sales","career","wellness","science","travel_food","product_comparison")
def validate_loop(genre, captions, duration=20):
    if genre not in GENRES: raise ValueError("unknown genre")
    if not captions or captions[0][0] != 0 or captions[-1][1] != duration:
        raise ValueError("incomplete timeline")
    for i, (start, end, caption) in enumerate(captions):
        if end - start < 1: raise ValueError("caption shorter than 1 second")
        if not caption or len(caption) > 36: raise ValueError("invalid caption")
        if i and captions[i-1][1] != start: raise ValueError("gap or overlap")
    if captions[0][2] != captions[-1][2]:
        raise ValueError("last caption must re-enter first hook")
    return True
