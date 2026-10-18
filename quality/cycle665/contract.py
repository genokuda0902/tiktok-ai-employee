def caption_matches_script(caption, spoken_text):
    return isinstance(caption, str) and caption == spoken_text and bool(caption.strip())

def count_genres(genres):
    return len(genres)
