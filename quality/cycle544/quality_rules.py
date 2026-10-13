"""Review-only reusable video timing rules for ten genres."""
GENRES = ('ai_work', 'finance', 'science', 'history', 'lifehacks', 'career', 'business', 'education', 'travel', 'creative')

def valid_hook(first_cut_seconds, caption_y, genre):
    return genre in GENRES and 0 < first_cut_seconds <= 1.5 and 180 <= caption_y <= 1500
