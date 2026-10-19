"""Reusable 10-genre hero contract for cycle696 (no posting or network)."""
GENRES = {
    'ai_work':'#47E6D2', 'beauty':'#FF92CA',
    'love_psychology':'#FFB1D2', 'saving':'#77E5A2',
    'sales_business':'#59C8F2', 'career':'#A1BEFF',
    'health':'#81E5BC', 'science':'#47E6D2',
    'travel_food':'#FFBC68', 'product_comparison':'#BDA4FF'
}
WIDTH, HEIGHT, FPS, HOOK_FRAMES = 1080, 1920, 30, 60
TEXT_BOTTOM = 1654

def validate(genre: str) -> str:
    if genre not in GENRES:
        raise ValueError('Unknown genre')
    if TEXT_BOTTOM >= HEIGHT - 240:
        raise ValueError('Text overlaps reserved bottom zone')
    return GENRES[genre]
